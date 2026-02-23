# Final Deployment Steps - Working Configuration

## Current Status

✅ Backend is deployed and working at: `https://tire-shop-backend-fdoz.onrender.com`
✅ Admin user created: username=`admin`, password=`admin`
❌ Frontend is not connecting to backend (using localhost instead)

## The Problem

Vercel is not reading the `VITE_API_URL` environment variable correctly. The frontend keeps trying to connect to `localhost:8000`.

## Solution: Force Vercel to Use Correct URL

### Option 1: Delete and Redeploy (Recommended)

1. Go to Vercel dashboard
2. Click your project
3. Go to **Settings** → **General**
4. Scroll down and click **"Delete Project"**
5. Confirm deletion
6. Go back to Vercel home
7. Click **"Add New..."** → **"Project"**
8. Import your repo again
9. Configure:
   - Framework: **Vite**
   - Root Directory: **frontend**
   - Build Command: **npm run build**
   - Output Directory: **dist**
10. Add Environment Variable:
    - Key: `VITE_API_URL`
    - Value: `https://tire-shop-backend-fdoz.onrender.com`
    - Check all environments
11. Click **Deploy**

### Option 2: Clear Build Cache

1. Go to Vercel → Your Project → **Settings**
2. Go to **Environment Variables**
3. Verify `VITE_API_URL` = `https://tire-shop-backend-fdoz.onrender.com`
4. Go to **Deployments**
5. Click **"..."** on latest → **"Redeploy"**
6. **UNCHECK** "Use existing Build Cache"
7. Click **Redeploy**

### Option 3: Add to vercel.json (If above don't work)

Add this to `frontend/vercel.json`:

```json
{
  "env": {
    "VITE_API_URL": "https://tire-shop-backend-fdoz.onrender.com"
  }
}
```

Then commit and push.

## Test After Deployment

1. Open your Vercel URL
2. Open browser console (F12)
3. Look for: `API Base URL: https://tire-shop-backend-fdoz.onrender.com`
4. If you see `localhost:8000`, the env variable still isn't working
5. If you see the correct URL, try logging in with: `admin` / `admin`

## Backend URLs (For Reference)

- Health Check: https://tire-shop-backend-fdoz.onrender.com/health
- API Docs: https://tire-shop-backend-fdoz.onrender.com/docs
- Root: https://tire-shop-backend-fdoz.onrender.com/

## Login Credentials

- Username: `admin`
- Password: `admin`

## If Still Not Working

The issue is 100% that Vercel is not passing the environment variable during build. Try Option 1 (delete and redeploy) - this forces a completely fresh deployment.
