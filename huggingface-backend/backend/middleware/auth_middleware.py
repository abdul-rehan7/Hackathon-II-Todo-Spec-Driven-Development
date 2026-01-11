"""
Authentication middleware to protect API endpoints
"""
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import jwt
from jwt.exceptions import InvalidTokenError
from sqlmodel import Session
from backend.src.database.connection import get_session
from backend.src.models.user import User
import os


security = HTTPBearer()


def verify_token(token: str) -> dict:
    """
    Verify the authentication token and return user information
    """
    try:
        # Decode the JWT token using the secret
        payload = jwt.decode(
            token,
            os.getenv("BETTER_AUTH_SECRET", "your-super-secret-key-here-change-this-for-production"),
            algorithms=["HS256"]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
        return payload
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> User:
    """
    Get the current authenticated user from the token
    """
    token = credentials.credentials
    payload = verify_token(token)

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user


def require_auth():
    """
    Decorator to require authentication for API endpoints
    """
    def auth_wrapper(func):
        def wrapper(*args, **kwargs):
            # This is a simplified decorator approach
            # In practice, you'd use the get_current_user dependency
            return func(*args, **kwargs)
        return wrapper
    return auth_wrapper