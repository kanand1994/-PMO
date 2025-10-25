@echo off
title Plan My Outings - Development Mode
color 0B

echo ===============================================
echo    PLAN MY OUTINGS - DEVELOPMENT MODE
echo ===============================================
echo.

set BACKEND_DIR=plan-my-outings\backend
set FRONTEND_DIR=plan-my-outings\frontend

echo Starting in Development Mode with auto-reload...
echo.

REM Start backend with debug mode
echo Starting Backend (Debug Mode)...
start "Backend Debug" cmd /k "cd /d %BACKEND_DIR% && call venv\Scripts\activate.bat && set FLASK_DEBUG=1 && python app.py"

REM Wait a bit for backend
timeout /t 3 /nobreak >nul

REM Start frontend
echo Starting Frontend (Development Mode)...
start "Frontend Dev" cmd /k "cd /d %FRONTEND_DIR% && npm start"

echo.
echo Development servers started!
echo - Backend: http://localhost:5000 (Auto-reload enabled)
echo - Frontend: http://localhost:3000 (Hot-reload enabled)
echo.
echo Press any key to open the application...
pause >nul

start http://localhost:3000

echo.
echo Development mode active. Files will auto-reload on changes.
echo.
pause