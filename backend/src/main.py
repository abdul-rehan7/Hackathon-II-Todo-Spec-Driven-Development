from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.src.database.connection import create_db_and_tables, get_session
from backend.src.models.todo import Todo # Ensure all models are imported
import os

from backend.src.api.v1.endpoints import todos # New import
from backend.src.api import auth  # Import auth endpoints

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
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
