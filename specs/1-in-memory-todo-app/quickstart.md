# Quickstart: In-Memory Todo CLI

This guide explains how to run the In-Memory Todo CLI application.

## Prerequisites

- Python 3.13+
- `uv` installed

## Running the Application

1.  **Initialize the project and install dependencies:**
    ```bash
    uv pip install -r requirements.txt
    ```

2.  **Run the CLI:**
    ```bash
    python src/todo/main.py
    ```

3.  **Available Commands:**
    - `add <task title>`: Add a new task.
    - `view`: View all tasks.
    - `done <task id>`: Mark a task as complete.
    - `edit <task id> <new title>`: Update a task's title.
    - `del <task id>`: Delete a task.
    - `exit`: Exit the application.
