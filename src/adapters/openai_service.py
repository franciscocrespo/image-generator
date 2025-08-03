"""OpenAI adapter for image operations."""
import logging
from typing import Optional

from openai import AsyncOpenAI
from pydantic import HttpUrl

from src.domain.models import (
    ImageGenerationRequest,
    ImageEditRequest,
    ImageOperationResult,
    ImageResponse,
)
from src.ports.image_service import ImageServicePort

logger = logging.getLogger(__name__)


class OpenAIImageService(ImageServicePort):
    """OpenAI implementation of image service."""

    def __init__(self, api_key: str) -> None:
        """Initialize OpenAI client.
        
        Args:
            api_key: OpenAI API key
        """
        self.client = AsyncOpenAI(api_key=api_key)

    async def generate_image(self, request: ImageGenerationRequest) -> ImageOperationResult:
        """Generate image using DALL-E.
        
        Args:
            request: Image generation parameters
            
        Returns:
            Result containing generated images or error
        """
        try:
            response = await self.client.images.generate(
                model="dall-e-3",
                prompt=request.prompt,
                size=request.size,
                quality=request.quality,
                n=request.n,
            )
            
            images = [
                ImageResponse(
                    url=HttpUrl(img.url),
                    revised_prompt=img.revised_prompt,
                )
                for img in response.data
            ]
            
            return ImageOperationResult(success=True, images=images)
            
        except Exception as e:
            logger.error(f"Error generating image: {str(e)}")
            return ImageOperationResult(
                success=False,
                images=[],
                error_message=str(e),
            )

    async def edit_image(self, request: ImageEditRequest) -> ImageOperationResult:
        """Edit image using DALL-E.
        
        Args:
            request: Image editing parameters
            
        Returns:
            Result containing edited images or error
        """
        try:
            # Para MVP, utilizamos la función de edición básica de OpenAI
            # En el futuro se puede expandir para diferentes tipos de edición
            response = await self.client.images.edit(
                image=str(request.image_url),
                mask=str(request.mask_url) if request.mask_url else None,
                prompt=request.prompt,
                n=request.n,
                size=request.size,
            )
            
            images = [
                ImageResponse(url=HttpUrl(img.url))
                for img in response.data
            ]
            
            return ImageOperationResult(success=True, images=images)
            
        except Exception as e:
            logger.error(f"Error editing image: {str(e)}")
            return ImageOperationResult(
                success=False,
                images=[],
                error_message=str(e),
            )

    async def remove_background(self, image_url: str) -> ImageOperationResult:
        """Remove background from image.
        
        Note: OpenAI no tiene una función específica para remover fondo,
        por lo que utilizamos edición con un prompt específico.
        
        Args:
            image_url: URL of the image to process
            
        Returns:
            Result containing processed image or error
        """
        try:
            edit_request = ImageEditRequest(
                image_url=HttpUrl(image_url),
                prompt="remove background, transparent background",
            )
            
            return await self.edit_image(edit_request)
            
        except Exception as e:
            logger.error(f"Error removing background: {str(e)}")
            return ImageOperationResult(
                success=False,
                images=[],
                error_message=str(e),
            )
