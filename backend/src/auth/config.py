"""
Configuration for better-auth SDK
"""
from better_auth import init, models
from better_auth.types import Config


def get_auth_config() -> Config:
    """
    Returns the configuration for better-auth
    """
    return init(
        secret="your-super-secret-key-here-change-this-for-production",
        base_url="http://localhost:8000",
        email_password={
            "enabled": True,
        },
        database={
            "provider": "postgresql",
            "url": "postgresql://username:password@localhost:5432/donezo_db"
        }
    )


# Initialize the auth instance
auth = get_auth_config()