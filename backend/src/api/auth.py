"""
Authentication API endpoints for user registration, login, and logout
"""
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import HTTPAuthorizationCredentials
from sqlmodel import Session
from backend.src.database.connection import get_session
from backend.src.models.user import UserCreate, UserRead, User
from backend.src.services.auth_service import AuthService
from backend.src.middleware.auth_middleware import security, get_current_user as get_user_from_token
from datetime import datetime
from typing import Dict, Any


router = APIRouter(prefix="/auth", tags=["auth"])


# Define the dependency function to get current user from middleware
async def get_current_user_dependency(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> User:
    """
    Get current authenticated user from token in middleware
    """
    user = get_user_from_token(credentials, session)
    return user


@router.post("/register", status_code=201)
async def register(
    email: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)
):
    """
    Register a new user
    """
    # Create user data object
    user_data = UserCreate(email=email, password=password)
    auth_service = AuthService(session)

    try:
        # Create the user
        user = auth_service.create_user(user_data)

        # Create access token for the new user
        access_token = auth_service.create_access_token(user.id)

        # Return user data and session info
        return {
            "user": {
                "id": user.id,
                "email": user.email
            },
            "session": {
                "token": access_token,
                "expiresAt": (datetime.utcnow().timestamp() + 1800)  # 30 minutes from now
            }
        }
    except ValueError as e:
        # Handle validation errors
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Handle other errors (like duplicate email)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.post("/login")
async def login(
    email: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)
):
    """
    Authenticate user and return access token
    """
    auth_service = AuthService(session)

    # Authenticate the user
    user = auth_service.authenticate_user(email, password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Create access token
    access_token = auth_service.create_access_token(user.id)

    return {
        "user": {
            "id": user.id,
            "email": user.email
        },
        "session": {
            "token": access_token,
            "expiresAt": (datetime.utcnow().timestamp() + 1800)  # 30 minutes from now
        }
    }


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user_dependency),
    session: Session = Depends(get_session)
):
    """
    Logout user and perform cleanup operations
    """
    auth_service = AuthService(session)

    # Perform logout operations
    logout_success = auth_service.logout_user(current_user.id)

    if not logout_success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error during logout process"
        )

    return {"message": "Successfully logged out"}


@router.get("/me")
async def get_current_user(
    current_user: User = Depends(get_current_user_dependency)
):
    """
    Get current authenticated user's information
    """
    return {
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "createdAt": current_user.created_at
        }
    }