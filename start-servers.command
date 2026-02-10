#!/bin/bash

# Start Speech-to-Text App Servers
# Double-click this file to start both backend and frontend servers

cd "$(dirname "$0")"

echo "🚀 Starting Speech-to-Text servers..."
echo ""
echo "Backend server: http://localhost:8001"
echo "Frontend server: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Check if servers are already running
if lsof -ti:8001 > /dev/null 2>&1; then
    echo "⚠️  Backend server (port 8001) is already running"
else
    echo "Starting backend server..."
    uvicorn server:app --reload --port 8001 > /dev/null 2>&1 &
    BACKEND_PID=$!
    echo "Backend started (PID: $BACKEND_PID)"
fi

if lsof -ti:3000 > /dev/null 2>&1; then
    echo "⚠️  Frontend server (port 3000) is already running"
else
    echo "Starting frontend server..."
    python3 -m http.server 3000 > /dev/null 2>&1 &
    FRONTEND_PID=$!
    echo "Frontend started (PID: $FRONTEND_PID)"
fi

echo ""
echo "✅ Servers are running!"
echo ""
echo "Opening app in browser..."
sleep 2
open http://localhost:3000

echo ""
echo "To stop servers, close this window or press Ctrl+C"
echo "Or run: kill $BACKEND_PID $FRONTEND_PID"

# Wait for user to stop
wait

