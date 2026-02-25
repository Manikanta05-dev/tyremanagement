# Render Deployment Guide - Production Ready

## Changes Made ✅

### 1. Database Connection (SSL Support)
- ✅ Auto-detects Render environment
- ✅ Adds `sslmode=require` for PostgreSQL
- ✅ Connection pooling with pre-ping
- ✅ Works locally and in production

### 2. Auto Create Tables
- ✅ Tables created on startup event
- ✅ No manual migration needed
- ✅ Logs success/failure

### 3. User Authentication
- ✅ Register endpoint accepts JSON
- ✅ Login endpoint accepts JSON
- ✅ Proper error codes (400, 401, 500)
- ✅ Duplicate username/email validation
- ✅ Password hashing with bcrypt

### 4. Configuration
- ✅ Reads from environment variables
- ✅ Fallback to defaults for local dev
- ✅ SECRET_KEY from environment
- ✅ CORS from environment

### 5. Dockerfile
- ✅ Exposes port 10000
- ✅ Uses $PORT from Render
- ✅ Proper startup command

---

## Deployment Steps

### Step 1: Create PostgreSQL Database

1. Go to https://render.com
2. Click "New +" → "PostgreSQL"
3. Configure:
   - Name: `tire-shop-db`
   - Database: `tireshop`
   - Plan: **Free**
4. Click "Create Database"
5. Wait 2 minutes

### Step 2: Deploy Backend

1. Click "New +" → "Web Service"
2. Connect GitHub repo: `Manikanta05-dev/tyremanagement`
3. Configure:
   - **Name:** `tire-shop-backend`
   - **Language:** Python
   - **Branch:** main
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free

4. **Environment Variables:**

   Click "Add Environment Variable":

   **Variable 1:**
   - Key: `DATABASE_URL`
   - Click "Add from Database" → Select `tire-shop-db` → "Internal Database URL"

   **Variable 2:**
   - Key: `SECRET_KEY`
   - Value: `your-super-secret-key-change-this-12345678`

   **Variable 3:**
   - Key: `ALLOWED_ORIGINS`
   - Value: `http://localhost:3000,http://localhost:5173,https://*.vercel.app`

5. Click "Create Web Service"
6. Wait 5-10 minutes

### Step 3: Verify Backend

Open: `https://your-backend.onrender.com/health`

Should show:
```json
{"status": "healthy", "version": "2.0.0"}
```

Check logs for:
```
🚀 Starting up...
📊 Database URL: postgresql://...
✅ Database tables created successfully
```

### Step 4: Create First User

Go to: `https://your-backend.onrender.com/docs`

Find **POST /auth/register** and execute:

```json
{
  "username": "admin",
  "password": "admin123",
  "email": "admin@example.com",
  "full_name": "Admin User",
  "role": "admin"
}
```

Should return **201 Created** with user details.

### Step 5: Test Login

Find **POST /auth/login** and execute:

```json
{
  "username": "admin",
  "password": "admin123"
}
```

Should return:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "username": "admin",
    "email": "admin@example.com",
    "full_name": "Admin User",
    "role": "admin",
    "id": 1
  }
}
```

---

## Frontend Deployment (Vercel)

1. Go to https://vercel.com
2. Import your GitHub repo
3. Configure:
   - Framework: **Vite**
   - Root Directory: **frontend**
   - Build Command: **npm run build**
   - Output Directory: **dist**

4. **Environment Variable:**
   - Key: `VITE_API_URL`
   - Value: `https://your-backend.onrender.com`

5. Deploy

---

## Troubleshooting

### Database Connection Error
- Check DATABASE_URL includes `sslmode=require`
- Verify PostgreSQL service is running
- Check logs for SSL errors

### Tables Not Created
- Check startup logs for "✅ Database tables created"
- Verify DATABASE_URL is correct
- Check PostgreSQL permissions

### Login Returns 500
- Check SECRET_KEY is set
- Verify user exists in database
- Check password hashing works

### CORS Error
- Add your Vercel domain to ALLOWED_ORIGINS
- Redeploy backend after changing

---

## Environment Variables Summary

### Backend (Render)
```
DATABASE_URL=<from PostgreSQL service>
SECRET_KEY=your-secret-key-here
ALLOWED_ORIGINS=http://localhost:3000,https://*.vercel.app
```

### Frontend (Vercel)
```
VITE_API_URL=https://your-backend.onrender.com
```

---

## Success Checklist

- [ ] PostgreSQL database created
- [ ] Backend deployed successfully
- [ ] Health check returns 200
- [ ] Tables created (check logs)
- [ ] User registered successfully
- [ ] Login returns JWT token
- [ ] Frontend deployed
- [ ] Frontend connects to backend
- [ ] Login works from frontend

---

**All production issues fixed! Ready to deploy! 🚀**
