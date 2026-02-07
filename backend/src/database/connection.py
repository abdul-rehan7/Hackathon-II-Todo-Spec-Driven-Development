from sqlmodel import create_engine, Session, SQLModel
from backend.src.models.todo import Todo # Ensure all models are imported
import os

# Dynamic database URL from environment variable
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./database.db")

# Create the engine with additional parameters to handle locking issues
engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

def create_db_and_tables():
    try:
        SQLModel.metadata.create_all(engine)
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating database tables: {e}")

def get_session():
    with Session(engine) as session:
        yield session
