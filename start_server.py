#!/usr/bin/env python
"""
Server startup script with debugging
"""
import sys
import os

print("=== Starting Hawaii BI System ===", flush=True)
print(f"Python: {sys.version}", flush=True)
print(f"Working directory: {os.getcwd()}", flush=True)
print(f"Files in directory: {os.listdir('.')}", flush=True)
print(f"PORT environment: {os.getenv('PORT', 'not set')}", flush=True)

try:
    print("Importing FastAPI...", flush=True)
    from fastapi import FastAPI
    print("✓ FastAPI imported", flush=True)
    
    print("Importing uvicorn...", flush=True)
    import uvicorn
    print("✓ Uvicorn imported", flush=True)
    
    print("Importing app...", flush=True)
    from app import app
    print("✓ App imported", flush=True)
    
    port = int(os.getenv("PORT", 8080))
    print(f"Starting server on port {port}...", flush=True)
    
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
    
except Exception as e:
    print(f"ERROR: {e}", flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)