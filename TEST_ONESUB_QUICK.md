# 🧪 Quick 1sub.io Testing Guide

## ✅ Your Current Status

Based on the test results:
- ✅ **Configuration**: All environment variables are set correctly
- ✅ **OneSubClient**: Can be initialized successfully
- ⚠️ **API Connectivity**: Test failed (might be network/firewall issue)
- ⚠️ **Backend Integration**: Needs full server initialization

## 🔍 Check Render Deployment

### Step 1: Verify Environment Variables in Render

1. Go to: https://dashboard.render.com
2. Click: Your service (`ecss-hunt-backend`)
3. Go to: **Environment** tab
4. Verify these are set:
   - `ONESUB_API_KEY` = `sk-tool-4tvtt2bqic4`
   - `ONESUB_TOOL_ID` = `0a080b57-d0f8-430a-835f-a1c86314c3cc`
   - `FLASK_SESSION_SECRET_KEY` = `0kwRhpjHgTQokkKzYE8dfF_YsmBiGjqNFLrcyExpemA`

### Step 2: Check Render Logs

1. Go to: **Logs** tab in Render
2. Look for these messages on startup:
   - `✅ 1sub API client initialized` ← **This confirms it's working**
   - `❌ Failed to initialize 1sub client` ← **This means there's an issue**

### Step 3: Test Backend Endpoints

#### Test 1: Tool ID Endpoint

```bash
curl https://ecss-hunt.onrender.com/api/config/tool-id
```

**Expected Response:**
```json
{
  "tool_id": "0a080b57-d0f8-430a-835f-a1c86314c3cc"
}
```

If this works, 1sub is connected! ✅

#### Test 2: Session Endpoint

```bash
curl https://ecss-hunt.onrender.com/api/auth/session
```

**Expected Response** (if not authenticated):
```json
{
  "authenticated": false,
  "message": "No active session"
}
```

If this works without errors, 1sub is connected! ✅

## 🎯 Test Full Flow

### Option 1: Test from Frontend

1. **Visit**: https://ecss-hunt.vercel.app/demo
2. **Click**: "Purchase Access" button
3. **Should redirect to**: https://1sub.io/login or checkout
4. **After purchase**: You'll be redirected back with `?token=...`
5. **Frontend should**: Automatically verify token and show "Connected"

### Option 2: Test Token Verification Manually

1. **Get a test token** from 1sub.io dashboard
2. **Test verification**:
   ```bash
   curl -X POST https://ecss-hunt.onrender.com/api/auth/verify \
     -H "Content-Type: application/json" \
     -d '{"token": "YOUR_TOKEN_HERE"}'
   ```

## 🔧 Common Issues & Solutions

### Issue: "1sub API client not initialized"

**Check Render Logs:**
- Look for: `❌ Failed to initialize 1sub client`
- Error message will tell you what's wrong

**Common Causes:**
1. `ONESUB_API_KEY` not set in Render
2. API key format is wrong
3. Network issue reaching 1sub.io

**Solution:**
1. Verify `ONESUB_API_KEY` is set in Render
2. Check it starts with `sk-tool-`
3. Redeploy backend after fixing

### Issue: Token Verification Fails

**Check:**
1. Token is valid and not expired
2. Tool ID matches between backend and 1sub.io
3. Backend logs show the error

**Solution:**
1. Verify tool ID in Render matches 1sub.io dashboard
2. Test with a fresh token
3. Check 1sub.io dashboard for token status

### Issue: Frontend Can't Get Tool ID

**Check:**
1. `/api/config/tool-id` endpoint works
2. CORS allows frontend to call backend
3. Browser console for errors

**Solution:**
1. Test endpoint directly: `curl https://ecss-hunt.onrender.com/api/config/tool-id`
2. Check browser console for CORS errors
3. Verify frontend is calling correct backend URL

## ✅ Success Checklist

Your 1sub integration is working if:

- [ ] Render logs show: `✅ 1sub API client initialized`
- [ ] `/api/config/tool-id` returns your tool ID
- [ ] `/api/auth/session` works without errors
- [ ] Frontend can get tool ID
- [ ] "Purchase Access" button redirects to 1sub.io
- [ ] Token verification works after purchase
- [ ] User can search after authentication

## 🚀 Quick Test Commands

```bash
# Test tool ID
curl https://ecss-hunt.onrender.com/api/config/tool-id

# Test session
curl https://ecss-hunt.onrender.com/api/auth/session

# Test health (should show 1sub initialized)
curl https://ecss-hunt.onrender.com/api/health
```

## 📝 Next Steps

1. ✅ Check Render logs for 1sub initialization
2. ✅ Test `/api/config/tool-id` endpoint
3. ✅ Test full authentication flow from frontend
4. ✅ Monitor logs during authentication

