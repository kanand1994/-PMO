@echo off
echo 🏗️ Building Plan My Outings for Unified Deployment
echo ================================================
echo.

echo 📋 Step 1: Installing frontend dependencies...
cd frontend
call npm install
if %errorlevel% neq 0 (
    echo ❌ Frontend dependency installation failed!
    pause
    exit /b 1
)

echo.
echo 📋 Step 2: Building React frontend...
call npm run build
if %errorlevel% neq 0 (
    echo ❌ Frontend build failed!
    pause
    exit /b 1
)

echo.
echo 📋 Step 3: Preparing backend...
cd ..\backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Backend dependency installation failed!
    pause
    exit /b 1
)

cd ..

echo.
echo ✅ Build Complete!
echo.
echo 📁 Your application is ready for unified deployment:
echo    - Frontend built in: frontend/build/
echo    - Backend will serve frontend automatically
echo    - Single deployment URL will serve both
echo.
echo 🚀 Next: Deploy to Render with root directory as 'backend'
echo    The Flask app will serve both API and frontend!
echo.
pause