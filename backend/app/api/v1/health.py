"""
Health check endpoint.

Maps to SRS: API Health and Monitoring Requirements.
"""

from fastapi import APIRouter
from ...schemas import HealthResponse
from ...core.config import settings

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    
    Returns service status and model availability.
    """
    # Check if model can be loaded (lazy check)
    model_loaded = False
    try:
        from ...models.embeddings import get_model
        get_model()  # Attempt to load model
        model_loaded = True
    except Exception:
        pass
    
    return HealthResponse(
        status="healthy",
        version=settings.VERSION,
        model_loaded=model_loaded
    )

