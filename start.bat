@echo off
echo 🚀 Starting AI Resume Analyzer...
echo.

echo 📋 Prerequisites:
echo - Python 3.8+ installed
echo - Node.js 16+ installed
echo - Both backend and frontend dependencies installed
echo.

echo 🔧 Starting Backend Server...
start "Backend Server" cmd /k "cd backend && python start.py"

echo ⏳ Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo 🌐 Starting Frontend Server...
start "Frontend Server" cmd /k "cd frontend && npm run dev"

echo.
echo 🎉 Both servers are starting!
echo 📖 Backend: http://localhost:8000
echo 🌐 Frontend: http://localhost:3000
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo Press any key to exit this window...
pause > nul




