"""FastAPI controllers for image operations."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import HttpUrl

from src.domain.models import (
    ImageGenerationRequest,
    ImageEditRequest,
    ImageOperationResult,
)
from src.ports.image_service import ImageServicePort


def create_image_router(image_service: ImageServicePort) -> APIRouter:
    """Create FastAPI router for image operations.
    
    Args:
        image_service: Image service implementation
        
    Returns:
        Configured APIRouter
    """
    router = APIRouter(prefix="/api/v1/images", tags=["images"])

    @router.post("/generate", response_model=ImageOperationResult)
    async def generate_image(request: ImageGenerationRequest) -> ImageOperationResult:
        """Generate image using AI.
        
        Args:
            request: Image generation parameters
            
        Returns:
            Generated image result
            
        Raises:
            HTTPException: If generation fails
        """
        result = await image_service.generate_image(request)
        
        if not result.success:
            raise HTTPException(
                status_code=500,
                detail=result.error_message or "Image generation failed",
            )
        
        return result

    @router.post("/edit", response_model=ImageOperationResult)
    async def edit_image(request: ImageEditRequest) -> ImageOperationResult:
        """Edit image using AI (inpainting/outpainting).
        
        Args:
            request: Image editing parameters
            
        Returns:
            Edited image result
            
        Raises:
            HTTPException: If editing fails
        """
        result = await image_service.edit_image(request)
        
        if not result.success:
            raise HTTPException(
                status_code=500,
                detail=result.error_message or "Image editing failed",
            )
        
        return result

    @router.post("/remove-background", response_model=ImageOperationResult)
    async def remove_background(image_url: HttpUrl) -> ImageOperationResult:
        """Remove background from image.
        
        Args:
            image_url: URL of the image to process
            
        Returns:
            Processed image result
            
        Raises:
            HTTPException: If background removal fails
        """
        result = await image_service.remove_background(str(image_url))
        
        if not result.success:
            raise HTTPException(
                status_code=500,
                detail=result.error_message or "Background removal failed",
            )
        
        return result

    return router
