# ✅ Deployment Checklist

Use this checklist to ensure you complete all deployment steps.

## 📦 Pre-Deployment

- [ ] All code changes committed
- [ ] Code pushed to GitHub
- [ ] `render.yaml` is present and correct
- [ ] `frontend/.env` is configured for production
- [ ] Backend CORS includes Vercel URLs

## 🔧 Backend Deployment (Render)

- [ ] Created Render account
- [ ] Created new Web Service
- [ ] Connected GitHub repository
- [ ] Set environment variables:
  - [ ] `MORPHIK_URI`
  - [ ] `OPENAI_API_KEY`
  - [ ] `ONESUB_API_KEY`
  - [ ] `ONESUB_TOOL_ID`
  - [ ] `FLASK_SESSION_SECRET_KEY`
- [ ] Deployment started
- [ ] Backend URL noted: `https://__________.onrender.com`
- [ ] Health endpoint tested: `/api/health`
- [ ] Status endpoint tested: `/api/status`

## 🎨 Frontend Deployment (Vercel)

- [ ] Created Vercel account
- [ ] Imported GitHub repository
- [ ] Set root directory to `frontend`
- [ ] Set environment variables:
  - [ ] `NEXT_PUBLIC_API_BASE_URL` (your Render backend URL)
  - [ ] `NEXT_PUBLIC_API_VERSION` (empty string)
  - [ ] `NODE_ENV` (production)
- [ ] Deployment started
- [ ] Frontend URL noted: `https://__________.vercel.app`
- [ ] Frontend loads without errors
- [ ] Browser console shows no errors

## 🔗 Post-Deployment

- [ ] Updated backend CORS with Vercel URL
- [ ] Redeployed backend (if CORS updated)
- [ ] Tested frontend → backend connection
- [ ] Tested authentication flow
- [ ] Tested search functionality
- [ ] Verified no CORS errors
- [ ] Tested on mobile device (optional)

## ✅ Verification

- [ ] Backend health check works
- [ ] Frontend loads correctly
- [ ] API calls succeed
- [ ] No CORS errors in console
- [ ] Authentication works
- [ ] Search functionality works

---

## 🚀 Quick Commands

### Commit and Push
```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### Test Backend
```bash
curl https://YOUR-BACKEND-URL.onrender.com/api/health
```

### Check Frontend
Visit: `https://YOUR-FRONTEND-URL.vercel.app`

---

**Status**: ⬜ Not Started | 🟡 In Progress | ✅ Complete

