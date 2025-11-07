# 🧪 1sub.io Integration Testing Guide

This guide will help you test the 1sub.io payment integration in your ECSS Hunt application.

## 📋 Prerequisites

1. **1sub.io Account**: You need an account at https://1sub.io
2. **Tool Created**: Your tool should be created in 1sub.io dashboard
3. **API Key**: You need your 1sub API key
4. **Tool ID**: You need your tool ID from 1sub.io

## ✅ Step 1: Verify Environment Variables

### Local Environment

Check your `backend/config/.env` file has:
```env
ONESUB_API_KEY=sk-tool-your-api-key
ONESUB_TOOL_ID=your-tool-id
FLASK_SESSION_SECRET_KEY=your-secret-key
```

### Render (Deployed) Environment

1. Go to: https://dashboard.render.com
2. Click: Your service (`ecss-hunt-backend`)
3. Go to: **Environment** tab
4. Verify these variables are set:
   - `ONESUB_API_KEY`
   - `ONESUB_TOOL_ID`
   - `FLASK_SESSION_SECRET_KEY`

## 🧪 Step 2: Test Local Configuration

Run the test script:
```bash
python test_1sub_integration.py
```

This will check:
- ✅ Environment variables are set
- ✅ OneSubClient can be initialized
- ✅ 1sub.io API is reachable
- ✅ Backend integration works

## 🔍 Step 3: Test Backend Endpoints

### Test 1: Health Check (Should show 1sub status)

```bash
# Local
curl http://localhost:8000/api/health

# Deployed
curl https://ecss-hunt.onrender.com/api/health
```

Look for:
- `status: "healthy"`
- No errors about 1sub client

### Test 2: Tool ID Endpoint

```bash
# Local
curl http://localhost:8000/api/config/tool-id

# Deployed
curl https://ecss-hunt.onrender.com/api/config/tool-id
```

Expected response:
```json
{
  "tool_id": "0a080b57-d0f8-430a-835f-a1c86314c3cc"
}
```

### Test 3: Session Endpoint (Should work without auth)

```bash
# Local
curl http://localhost:8000/api/auth/session

# Deployed
curl https://ecss-hunt.onrender.com/api/auth/session
```

Expected response (if not authenticated):
```json
{
  "authenticated": false,
  "message": "No active session"
}
```

## 🎯 Step 4: Test Full Authentication Flow

### Option A: Test with Real 1sub.io Token

1. **Set up 1sub.io Tool**:
   - Go to https://1sub.io/dashboard
   - Create or verify your tool
   - Note your Tool ID
   - Configure redirect URL: `https://ecss-hunt.vercel.app/demo?token={token}`

2. **Get a Test Token**:
   - In 1sub.io dashboard, you can generate test tokens
   - Or use the checkout flow to get a real token

3. **Test Token Verification**:
   ```bash
   curl -X POST https://ecss-hunt.onrender.com/api/auth/verify \
     -H "Content-Type: application/json" \
     -d '{"token": "YOUR_TEST_TOKEN_HERE"}'
   ```

4. **Expected Response** (if token is valid):
   ```json
   {
     "success": true,
     "user_id": "user-uuid",
     "tool_id": "tool-uuid",
     "expires_at": "2025-12-31T23:59:59Z"
   }
   ```

### Option B: Test from Frontend

1. **Visit your frontend**: `https://ecss-hunt.vercel.app/demo`
2. **Click "Purchase Access"** button
3. **This should redirect to 1sub.io**:
   - If not authenticated with 1sub: Login page
   - If authenticated: Checkout page
4. **Complete purchase** (test mode if available)
5. **You'll be redirected back** with `?token=...` in URL
6. **Frontend should automatically verify** the token
7. **Check if authenticated**: Should show "Connected" and "AI Search: Enabled"

## 🔧 Step 5: Test Credit Consumption

### Check Backend Logs

When a user performs a search:
1. Backend should log: `"Credits consumed: 0.01 for user ..."`
2. Check Render logs for these messages

### Test Search with Authentication

1. **Authenticate** using the flow above
2. **Perform a search** in the frontend
3. **Check backend logs** for:
   - Credit consumption
   - Any errors

## 🐛 Troubleshooting

### Problem: "1sub API client not initialized"

**Check:**
1. Environment variables are set in Render
2. Render logs show: `"✅ 1sub API client initialized"`
3. If not, check for initialization errors in logs

**Solution:**
- Verify `ONESUB_API_KEY` is set correctly
- Check API key format: Should start with `sk-tool-`
- Redeploy backend after setting variables

### Problem: "Token verification failed"

**Check:**
1. Token is valid and not expired
2. Tool ID matches between backend and 1sub.io
3. Backend can reach 1sub.io API

**Solution:**
- Verify tool ID in Render matches 1sub.io dashboard
- Test token manually: `curl https://1sub.io/api/v1/verify-user`
- Check Render logs for detailed error messages

### Problem: "Insufficient credits"

**Check:**
1. User has credits in 1sub.io account
2. Credit amount per search is reasonable (0.01)
3. Backend is correctly consuming credits

**Solution:**
- User needs to purchase credits via 1sub.io
- Check credit balance in 1sub.io dashboard
- Verify credit consumption logic in backend

### Problem: Frontend shows "Purchase Access" but nothing happens

**Check:**
1. `getToolId()` function works
2. `createCheckout()` function works
3. Browser console for errors

**Solution:**
- Check browser console (F12) for errors
- Verify `/api/config/tool-id` endpoint works
- Check CORS allows frontend to call backend
- Verify 1sub.io API is reachable from frontend

## 📊 Step 6: Monitor Integration

### Render Logs

Check for:
- ✅ `"✅ 1sub API client initialized"` - On startup
- ✅ `"User authenticated: ..."` - On token verification
- ✅ `"Credits consumed: ..."` - On search
- ❌ Any errors mentioning "onesub" or "1sub"

### Vercel Logs

Check for:
- Frontend API calls to `/api/auth/verify`
- Frontend API calls to `/api/config/tool-id`
- Any network errors

## ✅ Success Criteria

Your 1sub integration is working if:

1. ✅ Backend initializes 1sub client without errors
2. ✅ `/api/config/tool-id` returns your tool ID
3. ✅ Frontend can get tool ID
4. ✅ "Purchase Access" button redirects to 1sub.io
5. ✅ Token verification works after purchase
6. ✅ User can search after authentication
7. ✅ Credits are consumed on each search
8. ✅ Insufficient credits error shows when balance is low

## 🔗 Useful Links

- **1sub.io Dashboard**: https://1sub.io/dashboard
- **1sub.io API Docs**: https://1sub.io/docs
- **Your Tool**: https://1sub.io/dashboard/tools (find your tool)
- **Render Dashboard**: https://dashboard.render.com
- **Vercel Dashboard**: https://vercel.com/dashboard

## 🎯 Next Steps

1. ✅ Verify all environment variables are set
2. ✅ Test token verification endpoint
3. ✅ Test full authentication flow
4. ✅ Test credit consumption
5. ✅ Monitor logs for any issues

