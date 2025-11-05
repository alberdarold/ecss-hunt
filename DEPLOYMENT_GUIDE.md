# 🚀 Complete Deployment Guide - ECSS Hunt

This guide will walk you through deploying both the backend and frontend to production.

## 📋 Prerequisites

1. **GitHub Account** - For code repository
2. **Render Account** - For backend deployment (free tier available)
3. **Vercel Account** - For frontend deployment (free tier available)
4. **Git** - Installed on your computer

---

## 🎯 Step 1: Prepare Your Code

### 1.1 Commit All Changes

```bash
# Make sure all changes are committed
git status

# If there are uncommitted changes:
git add .
git commit -m "Prepare for deployment: Update CORS and API configuration"
```

### 1.2 Push to GitHub

```bash
# Push to your GitHub repository
git push origin main
# (or git push origin master if your default branch is master)
```

---

## 🔧 Step 2: Deploy Backend to Render

### 2.1 Create Render Account

1. Go to [https://render.com](https://render.com)
2. Sign up for a free account (use GitHub to sign in)
3. Verify your email address

### 2.2 Create New Web Service

1. Click **"New +"** button in the dashboard
2. Select **"Web Service"**
3. Connect your GitHub repository
4. Select the `ecss-hunt` repository

### 2.3 Configure Backend Service

**Service Settings:**
- **Name**: `ecss-hunt-backend`
- **Environment**: `Python 3`
- **Region**: Choose closest to your users (e.g., `Oregon (US West)`)
- **Branch**: `main` (or `master`)
- **Root Directory**: Leave empty (or `backend` if files are in subdirectory)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: 
  ```bash
  python main.py
  ```
  (Or use the one from `render.yaml` if it auto-detects)

**Alternative - Use render.yaml:**
- Render can auto-detect `render.yaml` in your repo
- If detected, it will use those settings automatically

### 2.4 Set Environment Variables

In the Render dashboard, go to **Environment** tab and add:

#### Required Variables:
```
MORPHIK_URI=morphik://ecss-hunt:YOUR_TOKEN@api.morphik.ai
OPENAI_API_KEY=sk-proj-YOUR_KEY
ONESUB_API_KEY=sk-tool-YOUR_KEY
ONESUB_TOOL_ID=YOUR_TOOL_ID
FLASK_SESSION_SECRET_KEY=YOUR_SECRET_KEY
```

#### Optional Variables:
```
ECSS_DOCUMENTS_PATH=./ECSS Published Standards/1-Active Standards/
MAX_DOCUMENTS=50
DEBUG=false
PORT=8000
COST_LIMIT_PER_DOC=2.0
```

**Note**: Render will set `PORT` automatically - don't override it unless needed.

### 2.5 Deploy

1. Click **"Create Web Service"**
2. Wait for deployment (5-10 minutes)
3. Render will provide a URL like: `https://ecss-hunt.onrender.com`

### 2.6 Verify Backend Deployment

Test the endpoints:
- Health: `https://ecss-hunt.onrender.com/api/health`
- Status: `https://ecss-hunt.onrender.com/api/status`

You should see JSON responses.

---

## 🎨 Step 3: Deploy Frontend to Vercel

### 3.1 Create Vercel Account

1. Go to [https://vercel.com](https://vercel.com)
2. Sign up for a free account (use GitHub to sign in)
3. Complete the onboarding

### 3.2 Import Project

1. Click **"Add New..." → "Project"**
2. Import your GitHub repository
3. Select the `ecss-hunt` repository

### 3.3 Configure Frontend Project

**Project Settings:**
- **Framework Preset**: Next.js (auto-detected)
- **Root Directory**: `frontend`
- **Build Command**: `npm run build` (auto-detected)
- **Output Directory**: `.next` (auto-detected)
- **Install Command**: `npm install` (auto-detected)

### 3.4 Set Environment Variables

In the **Environment Variables** section, add:

```
NEXT_PUBLIC_API_BASE_URL=https://ecss-hunt.onrender.com
NEXT_PUBLIC_API_VERSION=
NODE_ENV=production
```

**Important**: 
- Make sure to add these for **Production**, **Preview**, and **Development** environments
- Click "Add" after each variable

### 3.5 Deploy

1. Click **"Deploy"**
2. Wait for build to complete (2-5 minutes)
3. Vercel will provide a URL like: `https://ecss-hunt.vercel.app`

### 3.6 Verify Frontend Deployment

1. Visit your Vercel URL
2. Check browser console for errors
3. Test the application functionality

---

## 🔗 Step 4: Update CORS Configuration (If Needed)

### 4.1 Get Your Vercel URL

After deployment, note your Vercel frontend URL:
- Example: `https://ecss-hunt.vercel.app`
- Or: `https://ecss-hunt-xyz.vercel.app`

### 4.2 Update Backend CORS

If your Vercel URL is different from what's in the code:

1. **Update `backend/production/production_api_server.py`**:
   ```python
   allowed_origins = [
       "http://localhost:3000",
       "http://localhost:3001",
       "https://localhost:3000",
       "https://localhost:3001",
       "http://127.0.0.1:3000",
       "http://127.0.0.1:3001",
       "https://ecss-hunt.onrender.com",
       "https://ecss-hunt.vercel.app",  # Update this
       "https://ecss-hunt-frontend.vercel.app",  # Update this
       "https://YOUR-ACTUAL-VERCEL-URL.vercel.app",  # Add your actual URL
   ]
   ```

2. **Commit and push**:
   ```bash
   git add backend/production/production_api_server.py
   git commit -m "Update CORS with Vercel URL"
   git push
   ```

3. **Render will auto-redeploy** (or manually redeploy in Render dashboard)

---

## ✅ Step 5: Verify Everything Works

### 5.1 Test Backend

Open in browser:
```
https://ecss-hunt.onrender.com/api/health
```

Should return:
```json
{
  "status": "healthy",
  "timestamp": "...",
  ...
}
```

### 5.2 Test Frontend

1. Visit your Vercel URL
2. Open browser DevTools (F12) → Console tab
3. Check for errors
4. Test the application:
   - Try searching
   - Check authentication
   - Verify API connections

### 5.3 Check CORS

If you see CORS errors:
1. Verify your Vercel URL is in the backend's `allowed_origins` list
2. Redeploy backend after updating CORS
3. Clear browser cache and hard refresh (Ctrl+Shift+R)

---

## 🔧 Troubleshooting

### Backend Issues

**Problem: Build fails**
- Check Render logs for errors
- Verify `requirements.txt` is correct
- Check Python version compatibility

**Problem: Service crashes**
- Check environment variables are set correctly
- Verify `MORPHIK_URI` is valid
- Check Render logs for error messages

**Problem: CORS errors**
- Verify frontend URL is in `allowed_origins`
- Check Render logs for CORS-related errors
- Ensure `supports_credentials=True` in CORS config

### Frontend Issues

**Problem: Build fails**
- Check Vercel build logs
- Verify `package.json` dependencies
- Check for TypeScript errors

**Problem: API connection fails**
- Verify `NEXT_PUBLIC_API_BASE_URL` is set correctly
- Check backend is running and accessible
- Check browser console for errors

**Problem: 404 errors**
- Verify Next.js routing is correct
- Check `next.config.ts` configuration
- Ensure all pages are in correct directories

---

## 📊 Monitoring

### Render Dashboard
- View logs: Service → Logs
- Monitor metrics: Service → Metrics
- Check health: Service → Health

### Vercel Dashboard
- View deployments: Project → Deployments
- Check analytics: Project → Analytics
- View logs: Deployment → Functions Logs

---

## 🔄 Updating Deployments

### Backend Updates

1. Make changes locally
2. Commit and push to GitHub
3. Render auto-deploys (or manually trigger in dashboard)
4. Wait for deployment to complete

### Frontend Updates

1. Make changes locally
2. Commit and push to GitHub
3. Vercel auto-deploys
4. Wait for build to complete

---

## 📝 Environment Variables Checklist

### Backend (Render)
- [ ] `MORPHIK_URI`
- [ ] `OPENAI_API_KEY`
- [ ] `ONESUB_API_KEY`
- [ ] `ONESUB_TOOL_ID`
- [ ] `FLASK_SESSION_SECRET_KEY`
- [ ] `ECSS_DOCUMENTS_PATH` (optional)
- [ ] `MAX_DOCUMENTS` (optional)
- [ ] `DEBUG` (set to `false`)

### Frontend (Vercel)
- [ ] `NEXT_PUBLIC_API_BASE_URL` (your Render backend URL)
- [ ] `NEXT_PUBLIC_API_VERSION` (empty string)
- [ ] `NODE_ENV` (set to `production`)

---

## 🎉 Success!

Once deployed, your application will be:
- ✅ Accessible from anywhere
- ✅ Running on HTTPS
- ✅ No CORS issues
- ✅ Production-ready
- ✅ Auto-deploying on git push

**Frontend URL**: `https://ecss-hunt.vercel.app` (or your custom URL)
**Backend URL**: `https://ecss-hunt.onrender.com` (or your custom URL)

---

## 🆘 Need Help?

If you encounter issues:
1. Check the logs in Render/Vercel dashboards
2. Verify all environment variables are set
3. Test endpoints individually
4. Check browser console for errors
5. Verify CORS configuration matches your URLs

