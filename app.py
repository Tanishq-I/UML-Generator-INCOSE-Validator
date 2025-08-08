from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langgraph_workflow import workflow
from config import GROQ_API_KEY, AVAILABLE_MODELS
from groq_client import GroqUMLClient
from incose_validator import INCOSEValidator
from typing import Optional, List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class ScenarioRequest(BaseModel):
    scenario: str
    uml_type: Optional[str] = None
    model: Optional[str] = "llama3-8b-8192"

class UMLResponse(BaseModel):
    dot_source: str
    uml_diagram: Optional[str] = None
    error: Optional[str] = None

class RequirementRequest(BaseModel):
    requirement: str
    model: Optional[str] = "llama3-8b-8192"

class RequirementResponse(BaseModel):
    result: str  # "VALID" or "INVALID"
    reason: str  # Detailed reasoning from the validator

class ModelInfo(BaseModel):
    id: str
    name: str
    description: str
    provider: str

class ModelsResponse(BaseModel):
    models: List[ModelInfo]

@app.get("/models", response_model=ModelsResponse)
def get_available_models():
    models = []
    for model_id, model_info in AVAILABLE_MODELS.items():
        models.append(ModelInfo(
            id=model_id,
            name=model_info["name"],
            description=model_info["description"],
            provider=model_info["provider"]
        ))
    return ModelsResponse(models=models)

@app.post("/generate-uml", response_model=UMLResponse)
def generate_uml_endpoint(req: ScenarioRequest):
    if not GROQ_API_KEY:
        raise HTTPException(status_code=400, detail="GROQ_API_KEY not set.")
    scenario = req.scenario.strip()
    uml_type = req.uml_type
    model = req.model or "llama3-8b-8192"
    
    if model not in AVAILABLE_MODELS:
        raise HTTPException(status_code=400, detail=f"Invalid model: {model}")
    
    if not scenario:
        raise HTTPException(status_code=400, detail="Scenario description is required.")
    try:
        print(f"Requested UML type: {uml_type}, Model: {model}")
        result = workflow.invoke({
            "scenario": scenario,
            "uml_diagram": None,
            "dot_source": "",
            "error": "",
            "uml_type": uml_type,
            "model": model
        })
        uml_diagram_obj = result.get("uml_diagram", None)
        uml_diagram_str = uml_diagram_obj.json() if uml_diagram_obj else None
        return UMLResponse(
            dot_source=result.get("dot_source", ""),
            uml_diagram=uml_diagram_str,
            error=result.get("error", None)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/evaluate-requirement", response_model=RequirementResponse)
def evaluate_requirement_endpoint(req: RequirementRequest):
    if not GROQ_API_KEY:
        raise HTTPException(status_code=400, detail="GROQ_API_KEY not set.")
    
    requirement = req.requirement.strip()
    model = req.model or "llama3-8b-8192"
    
    if model not in AVAILABLE_MODELS:
        raise HTTPException(status_code=400, detail=f"Invalid model: {model}")
    
    if not requirement:
        return RequirementResponse(
            result="INVALID",
            reason="Requirement cannot be empty."
        )
    
    try:
        groq_client = GroqUMLClient(model=model)
        validator = INCOSEValidator(groq_client)
        
        validation_result = validator.validate_requirement(requirement)
        
        # Convert ValidationResult to our response format
        result = "VALID" if validation_result.is_valid else "INVALID"
        
        # Format the reason with all available information
        reason_parts = []
        
        # Add overall percentage score at the top
        reason_parts.append(f"Overall Score: {validation_result.score:.1f}%")
        reason_parts.append("")  # Add empty line
        
        # Add detailed analysis for each INCOSE criteria
        if validation_result.analysis:
            reason_parts.append("INCOSE Criteria Analysis:")
            for criterion, assessment in validation_result.analysis.items():
                criterion_name = criterion.upper()
                reason_parts.append(f"• {criterion_name}: {assessment}")
            reason_parts.append("")  # Add empty line
        
        if validation_result.detailed_reasoning:
            reason_parts.append("Overall Assessment:")
            reason_parts.append(validation_result.detailed_reasoning)
            reason_parts.append("")  # Add empty line
        
        if validation_result.issues:
            reason_parts.append("Issues Identified:")
            for issue in validation_result.issues:
                reason_parts.append(f"• {issue}")
            reason_parts.append("")  # Add empty line
        
        if validation_result.suggestions:
            reason_parts.append("Improvement Suggestions:")
            for suggestion in validation_result.suggestions:
                reason_parts.append(f"• {suggestion}")
            reason_parts.append("")  # Add empty line
        
        # Add improvements section
        reason_parts.append("Improvements:")
        if validation_result.is_valid and validation_result.score >= 80:
            reason_parts.append("• This requirement meets INCOSE standards well")
            reason_parts.append("• Consider minor refinements for enhanced clarity if needed")
        elif validation_result.is_valid and validation_result.score >= 60:
            reason_parts.append("• This requirement is acceptable but has room for improvement")
            reason_parts.append("• Focus on addressing the issues identified above")
            reason_parts.append("• Consider making the requirement more specific and measurable")
        else:
            reason_parts.append("• This requirement needs significant improvements to meet INCOSE standards")
            reason_parts.append("• Rewrite the requirement to address all identified issues")
            reason_parts.append("• Ensure clarity, completeness, and verifiability")
            reason_parts.append("• Consider breaking complex requirements into smaller, more manageable parts")
        
        reason = "\n".join(reason_parts)
        
        return RequirementResponse(
            result=result,
            reason=reason
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating requirement: {str(e)}")
