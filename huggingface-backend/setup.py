from setuptools import setup, find_packages

setup(
    name="todo-backend",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0",
        "sqlmodel==0.0.16",
        "python-multipart==0.0.6",
    ],
    author="Todo App Developer",
    author_email="todo@example.com",
    description="A FastAPI backend for the Todo application",
    python_requires=">=3.7",
)