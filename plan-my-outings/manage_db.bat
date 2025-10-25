@echo off
title Plan My Outings - Database Management
color 0E

echo ===============================================
echo    DATABASE MANAGEMENT TOOLS
echo ===============================================
echo.

set BACKEND_DIR=backend\instance

:menu
cls
echo Database Management Options:
echo.
echo 1. Create/Update Database Tables
echo 2. Reset Database (WARNING: Deletes all data!)
echo 3. Backup Database
echo 4. View Database Info
echo 5. Return to Main Menu
echo.
set /p choice="Select option (1-5): "

if "%choice%"=="1" goto create_db
if "%choice%"=="2" goto reset_db
if "%choice%"=="3" goto backup_db
if "%choice%"=="4" goto db_info
if "%choice%"=="5" goto exit
echo Invalid choice! Press any key to try again.
pause >nul
goto menu

:create_db
echo Creating/Updating database tables...
cd %BACKEND_DIR%
call venv\Scripts\activate.bat
python -c "from app import app, db; with app.app_context(): db.create_all(); print('Database tables created successfully!')"
cd ..
echo.
echo Press any key to continue...
pause >nul
goto menu

:reset_db
echo.
echo WARNING: This will delete ALL data in the database!
set /p confirm="Are you sure? (yes/no): "
if /i not "%confirm%"=="yes" (
    echo Operation cancelled.
    goto menu
)

echo Resetting database...
cd %BACKEND_DIR%
call venv\Scripts\activate.bat
python -c "import os; os.remove('plan_my_outings.db') if os.path.exists('plan_my_outings.db') else None; from app import app, db; with app.app_context(): db.create_all(); print('Database reset successfully!')"
cd ..
echo.
echo Press any key to continue...
pause >nul
goto menu

:backup_db
echo Creating database backup...
set timestamp=%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%
if exist "%BACKEND_DIR%\plan_my_outings.db" (
    copy "%BACKEND_DIR%\plan_my_outings.db" "%BACKEND_DIR%\backup_%timestamp%.db" >nul
    echo Backup created: %BACKEND_DIR%\backup_%timestamp%.db
) else (
    echo No database file found to backup.
)
echo.
echo Press any key to continue...
pause >nul
goto menu

:db_info
echo Database Information:
echo.
if exist "%BACKEND_DIR%\plan_my_outings.db" (
    echo - Database file: %BACKEND_DIR%\plan_my_outings.db
    for /f "tokens=1-3" %%a in ('dir "%BACKEND_DIR%\plan_my_outings.db" ^| find "plan_my_outings.db"') do (
        echo - Size: %%a %%b
    )
) else (
    echo - Database file: Not found
)
echo.
echo Press any key to continue...
pause >nul
goto menu

:exit
echo Returning to main menu...