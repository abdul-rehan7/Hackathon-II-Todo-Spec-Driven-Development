from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
import logging

# Add the project root to the Python path to access the backend modules
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Import your backend modules - using relative imports for Hugging Face
from backend.database.connection import create_db_and_tables
from backend.api.v1.endpoints import todos
from backend.api import auth  # Import auth endpoints
from backend.api.v1.chat import router as chat_router  # Import chat endpoints

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_db_and_tables()
    yield
    # Shutdown (if needed)

app = FastAPI(lifespan=lifespan)

# Add CORS middleware - configured for your Vercel domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://hackathon-ii-todo-spec-driven-devel-pi.vercel.app", "http://localhost:3000", "http://localhost:8000"],  # Allow your Vercel domain and local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your todo router
app.include_router(todos.router, prefix="/api/v1")
# Include auth router
app.include_router(auth.router, prefix="/api/v1")  # Include auth router
# Include chat router
app.include_router(chat_router, prefix="/api/v1")  # Include chat router

@app.get("/")
def read_root():
    return {"message": "Todo API is running on Hugging Face Spaces!"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is operational"}

# For Hugging Face Spaces compatibility
def start_server():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 7860)))

if __name__ == "__main__":
    start_server()