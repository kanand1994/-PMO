@echo off
title Plan My Outings - Database Management
color 0E

echo ===============================================
echo    DATABASE MANAGEMENT TOOLS
echo ===============================================
echo.

set BACKEND_DIR=plan-my-outings\backend\instance

:menu
cls
echo Database Management Options:
echo.
echo 1. Create/Update Database Tables
echo 2. Reset Database (WARNING: Deletes all data!)
echo 3. Backup Database
echo 4. View Database Info
echo 5. Direct SQLite Access (SQL Commands)
echo 6. Show Database Schema
echo 7. Quick SQL Queries
echo 8. Return to Main Menu
echo.
set /p choice="Select option (1-8): "

if "%choice%"=="1" goto create_db
if "%choice%"=="2" goto reset_db
if "%choice%"=="3" goto backup_db
if "%choice%"=="4" goto db_info
if "%choice%"=="5" goto sqlite_access
if "%choice%"=="6" goto show_schema
if "%choice%"=="7" goto quick_queries
if "%choice%"=="8" goto exit
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

:sqlite_access
echo ===============================================
echo    DIRECT SQLITE ACCESS
echo ===============================================
echo.
echo Opening SQLite command line interface...
echo Database: backend\instance\plan_my_outings.db
echo.
echo Useful SQLite commands:
echo   .tables                    - List all tables
echo   .schema table_name         - Show table structure
echo   .headers on                - Show column headers
echo   .mode column               - Format output in columns
echo   SELECT * FROM users;       - View all users
echo   .quit                      - Exit SQLite
echo.
echo Press any key to open SQLite CLI...
pause >nul
cd backend\instance
sqlite3 plan_my_outings.db
cd ..\..
echo.
echo SQLite session ended.
echo Press any key to continue...
pause >nul
goto menu

:show_schema
echo ===============================================
echo    DATABASE SCHEMA
echo ===============================================
echo.
if exist "backend\instance\plan_my_outings.db" (
    echo Showing database schema...
    echo.
    cd backend\instance
    sqlite3 plan_my_outings.db ".schema"
    cd ..\..
) else (
    echo Database file not found!
)
echo.
echo Press any key to continue...
pause >nul
goto menu

:quick_queries
echo ===============================================
echo    QUICK SQL QUERIES
echo ===============================================
echo.
if not exist "backend\instance\plan_my_outings.db" (
    echo Database file not found!
    goto menu
)

echo Select a quick query:
echo.
echo 1. List all tables
echo 2. Count all users
echo 3. Count all groups
echo 4. Count all events
echo 5. Show recent users (last 10)
echo 6. Show all users
echo 7. Show all groups
echo 8. Show all events
echo 9. Custom SQL query
echo 0. Back to main menu
echo.
set /p query_choice="Select query (0-9): "

cd backend\instance

if "%query_choice%"=="1" (
    echo.
    echo Tables in database:
    sqlite3 plan_my_outings.db ".tables"
)
if "%query_choice%"=="2" (
    echo.
    echo User count:
    sqlite3 plan_my_outings.db "SELECT COUNT(*) as total_users FROM user;"
)
if "%query_choice%"=="3" (
    echo.
    echo Group count:
    sqlite3 plan_my_outings.db "SELECT COUNT(*) as total_groups FROM 'group';"
)
if "%query_choice%"=="4" (
    echo.
    echo Event count:
    sqlite3 plan_my_outings.db "SELECT COUNT(*) as total_events FROM event;"
)
if "%query_choice%"=="5" (
    echo.
    echo Recent users:
    sqlite3 -header -column plan_my_outings.db "SELECT id, username, email, first_name, last_name, created_at FROM user ORDER BY created_at DESC LIMIT 10;"
)
if "%query_choice%"=="6" (
    echo.
    echo All users:
    sqlite3 -header -column plan_my_outings.db "SELECT id, username, email, first_name, last_name, year_of_birth, created_at FROM user ORDER BY created_at DESC;"
)
if "%query_choice%"=="7" (
    echo.
    echo All groups:
    sqlite3 -header -column plan_my_outings.db "SELECT id, name, description, created_by, created_at FROM 'group' ORDER BY created_at DESC;"
)
if "%query_choice%"=="8" (
    echo.
    echo All events:
    sqlite3 -header -column plan_my_outings.db "SELECT id, title, event_type, group_id, created_by, created_at FROM event ORDER BY created_at DESC;"
)
if "%query_choice%"=="9" (
    echo.
    echo Enter your SQL query (press Enter when done):
    set /p custom_query="SQL> "
    if not "%custom_query%"=="" (
        echo.
        echo Executing: %custom_query%
        sqlite3 -header -column plan_my_outings.db "%custom_query%"
    )
)

cd ..\..
echo.
echo Press any key to continue...
pause >nul
goto menu

:exit
echo Returning to main menu...