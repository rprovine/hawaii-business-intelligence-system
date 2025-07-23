#!/bin/bash
# Hawaii Business Intelligence System - Local Startup Script

echo "Starting Hawaii Business Intelligence System..."

# Start backend API
echo "Starting backend API..."
cd backend && python main.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Start frontend
echo "Starting frontend dashboard..."
cd ../frontend && npm start &
FRONTEND_PID=$!

echo ""
echo "✓ System started!"
echo "  - API running at: http://localhost:8000"
echo "  - Dashboard at: http://localhost:3002"
echo ""
echo "To start data collection, run in a new terminal:"
echo "  cd data-collectors && python scheduler.py"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for interrupt
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait