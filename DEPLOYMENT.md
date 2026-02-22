# Deployment Guide

## Step 1: Deploy Backend to Render

1. Go to https://render.com and sign in with GitHub
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name:** tire-shop-backend
   - **Environment:** Docker
   - **Dockerfile Path:** Dockerfile.backend
   - **Plan:** Free

5. Add Environment Variables:
   ```
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=(will be added from database)
   ```

6. Create PostgreSQL Database:
   - Click "New +" → "PostgreSQL"
   - **Name:** tire-shop-db
   - **Plan:** Free
   - Link to web service

7. Deploy and wait 5-10 minutes

8. Get your backend URL (e.g., https://tire-shop-backend.onrender.com)

## Step 2: Create Admin User

1. Go to your backend URL + /docs (e.g., https://tire-shop-backend.onrender.com/docs)
2. Find POST /auth/register
3. Click "Try it out"
4. Enter:
   ```json
   {
     "username": "admin",
     "password": "admin123",
     "full_name": "Admin User",
     "email": "admin@example.com",
     "role": "admin"
   }
   ```
5. Click "Execute"

## Step 3: Deploy Frontend to Vercel

1. Go to https://vercel.com and sign in with GitHub
2. Click "Add New..." → "Project"
3. Import your GitHub repository
4. Configure:
   - **Framework Preset:** Vite
   - **Root Directory:** frontend
   - **Build Command:** npm run build
   - **Output Directory:** dist

5. Add Environment Variable:
   ```
   VITE_API_URL=https://your-backend-url.onrender.com
   ```
   (Replace with your actual Render backend URL)

6. Click "Deploy"

7. Wait 2-3 minutes

## Step 4: Test

1. Open your Vercel URL
2. Login with: admin / admin123
3. Test all features

## Troubleshooting

**Login fails on mobile:**
- Clear browser cache
- Check if backend URL is accessible on mobile
- Verify VITE_API_URL in Vercel settings

**Backend not starting:**
- Check Render logs
- Verify DATABASE_URL is set
- Ensure all dependencies in requirements.txt

**Build fails:**
- Check build logs in Render/Vercel
- Verify Dockerfile.backend path
- Ensure all files are committed to GitHub

## Support

For issues, check the logs in Render/Vercel dashboards.
