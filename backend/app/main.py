"""
FastAPI main application.

CCGT API entry point. Provides endpoints for text coherence evaluation.
Maps to SRS: API Architecture and Endpoints.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .core.logging import logger
from .api.v1 import evaluate, health

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Contextual Coherence Graph Transformer API for text coherence evaluation"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix=settings.API_V1_PREFIX, tags=["health"])
app.include_router(evaluate.router, prefix=settings.API_V1_PREFIX, tags=["evaluation"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs",
        "health": f"{settings.API_V1_PREFIX}/health"
    }


@app.on_event("startup")
async def startup_event():
    """Initialize on startup."""
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    logger.info(f"API docs available at /docs")
    logger.info(f"Memory-optimized mode: batch_size={settings.BATCH_SIZE}, float16={settings.USE_FLOAT16}")
    
    # Pre-warm the embedding model (lazy load on first use instead)
    # This helps identify model loading issues early
    try:
        from .models.embeddings import get_model
        logger.info("Model will be loaded on first request (lazy loading)")
    except Exception as e:
        logger.warning(f"Model import check failed: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down CCGT API")

