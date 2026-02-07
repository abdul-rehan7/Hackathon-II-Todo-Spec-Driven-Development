"""
Todo creation skill for the AI-powered conversational todo interface.

This skill handles the creation of new todos based on natural language input.
"""

from typing import Dict, Any
from pydantic import BaseModel
from .skill_interface import SkillInterface, SkillResult
from ..models.todo import Todo, TodoCreate, Priority
from ..database import get_session
from sqlmodel import Session, select
from uuid import UUID
import re


class TodoCreateParams(BaseModel):
    """Parameters for todo creation skill."""
    content: str
    due_date: str = None
    priority: str = "medium"
    category: str = None


class TodoCreateSkill(SkillInterface):
    """
    Skill for creating new todos based on natural language input.

    Implements the CREATE_TODO intent as specified in the research and plan documents.
    """

    @property
    def name(self) -> str:
        return "todo_create_skill"

    @property
    def description(self) -> str:
        return "Creates new todos based on natural language input"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "The content/description of the todo"
                },
                "due_date": {
                    "type": "string",
                    "description": "Due date for the todo (optional)"
                },
                "priority": {
                    "type": "string",
                    "enum": ["low", "medium", "high"],
                    "description": "Priority level (default: medium)"
                },
                "category": {
                    "type": "string",
                    "description": "Category/area of life for the todo (optional)"
                }
            },
            "required": ["content"]
        }

    def execute(self, user_id: str, parameters: Dict[str, Any]) -> SkillResult:
        """
        Execute the todo creation skill.

        Args:
            user_id: The ID of the user requesting the action
            parameters: Dictionary containing content and optional parameters

        Returns:
            SkillResult indicating success or failure
        """
        try:
            # Validate parameters
            if not self.validate_parameters(parameters):
                return SkillResult(
                    success=False,
                    message="Invalid parameters provided",
                    error="Required parameters missing or invalid"
                )

            # Extract parameters
            content = parameters.get("content", "").strip()
            due_date = parameters.get("due_date")
            priority_str = parameters.get("priority", "medium").lower()
            category = parameters.get("category")

            # Validate content
            if not content:
                return SkillResult(
                    success=False,
                    message="Cannot create a todo without content",
                    error="Empty content provided"
                )

            # Map priority string to integer value (1=high, 3=medium, 5=low)
            priority_map = {
                "high": 1,
                "medium": 3,
                "low": 5
            }
            priority = priority_map.get(priority_str, 3)  # Default to medium (3)

            # Create the todo using the database session
            with get_session() as session:
                # Create a new Todo instance
                new_todo = Todo(
                    title=content,
                    description=content,  # Using content as description as well
                    completed=False,
                    priority=priority,
                    user_id=user_id  # Associate with the authenticated user
                )

                # Set due date if provided
                if due_date:
                    # This would require additional processing depending on the format
                    # For now, we'll just store it as a string representation
                    # In a real implementation, this would convert to a proper datetime
                    new_todo.due_date = due_date

                # Add and commit the new todo
                session.add(new_todo)
                session.commit()
                session.refresh(new_todo)

            return SkillResult(
                success=True,
                message=f"Successfully created todo: '{content}'",
                data={
                    "todo_id": new_todo.id,
                    "content": content,
                    "due_date": str(new_todo.due_date) if new_todo.due_date else None,
                    "priority": priority_str,
                    "category": category
                }
            )

        except Exception as e:
            return SkillResult(
                success=False,
                message="Failed to create todo",
                error=str(e)
            )


# Create an instance of the skill for registration
todo_create_skill = TodoCreateSkill()