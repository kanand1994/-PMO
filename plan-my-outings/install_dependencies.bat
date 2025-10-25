@echo off
title Plan My Outings - Dependency Installer
color 0D

echo ===============================================
echo    DEPENDENCY INSTALLATION
echo ===============================================
echo.

set BACKEND_DIR=backend
set FRONTEND_DIR=frontend

echo This will install all required dependencies for the project.
echo.

REM Check Python
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)
python --version

REM Check Node.js
echo Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js not found!
    echo Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)
node --version

echo.
echo Installing Backend Dependencies...
echo.

REM Setup backend virtual environment
cd %BACKEND_DIR%
echo Creating Python virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment!
    pause
    exit /b 1
)

echo Activating virtual environment and installing packages...
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install backend dependencies!
    pause
    exit /b 1
)
cd ..

echo.
echo Installing Frontend Dependencies...
echo.

REM Setup frontend dependencies
cd %FRONTEND_DIR%
npm install
if errorlevel 1 (
    echo ERROR: Failed to install frontend dependencies!
    pause
    exit /b 1
)
cd ..

echo.
echo ===============================================
echo DEPENDENCY INSTALLATION COMPLETE!
echo ===============================================
echo.
echo All dependencies have been installed successfully.
echo You can now run 'start_services.bat' to start the application.
echo.
pause