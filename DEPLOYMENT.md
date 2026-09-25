# AI Resume Analyzer - Deployment Guide

## 🚀 Quick Deployment Solutions

### Option 1: Netlify (Recommended for Frontend)

1. **Connect your GitHub repository to Netlify:**
   - Go to [netlify.com](https://netlify.com)
   - Click "New site from Git"
   - Connect your GitHub account
   - Select the `AI-Resume-Analyzer` repository

2. **Configure build settings:**
   - Build command: `cd frontend && npm install && npm run build`
   - Publish directory: `frontend/out`
   - The `netlify.toml` file is already configured

3. **Set environment variables:**
   - In Netlify dashboard, go to Site settings > Environment variables
   - Add `NEXT_PUBLIC_API_URL` with the real public HTTPS URL of the deployed Flask backend.
   - This variable is required during the Netlify build; do not use `localhost` or a placeholder URL.

### Option 2: Vercel (Alternative)

1. **Connect to Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - The `vercel.json` file is already configured

2. **Set environment variables:**
   - Add `NEXT_PUBLIC_API_URL` in Vercel dashboard

## 🔧 Backend Deployment

### Render Deployment (Recommended)

Create a Render **Web Service** connected to the repository with these settings:

- Root Directory: leave blank (repository root)
- Build Command: `pip install -r backend/requirements.txt`
- Start Command: `cd backend && gunicorn app.main:app --bind 0.0.0.0:$PORT`
- Python version: `3.11.6` from `runtime.txt`
- Health Check Path: `/health`

Set these Render environment variables:

```env
FLASK_ENV=production
FLASK_DEBUG=False
HOST=0.0.0.0
RELOAD=False
CORS_ORIGINS=https://resume-ai-an.netlify.app,https://ai-resume-analyzer-main001.netlify.app
MAX_FILE_SIZE=10485760
ALLOWED_FILE_TYPES=.pdf,.docx
```

Render supplies `PORT` automatically. After deployment, verify `https://YOUR-BACKEND-URL/health` returns HTTP 200. Then set the Netlify build environment variable `NEXT_PUBLIC_API_URL` to `https://YOUR-BACKEND-URL` and redeploy the frontend.

### Heroku Deployment

1. **Prepare backend for Heroku:**
   ```bash
   cd backend
   pip freeze > requirements.txt
   ```

2. **Create Heroku app:**
   ```bash
   heroku create your-app-name
   ```

3. **Deploy:**
   ```bash
   git subtree push --prefix backend heroku main
   ```

### Alternative Backend Hosting
- **Railway**: Easy Python deployment
- **Render**: Free tier available
- **PythonAnywhere**: Simple Flask hosting

## 🐛 Fixing 404 Errors

The 404 errors were caused by:
1. Missing static export configuration
2. No deployment redirects for SPA routing
3. Incorrect build settings

**Fixed with:**
- ✅ `next.config.js` with `output: 'export'`
- ✅ `netlify.toml` with proper redirects
- ✅ `vercel.json` for Vercel deployment
- ✅ Updated build scripts

## 📝 Environment Variables

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=https://YOUR-PUBLIC-BACKEND-URL
NEXT_PUBLIC_APP_NAME=AI Resume Analyzer
NEXT_PUBLIC_APP_VERSION=1.0.0
```

### Backend (.env)
```env
FLASK_ENV=production
FLASK_DEBUG=False
CORS_ORIGINS=https://resume-ai-an.netlify.app
```

`NEXT_PUBLIC_API_URL` is read while Next.js builds the static frontend. After changing it in Netlify, trigger a new deploy.

## 🔄 Update Process

1. **Make changes to your code**
2. **Commit and push to GitHub:**
   ```bash
   git add .
   git commit -m "Fix deployment configuration"
   git push origin main
   ```
3. **Netlify/Vercel will auto-deploy**

## 🎯 Testing Deployment

1. **Build locally:**
   ```bash
   cd frontend
   npm run build
   ```
2. **Test the out folder:**
   ```bash
   npx serve out
   ```
3. **Verify all routes work**

## 🆘 Troubleshooting

### Common Issues:
- **404 on refresh**: Fixed with redirects in netlify.toml
- **API not connecting**: Check environment variables
- **Build fails**: Ensure all dependencies are in package.json

### Support:
- Check the console for errors
- Verify environment variables are set
- Ensure backend is deployed and accessible
