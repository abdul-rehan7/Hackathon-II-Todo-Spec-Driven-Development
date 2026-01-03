from .models import Todo
from typing import List, Optional

class TodoManager:
    """Manages to-do items in memory."""

    def __init__(self):
        self._tasks: List[Todo] = []
        self._next_id = 1

    def add_task(self, title: str) -> Todo:
        new_task = Todo(id=self._next_id, title=title)
        self._tasks.append(new_task)
        self._next_id += 1
        return new_task

    def list_tasks(self) -> List[Todo]:
        return self._tasks

    def mark_complete(self, task_id: int) -> Optional[Todo]:
        for task in self._tasks:
            if task.id == task_id:
                task.is_completed = True
                return task
        return None

    def delete_task(self, task_id: int) -> bool:
        task_to_delete = None
        for task in self._tasks:
            if task.id == task_id:
                task_to_delete = task
                break
        if task_to_delete:
            self._tasks.remove(task_to_delete)
            return True
        return False
