#!/bin/bash

echo "🚀 Starting AI Resume Analyzer..."
echo

echo "📋 Prerequisites:"
echo "- Python 3.8+ installed"
echo "- Node.js 16+ installed"
echo "- Both backend and frontend dependencies installed"
echo

# Function to cleanup background processes on exit
cleanup() {
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

echo "🔧 Starting Backend Server..."
cd backend
python start.py &
BACKEND_PID=$!
cd ..

echo "⏳ Waiting for backend to start..."
sleep 5

echo "🌐 Starting Frontend Server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo
echo "🎉 Both servers are starting!"
echo "📖 Backend: http://localhost:8000"
echo "🌐 Frontend: http://localhost:3000"
echo "📚 API Docs: http://localhost:8000/docs"
echo
echo "Press Ctrl+C to stop both servers..."

# Wait for both processes
wait

