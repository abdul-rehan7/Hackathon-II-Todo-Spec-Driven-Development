#!/usr/bin/env python
"""
Entrypoint for Hugging Face Spaces
"""
import os
import sys

# Add the project root to Python path
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_dir)

# Import and run the main app
from app import start_server

if __name__ == "__main__":
    start_server()