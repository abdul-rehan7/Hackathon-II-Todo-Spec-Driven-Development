"""
Todo query skill for the AI-powered conversational todo interface.

This skill handles querying and retrieving todos based on natural language input.
"""

from typing import Dict, Any
from pydantic import BaseModel
from .skill_interface import SkillInterface, SkillResult
from ..models.todo import Todo
from ..database import get_session
from sqlmodel import Session, select
from uuid import UUID


class TodoQueryParams(BaseModel):
    """Parameters for todo query skill."""
    status: str = None  # "completed", "pending", or None for all
    priority: str = None  # "high", "medium", "low", or None for all
    category: str = None  # Not implemented in current model but could be extended
    due_date_filter: str = None  # "today", "this-week", "overdue", etc.


class TodoQuerySkill(SkillInterface):
    """
    Skill for querying and retrieving todos based on natural language input.

    Implements the QUERY_TODOS intent as specified in the research and plan documents.
    """

    @property
    def name(self) -> str:
        return "todo_query_skill"

    @property
    def description(self) -> str:
        return "Queries and retrieves user's todos based on natural language input"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": ["completed", "pending", "all"],
                    "description": "Filter by completion status (optional)"
                },
                "priority": {
                    "type": "string",
                    "enum": ["high", "medium", "low"],
                    "description": "Filter by priority level (optional)"
                },
                "category": {
                    "type": "string",
                    "description": "Filter by category (optional)"
                },
                "due_date_filter": {
                    "type": "string",
                    "enum": ["today", "this-week", "overdue", "upcoming"],
                    "description": "Filter by due date context (optional)"
                }
            }
        }

    def execute(self, user_id: str, parameters: Dict[str, Any]) -> SkillResult:
        """
        Execute the todo query skill.

        Args:
            user_id: The ID of the user requesting the action
            parameters: Dictionary containing optional filter parameters

        Returns:
            SkillResult indicating success or failure with query results
        """
        try:
            # Build query with filters
            with get_session() as session:
                statement = select(Todo).where(Todo.user_id == user_id)

                # Apply status filter
                status_filter = parameters.get("status")
                if status_filter == "completed":
                    statement = statement.where(Todo.completed == True)
                elif status_filter == "pending":
                    statement = statement.where(Todo.completed == False)

                # Apply priority filter
                priority_filter = parameters.get("priority")
                if priority_filter:
                    # Map priority string to integer value (1=high, 3=medium, 5=low)
                    priority_map = {
                        "high": 1,
                        "medium": 3,
                        "low": 5
                    }
                    priority_int = priority_map.get(priority_filter, None)
                    if priority_int:
                        statement = statement.where(Todo.priority == priority_int)

                # Apply due date filters (simplified for this implementation)
                due_date_filter = parameters.get("due_date_filter")
                # Note: This would require more complex date handling in a full implementation

                # Execute the query
                todos = session.exec(statement).all()

                # Format the results
                todo_list = []
                for todo in todos:
                    # Map priority integer back to string
                    priority_map = {1: "high", 3: "medium", 5: "low"}
                    priority_str = priority_map.get(todo.priority, "medium")

                    todo_dict = {
                        "id": todo.id,
                        "title": todo.title,
                        "description": todo.description,
                        "completed": todo.completed,
                        "priority": priority_str,
                        "due_date": str(todo.due_date) if todo.due_date else None
                    }
                    todo_list.append(todo_dict)

                # Generate a human-readable response
                if not todo_list:
                    status_desc = f" {status_filter}" if status_filter else ""
                    priority_desc = f" {priority_filter}" if priority_filter else ""
                    response_msg = f"You don't have any{status_desc}{priority_desc} tasks right now."
                else:
                    count = len(todo_list)
                    status_desc = f" {status_filter}" if status_filter else ""
                    priority_desc = f" {priority_filter}" if priority_filter else ""
                    response_msg = f"You have {count} {status_desc}{priority_desc} task{'s' if count != 1 else ''}:"

                    # Add titles of the first few tasks to the response
                    for i, todo in enumerate(todo_list[:3]):  # Show first 3 tasks
                        response_msg += f"\n- [{'' if not todo['completed'] else 'x'}] {todo['title']}"

                    if count > 3:
                        response_msg += f"\n... and {count - 3} more."

            return SkillResult(
                success=True,
                message=response_msg,
                data={
                    "count": len(todo_list),
                    "todos": todo_list,
                    "filters_applied": {k: v for k, v in parameters.items() if v is not None}
                }
            )

        except Exception as e:
            return SkillResult(
                success=False,
                message="Failed to query todos",
                error=str(e)
            )


# Create an instance of the skill for registration
todo_query_skill = TodoQuerySkill()