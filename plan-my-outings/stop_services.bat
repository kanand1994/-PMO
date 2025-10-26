@echo off
title Plan My Outings - Stop Services
color 0C

echo ===============================================
echo    STOPPING PLAN MY OUTINGS SERVICES
echo ===============================================
echo.

echo Stopping backend and frontend servers...

REM Kill processes by window title and close windows
taskkill /FI "WINDOWTITLE eq Plan My Outings - Backend*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Plan My Outings - Frontend*" /F >nul 2>&1

REM Close the command prompt windows by title
for /f "tokens=2" %%i in ('tasklist /FI "IMAGENAME eq cmd.exe" /FO TABLE /NH') do (
    for /f "tokens=*" %%j in ('wmic process where "ProcessId=%%i" get CommandLine /value 2^>nul ^| findstr "CommandLine"') do (
        echo %%j | findstr /C:"Plan My Outings - Backend" >nul && taskkill /PID %%i /F >nul 2>&1
        echo %%j | findstr /C:"Plan My Outings - Frontend" >nul && taskkill /PID %%i /F >nul 2>&1
    )
)

REM Also kill by port if needed
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000') do (
    taskkill /PID %%a /F >nul 2>&1
)

for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3000') do (
    taskkill /PID %%a /F >nul 2>&1
)

REM Force close any remaining windows with those titles
powershell -Command "Get-Process | Where-Object {$_.MainWindowTitle -like '*Plan My Outings - Backend*' -or $_.MainWindowTitle -like '*Plan My Outings - Frontend*'} | ForEach-Object {$_.CloseMainWindow(); Start-Sleep 1; if (!$_.HasExited) {$_.Kill()}}" >nul 2>&1

echo All services stopped successfully!
echo.
pause