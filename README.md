# 🎯 UML Generator & INCOSE Validator

![GitHub License](https://img.shields.io/github/license/Tanishq-I/UML-Generator-INCOSE-Validator)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green)
![React](https://img.shields.io/badge/React-Frontend-61DAFB)
![Groq](https://img.shields.io/badge/Groq-LLM%20API-FF6B6B)

An AI-powered application for generating UML diagrams from natural language descriptions and validating system requirements against INCOSE standards. Leverage the power of large language models through Groq to create professional UML diagrams and ensure your system requirements meet industry standards.

![UML Generator Demo](https://via.placeholder.com/800x400?text=UML+Generator+%26+INCOSE+Validator)

## 📖 Table of Contents
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Development](#-development)
- [License](#-license)

## ✨ Features

### 🎨 UML Generation
- Generate UML diagrams from natural language descriptions
- Support for multiple diagram types:
  - **Class Diagrams**: System structure and relationships
  - **Sequence Diagrams**: Interactions over time
  - **Use Case Diagrams**: System functionality and actors
  - **Activity Diagrams**: Workflow and business processes
  - **State Diagrams**: Object state transitions
- Export diagrams as Graphviz DOT format
- Interactive visualization in the web interface

### ✅ INCOSE Requirements Validation
- Validate system requirements against INCOSE standards
- Detailed scoring (0-100%) with comprehensive analysis
- Evaluation criteria:
  - Clarity and comprehensibility
  - Completeness and consistency
  - Verifiability and measurability
  - Feasibility and necessity
- Actionable improvement suggestions

### 💬 Session Management
- Maintain conversation history across interactions
- Organize work by projects or topics
- Track changes and requirements evolution

### 🤖 AI Model Integration
- Powered by advanced Large Language Models via Groq
- Support for multiple model options:
  - Llama 3 (8B and 70B parameters)
  - Mixtral (8x7B mixture of experts)
  - Gemma (7B and 9B parameters)
- Optimized prompting for accurate UML and validation
- Configurable model selection based on task complexity

## 🛠️ Tech Stack

### Backend
- **FastAPI**: High-performance API framework
- **Pydantic**: Data validation and settings management
- **LangGraph**: AI workflow orchestration
- **Groq**: High-performance AI inference
- **ChromaDB**: Vector database for INCOSE standards
- **SQLite**: Chat history persistence
- **Graphviz**: UML diagram rendering
- **Python 3.8+**: Modern programming language

### Frontend
- **React**: Modern frontend library
- **JavaScript/CSS**: UI implementation
- **React Router**: Navigation and routing
- **Axios**: API communication
- **Bootstrap**: Responsive UI components

## 📂 Project Structure

```
UML-Generator-INCOSE-Validator/
├── app.py                 # FastAPI application
├── config.py              # Configuration settings
├── groq_client.py         # AI model client
├── incose_validator.py    # INCOSE validation logic
├── langgraph_workflow.py  # UML generation workflow
├── chat_history.py        # Session management
├── uml_generator.py       # UML diagram generation
├── uml_models.py          # UML data models
├── setup_vectorstore.py   # Vector database setup
├── requirements.txt       # Python dependencies
├── chroma_db_incose/      # Vector database files
├── static/                # Static files
│   └── api_docs.html      # Custom API documentation
├── test_api.py            # API test suite
└── frontend/              # React frontend
    ├── package.json       # Frontend dependencies
    ├── public/            # Public assets
    └── src/               # React source code
        ├── components/    # UI components
        ├── pages/         # Application pages
        ├── services/      # API services
        └── utils/         # Utility functions
```

## 🚀 Installation

### Prerequisites
- Python 3.8+
- Node.js and npm (for frontend)
- Groq API Key ([Get a key here](https://console.groq.com/keys))
- Git

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Tanishq-I/UML-Generator-INCOSE-Validator.git
   cd UML-Generator-INCOSE-Validator
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   # Copy example env file
   cp .env.example .env
   # Edit .env and add your Groq API key
   # GROQ_API_KEY=your_api_key_here
   ```

5. Initialize the vector database:
   ```bash
   python setup_vectorstore.py
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## 🖥️ Usage

### Running the Backend

Start the FastAPI server:
```bash
uvicorn app:app --reload
```

The API will be available at http://localhost:8000

### Running the Frontend

Start the React development server:
```bash
cd frontend
npm start
```

The frontend will be available at http://localhost:3000

### Using the Application

1. **Generate UML Diagrams**:
   - Enter a natural language description of your system
   - Select the UML diagram type
   - View and export the generated diagram

2. **Validate Requirements**:
   - Enter system requirements
   - Get detailed validation results
   - Review improvement suggestions

3. **Manage Sessions**:
   - Create new sessions for different projects
   - View history of generated diagrams and validations
   - Export session data for documentation

## 📚 API Documentation

The API documentation is available through multiple interfaces:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json
- **Custom Documentation**: http://localhost:8000/

### Key Endpoints

| Endpoint | Description | Method |
|----------|-------------|--------|
| `/generate-uml` | Generate UML diagrams | POST |
| `/evaluate-requirement` | Validate requirements | POST |
| `/models` | List available AI models | GET |
| `/chat/sessions` | Manage chat sessions | POST, GET |
| `/chat/sessions/{session_id}/messages` | Get session messages | GET |
| `/chat/sessions/{session_id}/title` | Update session title | PUT |
| `/chat/sessions/{session_id}` | Delete session | DELETE |
| `/health` | Health check | GET |

Detailed API documentation is available in the [API_DOCUMENTATION.md](API_DOCUMENTATION.md) file.

## 👨‍💻 Development

### Architecture

The application follows a modern architecture:

1. **Frontend**: React-based single-page application
2. **Backend API**: FastAPI REST API
3. **AI Processing**: LangGraph workflow for UML generation
4. **Vector Database**: ChromaDB for INCOSE standards
5. **Persistence**: SQLite for chat history

### Testing

Run the API tests:
```bash
python test_api.py
```

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add some amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/) for the powerful API framework
- [Groq](https://groq.com/) for the high-performance AI models
- [React](https://reactjs.org/) for the frontend framework
- [LangGraph](https://github.com/langchain-ai/langgraph) for AI workflow orchestration
- [INCOSE](https://www.incose.org/) for systems engineering standards

---

Created with ❤️ by [Tanishq-I](https://github.com/Tanishq-I)
