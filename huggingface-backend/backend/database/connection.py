from sqlmodel import create_engine, Session, SQLModel
from backend.src.models.todo import Todo # Ensure all models are imported
import os

# Dynamic database URL from environment variable
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./database.db")

# Create the engine with additional parameters to handle locking issues
# Use different parameters depending on the database type
if DATABASE_URL.startswith("sqlite"):
    # For SQLite, use check_same_thread=False
    engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
else:
    # For PostgreSQL and other databases, don't use check_same_thread
    engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    try:
        SQLModel.metadata.create_all(engine)
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating database tables: {e}")

def get_session():
    with Session(engine) as session:
        yield session
