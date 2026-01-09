from datetime import datetime
from typing import Optional, List
from enum import Enum
import json
from sqlmodel import Field, SQLModel, Column
from sqlalchemy import String
from sqlalchemy.types import TypeDecorator, TEXT

class JSONList(TypeDecorator):
    impl = TEXT
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)
        return value


class Priority(str, Enum):
    low = "Low"
    medium = "Medium"
    high = "High"

class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, index=False)
    completed: bool = Field(default=False)
    priority: int = Field(default=1, ge=1, le=5) # 1 (high) to 5 (low)
    due_date: Optional[datetime] = Field(default=None)

    # tags: List["TodoTagLink"] = Relationship(back_populates="todo") # Commenting out for now as tags are not directly implemented in this phase

class TodoCreate(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    priority: int = Field(default=1, ge=1, le=5)
    due_date: Optional[datetime] = None

class TodoRead(SQLModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    priority: int
    due_date: Optional[datetime] = None

class TodoUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[int] = Field(default=None, ge=1, le=5)
    due_date: Optional[datetime] = None

