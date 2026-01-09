from sqlmodel import create_engine, Session, SQLModel
from backend.src.models.todo import Todo # Ensure all models are imported
import os

# Dynamic database URL from environment variable
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./database.db")

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
