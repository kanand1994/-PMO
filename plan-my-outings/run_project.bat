@echo off
title Plan My Outings - Master Control
color 0F

:main_menu
cls
echo ===============================================
echo    PLAN MY OUTINGS - MASTER CONTROL PANEL
echo ===============================================
echo.
echo 1. Start All Services (Production)
echo 2. Start Development Mode (Auto-reload)
echo 3. Install Dependencies
echo 4. Database Management
echo 5. Stop All Services
echo 6. Exit
echo.
set /p choice="Select option (1-6): "

if "%choice%"=="1" goto start_services
if "%choice%"=="2" goto dev_mode
if "%choice%"=="3" goto install_deps
if "%choice%"=="4" goto db_manage
if "%choice%"=="5" goto stop_services
if "%choice%"=="6" goto exit
echo Invalid choice! Press any key to try again.
pause >nul
goto main_menu

:start_services
call start_services.bat
goto main_menu

:dev_mode
call dev_mode.bat
goto main_menu

:install_deps
call install_dependencies.bat
goto main_menu

:db_manage
call manage_db.bat
goto main_menu

:stop_services
call stop_services.bat
goto main_menu

:exit
echo Thank you for using Plan My Outings!
timeout /t 2 /nobreak >nul
exit