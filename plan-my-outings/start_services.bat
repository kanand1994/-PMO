@echo off
title Plan My Outings - Service Manager
color 0A

echo ===============================================
echo    PLAN MY OUTINGS - SERVICE STARTUP MANAGER
echo ===============================================
echo.

set BACKEND_DIR=plan-my-outings\backend
set FRONTEND_DIR=plan-my-outings\frontend
set BACKEND_PORT=5000
set FRONTEND_PORT=3000

REM Check if directories exist
if not exist "%BACKEND_DIR%" (
    echo ERROR: Backend directory (%BACKEND_DIR%) not found!
    echo Please run this script from the project root directory.
    pause
    exit /b 1
)

if not exist "%FRONTEND_DIR%" (
    echo ERROR: Frontend directory (%FRONTEND_DIR%) not found!
    echo Please run this script from the project root directory.
    pause
    exit /b 1
)

REM Check for Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.7+ and try again.
    pause
    exit /b 1
)

REM Check for Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH!
    echo Please install Node.js and try again.
    pause
    exit /b 1
)

REM Check for npm
npm --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: npm is not installed or not in PATH!
    echo Please install Node.js (which includes npm) and try again.
    pause
    exit /b 1
)

echo Checking dependencies...
echo.

REM Check backend dependencies
if not exist "%BACKEND_DIR%\venv" (
    echo Creating Python virtual environment...
    cd %BACKEND_DIR%
    python -m venv venv
    cd ..
)

REM Check if backend requirements are installed
echo Installing/Checking backend dependencies...
call "%BACKEND_DIR%\venv\Scripts\activate.bat"
cd %BACKEND_DIR%
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Installing Python packages from requirements.txt...
    pip install -r requirements.txt
) else (
    echo Backend dependencies already installed.
)
cd ..

REM Check frontend dependencies
echo Installing/Checking frontend dependencies...
cd %FRONTEND_DIR%
if not exist "node_modules" (
    echo Installing Node.js packages...
    npm install
) else (
    echo Frontend dependencies already installed.
)
cd ..

echo.
echo ===============================================
echo Starting Services...
echo ===============================================
echo.

REM Function to check if port is available
:check_port
setlocal
set port=%1
netstat -an | findstr ":%port% " >nul
if %errorlevel% == 0 (
    echo WARNING: Port %port% is already in use!
    echo Please close any applications using port %port% and try again.
    endlocal
    exit /b 1
)
endlocal
exit /b 0

REM Check ports
call :check_port %BACKEND_PORT%
if errorlevel 1 (
    pause
    exit /b 1
)

call :check_port %FRONTEND_PORT%
if errorlevel 1 (
    pause
    exit /b 1
)

echo Starting Backend Server (Port %BACKEND_PORT%)...
start "Plan My Outings - Backend" cmd /k "cd /d %BACKEND_DIR% && call venv\Scripts\activate.bat && echo Starting Backend Server... && python app.py"

REM Wait for backend to start
echo Waiting for backend to initialize...
timeout /t 5 /nobreak >nul

echo Starting Frontend Server (Port %FRONTEND_PORT%)...
start "Plan My Outings - Frontend" cmd /k "cd /d %FRONTEND_DIR% && echo Starting Frontend Server... && npm start"

echo.
echo ===============================================
echo Services Started Successfully!
echo ===============================================
echo.
echo Backend:  http://localhost:%BACKEND_PORT%
echo Frontend: http://localhost:%FRONTEND_PORT%
echo.
echo Press any key to open the application...
pause >nul

REM Open the application in default browser
start http://localhost:%FRONTEND_PORT%

echo.
echo To stop all services, run 'stop_services.bat' or close the command windows.
echo.
pause