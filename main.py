"""
Root-level main.py that imports the actual app from backend
This is a workaround for Render deployment
"""
import sys
import os

# Add backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Import the actual app
from backend.main import app

# Export app for uvicorn
__all__ = ['app']