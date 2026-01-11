from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
import logging

# Add the project root to the Python path to access the backend modules
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Import your backend modules - using absolute imports
from backend.src.database.connection import create_db_and_tables
from backend.src.api.v1.endpoints import todos
from backend.src.api import auth  # Import auth endpoints

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_db_and_tables()
    yield
    # Shutdown (if needed)

app = FastAPI(lifespan=lifespan)

# Add CORS middleware - adjust origins for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your todo router
app.include_router(todos.router, prefix="/api/v1")
# Include auth router
app.include_router(auth.router, prefix="/api/v1")  # Include auth router

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