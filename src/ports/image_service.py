"""Port interface for image services."""
from abc import ABC, abstractmethod

from src.domain.models import (
    ImageGenerationRequest,
    ImageEditRequest,
    ImageOperationResult,
)


class ImageServicePort(ABC):
    """Abstract interface for image operations."""

    @abstractmethod
    async def generate_image(self, request: ImageGenerationRequest) -> ImageOperationResult:
        """Generate image using AI.
        
        Args:
            request: Image generation parameters
            
        Returns:
            Result containing generated images or error
        """
        pass

    @abstractmethod
    async def edit_image(self, request: ImageEditRequest) -> ImageOperationResult:
        """Edit image using AI (inpainting/outpainting).
        
        Args:
            request: Image editing parameters
            
        Returns:
            Result containing edited images or error
        """
        pass

    @abstractmethod
    async def remove_background(self, image_url: str) -> ImageOperationResult:
        """Remove background from image.
        
        Args:
            image_url: URL of the image to process
            
        Returns:
            Result containing processed image or error
        """
        pass
