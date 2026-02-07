"""
Todo update skill for the AI-powered conversational todo interface.

This skill handles the updating of existing todos based on natural language input.
"""

from typing import Dict, Any
from pydantic import BaseModel
from .skill_interface import SkillInterface, SkillResult
from ..models.todo import Todo, TodoUpdate, Priority
from ..database import get_session
from sqlmodel import Session, select
from uuid import UUID


class TodoUpdateParams(BaseModel):
    """Parameters for todo update skill."""
    todo_id: int
    title: str = None
    description: str = None
    completed: bool = None
    priority: str = None
    due_date: str = None


class TodoUpdateSkill(SkillInterface):
    """
    Skill for updating existing todos based on natural language input.

    Implements the UPDATE_TODO intent as specified in the research and plan documents.
    """

    @property
    def name(self) -> str:
        return "todo_update_skill"

    @property
    def description(self) -> str:
        return "Updates existing todos based on natural language input"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "todo_id": {
                    "type": "integer",
                    "description": "The ID of the todo to update"
                },
                "title": {
                    "type": "string",
                    "description": "The new title for the todo (optional)"
                },
                "description": {
                    "type": "string",
                    "description": "The new description for the todo (optional)"
                },
                "completed": {
                    "type": "boolean",
                    "description": "Whether the todo is completed (optional)"
                },
                "priority": {
                    "type": "string",
                    "enum": ["low", "medium", "high"],
                    "description": "The new priority level (optional)"
                },
                "due_date": {
                    "type": "string",
                    "description": "The new due date for the todo (optional)"
                }
            },
            "required": ["todo_id"]
        }

    def execute(self, user_id: str, parameters: Dict[str, Any]) -> SkillResult:
        """
        Execute the todo update skill.

        Args:
            user_id: The ID of the user requesting the action
            parameters: Dictionary containing todo ID and optional update fields

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
            todo_id = parameters.get("todo_id")

            # Prepare update data
            update_data = {}
            if "title" in parameters and parameters["title"] is not None:
                update_data["title"] = parameters["title"]
            if "description" in parameters and parameters["description"] is not None:
                update_data["description"] = parameters["description"]
            if "completed" in parameters and parameters["completed"] is not None:
                update_data["completed"] = parameters["completed"]
            if "due_date" in parameters and parameters["due_date"] is not None:
                update_data["due_date"] = parameters["due_date"]
            if "priority" in parameters and parameters["priority"] is not None:
                # Map priority string to integer value (1=high, 3=medium, 5=low)
                priority_map = {
                    "high": 1,
                    "medium": 3,
                    "low": 5
                }
                priority = priority_map.get(parameters["priority"], 3)  # Default to medium (3)
                update_data["priority"] = priority

            # Check if there's anything to update
            if not update_data:
                return SkillResult(
                    success=False,
                    message="No valid fields to update",
                    error="No update parameters provided"
                )

            # Update the todo in the database
            with get_session() as session:
                # Find the todo that belongs to the user
                statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
                todo = session.exec(statement).first()

                if not todo:
                    return SkillResult(
                        success=False,
                        message=f"Todo with ID {todo_id} not found or doesn't belong to user",
                        error="Todo not found or access denied"
                    )

                # Update the todo with the provided data
                for key, value in update_data.items():
                    setattr(todo, key, value)

                # Commit the changes
                session.add(todo)
                session.commit()
                session.refresh(todo)

            return SkillResult(
                success=True,
                message=f"Successfully updated todo ID {todo_id}",
                data={
                    "todo_id": todo.id,
                    "title": todo.title,
                    "completed": todo.completed,
                    "priority": todo.priority,
                    "updated_fields": list(update_data.keys())
                }
            )

        except Exception as e:
            return SkillResult(
                success=False,
                message="Failed to update todo",
                error=str(e)
            )


# Create an instance of the skill for registration
todo_update_skill = TodoUpdateSkill()