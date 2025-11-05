"""
Core configuration module for CCGT backend.

This module handles application settings, environment variables, and model configuration.
Maps to SRS: Configuration and Environment Setup.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "CCGT API"
    VERSION: str = "1.0.0"
    
    # Server Configuration
    HOST: str = "127.0.0.1"  # Local only
    PORT: int = 8000
    WORKERS: int = 1  # Single worker for memory efficiency
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    API_KEY_HEADER: str = "Authorization"
    
    # Model Configuration
    MODEL_NAME: str = "sentence-transformers/all-mpnet-base-v2"
    MODEL_CACHE_DIR: str = "./models"
    DEVICE: str = "cpu"  # Force CPU-only for memory efficiency
    
    # Graph Transformer Configuration
    GNN_HIDDEN_DIM: int = 128
    GNN_NUM_LAYERS: int = 3
    GNN_NUM_HEADS: int = 4
    GNN_DROPOUT: float = 0.1
    GNN_USE_GAT: bool = True
    
    # Pipeline Configuration (optimized for 6GB RAM)
    BATCH_SIZE: int = 8  # Reduced for memory efficiency
    MAX_SEQUENCE_LENGTH: int = 512
    CACHE_EMBEDDINGS: bool = True
    EMBEDDING_CACHE_DIR: str = "./models/embedding_cache"
    USE_FLOAT16: bool = True  # Use half precision for embeddings

    # Optimization toggle
    OPTIMIZED_MODE: bool = True
    ALPHA: float = 0.7
    BETA: float = 0.2
    GAMMA: float = 0.1
    
    # Database (for future use)
    DATABASE_URL: Optional[str] = None
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()


def get_device() -> str:
    """Auto-detect available device."""
    import torch
    if settings.DEVICE == "auto":
        return "cuda" if torch.cuda.is_available() else "cpu"
    return settings.DEVICE

