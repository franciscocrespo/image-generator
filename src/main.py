"""Main FastAPI application."""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.adapters.api_controllers import create_image_router
from src.adapters.openai_service import OpenAIImageService
from src.config import get_settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("Starting Image Generator API")
    yield
    logger.info("Shutting down Image Generator API")


def create_app() -> FastAPI:
    """Create and configure FastAPI application.
    
    Returns:
        Configured FastAPI app
    """
    settings = get_settings()
    
    # Validate OpenAI API key
    if not settings.openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    
    app = FastAPI(
        title=settings.title,
        description=settings.description,
        version=settings.version,
        lifespan=lifespan,
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_credentials,
        allow_methods=settings.cors_methods,
        allow_headers=settings.cors_headers,
    )
    
    # Initialize services
    image_service = OpenAIImageService(api_key=settings.openai_api_key)
    
    # Add routers
    image_router = create_image_router(image_service)
    app.include_router(image_router)
    
    @app.get("/health")
    async def health_check() -> dict[str, str]:
        """Health check endpoint.
        
        Returns:
            Health status
        """
        return {"status": "healthy"}
    
    return app


app = create_app()
