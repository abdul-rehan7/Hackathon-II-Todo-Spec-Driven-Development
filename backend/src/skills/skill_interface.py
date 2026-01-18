"""
Skill interface definition for the AI-powered conversational todo interface.

This module defines the abstract base class that all skills must implement,
ensuring consistent behavior and structure across all skill implementations.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel


class SkillResult(BaseModel):
    """Standard result structure returned by all skills."""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class SkillInterface(ABC):
    """
    Abstract base class for all skills in the AI-powered conversational todo interface.

    All skills must inherit from this class and implement the execute method.
    Skills should be stateless and deterministic as required by the constitutional principles.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique identifier for the skill."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable description of what the skill does."""
        pass

    @property
    @abstractmethod
    def input_schema(self) -> Dict[str, Any]:
        """JSON schema defining expected input parameters for the skill."""
        pass

    @abstractmethod
    def execute(self, user_id: str, parameters: Dict[str, Any]) -> SkillResult:
        """
        Execute the skill with the given parameters for the specified user.

        Args:
            user_id: The ID of the user executing the skill
            parameters: Dictionary containing input parameters for the skill

        Returns:
            SkillResult containing the outcome of the execution
        """
        pass

    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """
        Validate that the provided parameters match the expected schema.

        Args:
            parameters: Parameters to validate

        Returns:
            True if parameters are valid, False otherwise
        """
        # Basic validation based on schema keys
        required_keys = [key for key, value in self.input_schema.get('properties', {}).items()
                        if key in self.input_schema.get('required', [])]

        for key in required_keys:
            if key not in parameters:
                return False

        return True