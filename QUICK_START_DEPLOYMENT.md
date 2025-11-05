# 🚀 Quick Start - Deploy to Production

Follow these steps to deploy your application online and avoid local CORS issues.

## ⚡ Quick Steps (5 minutes)

### 1. Prepare Code (2 minutes)

```bash
# Add all changes
git add .

# Commit with deployment message
git commit -m "Prepare for deployment: Update CORS, API config, and add deployment guides"

# Push to GitHub
git push origin main
```

### 2. Deploy Backend to Render (3 minutes)

1. **Go to**: https://render.com
2. **Sign up** (or log in) with GitHub
3. **Click**: "New +" → "Web Service"
4. **Connect** your GitHub repository
5. **Select**: `ecss-hunt` repository
6. **Configure**:
   - Name: `ecss-hunt-backend`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`
7. **Add Environment Variables** (in Render dashboard):
   ```
   MORPHIK_URI=your_morphik_uri
   OPENAI_API_KEY=your_openai_key
   ONESUB_API_KEY=your_onesub_key
   ONESUB_TOOL_ID=your_onesub_tool_id
   FLASK_SESSION_SECRET_KEY=your_secret_key
   DEBUG=false
   ```
8. **Click**: "Create Web Service"
9. **Wait**: 5-10 minutes for deployment
10. **Note**: Your backend URL (e.g., `https://ecss-hunt.onrender.com`)

### 3. Deploy Frontend to Vercel (2 minutes)

1. **Go to**: https://vercel.com
2. **Sign up** (or log in) with GitHub
3. **Click**: "Add New..." → "Project"
4. **Import** your GitHub repository
5. **Configure**:
   - Root Directory: `frontend`
   - Framework: Next.js (auto-detected)
6. **Add Environment Variables**:
   ```
   NEXT_PUBLIC_API_BASE_URL=https://ecss-hunt.onrender.com
   NEXT_PUBLIC_API_VERSION=
   NODE_ENV=production
   ```
   (Replace `ecss-hunt.onrender.com` with your actual Render URL)
7. **Click**: "Deploy"
8. **Wait**: 2-5 minutes for deployment
9. **Note**: Your frontend URL (e.g., `https://ecss-hunt.vercel.app`)

### 4. Update CORS (if needed)

If your Vercel URL is different from `ecss-hunt.vercel.app`:

1. **Edit**: `backend/production/production_api_server.py`
2. **Find**: `allowed_origins` list (around line 127)
3. **Add**: Your actual Vercel URL
4. **Commit and push**:
   ```bash
   git add backend/production/production_api_server.py
   git commit -m "Update CORS with Vercel URL"
   git push
   ```
5. **Wait**: Render will auto-redeploy

### 5. Test (1 minute)

1. **Visit**: Your Vercel frontend URL
2. **Open**: Browser DevTools (F12)
3. **Check**: Console tab for errors
4. **Test**: Try searching or using the app

---

## ✅ Success Checklist

- [ ] Backend deployed to Render
- [ ] Frontend deployed to Vercel
- [ ] Backend URL accessible
- [ ] Frontend URL accessible
- [ ] No CORS errors in browser console
- [ ] Application works correctly

---

## 🔍 Troubleshooting

### CORS Errors Still Appear?

1. **Verify** your Vercel URL is in backend's `allowed_origins`
2. **Redeploy** backend after updating CORS
3. **Clear** browser cache (Ctrl+Shift+R)
4. **Check** Render logs for CORS-related errors

### Backend Not Starting?

1. **Check** Render logs for errors
2. **Verify** all environment variables are set
3. **Check** `MORPHIK_URI` is valid
4. **Verify** `requirements.txt` is correct

### Frontend Build Fails?

1. **Check** Vercel build logs
2. **Verify** environment variables are set
3. **Check** `package.json` dependencies
4. **Verify** TypeScript compilation

---

## 📚 Full Documentation

For detailed instructions, see:
- **DEPLOYMENT_GUIDE.md** - Complete step-by-step guide
- **DEPLOYMENT_CHECKLIST.md** - Detailed checklist

---

## 🎉 You're Done!

Your application is now:
- ✅ Live on the internet
- ✅ No CORS issues
- ✅ Accessible from anywhere
- ✅ Production-ready

**Frontend**: https://ecss-hunt.vercel.app  
**Backend**: https://ecss-hunt.onrender.com

*(Replace with your actual URLs)*

