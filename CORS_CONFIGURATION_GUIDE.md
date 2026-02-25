# CORS Configuration Guide

## Problem

Frontend deployed on Vercel cannot access backend API on Render:

```
Access to XMLHttpRequest at 'https://backend.onrender.com/auth/login' 
from origin 'https://tyremanagement.vercel.app' has been blocked by CORS policy:
No 'Access-Control-Allow-Origin' header is present.
```

## Root Cause

CORS (Cross-Origin Resource Sharing) blocks requests from different origins by default. The backend must explicitly allow the frontend's origin.

### Common CORS Mistakes:

1. **Using wildcard with credentials:**
   ```python
   # ❌ WRONG - Cannot use "*" with allow_credentials=True
   allow_origins=["*"]
   allow_credentials=True
   ```

2. **Wildcard subdomain patterns:**
   ```python
   # ❌ WRONG - CORS doesn't support wildcard subdomains
   allow_origins=["https://*.vercel.app"]
   ```

3. **Hardcoded origins:**
   ```python
   # ❌ WRONG - Not flexible for different environments
   allow_origins=["https://myapp.vercel.app"]
   ```

## Solution

### 1. Configure CORS in `backend/app/main.py`:

```python
import os
from fastapi.middleware.cors import CORSMiddleware

# Read from environment variable
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173")
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",") if origin.strip()]

# Log for debugging
print(f"🌐 CORS allowed origins: {allowed_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Specific origins only
    allow_credentials=True,         # Allow cookies/auth headers
    allow_methods=["*"],            # Allow all HTTP methods
    allow_headers=["*"],            # Allow all headers
)
```

### 2. Set Environment Variable in Render:

In `render.yaml`:

```yaml
envVars:
  - key: ALLOWED_ORIGINS
    value: http://localhost:3000,http://localhost:5173,https://tyremanagement.vercel.app
```

Or in Render Dashboard:
- Go to your service → Environment
- Add variable: `ALLOWED_ORIGINS`
- Value: `http://localhost:5173,https://tyremanagement.vercel.app`

### 3. Update Frontend API URL:

In your Vercel deployment, set environment variable:

```bash
VITE_API_URL=https://your-backend.onrender.com
```

## How It Works

### Request Flow:

1. **Browser sends preflight request (OPTIONS):**
   ```
   Origin: https://tyremanagement.vercel.app
   Access-Control-Request-Method: POST
   Access-Control-Request-Headers: content-type
   ```

2. **Backend responds with CORS headers:**
   ```
   Access-Control-Allow-Origin: https://tyremanagement.vercel.app
   Access-Control-Allow-Credentials: true
   Access-Control-Allow-Methods: *
   Access-Control-Allow-Headers: *
   ```

3. **Browser allows actual request:**
   ```
   POST /auth/login
   Origin: https://tyremanagement.vercel.app
   Content-Type: application/json
   ```

## Multiple Frontend Deployments

If you have multiple Vercel deployments (staging, production, preview):

### Option 1: List all origins (Recommended)

```bash
ALLOWED_ORIGINS=https://app.vercel.app,https://app-staging.vercel.app,https://app-preview.vercel.app
```

### Option 2: Dynamic CORS (Advanced)

For preview deployments with dynamic URLs:

```python
from fastapi import Request

@app.middleware("http")
async def dynamic_cors(request: Request, call_next):
    origin = request.headers.get("origin")
    
    # Allow all Vercel preview deployments
    if origin and origin.endswith(".vercel.app"):
        response = await call_next(request)
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        return response
    
    return await call_next(request)
```

## Testing CORS

### Test from Browser Console:

```javascript
fetch('https://your-backend.onrender.com/health', {
  method: 'GET',
  credentials: 'include'
})
.then(r => r.json())
.then(data => console.log('CORS working:', data))
.catch(err => console.error('CORS error:', err));
```

### Test with curl:

```bash
curl -H "Origin: https://tyremanagement.vercel.app" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: content-type" \
     -X OPTIONS \
     https://your-backend.onrender.com/auth/login -v
```

Should return:
```
Access-Control-Allow-Origin: https://tyremanagement.vercel.app
Access-Control-Allow-Credentials: true
```

## Debugging CORS Issues

### Check Backend Logs:

Look for the CORS origins log:
```
🌐 CORS allowed origins: ['http://localhost:5173', 'https://tyremanagement.vercel.app']
```

### Check Browser Network Tab:

1. Open DevTools → Network
2. Look for failed request
3. Check Response Headers:
   - Should have `Access-Control-Allow-Origin`
   - Should match your frontend origin

### Common Issues:

1. **Origin not in allowed list:**
   - Add exact origin to ALLOWED_ORIGINS
   - Check for typos (http vs https, trailing slash)

2. **Credentials issue:**
   - Ensure `allow_credentials=True` in backend
   - Ensure `credentials: 'include'` in frontend fetch

3. **Preflight failure:**
   - Check OPTIONS request succeeds
   - Ensure all required headers are allowed

## Environment-Specific Configuration

### Development (Local):

```bash
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Staging:

```bash
ALLOWED_ORIGINS=http://localhost:5173,https://app-staging.vercel.app
```

### Production:

```bash
ALLOWED_ORIGINS=https://tyremanagement.vercel.app
```

## Security Best Practices

1. ✅ **Never use wildcard (`*`) with credentials**
2. ✅ **List specific origins only**
3. ✅ **Use HTTPS in production**
4. ✅ **Read origins from environment variables**
5. ✅ **Log allowed origins for debugging**
6. ❌ **Don't allow all origins in production**
7. ❌ **Don't hardcode origins in code**

## Current Configuration

### Backend (Render):
```
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,https://tyremanagement.vercel.app
```

### Frontend (Vercel):
```
VITE_API_URL=https://tire-shop-backend-fdoz.onrender.com
```

## Status

✅ **FIXED** - CORS properly configured for Vercel frontend

The frontend can now make authenticated requests to the backend!
