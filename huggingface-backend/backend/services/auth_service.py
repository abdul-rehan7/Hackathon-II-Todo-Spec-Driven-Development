"""
Authentication service layer for user registration, login, and session management
"""
from sqlmodel import Session, select
from backend.src.models.user import User, UserCreate, UserRead
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
import os
from typing import Optional
from backend.src.utils.validation import is_valid_email, is_strong_password


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """
    Service class for handling authentication operations
    """

    def __init__(self, session: Session):
        self.session = session

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain password against its hash
        """
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """
        Generate a hash for the given password
        """
        return pwd_context.hash(password)

    def create_user(self, user_data: UserCreate) -> UserRead:
        """
        Create a new user with hashed password
        """
        # Validate email format
        if not is_valid_email(user_data.email):
            raise ValueError("Invalid email format")

        # Validate password strength
        is_valid, error_msg = is_strong_password(user_data.password)
        if not is_valid:
            raise ValueError(error_msg)

        # Check if user with this email already exists
        existing_user = self.session.exec(
            select(User).where(User.email == user_data.email)
        ).first()

        if existing_user:
            raise ValueError("User with this email already exists")

        # Hash the password
        password_hash = self.get_password_hash(user_data.password)

        # Create the user
        db_user = User(
            email=user_data.email,
            password_hash=password_hash,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)

        return UserRead.from_orm(db_user) if hasattr(UserRead, 'from_orm') else UserRead(
            id=db_user.id,
            email=db_user.email,
            created_at=db_user.created_at
        )

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user by email and password
        """
        user = self.session.exec(
            select(User).where(User.email == email)
        ).first()

        if not user or not self.verify_password(password, user.password_hash):
            return None

        return user

    def create_access_token(self, user_id: str) -> str:
        """
        Create a JWT access token for the user
        """
        expire = datetime.utcnow() + timedelta(minutes=30)  # Token expires in 30 minutes
        to_encode = {
            "sub": user_id,
            "exp": expire.timestamp(),
            "iat": datetime.utcnow().timestamp()
        }

        secret = os.getenv("BETTER_AUTH_SECRET", "fallback-secret")
        encoded_jwt = jwt.encode(to_encode, secret, algorithm="HS256")
        return encoded_jwt

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get a user by their email address
        """
        user = self.session.exec(
            select(User).where(User.email == email)
        ).first()

        return user

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        Get a user by their ID
        """
        user = self.session.get(User, user_id)
        return user

    def logout_user(self, user_id: str) -> bool:
        """
        Perform logout operations for the user (e.g., invalidate sessions)
        Currently a placeholder - in a real implementation, you might want to
        maintain a blacklist of tokens or invalidate active sessions.
        """
        # In a production implementation, you would typically:
        # 1. Add token to a blacklist
        # 2. Invalidate active sessions
        # 3. Perform cleanup operations
        # For now, this is a placeholder that just returns True

        # Placeholder for actual logout logic
        # In a real implementation with JWT, you might add the token to a
        # revocation list or maintain invalidated tokens in a database
        return True