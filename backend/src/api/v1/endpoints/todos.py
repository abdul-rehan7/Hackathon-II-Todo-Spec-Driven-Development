from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from backend.src.models.todo import Todo, TodoCreate, TodoRead, TodoUpdate
from backend.src.database.connection import get_session
import logging

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/todos/", response_model=TodoRead, status_code=status.HTTP_201_CREATED)
def create_todo(*, session: Session = Depends(get_session), todo: TodoCreate):
    """
    Create a new todo item.
    """
    try:
        # Validate input data
        if not todo.title or len(todo.title.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Todo title cannot be empty"
            )

        db_todo = Todo.model_validate(todo)
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
        logger.info(f"Created new todo with ID: {db_todo.id}")
        return db_todo
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating todo: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the todo"
        )

@router.get("/todos/", response_model=List[TodoRead])
def read_todos(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = 100
):
    """
    Retrieve a list of todo items with pagination.
    """
    try:
        # Validate pagination parameters
        if offset < 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Offset cannot be negative"
            )
        if limit <= 0 or limit > 1000:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Limit must be between 1 and 1000"
            )

        todos = session.exec(select(Todo).offset(offset).limit(limit)).all()
        logger.info(f"Retrieved {len(todos)} todos")
        return todos
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving todos: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving todos"
        )

@router.get("/todos/{todo_id}", response_model=TodoRead)
def read_todo(*, session: Session = Depends(get_session), todo_id: int):
    """
    Retrieve a specific todo item by ID.
    """
    try:
        if todo_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Todo ID must be a positive integer"
            )

        todo = session.get(Todo, todo_id)
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo with ID {todo_id} not found"
            )
        logger.info(f"Retrieved todo with ID: {todo_id}")
        return todo
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving todo with ID {todo_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the todo"
        )

@router.put("/todos/{todo_id}", response_model=TodoRead)
def update_todo(*, session: Session = Depends(get_session), todo_id: int, todo: TodoUpdate):
    """
    Update a specific todo item by ID.
    """
    try:
        if todo_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Todo ID must be a positive integer"
            )

        db_todo = session.get(Todo, todo_id)
        if not db_todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo with ID {todo_id} not found"
            )

        # Validate update data if title is being updated
        if todo.title is not None and len(todo.title.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Todo title cannot be empty"
            )

        todo_data = todo.model_dump(exclude_unset=True)
        for key, value in todo_data.items():
            setattr(db_todo, key, value)
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
        logger.info(f"Updated todo with ID: {todo_id}")
        return db_todo
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating todo with ID {todo_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the todo"
        )

@router.delete("/todos/{todo_id}", status_code=status.HTTP_200_OK)
def delete_todo(*, session: Session = Depends(get_session), todo_id: int):
    """
    Delete a specific todo item by ID.
    """
    try:
        if todo_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Todo ID must be a positive integer"
            )

        todo = session.get(Todo, todo_id)
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo with ID {todo_id} not found"
            )

        session.delete(todo)
        session.commit()
        logger.info(f"Deleted todo with ID: {todo_id}")
        return {"message": "Todo deleted successfully", "id": todo_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting todo with ID {todo_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the todo"
        )
