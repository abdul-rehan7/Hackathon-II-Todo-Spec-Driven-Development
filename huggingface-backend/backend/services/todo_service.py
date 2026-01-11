"""
Todo service layer for handling business logic related to Todo operations
"""
from sqlmodel import Session, select
from typing import List, Optional
from backend.src.models.todo import Todo, TodoCreate, TodoUpdate
from backend.src.models.user import User
from datetime import datetime


class TodoService:
    """
    Service class for handling Todo operations with user scoping
    """

    def __init__(self, session: Session):
        self.session = session

    def create_todo(self, todo_data: TodoCreate, user_id: str) -> Todo:
        """
        Create a new todo for the specified user
        """
        db_todo = Todo.model_validate(todo_data)
        db_todo.user_id = user_id
        db_todo.created_at = datetime.utcnow()
        db_todo.updated_at = datetime.utcnow()

        self.session.add(db_todo)
        self.session.commit()
        self.session.refresh(db_todo)

        return db_todo

    def get_todos_by_user(self, user_id: str, offset: int = 0, limit: int = 100) -> List[Todo]:
        """
        Get all todos for the specified user with pagination
        """
        todos = self.session.exec(
            select(Todo)
            .where(Todo.user_id == user_id)
            .offset(offset)
            .limit(limit)
        ).all()

        return todos

    def get_todo_by_id_and_user(self, todo_id: int, user_id: str) -> Optional[Todo]:
        """
        Get a specific todo by ID for the specified user
        """
        todo = self.session.exec(
            select(Todo)
            .where(Todo.id == todo_id)
            .where(Todo.user_id == user_id)
        ).first()

        return todo

    def update_todo_by_id_and_user(self, todo_id: int, user_id: str, todo_data: TodoUpdate) -> Optional[Todo]:
        """
        Update a specific todo by ID for the specified user
        """
        db_todo = self.session.exec(
            select(Todo)
            .where(Todo.id == todo_id)
            .where(Todo.user_id == user_id)
        ).first()

        if not db_todo:
            return None

        # Update only the fields that are provided
        todo_data_dict = todo_data.model_dump(exclude_unset=True)
        for key, value in todo_data_dict.items():
            setattr(db_todo, key, value)

        db_todo.updated_at = datetime.utcnow()
        self.session.add(db_todo)
        self.session.commit()
        self.session.refresh(db_todo)

        return db_todo

    def delete_todo_by_id_and_user(self, todo_id: int, user_id: str) -> bool:
        """
        Delete a specific todo by ID for the specified user
        """
        db_todo = self.session.exec(
            select(Todo)
            .where(Todo.id == todo_id)
            .where(Todo.user_id == user_id)
        ).first()

        if not db_todo:
            return False

        self.session.delete(db_todo)
        self.session.commit()

        return True