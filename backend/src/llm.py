import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from groq import Groq

# Cargar variables del archivo .env
load_dotenv()

class GroqModelHandler:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        model_name = os.getenv("TEXT_MODEL_NAME")

        # Validate that the API key is set
        if not api_key:
            raise ValueError("Groq API key is not set in the .env file.")
        if not model_name:
            raise ValueError("Text model name is not set in the .env file.")

        # Initialize the Groq client and ChatGroq LLM
        self.client = Groq(api_key=api_key)
        self.llm = ChatGroq(
            temperature=0.1,
            model_name=model_name,
            groq_api_key=api_key,
        )

    def get_client(self):
        """Return the Groq client instance."""
        return self.client

    def get_llm(self):
        """Return the LangChain LLM instance."""
        return self.llm