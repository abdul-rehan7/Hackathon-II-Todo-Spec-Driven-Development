# Todo Backend API

A FastAPI backend for the Todo application deployed on Hugging Face Spaces.

## Endpoints

- `GET /api/v1/todos/` - Get all todos
- `POST /api/v1/todos/` - Create a new todo
- `GET /api/v1/todos/{todo_id}` - Get a specific todo
- `PUT /api/v1/todos/{todo_id}` - Update a specific todo
- `DELETE /api/v1/todos/{todo_id}` - Delete a specific todo

## Health Check

- `GET /health` - Check API health status

## Tech Stack

- FastAPI
- SQLModel
- SQLite (for Hugging Face Spaces)
- Uvicorn ASGI server

## Environment Variables

- `PORT` (optional, defaults to 7860)
- `DATABASE_URL` (optional, defaults to SQLite)

## Development

To run locally:
```
uvicorn app:app --reload --port 8000
```

## About Hugging Face Spaces

This backend is deployed on Hugging Face Spaces, providing a free hosting solution for machine learning and web applications.