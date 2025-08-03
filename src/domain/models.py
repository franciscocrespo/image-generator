"""Domain models for image operations."""
from typing import Optional
from pydantic import BaseModel, HttpUrl


class ImageGenerationRequest(BaseModel):
    """Request model for image generation."""
    
    prompt: str
    size: str = "1024x1024"
    quality: str = "standard"
    n: int = 1


class ImageEditRequest(BaseModel):
    """Request model for image editing operations."""
    
    image_url: HttpUrl
    prompt: str
    mask_url: Optional[HttpUrl] = None
    size: str = "1024x1024"
    n: int = 1


class ImageResponse(BaseModel):
    """Response model for image operations."""
    
    url: HttpUrl
    revised_prompt: Optional[str] = None


class ImageOperationResult(BaseModel):
    """Result model for image operations."""
    
    success: bool
    images: list[ImageResponse]
    error_message: Optional[str] = None
