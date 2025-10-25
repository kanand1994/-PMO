@echo off
title Plan My Outings - Stop Services
color 0C

echo ===============================================
echo    STOPPING PLAN MY OUTINGS SERVICES
echo ===============================================
echo.

echo Stopping backend and frontend servers...

REM Kill processes by window title
taskkill /FI "WINDOWTITLE eq Plan My Outings - Backend*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Plan My Outings - Frontend*" /F >nul 2>&1

REM Also kill by port if needed
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000') do (
    taskkill /PID %%a /F >nul 2>&1
)

for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3000') do (
    taskkill /PID %%a /F >nul 2>&1
)

echo All services stopped successfully!
echo.
pause