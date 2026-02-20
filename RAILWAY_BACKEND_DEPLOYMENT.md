# Deploy Backend to Railway - Complete Guide

## Step 1: Sign Up for Railway

1. Go to **https://railway.app**
2. Click **"Login"** or **"Start a New Project"**
3. Sign in with your **GitHub account**
4. Authorize Railway to access your repositories

## Step 2: Create New Project

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your repository: **`Manikanta05-dev/tyremanagement`**
4. Railway will automatically detect the Dockerfile

## Step 3: Add PostgreSQL Database

1. In your Railway project dashboard, click **"New"**
2. Select **"Database"**
3. Choose **"Add PostgreSQL"**
4. Railway will automatically create a database and generate connection details

## Step 4: Configure Environment Variables

Click on your backend service → **"Variables"** tab → Add these:

### Required Variables:

```bash
# Database (Railway auto-generates this, but verify it exists)
DATABASE_URL=${{Postgres.DATABASE_URL}}

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production-12345

# CORS - Add your Vercel domain
ALLOWED_ORIGINS=https://your-app-name.vercel.app,http://localhost:3000

# Optional: Twilio for WhatsApp (if you want invoice sending)
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

**Important:** Replace `your-app-name.vercel.app` with your actual Vercel URL!

## Step 5: Deploy

1. Railway will automatically start deploying
2. Wait 3-5 minutes for the build to complete
3. Check the **"Deployments"** tab for progress
4. Look for **"Success"** status

## Step 6: Get Your Backend URL

1. Go to **"Settings"** tab
2. Scroll to **"Domains"** section
3. Click **"Generate Domain"**
4. Copy the URL (e.g., `https://tyremanagement-production.up.railway.app`)

## Step 7: Test Your Backend

Open your Railway URL in browser:
- `https://your-app.railway.app/` - Should show API info
- `https://your-app.railway.app/health` - Should show `{"status": "healthy"}`
- `https://your-app.railway.app/docs` - Should show API documentation

## Step 8: Update Vercel Frontend

1. Go to **Vercel Dashboard** → Your Project
2. Click **"Settings"** → **"Environment Variables"**
3. Find `VITE_API_URL` and click **"Edit"**
4. Change value to: `https://your-app.railway.app/api`
5. Click **"Save"**
6. Go to **"Deployments"** tab
7. Click **"Redeploy"** on the latest deployment

## Step 9: Create First User (Admin)

You need to create an admin user. Two options:

### Option A: Using Railway CLI

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Run database migration/seed
railway run python -c "from app.core.database import create_admin_user; create_admin_user()"
```

### Option B: Using API directly

Use a tool like Postman or curl:

```bash
curl -X POST https://your-app.railway.app/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123",
    "full_name": "Admin User",
    "email": "admin@example.com",
    "role": "admin"
  }'
```

## Step 10: Test Complete Flow

1. Open your Vercel app: `https://your-app.vercel.app`
2. Try to login with the admin credentials
3. Should successfully login and see dashboard
4. Test creating inventory, sales, etc.

## Troubleshooting

### Build Failed
- Check **"Deployments"** → **"View Logs"**
- Verify `Dockerfile.backend` is correct
- Ensure all dependencies in `requirements.txt`

### Database Connection Error
- Verify `DATABASE_URL` variable exists
- Check PostgreSQL service is running
- Look at logs for connection errors

### CORS Error
- Update `ALLOWED_ORIGINS` to include your Vercel URL
- Redeploy backend after changing variables

### 502 Bad Gateway
- Check if app is listening on correct PORT
- Verify `CMD` in Dockerfile uses `${PORT:-8000}`
- Check deployment logs for startup errors

## Railway Free Tier Limits

- **$5 credit per month** (resets monthly)
- **500 hours of usage** (enough for 24/7 small apps)
- **100 GB bandwidth**
- **1 GB RAM per service**

Your app should easily fit within free tier limits!

## Monitoring

- **View Logs**: Click on service → "Deployments" → "View Logs"
- **Metrics**: Click on service → "Metrics" tab
- **Database**: Click on PostgreSQL → "Data" to view tables

## Updating Your App

Railway auto-deploys when you push to GitHub:

```bash
git add .
git commit -m "Update backend"
git push origin main
```

Railway will automatically rebuild and redeploy!

---

## Quick Checklist

- [ ] Railway account created
- [ ] Project deployed from GitHub
- [ ] PostgreSQL database added
- [ ] Environment variables configured
- [ ] Domain generated
- [ ] Backend URL tested (shows API info)
- [ ] Vercel frontend updated with backend URL
- [ ] Admin user created
- [ ] Login tested successfully

**Your backend is now live on Railway! 🚀**

