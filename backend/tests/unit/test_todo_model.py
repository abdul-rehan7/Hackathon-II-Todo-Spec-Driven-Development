from datetime import datetime, timedelta
import pytest
from pydantic import ValidationError
from backend.src.models.todo import Todo, TodoCreate, TodoRead, TodoUpdate # Import the actual models

def test_todo_create_valid():
    todo = TodoCreate(title="Test Todo")
    assert todo.title == "Test Todo"
    assert todo.description is None
    assert todo.priority == 1
    assert todo.due_date is None

def test_todo_create_with_all_fields():
    due = datetime.now() + timedelta(days=1)
    todo = TodoCreate(
        title="Full Todo",
        description="A complete todo item",
        priority=3,
        due_date=due
    )
    assert todo.title == "Full Todo"
    assert todo.description == "A complete todo item"
    assert todo.priority == 3
    assert todo.due_date == due

def test_todo_create_empty_title_fails():
    with pytest.raises(ValidationError):
        TodoCreate(title="")

def test_todo_create_long_title_fails():
    with pytest.raises(ValidationError):
        TodoCreate(title="a" * 256) # Assuming a max length of 255 for title

def test_todo_create_priority_too_low_fails():
    with pytest.raises(ValidationError):
        TodoCreate(title="Test", priority=0)

def test_todo_create_priority_too_high_fails():
    with pytest.raises(ValidationError):
        TodoCreate(title="Test", priority=6)

def test_todo_create_past_due_date_succeeds():
    # Due dates can be in the past
    past_due = datetime.now() - timedelta(days=1)
    todo = TodoCreate(title="Past Due", due_date=past_due)
    assert todo.due_date == past_due

def test_todo_update_valid():
    todo_update = TodoUpdate(title="Updated Title", completed=True, priority=2)
    assert todo_update.title == "Updated Title"
    assert todo_update.completed is True
    assert todo_update.priority == 2

def test_todo_update_priority_too_low_fails():
    with pytest.raises(ValidationError):
        TodoUpdate(priority=0)

def test_todo_update_priority_too_high_fails():
    with pytest.raises(ValidationError):
        TodoUpdate(priority=6)

def test_todo_update_no_fields():
    todo_update = TodoUpdate()
    assert todo_update.title is None
    assert todo_update.description is None
    assert todo_update.completed is None
    assert todo_update.priority is None
    assert todo_update.due_date is None

