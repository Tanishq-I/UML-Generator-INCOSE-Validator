# 🚀 Quick Start Guide

This guide will help you get the UML Generator & INCOSE Validator up and running quickly.

## ⚙️ Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- Node.js 14.0 or higher
- npm 6.0 or higher
- Git

You'll also need a Groq API key, which you can obtain from [https://console.groq.com/keys](https://console.groq.com/keys). 
Groq provides fast inference with various large language models used for UML generation and INCOSE validation.

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Tanishq-I/UML-Generator-INCOSE-Validator.git
cd UML-Generator-INCOSE-Validator
```

### 2. Set Up Backend

#### Create a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your Groq API key
# On Windows
notepad .env
# On macOS/Linux
nano .env
```

Add your Groq API key to the `.env` file:
```
GROQ_API_KEY=your_groq_api_key_here
```

#### Initialize Vector Database

This step creates the vector database with INCOSE standards for requirement validation:

```bash
python setup_vectorstore.py
```

The process may take a few minutes as it processes the INCOSE standards document.

### 3. Set Up Frontend

```bash
cd frontend
npm install
```

## 🚀 Running the Application

### Start the Backend Server

From the project root directory:

```bash
# Make sure your virtual environment is activated
uvicorn app:app --reload
```

The API will be available at http://localhost:8000

You can access the API documentation at:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

### Start the Frontend Development Server

In a new terminal window:

```bash
cd frontend
npm start
```

The frontend will be available at http://localhost:3000

## 🎮 Using the Application

### Generate UML Diagrams

1. Navigate to http://localhost:3000 in your browser
2. Select "Generate UML" from the navigation menu
3. Enter a natural language description of your system
4. Choose a UML diagram type (class, sequence, use case, activity, state)
5. Select an AI model (Llama 3, Mixtral, or Gemma)
6. Click "Generate" and wait for the result
7. View, download, or export the generated diagram

### Validate Requirements

1. Navigate to http://localhost:3000 in your browser
2. Select "Validate Requirement" from the navigation menu
3. Enter a system requirement statement
4. Select an AI model (Llama 3 recommended for best results)
5. Click "Validate" and wait for the analysis
6. Review the validation results, score, and improvement suggestions

### Manage Sessions

1. Create a new session for your project
2. All UML diagrams and requirement validations will be saved in your session
3. Switch between sessions to manage different projects
4. Rename or delete sessions as needed

## 🧪 Testing

To run the API tests:

```bash
python test_api.py
```

## 📚 Additional Resources

- [API Documentation](API_DOCUMENTATION.md)
- [Contributing Guide](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

## ❓ Troubleshooting

### API Server Won't Start

- Check that you have the correct Python version (3.8+)
- Verify that all dependencies are installed correctly
- Ensure the `.env` file exists and has the correct GROQ_API_KEY
- Check the error output in the terminal for specific issues

### Frontend Server Won't Start

- Verify that Node.js (14.0+) and npm (6.0+) are correctly installed
- Check that all frontend dependencies are installed with `npm install`
- Ensure no other service is using port 3000
- Try clearing npm cache: `npm cache clean --force`

### UML Generation Errors

- Ensure your Groq API key is valid and has sufficient quota
- Check that your scenario description is clear and detailed
- Try using a more powerful model (e.g., llama3-70b-8192) for complex scenarios
- Simplify complex scenarios into smaller components

### Validation Errors

- Ensure your requirement statement is written in English
- Try different AI models if you receive inconsistent results
- Check that the vector database was initialized correctly

### Other Issues

For other issues, please check the [GitHub issues](https://github.com/Tanishq-I/UML-Generator-INCOSE-Validator/issues) or create a new one.

---

Happy Modeling! 📊
