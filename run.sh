#!/bin/bash
# Root-level startup script for Render deployment

echo "Starting Hawaii Business Intelligence System API..."

# Change to backend directory
cd backend

# Set Python path
export PYTHONPATH=$(pwd):${PYTHONPATH}

echo "Current directory: $(pwd)"
echo "Python path: $PYTHONPATH"

# Start the FastAPI application
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}