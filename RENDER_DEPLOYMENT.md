# Deploy to Render - Complete Step-by-Step Guide

Render is simpler than Railway and has a generous free tier!

## Step 1: Create Render Account

1. Go to **https://render.com**
2. Click **"Get Started"** or **"Sign Up"**
3. Choose **"Sign up with GitHub"**
4. Authorize Render to access your GitHub repositories
5. You're now logged into Render!

---

## Step 2: Create PostgreSQL Database First

We need to create the database before the backend service.

1. From Render dashboard, click **"New +"** (top right)
2. Select **"PostgreSQL"**
3. Fill in the details:
   - **Name**: `tire-shop-db`
   - **Database**: `tireshop`
   - **User**: `tireshop`
   - **Region**: Choose closest to you
   - **Plan**: **Free**
4. Click **"Create Database"**
5. Wait 1-2 minutes for database to be created
6. **IMPORTANT**: Keep this tab open, you'll need the connection details!

---

## Step 3: Create Web Service (Backend)

1. Click **"New +"** again (top right)
2. Select **"Web Service"**
3. Click **"Build and deploy from a Git repository"**
4. Click **"Connect account"** if needed, or select your GitHub account
5. Find and click **"Connect"** next to: `Manikanta05-dev/tyremanagement`

---

## Step 4: Configure Web Service

Fill in these settings:

### Basic Settings:
- **Name**: `tire-shop-backend`
- **Region**: Same as your database
- **Branch**: `main`
- **Root Directory**: Leave empty (blank)
- **Environment**: **Docker**
- **Dockerfile Path**: `Dockerfile.backend`

### Instance Settings:
- **Plan**: **Free**

### Advanced Settings:
- **Health Check Path**: `/health`
- **Auto-Deploy**: Yes (enabled by default)

---

## Step 5: Add Environment Variables

Scroll down to **"Environment Variables"** section and click **"Add Environment Variable"**:

### Variable 1:
- **Key**: `DATABASE_URL`
- **Value**: Click **"Add from Database"**
  - Select your database: `tire-shop-db`
  - Select: **Internal Database URL**
  - Click **"Add"**

### Variable 2:
- **Key**: `SECRET_KEY`
- **Value**: `tire-shop-secret-key-2024-change-this-to-random-string`

### Variable 3:
- **Key**: `ALLOWED_ORIGINS`
- **Value**: `http://localhost:3000,https://*.vercel.app`

---

## Step 6: Deploy!

1. Click **"Create Web Service"** (bottom of page)
2. Render will start building your Docker image
3. This takes 5-10 minutes (first time is slower)
4. Watch the logs scroll in real-time
5. Wait for **"Your service is live 🎉"** message

---

## Step 7: Get Your Backend URL

1. Once deployed, you'll see your service dashboard
2. At the top, you'll see your URL: `https://tire-shop-backend.onrender.com`
3. **COPY THIS URL** - you need it for Vercel!

---

## Step 8: Test Your Backend

1. Open a new browser tab
2. Go to: `https://tire-shop-backend.onrender.com/`
3. You should see:
   ```json
   {
     "message": "Tire Shop Management API v2.0",
     "status": "running"
   }
   ```

4. Test health: `https://tire-shop-backend.onrender.com/health`
   - Should show: `{"status": "healthy"}`

5. Test docs: `https://tire-shop-backend.onrender.com/docs`
   - Should show API documentation

**If all work, your backend is live! ✅**

---

## Step 9: Update Vercel Frontend

1. Go to **https://vercel.com**
2. Click on your tire shop project
3. Go to **Settings** → **Environment Variables**
4. Find `VITE_API_URL` and click **Edit**
5. Change to: `https://tire-shop-backend.onrender.com/api`
   - **Important**: Add `/api` at the end!
6. Click **Save**
7. Go to **Deployments** tab
8. Click **"..."** on latest deployment → **"Redeploy"**
9. Wait 1-2 minutes

---

## Step 10: Create Admin User

1. Go to: `https://tire-shop-backend.onrender.com/docs`
2. Find **POST /api/auth/register**
3. Click **"Try it out"**
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
5. Click **"Execute"**
6. Should see **Response code: 200**

---

## Step 11: Test Complete App

1. Open your Vercel app: `https://your-app.vercel.app`
2. Login with:
   - Username: `admin`
   - Password: `admin123`
3. You should see the dashboard!
4. Test adding inventory, sales, etc.

**Everything should work now! 🎉**

---

## Important Notes About Render Free Tier

### Free Tier Includes:
- ✅ 750 hours/month (enough for 24/7)
- ✅ 512 MB RAM
- ✅ 100 GB bandwidth/month
- ✅ Free PostgreSQL database (90 days, then expires)
- ✅ Automatic HTTPS
- ✅ Auto-deploy from GitHub

### Important Limitation:
⚠️ **Free services spin down after 15 minutes of inactivity**
- First request after inactivity takes 30-60 seconds to wake up
- Subsequent requests are fast
- This is normal for free tier!

### To Keep Service Always Active (Optional):
Use a service like **UptimeRobot** (free) to ping your backend every 10 minutes:
1. Go to https://uptimerobot.com
2. Add monitor for: `https://tire-shop-backend.onrender.com/health`
3. Check interval: 10 minutes

---

## Troubleshooting

### Build Failed
- Check **"Logs"** tab for errors
- Verify `Dockerfile.backend` path is correct
- Ensure all dependencies in `requirements.txt`

### Database Connection Error
- Go to database → **"Info"** tab
- Copy **Internal Database URL**
- Update `DATABASE_URL` in web service environment variables
- Click **"Manual Deploy"** → **"Deploy latest commit"**

### CORS Error in Browser
- Check `ALLOWED_ORIGINS` includes your Vercel URL
- Should be: `http://localhost:3000,https://*.vercel.app`
- Redeploy if you change it

### Service Takes Long to Respond
- This is normal for free tier after inactivity
- Service "spins down" after 15 minutes of no requests
- First request wakes it up (30-60 seconds)
- Use UptimeRobot to keep it active

---

## Monitoring & Logs

- **View Logs**: Click on service → "Logs" tab
- **Metrics**: Click on service → "Metrics" tab
- **Database**: Click on database → "Info" for connection details

---

## Updating Your App

Render auto-deploys when you push to GitHub:

```bash
git add .
git commit -m "Update backend"
git push origin main
```

Render automatically rebuilds and redeploys!

---

## Quick Checklist

- [ ] Render account created
- [ ] PostgreSQL database created
- [ ] Web service created and deployed
- [ ] Environment variables configured
- [ ] Backend URL tested (shows API info)
- [ ] Vercel frontend updated with backend URL
- [ ] Admin user created
- [ ] Login tested successfully

**Your app is now fully deployed! 🚀**

Frontend: Vercel
Backend: Render
Database: Render PostgreSQL
