#!/bin/bash

# AI Resume Analyzer - Deployment Script
# This script helps deploy both frontend and backend

echo "🚀 AI Resume Analyzer Deployment Script"
echo "======================================"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not initialized. Please run 'git init' first."
    exit 1
fi

# Function to deploy frontend to Netlify
deploy_frontend() {
    echo "📦 Deploying Frontend to Netlify..."
    
    # Build frontend
    cd frontend
    npm install
    npm run build
    
    if [ $? -eq 0 ]; then
        echo "✅ Frontend build successful!"
        echo "📋 Next steps for Netlify:"
        echo "1. Go to https://netlify.com"
        echo "2. Connect your GitHub repository"
        echo "3. Build command: npm run build"
        echo "4. Publish directory: out"
        echo "5. Set environment variable: NEXT_PUBLIC_API_URL=https://your-backend-url.herokuapp.com"
    else
        echo "❌ Frontend build failed!"
        exit 1
    fi
    
    cd ..
}

# Function to deploy backend to Heroku
deploy_backend() {
    echo "🔧 Deploying Backend to Heroku..."
    
    # Check if Heroku CLI is installed
    if ! command -v heroku &> /dev/null; then
        echo "❌ Heroku CLI not found. Please install it first:"
        echo "https://devcenter.heroku.com/articles/heroku-cli"
        exit 1
    fi
    
    # Check if user is logged in to Heroku
    if ! heroku auth:whoami &> /dev/null; then
        echo "❌ Not logged in to Heroku. Please run 'heroku login' first."
        exit 1
    fi
    
    echo "📋 Backend deployment commands:"
    echo "1. heroku create your-app-name"
    echo "2. heroku config:set CORS_ORIGINS=https://your-frontend-url.netlify.app"
    echo "3. git subtree push --prefix backend heroku main"
}

# Main menu
echo "Select deployment option:"
echo "1) Deploy Frontend (Netlify)"
echo "2) Deploy Backend (Heroku)"
echo "3) Deploy Both"
echo "4) Exit"

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        deploy_frontend
        ;;
    2)
        deploy_backend
        ;;
    3)
        deploy_frontend
        echo ""
        deploy_backend
        ;;
    4)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "🎉 Deployment process completed!"
echo "📖 Check DEPLOYMENT.md for detailed instructions."
