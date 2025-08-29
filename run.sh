#!/bin/bash
# Root-level startup script for Render deployment

echo "Starting Hawaii Business Intelligence System API..."
echo "Initial directory: $(pwd)"
echo "Directory contents:"
ls -la

# Change to backend directory
cd backend || exit 1

echo "After cd backend:"
echo "Current directory: $(pwd)"
echo "Backend contents:"
ls -la

# Set Python path
export PYTHONPATH=$(pwd):${PYTHONPATH}
echo "Python path: $PYTHONPATH"

# Start the FastAPI application
exec python -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}