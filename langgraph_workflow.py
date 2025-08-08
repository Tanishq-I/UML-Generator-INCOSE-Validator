from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
from groq_client import GroqUMLClient
from uml_generator import UMLDiagramGenerator
from uml_models import UMLDiagram

class WorkflowState(TypedDict):
    scenario: str
    uml_diagram: Optional[UMLDiagram]
    dot_source: str
    error: str
    uml_type: Optional[str]
    model: Optional[str]

def create_uml_workflow():
    uml_generator = UMLDiagramGenerator()
    def generate_uml(state: WorkflowState) -> WorkflowState:
        try:
            scenario = state["scenario"]
            uml_type = state.get("uml_type", "class")
            model = state.get("model", "llama3-8b-8192")
            groq_client = GroqUMLClient(model=model)
            uml_diagram = groq_client.generate_uml(scenario, uml_type)
            state["uml_diagram"] = uml_diagram
            state["error"] = ""
        except Exception as e:
            state["error"] = f"Error generating UML: {str(e)}"
        return state
    def create_diagram(state: WorkflowState) -> WorkflowState:
        try:
            if "uml_diagram" in state and state["uml_diagram"]:
                dot_source = uml_generator.generate_diagram(state["uml_diagram"])
                state["dot_source"] = dot_source
                state["error"] = ""
            else:
                state["error"] = "No UML diagram to process"
        except Exception as e:
            state["error"] = f"Error creating diagram: {str(e)}"
        return state
    workflow = StateGraph(WorkflowState)
    workflow.add_node("generate_uml", generate_uml)
    workflow.add_node("create_diagram", create_diagram)
    workflow.set_entry_point("generate_uml")
    workflow.add_edge("generate_uml", "create_diagram")
    workflow.add_edge("create_diagram", END)
    return workflow.compile()
workflow = create_uml_workflow() 