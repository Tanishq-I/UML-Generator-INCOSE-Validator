# 🎯 UML Generator & INCOSE Validator API Documentation

A comprehensive FastAPI-based service for generating UML diagrams and validating system requirements against INCOSE standards.

## 📖 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [API Documentation](#api-documentation)
- [Quick Start](#quick-start)
- [Endpoints](#endpoints)
- [Models and Schemas](#models-and-schemas)
- [Examples](#examples)
- [Error Handling](#error-handling)
- [Development](#development)

## 🌟 Overview

This API provides professional-grade tools for:
- **UML Diagram Generation**: Create various UML diagrams from natural language descriptions
- **INCOSE Requirement Validation**: Validate system requirements against INCOSE standards
- **Session Management**: Track conversation history and project progress
- **Multi-Model Support**: Use different AI models for optimal performance
- **Swagger Documentation**: Comprehensive interactive API documentation

## ✨ Features

### 🎨 UML Generation
- **Class Diagrams**: System structure and relationships
- **Sequence Diagrams**: Interactions over time
- **Use Case Diagrams**: System functionality and actors
- **Activity Diagrams**: Workflow and business processes
- **State Diagrams**: Object state transitions

### ✅ INCOSE Validation
- **Clarity Assessment**: Clear and unambiguous requirements
- **Completeness Checking**: All necessary information included
- **Verifiability Analysis**: Testable and measurable criteria
- **Feasibility Evaluation**: Technical and economic viability
- **Scoring System**: 0-100% quality scoring with detailed feedback

### 💬 Session Management
- Create and manage chat sessions
- Track conversation history
- Organize work by project or topic
- Export session data

### 🤖 AI Model Support
- Multiple Groq models available:
  - Llama 3 (8B and 70B parameters)
  - Mixtral 8x7B (mixture of experts)
  - Gemma 7B and 9B (instruction-tuned)
- Model comparison and selection
- Optimized for different use cases
- Configurable parameters

## 📚 API Documentation

### Interactive Documentation
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **OpenAPI Schema**: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

### Custom Documentation
- **Welcome Page**: [http://localhost:8000/](http://localhost:8000/)
- **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

## 🚀 Quick Start

### Prerequisites
1. Python 3.8+
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables (see `.env.example`)
4. Groq API Key ([Get a key here](https://console.groq.com/keys))

### Starting the Server
```bash
uvicorn app:app --reload
```

### Basic Usage Examples

#### Generate a UML Class Diagram
```bash
curl -X POST "http://localhost:8000/generate-uml" \
-H "Content-Type: application/json" \
-d '{
  "scenario": "A library management system where users can borrow books, librarians can manage inventory, and the system tracks due dates",
  "uml_type": "class",
  "model": "llama3-8b-8192"
}'
```

#### Validate a System Requirement
```bash
curl -X POST "http://localhost:8000/evaluate-requirement" \
-H "Content-Type: application/json" \
-d '{
  "requirement": "The system shall process user login requests within 2 seconds under normal operating conditions",
  "model": "llama3-8b-8192"
}'
```

## 🔗 Endpoints

### Core Functionality

| Method | Endpoint | Description | Tags |
|--------|----------|-------------|------|
| `POST` | `/generate-uml` | Generate UML diagrams from scenarios | UML Generation |
| `POST` | `/evaluate-requirement` | Validate requirements against INCOSE | INCOSE Validation |
| `GET` | `/models` | Get available AI models | AI Models |

### Session Management

| Method | Endpoint | Description | Tags |
|--------|----------|-------------|------|
| `POST` | `/chat/sessions` | Create new chat session | Chat Sessions |
| `GET` | `/chat/sessions` | Get all chat sessions | Chat Sessions |
| `GET` | `/chat/sessions/{session_id}/messages` | Get session messages | Chat Sessions |
| `PUT` | `/chat/sessions/{session_id}/title` | Update session title | Chat Sessions |
| `DELETE` | `/chat/sessions/{session_id}` | Delete session | Chat Sessions |

### System

| Method | Endpoint | Description | Tags |
|--------|----------|-------------|------|
| `GET` | `/` | API documentation homepage | Documentation |
| `GET` | `/health` | Health check and status | System |

## 📋 Models and Schemas

### Request Models

#### `ScenarioRequest`
```json
{
  "scenario": "string (required)",
  "uml_type": "string (optional, enum: class|sequence|usecase|activity|state)",
  "model": "string (optional, default: llama3-8b-8192)",
  "session_id": "string (optional)"
}
```

#### `RequirementRequest`
```json
{
  "requirement": "string (required)",
  "model": "string (optional, default: llama3-8b-8192)",
  "session_id": "string (optional)"
}
```

#### `SessionRequest`
```json
{
  "title": "string (required)"
}
```

### Response Models

#### `UMLResponse`
```json
{
  "dot_source": "string",
  "uml_diagram": "string (optional)",
  "error": "string (optional)",
  "session_id": "string (optional)"
}
```

#### `RequirementResponse`
```json
{
  "result": "string (enum: VALID|INVALID)",
  "reason": "string",
  "score": "number (0-100)",
  "session_id": "string (optional)"
}
```

#### `ModelInfo`
```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "provider": "string"
}
```

#### `ModelsResponse`
```json
{
  "models": [
    {
      "id": "string",
      "name": "string",
      "description": "string",
      "provider": "string"
    }
  ]
}
```

## 💡 Examples

### Complete UML Generation Workflow

1. **Create a session**:
```json
POST /chat/sessions
{
  "title": "E-commerce System Design"
}
```

2. **Generate a class diagram**:
```json
POST /generate-uml
{
  "scenario": "An e-commerce platform with customers, products, orders, and payments",
  "uml_type": "class",
  "session_id": "your-session-id"
}
```

3. **Generate a sequence diagram**:
```json
POST /generate-uml
{
  "scenario": "Customer places an order and makes payment",
  "uml_type": "sequence",
  "session_id": "your-session-id"
}
```

### INCOSE Validation Examples

#### Valid Requirement
```json
POST /evaluate-requirement
{
  "requirement": "The login system shall authenticate users within 3 seconds with 99.9% uptime during peak hours (1000+ concurrent users)"
}
```

**Expected Response**:
```json
{
  "result": "VALID",
  "reason": "Overall Score: 88.0%\n\nINCOSE Criteria Analysis:\n• CLARITY: Requirement is clear and specific\n• VERIFIABILITY: Measurable performance criteria provided\n• COMPLETENESS: Includes timing, reliability, and load specifications\n\nStrengths:\n• Specific timing requirement (3 seconds)\n• Quantified reliability target (99.9%)\n• Defined operating conditions\n\nMinor Suggestions:\n• Consider specifying authentication method\n• Define 'peak hours' time range"
}
```

#### Invalid Requirement
```json
POST /evaluate-requirement
{
  "requirement": "The system should be fast and reliable"
}
```

**Expected Response**:
```json
{
  "result": "INVALID",
  "reason": "Overall Score: 25.0%\n\nINCOSE Criteria Analysis:\n• CLARITY: Vague and subjective terms used\n• VERIFIABILITY: No measurable criteria\n• COMPLETENESS: Missing specific requirements\n\nIssues:\n• 'Fast' is subjective - specify timing\n• 'Reliable' is unmeasurable - provide metrics\n• No context or conditions specified\n\nSuggestions:\n• Define specific performance thresholds\n• Include measurable acceptance criteria\n• Specify operating conditions"
}
```

## ⚠️ Error Handling

### HTTP Status Codes

| Code | Description | Example |
|------|-------------|---------|
| `200` | Success | Request completed successfully |
| `400` | Bad Request | Invalid input parameters |
| `404` | Not Found | Session or resource not found |
| `500` | Server Error | Internal processing error |

### Error Response Format
```json
{
  "detail": "Error description"
}
```

### Common Error Scenarios

1. **Missing API Key**:
   ```json
   {"detail": "GROQ_API_KEY not set."}
   ```

2. **Invalid Model**:
   ```json
   {"detail": "Invalid model: invalid-model-name"}
   ```

3. **Empty Scenario**:
   ```json
   {"detail": "Scenario description is required."}
   ```

4. **Session Not Found**:
   ```json
   {"detail": "Session not found"}
   ```

## 🛠️ Development

### Project Structure
```
├── app.py                 # Main FastAPI application
├── config.py              # Configuration and settings
├── groq_client.py         # Groq AI client
├── incose_validator.py    # INCOSE validation logic
├── langgraph_workflow.py  # UML generation workflow
├── chat_history.py        # Session management
├── uml_generator.py       # UML diagram generation
├── uml_models.py          # UML data models
├── requirements.txt       # Python dependencies
├── static/
│   └── api_docs.html      # Custom documentation page
├── test_api.py            # API test suite  
└── chroma_db_incose/      # Vector database for INCOSE standards
```

### Key Dependencies
- **FastAPI**: Modern web framework for APIs
- **Pydantic**: Data validation and serialization
- **LangGraph**: AI workflow orchestration
- **Groq**: High-performance AI inference
- **ChromaDB**: Vector database for semantic search
- **Graphviz**: UML diagram rendering
- **SQLite**: Database for chat history

### Environment Variables
```bash
GROQ_API_KEY=your_groq_api_key_here
# Add other configuration as needed
```

### Running Tests
```bash
python test_api.py
```

### API Versioning
- Current version: `v1.0.0`
- Versioning strategy: Semantic versioning
- Breaking changes will increment major version

## 📞 Support

- **Documentation**: Available at `/docs` and `/redoc`
- **Health Check**: Monitor API status at `/health`
- **Issues**: Report issues in the project repository

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

---

**Generated with FastAPI automatic documentation** 🚀
