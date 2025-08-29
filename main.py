"""
Root-level main.py that imports the actual app from backend
This is a workaround for Render deployment
"""
import sys
import os

# Add backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Now import main from the backend directory (which is now in the path)
import main

# Export the app
app = main.app

__all__ = ['app']