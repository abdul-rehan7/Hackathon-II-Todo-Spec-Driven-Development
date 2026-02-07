from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database.connection import create_db_and_tables, get_session
from backend.models.todo import Todo # Ensure all models are imported
import os

from backend.api.v1.endpoints import todos # New import
from backend.api import auth  # Import auth endpoints

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://hackathon-ii-todo-spec-driven-devel-pi.vercel.app", "http://localhost:3000", "http://localhost:8000"],  # Allow your Vercel domain and local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(todos.router, prefix="/api/v1") # New line to include router
app.include_router(auth.router, prefix="/api/v1")  # Include auth router

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}
