# CORS Troubleshooting Guide

## Issue: CORS Blocked Despite Correct Configuration

### Symptom:
```
Access to XMLHttpRequest at 'https://backend.onrender.com/auth/login' 
from origin 'https://tyremanagement.vercel.app' has been blocked by CORS policy:
No 'Access-Control-Allow-Origin' header is present.
```

## Root Cause: Whitespace in Environment Variables

When setting environment variables in Render dashboard or YAML files, extra whitespace can be accidentally added:

```yaml
# ❌ WRONG - Has whitespace
ALLOWED_ORIGINS: " http://localhost:5173 , https://tyremanagement.vercel.app "

# ✅ CORRECT - No extra whitespace
ALLOWED_ORIGINS: "http://localhost:5173,https://tyremanagement.vercel.app"
```

### Why This Breaks CORS:

1. **Origin with whitespace**: `" https://tyremanagement.vercel.app"` (note leading space)
2. **Actual origin**: `"https://tyremanagement.vercel.app"` (no space)
3. **String comparison fails**: `" https://tyremanagement.vercel.app" !== "https://tyremanagement.vercel.app"`
4. **CORS header not added**: Backend doesn't recognize the origin

## Solution Implemented

### Code Fix in `backend/app/main.py`:

```python
# Read and parse ALLOWED_ORIGINS with whitespace stripping
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173")
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",") if origin.strip()]

# Enhanced logging for debugging
print(f"🌐 CORS Configuration:")
print(f"   Raw ALLOWED_ORIGINS: {repr(allowed_origins_str)}")
print(f"   Parsed origins: {allowed_origins}")
print(f"   Total origins: {len(allowed_origins)}")
```

### What This Does:

1. **Splits by comma**: `"a , b , c"` → `["a ", " b ", " c"]`
2. **Strips whitespace**: `["a ", " b ", " c"]` → `["a", "b", "c"]`
3. **Filters empty strings**: Removes any empty entries
4. **Logs for debugging**: Shows both raw and parsed values

## Verification Steps

### 1. Check Backend Logs

After deployment, look for CORS configuration in logs:

```
🌐 CORS Configuration:
   Raw ALLOWED_ORIGINS: 'http://localhost:5173,https://tyremanagement.vercel.app'
   Parsed origins: ['http://localhost:5173', 'https://tyremanagement.vercel.app']
   Total origins: 2
```

### 2. Use Debug Endpoint

Call the CORS debug endpoint:

```bash
curl https://your-backend.onrender.com/debug/cors_config
```

Expected response:
```json
{
  "status": "success",
  "raw_value": "http://localhost:5173,https://tyremanagement.vercel.app",
  "parsed_origins": [
    "http://localhost:5173",
    "https://tyremanagement.vercel.app"
  ],
  "total_origins": 2,
  "has_whitespace": false,
  "environment": "production"
}
```

### 3. Test CORS from Browser

Open browser console on your frontend and run:

```javascript
fetch('https://your-backend.onrender.com/health', {
  method: 'GET',
  credentials: 'include'
})
.then(r => {
  console.log('CORS Headers:', r.headers.get('access-control-allow-origin'));
  return r.json();
})
.then(data => console.log('Success:', data))
.catch(err => console.error('Error:', err));
```

Should log:
```
CORS Headers: https://tyremanagement.vercel.app
Success: {status: "healthy", version: "2.0.0"}
```

## Common CORS Issues and Fixes

### Issue 1: Origin Mismatch

**Problem**: Frontend uses `https://app.vercel.app` but backend allows `https://app.vercel.app/`

**Fix**: Ensure exact match (no trailing slash):
```yaml
ALLOWED_ORIGINS: "https://tyremanagement.vercel.app"
```

### Issue 2: HTTP vs HTTPS

**Problem**: Frontend uses HTTPS but backend allows HTTP

**Fix**: Use HTTPS in production:
```yaml
# ❌ WRONG
ALLOWED_ORIGINS: "http://tyremanagement.vercel.app"

# ✅ CORRECT
ALLOWED_ORIGINS: "https://tyremanagement.vercel.app"
```

### Issue 3: Multiple Vercel Deployments

**Problem**: Preview deployments have different URLs

**Fix**: Add all deployment URLs:
```yaml
ALLOWED_ORIGINS: "https://app.vercel.app,https://app-staging.vercel.app,https://app-git-feature.vercel.app"
```

### Issue 4: Wildcard Not Working

**Problem**: Using `https://*.vercel.app` doesn't work

**Fix**: CORS doesn't support wildcard subdomains. List each URL explicitly or implement dynamic CORS:

```python
from fastapi import Request

@app.middleware("http")
async def dynamic_cors(request: Request, call_next):
    origin = request.headers.get("origin")
    response = await call_next(request)
    
    # Allow all Vercel deployments
    if origin and origin.endswith(".vercel.app"):
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
    
    return response
```

### Issue 5: Credentials Not Working

**Problem**: Cookies/auth tokens not sent

**Fix**: Ensure both backend and frontend have credentials enabled:

Backend:
```python
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,  # ← Must be True
    ...
)
```

Frontend:
```javascript
fetch(url, {
  credentials: 'include'  // ← Must be 'include'
})
```

## Testing Checklist

Before deploying:

- [ ] ALLOWED_ORIGINS has no extra whitespace
- [ ] All origins use HTTPS in production
- [ ] No trailing slashes in origins
- [ ] Origins match exactly (case-sensitive)
- [ ] `allow_credentials=True` in backend
- [ ] `credentials: 'include'` in frontend
- [ ] Test with curl or browser console
- [ ] Check backend logs for parsed origins

## Debug Endpoints

### 1. CORS Configuration
```bash
GET /debug/cors_config
```

Shows:
- Raw ALLOWED_ORIGINS value
- Parsed origins list
- Whitespace detection
- Environment

### 2. Health Check
```bash
GET /health
```

Test basic CORS functionality

### 3. Database Status
```bash
GET /debug/db_status
```

Verify backend is working

## Production Configuration

### Render Environment Variables:

```yaml
envVars:
  - key: ALLOWED_ORIGINS
    value: http://localhost:5173,https://tyremanagement.vercel.app
  - key: ENVIRONMENT
    value: production
```

### Vercel Environment Variables:

```bash
VITE_API_URL=https://tire-shop-backend-fdoz.onrender.com
```

## Mobile App Considerations

If using mobile app (React Native, Flutter, etc.):

1. **Add mobile origins**: May need to allow `capacitor://localhost` or `ionic://localhost`
2. **Test on device**: CORS behaves differently on mobile
3. **Use HTTPS**: Mobile apps require secure connections

Example:
```yaml
ALLOWED_ORIGINS: "http://localhost:5173,https://tyremanagement.vercel.app,capacitor://localhost"
```

## Status

✅ **FIXED** - Whitespace stripping implemented
✅ **VERIFIED** - Debug endpoint added
✅ **TESTED** - Works with whitespace in env vars

The CORS configuration now correctly handles whitespace and provides debugging tools!
