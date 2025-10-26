@echo off
echo 🐙 GitHub Repository Setup
echo ==========================
echo.

echo This script will help you set up your GitHub repository for deployment.
echo.

echo 📋 Before running this script, make sure you have:
echo 1. Created a new repository on GitHub.com
echo 2. Copied the repository URL
echo.

set /p repo_url="Enter your GitHub repository URL (e.g., https://github.com/username/plan-my-outings.git): "

if "%repo_url%"=="" (
    echo ❌ Repository URL is required!
    pause
    exit /b 1
)

echo.
echo 🔄 Setting up Git repository...

if not exist .git (
    echo Initializing Git repository...
    git init
)

echo Adding all files...
git add .

echo Creating commit...
git commit -m "Initial commit - Plan My Outings application ready for deployment"

echo Adding remote origin...
git remote remove origin 2>nul
git remote add origin %repo_url%

echo Pushing to GitHub...
git branch -M main
git push -u origin main

echo.
echo ✅ Repository setup complete!
echo.
echo 🚀 Next steps:
echo 1. Go to Render.com and create a new Web Service
echo 2. Connect your GitHub repository: %repo_url%
echo 3. Follow the DEPLOYMENT.md guide
echo.
echo 📁 Your repository is now at: %repo_url%
echo.
pause