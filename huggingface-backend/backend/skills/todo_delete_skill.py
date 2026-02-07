"""
Todo deletion skill for the AI-powered conversational todo interface.

This skill handles the deletion of existing todos based on natural language input.
"""

from typing import Dict, Any
from pydantic import BaseModel
from .skill_interface import SkillInterface, SkillResult
from ..models.todo import Todo
from ..database import get_session
from sqlmodel import Session, select
from uuid import UUID


class TodoDeleteParams(BaseModel):
    """Parameters for todo deletion skill."""
    todo_id: int


class TodoDeleteSkill(SkillInterface):
    """
    Skill for deleting existing todos based on natural language input.

    Implements the DELETE_TODO intent as specified in the research and plan documents.
    """

    @property
    def name(self) -> str:
        return "todo_delete_skill"

    @property
    def description(self) -> str:
        return "Deletes existing todos based on natural language input"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "todo_id": {
                    "type": "integer",
                    "description": "The ID of the todo to delete"
                }
            },
            "required": ["todo_id"]
        }

    def execute(self, user_id: str, parameters: Dict[str, Any]) -> SkillResult:
        """
        Execute the todo deletion skill.

        Args:
            user_id: The ID of the user requesting the action
            parameters: Dictionary containing the todo ID to delete

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

            # Delete the todo from the database
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

                # Delete the todo
                session.delete(todo)
                session.commit()

            return SkillResult(
                success=True,
                message=f"Successfully deleted todo: '{todo.title}' (ID: {todo_id})",
                data={
                    "deleted_todo_id": todo_id,
                    "deleted_title": todo.title
                }
            )

        except Exception as e:
            return SkillResult(
                success=False,
                message="Failed to delete todo",
                error=str(e)
            )


# Create an instance of the skill for registration
todo_delete_skill = TodoDeleteSkill()