import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from core.config_loader import load_config


class ModelLoader:
    """Utility class to load embedding and LLM models."""
    
    def __init__(self):
        load_dotenv()
        self._validate_env()
        self.config = load_config()

    def _validate_env(self):
        """Validate required environment variables."""
        required_vars = ["GOOGLE_API_KEY", "GROQ_API_KEY"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            raise EnvironmentError(f"Missing environment variables: {missing_vars}")
        
        self.groq_api_key = os.getenv("GROQ_API_KEY")

    def load_embeddings(self):
        """Load and return the embedding model."""
        model_name = self.config["embedding_model"]["model_name"]
        return GoogleGenerativeAIEmbeddings(model=model_name)

    def load_llm(self):
        """Load and return the LLM model."""
        model_name = self.config["llm"]["model_name"]
        return ChatGroq(model=model_name, api_key=self.groq_api_key)
