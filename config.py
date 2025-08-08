import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama3-8b-8192"

AVAILABLE_MODELS = {
    "llama3-8b-8192": {
        "name": "LLAMA3 8B",
        "description": "Fast and efficient 8B parameter model",
        "provider": "groq"
    },
    "llama3-70b-8192": {
        "name": "LLAMA3 70B",
        "description": "More powerful 70B parameter model",
        "provider": "groq"
    },
    "mistral-8x7b-32768": {
        "name": "Mistral 8x7B",
        "description": "Mixture of experts model with 32k context",
        "provider": "groq"
    },
    "gemma-7b-it": {
        "name": "Gemma 7B",
        "description": "Google's Gemma 7B instruction-tuned model",
        "provider": "groq"
    },
    "gemma2-9b-it": {
        "name": "Gemma 2 9B",
        "description": "Latest Gemma 2 9B instruction-tuned model",
        "provider": "groq"
    }
}