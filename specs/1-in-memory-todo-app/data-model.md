# Data Model: Todo Application

## Entity: Todo

This document defines the data schema for a `Todo` task.

### Schema

- **`id`**: `int`
  - A unique identifier for the task.
  - Will be auto-incremented.
- **`title`**: `str`
  - The description of the task.
  - Cannot be empty.
- **`is_completed`**: `bool`
  - The status of the task.
  - Defaults to `False`.
- **`created_at`**: `datetime`
  - The timestamp when the task was created.
  - Automatically set on creation.

### Implementation

This schema will be implemented as a Python `dataclass` or a `Pydantic` model in `src/todo/models.py`.
