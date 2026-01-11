"""
Security middleware for authentication and validation
"""
from fastapi import Request, Response, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Optional
import logging
import re

logger = logging.getLogger(__name__)

class SecurityMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add security headers and perform basic security validations
    """

    async def dispatch(self, request: Request, call_next):
        # Add security headers to response
        response: Response = await call_next(request)

        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = "default-src 'self'"

        return response


def validate_input(input_data: str, input_type: str = "general") -> tuple[bool, str]:
    """
    Validate input data for security purposes

    Args:
        input_data: The input to validate
        input_type: Type of input ('email', 'password', 'username', 'general')

    Returns:
        Tuple of (is_valid, error_message)
    """
    if input_data is None:
        return False, "Input cannot be null"

    # Check for common attack patterns
    dangerous_patterns = [
        r"<script",  # XSS attempts
        r"javascript:",  # JavaScript injection
        r"vbscript:",  # VBScript injection
        r"on\w+\s*=",  # Event handlers
        r"eval\s*\(",  # Eval function calls
        r"expression\s*\(",  # CSS expressions
    ]

    for pattern in dangerous_patterns:
        if re.search(pattern, input_data, re.IGNORECASE):
            return False, f"Potentially dangerous content detected: {pattern}"

    # Specific validation based on input type
    if input_type == "email":
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, input_data):
            return False, "Invalid email format"

    elif input_type == "password":
        # Basic password strength validation
        if len(input_data) < 8:
            return False, "Password must be at least 8 characters long"

        # Check for password complexity
        has_upper = bool(re.search(r'[A-Z]', input_data))
        has_lower = bool(re.search(r'[a-z]', input_data))
        has_digit = bool(re.search(r'\d', input_data))
        has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', input_data))

        if not (has_upper and has_lower and has_digit):
            return False, "Password must contain uppercase, lowercase, and numeric characters"

    return True, ""


def sanitize_input(input_data: str) -> str:
    """
    Sanitize input data by removing potentially dangerous characters
    """
    if not input_data:
        return input_data

    # Remove potentially dangerous characters
    sanitized = input_data.replace('<', '&lt;').replace('>', '&gt;')
    sanitized = sanitized.replace('"', '&quot;').replace("'", '&#x27;')
    sanitized = sanitized.replace('/', '&#x2F;')

    return sanitized


def rate_limit_check(identifier: str) -> tuple[bool, str]:
    """
    Check if a request should be rate-limited
    Note: This is a simplified version - in production, use redis or similar for distributed rate limiting
    """
    # This is a placeholder implementation
    # In a real application, you would track request counts in a distributed store
    return True, ""  # Allow all requests for now


def validate_jwt_payload(payload: dict) -> tuple[bool, str]:
    """
    Validate JWT payload for security requirements
    """
    try:
        # Check if token has expired
        import time
        exp = payload.get("exp")
        if exp and exp < time.time():
            return False, "Token has expired"

        # Check if token was issued in the past
        iat = payload.get("iat")
        if iat and iat > time.time():
            return False, "Token was issued in the future"

        # Validate subject exists
        sub = payload.get("sub")
        if not sub:
            return False, "Token subject is missing"

        return True, ""
    except Exception as e:
        return False, f"Token validation error: {str(e)}"