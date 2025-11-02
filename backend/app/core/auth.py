"""
Authentication and authorization module.

Implements JWT-based API key authentication for the CCGT API.
Maps to SRS: Security and Authentication Requirements.
"""

import os
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from .config import settings

security = HTTPBearer()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Verify JWT token from Authorization header.
    
    Args:
        credentials: HTTP Bearer token from request header
        
    Returns:
        Decoded token payload
        
    Raises:
        HTTPException: If token is invalid or missing
    """
    token = credentials.credentials
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_api_key() -> Optional[str]:
    """Get API key from environment (for development/testing)."""
    return os.getenv("API_KEY", None)


def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)) -> bool:
    """
    Verify API key authentication (simpler alternative to JWT).
    
    For production, use proper JWT tokens. This is a convenience for development.
    """
    token = credentials.credentials
    api_key = get_api_key()
    
    if api_key and token == api_key:
        return True
    
    # Fallback to JWT verification
    try:
        verify_token(credentials)
        return True
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key or token",
            headers={"WWW-Authenticate": "Bearer"},
        )

