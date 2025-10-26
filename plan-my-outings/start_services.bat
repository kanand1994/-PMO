@echo off
title Plan My Outings - Service Manager
color 0A

echo ===============================================
echo    PLAN MY OUTINGS - SERVICE STARTUP MANAGER
echo ===============================================
echo.

REM Check if directories exist
if not exist "backend" (
    echo ERROR: Backend directory not found!
    pause
    exit /b 1
)

if not exist "frontend" (
    echo ERROR: Frontend directory not found!
    pause
    exit /b 1
)

echo Starting Backend Server...
cd backend
start "Plan My Outings - Backend" cmd /k "call venv\Scripts\activate.bat & python app.py"
cd ..

echo Waiting for backend to initialize...
timeout /t 3 /nobreak >nul

echo Starting Frontend Server...
cd frontend
start "Plan My Outings - Frontend" cmd /k "npm start"
cd ..

echo.
echo ===============================================
echo Services Started Successfully!
echo ===============================================
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo To stop all services, run 'stop_services.bat'
echo.
pause