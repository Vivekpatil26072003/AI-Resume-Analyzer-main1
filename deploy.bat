@echo off
echo 🚀 AI Resume Analyzer - Deployment Script
echo ======================================

REM Check if git is initialized
if not exist ".git" (
    echo ❌ Git repository not initialized. Please run 'git init' first.
    pause
    exit /b 1
)

echo Select deployment option:
echo 1) Deploy Frontend (Netlify)
echo 2) Deploy Backend (Heroku)
echo 3) Deploy Both
echo 4) Exit

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto deploy_frontend
if "%choice%"=="2" goto deploy_backend
if "%choice%"=="3" goto deploy_both
if "%choice%"=="4" goto exit
echo ❌ Invalid choice. Please run the script again.
pause
exit /b 1

:deploy_frontend
echo 📦 Deploying Frontend to Netlify...
cd frontend
call npm install
call npm run build
if %errorlevel% equ 0 (
    echo ✅ Frontend build successful!
    echo 📋 Next steps for Netlify:
    echo 1. Go to https://netlify.com
    echo 2. Connect your GitHub repository
    echo 3. Build command: npm run build
    echo 4. Publish directory: out
    echo 5. Set environment variable: NEXT_PUBLIC_API_URL=https://your-backend-url.herokuapp.com
) else (
    echo ❌ Frontend build failed!
    pause
    exit /b 1
)
cd ..
goto end

:deploy_backend
echo 🔧 Deploying Backend to Heroku...
echo 📋 Backend deployment commands:
echo 1. heroku create your-app-name
echo 2. heroku config:set CORS_ORIGINS=https://your-frontend-url.netlify.app
echo 3. git subtree push --prefix backend heroku main
goto end

:deploy_both
call :deploy_frontend
echo.
call :deploy_backend
goto end

:exit
echo 👋 Goodbye!
exit /b 0

:end
echo.
echo 🎉 Deployment process completed!
echo 📖 Check DEPLOYMENT.md for detailed instructions.
pause
