"""
INCOSE Standards Requirement Validator
Validates requirements against INCOSE (International Council on Systems Engineering) standards.
"""

import json
import re
from typing import List, Dict
from dataclasses import dataclass

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from groq_client import GroqUMLClient

@dataclass
class ValidationResult:
    is_valid: bool
    score: float
    issues: List[str]
    suggestions: List[str]
    detailed_reasoning: str
    analysis: Dict[str, str] = None

class INCOSEValidator:
    def __init__(self, groq_client: GroqUMLClient):
        """Initialize the INCOSE validator with Groq client and vector database"""
        self.groq_client = groq_client
        
        # Set up the vector database
        persist_dir = "chroma_db_incose"
        
        # Initialize HuggingFace embeddings
        embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        
        # Initialize Chroma vector store
        self.vectorstore = Chroma(persist_directory=persist_dir, embedding_function=embedding_model)
        
        # Set up retriever
        self.retriever = self.vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 5}  # Get top 5 most relevant chunks
        )
        
        print("✅ INCOSE vector database initialized successfully")

    def validate_requirement(self, requirement_text: str) -> ValidationResult:
        """
        Validate a requirement against INCOSE standards
        
        Args:
            requirement_text (str): The requirement text to validate
            
        Returns:
            ValidationResult: The validation result with score, issues, and suggestions
        """
        try:
            # Get relevant INCOSE context
            context = self._get_relevant_context(requirement_text)
            
            # Use LLM to evaluate the requirement
            result = self._evaluate_with_llm(requirement_text, context)
            
            return result
            
        except Exception as e:
            print(f"Error validating requirement: {e}")
            return ValidationResult(
                is_valid=False,
                score=0.0,
                issues=[f"Validation failed: {str(e)}"],
                suggestions=["Please check the requirement format and try again"],
                detailed_reasoning=f"An error occurred during validation: {str(e)}",
                analysis={}
            )

    def _get_relevant_context(self, requirement_text: str) -> str:
        """Get relevant INCOSE context for the requirement"""
        try:
            # Use the retriever to get relevant documents
            relevant_docs = self.retriever.get_relevant_documents(requirement_text)
            
            # Combine the relevant documents into context
            context_parts = []
            for doc in relevant_docs:
                context_parts.append(doc.page_content)
            
            context = "\n\n".join(context_parts)
            return context[:2000]  # Limit context length to avoid token limits
            
        except Exception as e:
            print(f"Error getting context: {e}")
            return "Unable to retrieve INCOSE context. Using basic validation criteria."

    def _evaluate_with_llm(self, requirement_text: str, context: str) -> ValidationResult:
        """Use the LLM to evaluate the requirement"""
        
        # Escape the requirement text to prevent JSON issues
        escaped_requirement = requirement_text.replace('"', '\\"').replace("'", "\\'")
        
        prompt = f"""You are a systems engineering expert familiar with INCOSE standards.

Context (INCOSE Standards):
{context}

Requirement to Evaluate:
{escaped_requirement}

Task: Evaluate this requirement against INCOSE standards using the following criteria:

1. VALIDITY: Is the requirement valid according to INCOSE standards?
2. CLARITY: Is the requirement clear and unambiguous?
3. COMPLETENESS: Is the requirement complete and specific?
4. FEASIBILITY: Is the requirement technically feasible and practical?
5. VERIFIABILITY: Can the requirement be verified and tested?
6. TRACEABILITY: Is the requirement traceable and consistent with system context?

CRITICAL: You must respond with ONLY a valid JSON object. DO NOT include quotes within text values that would break JSON parsing.

JSON format (use exactly this structure):
{{
    "is_valid": true,
    "score": 85,
    "issues": ["Issue one", "Issue two"],
    "suggestions": ["Suggestion one", "Suggestion two"],
    "detailed_reasoning": "Brief explanation without quotes",
    "analysis": {{
        "validity": "Valid/Invalid - reason",
        "clarity": "Clear/Unclear - reason", 
        "completeness": "Complete/Incomplete - reason",
        "feasibility": "Feasible/Infeasible - reason",
        "verifiability": "Verifiable/Unverifiable - reason",
        "traceability": "Traceable/Untraceable - reason"
    }}
}}

Rules:
- Use only double quotes for JSON strings
- Do not use single quotes or apostrophes in text values
- Keep text values under 100 characters
- Ensure the JSON is valid and parseable
- Address all 6 criteria in the analysis section"""

        try:
            # Use the existing Groq client with increased tokens for detailed analysis
            response_content = self.groq_client._make_request(prompt, max_tokens=2000)
            
            # Clean the response content more thoroughly
            response_content = response_content.strip()
            
            # Remove common formatting issues
            response_content = response_content.replace('```json', '').replace('```', '').strip()
            
            # Fix common JSON issues
            response_content = response_content.replace("'", '"')  # Replace single quotes with double quotes
            response_content = response_content.replace('\\"', '"')  # Fix over-escaped quotes
            
            # Find JSON boundaries more precisely
            start_brace = response_content.find('{')
            end_brace = response_content.rfind('}')
            
            if start_brace != -1 and end_brace != -1 and end_brace > start_brace:
                json_content = response_content[start_brace:end_brace + 1]
            else:
                json_content = response_content
            
            # Try to fix malformed JSON
            json_content = self._fix_malformed_json(json_content)
            
            try:
                # Try to parse as JSON
                result_data = json.loads(json_content)
                
                # Validate and sanitize the data
                is_valid = bool(result_data.get("is_valid", False))
                score = max(0.0, min(100.0, float(result_data.get("score", 0.0))))
                
                issues = result_data.get("issues", [])
                if not isinstance(issues, list):
                    issues = [str(issues)] if issues else []
                # Clean up issues - remove partial JSON artifacts and limit length
                issues = [issue[:100] for issue in issues if isinstance(issue, str) and len(issue.strip()) > 0]
                
                suggestions = result_data.get("suggestions", [])
                if not isinstance(suggestions, list):
                    suggestions = [str(suggestions)] if suggestions else []
                # Clean up suggestions - remove partial JSON artifacts and limit length
                suggestions = [sugg[:100] for sugg in suggestions if isinstance(sugg, str) and len(sugg.strip()) > 0]
                
                detailed_reasoning = str(result_data.get("detailed_reasoning", "Analysis completed"))[:500]
                
                # Extract analysis if available
                analysis = result_data.get("analysis", {})
                if not isinstance(analysis, dict):
                    analysis = {}
                
                return ValidationResult(
                    is_valid=is_valid,
                    score=score,
                    issues=issues[:5],  # Limit to 5 issues
                    suggestions=suggestions[:5],  # Limit to 5 suggestions
                    detailed_reasoning=detailed_reasoning,
                    analysis=analysis
                )
                
            except json.JSONDecodeError as e:
                print(f"JSON parsing failed: {e}")
                print(f"Cleaned JSON content: {json_content[:300]}...")
                # Use enhanced fallback parsing
                return self._parse_llm_response_enhanced_fallback(response_content)
                
        except Exception as e:
            print(f"LLM evaluation error: {e}")
            return ValidationResult(
                is_valid=False,
                score=0.0,
                issues=[f"LLM evaluation failed: {str(e)}"],
                suggestions=["Try again with a different model or check your API key"],
                detailed_reasoning=f"Failed to get LLM response: {str(e)}"
            )

    def _fix_malformed_json(self, json_content: str) -> str:
        """Fix common JSON formatting issues from LLM responses"""
        
        # Step 1: Ensure property names are quoted
        json_content = re.sub(r'(\w+):', r'"\1":', json_content)
        
        # Step 2: Fix quoted boolean and number values
        json_content = re.sub(r':\s*"(true|false)"', r': \1', json_content)  # Fix quoted booleans
        json_content = re.sub(r':\s*"(\d+(?:\.\d+)?)"', r': \1', json_content)  # Fix quoted numbers
        
        # Step 3: Fix unquoted string values (but not booleans/numbers)
        json_content = re.sub(r':\s*([^",\[\]{}]\w[^",\[\]{}]*)', r': "\1"', json_content)
        
        # Step 4: Fix arrays with unquoted strings
        def fix_array_items(match):
            array_content = match.group(1)
            items = []
            parts = array_content.split(',')
            
            for part in parts:
                part = part.strip()
                if not part:
                    continue
                # Don't quote if already quoted or if it's a number/boolean
                if not (part.startswith('"') and part.endswith('"')) and not re.match(r'^(\d+(\.\d+)?|true|false|null)$', part):
                    # Escape any internal quotes
                    part = part.replace('"', '\\"')
                    part = f'"{part}"'
                items.append(part)
            
            return f"[{', '.join(items)}]"
        
        json_content = re.sub(r'\[([^\]]*)\]', fix_array_items, json_content)
        
        # Step 5: Fix unescaped quotes in string values
        def fix_string_quotes(match):
            content = match.group(1)
            # Escape internal quotes
            content = content.replace('"', '\\"')
            return f'"{content}"'
        
        # This is a simple approach - find strings and escape internal quotes
        # We need to be careful not to break the JSON structure
        
        return json_content

    def _parse_llm_response_enhanced_fallback(self, response: str) -> ValidationResult:
        """Enhanced fallback parser for LLM responses that aren't in JSON format"""
        
        # Default values
        is_valid = False
        score = 0.0
        issues = []
        suggestions = []
        detailed_reasoning = response
        
        # Try to extract key information using various patterns
        response_lower = response.lower()
        
        # Check for validity indicators
        if any(word in response_lower for word in ["valid", "meets", "complies", "satisfies"]) and \
           not any(word in response_lower for word in ["invalid", "not valid", "does not meet", "fails"]):
            is_valid = True
            score = 75.0
        elif any(word in response_lower for word in ["invalid", "not valid", "does not meet", "fails", "poor"]):
            is_valid = False
            score = 25.0
        
        # Look for score patterns
        score_patterns = [
            r'score[:\s]*(\d+)',
            r'(\d+)\s*(?:out of|/)\s*100',
            r'(\d+)%',
            r'rating[:\s]*(\d+)'
        ]
        
        for pattern in score_patterns:
            score_match = re.search(pattern, response_lower)
            if score_match:
                try:
                    extracted_score = float(score_match.group(1))
                    if 0 <= extracted_score <= 100:
                        score = extracted_score
                        break
                except (ValueError, IndexError):
                    continue
        
        # Extract issues
        issues_patterns = [
            r'issues?[:\s]*([^.]+\.)',
            r'problems?[:\s]*([^.]+\.)',
            r'concerns?[:\s]*([^.]+\.)',
            r'lacks?[:\s]*([^.]+\.)'
        ]
        
        for pattern in issues_patterns:
            matches = re.findall(pattern, response, re.IGNORECASE)
            for match in matches[:3]:  # Limit to 3 issues
                issues.append(match.strip())
        
        # Extract suggestions
        suggestions_patterns = [
            r'suggest[^.]*[:\s]*([^.]+\.)',
            r'recommend[^.]*[:\s]*([^.]+\.)',
            r'should[:\s]*([^.]+\.)',
            r'improvement[^.]*[:\s]*([^.]+\.)'
        ]
        
        for pattern in suggestions_patterns:
            matches = re.findall(pattern, response, re.IGNORECASE)
            for match in matches[:3]:  # Limit to 3 suggestions
                suggestions.append(match.strip())
        
        # If no specific issues/suggestions found, provide generic ones
        if not issues and not is_valid:
            issues = ["The requirement may not fully comply with INCOSE standards"]
        
        if not suggestions:
            suggestions = ["Review the requirement against INCOSE best practices", 
                         "Consider making the requirement more specific and measurable"]
        
        return ValidationResult(
            is_valid=is_valid,
            score=score,
            issues=issues,
            suggestions=suggestions,
            detailed_reasoning=detailed_reasoning,
            analysis={}
        )
