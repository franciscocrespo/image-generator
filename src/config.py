"""Application configuration."""
import os
from functools import lru_cache

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings."""
    
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    
    # FastAPI settings
    title: str = "Image Generator API"
    description: str = "API Backend for AI image generation and editing"
    version: str = "0.1.0"
    
    # CORS settings
    cors_origins: list[str] = ["*"]
    cors_credentials: bool = True
    cors_methods: list[str] = ["*"]
    cors_headers: list[str] = ["*"]


@lru_cache()
def get_settings() -> Settings:
    """Get application settings (cached).
    
    Returns:
        Settings instance
    """
    return Settings()
