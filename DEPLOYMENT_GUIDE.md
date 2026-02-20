# 🚀 Deployment Guide

Complete guide for deploying the Tire Shop Inventory Management System to various platforms.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Deployment](#local-deployment)
3. [Docker Deployment](#docker-deployment)
4. [Heroku Deployment](#heroku-deployment)
5. [Railway Deployment](#railway-deployment)
6. [Render Deployment](#render-deployment)
7. [Vercel + Railway](#vercel--railway)
8. [Environment Variables](#environment-variables)
9. [Database Migration](#database-migration)
10. [Troubleshooting](#troubleshooting)

---

## Prerequisites

- Git installed
- GitHub account
- PostgreSQL database (local or cloud)
- Node.js 18+ and Python 3.12+

---

## 1. Local Deployment

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/tire-shop-inventory.git
cd tire-shop-inventory
```

### Step 2: Backend Setup
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your settings
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 3: Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Step 4: Access
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 2. Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild after changes
docker-compose up -d --build
```

### Services:
- **Database**: PostgreSQL on port 5432
- **Backend**: FastAPI on port 8000
- **Frontend**: React on port 3000

### Manual Docker Build

```bash
# Build backend
docker build -f Dockerfile.backend -t tire-shop-backend .

# Build frontend
docker build -f frontend/Dockerfile.frontend -t tire-shop-frontend ./frontend

# Run containers
docker run -d -p 8000:8000 tire-shop-backend
docker run -d -p 3000:3000 tire-shop-frontend
```

---

## 3. Heroku Deployment

### Prerequisites
- Heroku account
- Heroku CLI installed

### Step 1: Create Heroku App
```bash
heroku login
heroku create tire-shop-inventory
```

### Step 2: Add PostgreSQL
```bash
heroku addons:create heroku-postgresql:mini
```

### Step 3: Set Environment Variables
```bash
heroku config:set SECRET_KEY=your-secret-key
heroku config:set ALLOWED_ORIGINS=https://your-frontend-url.com
```

### Step 4: Deploy
```bash
git push heroku main
```

### Step 5: Run Migrations
```bash
heroku run python backend/seed_data.py
```

### Step 6: Open App
```bash
heroku open
```

---

## 4. Railway Deployment

### Prerequisites
- Railway account
- Railway CLI (optional)

### Step 1: Create New Project
1. Go to [Railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Connect your repository

### Step 2: Add PostgreSQL
1. Click "New" → "Database" → "PostgreSQL"
2. Railway will automatically set DATABASE_URL

### Step 3: Configure Backend Service
1. Add new service from repo
2. Set root directory: `backend`
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Step 4: Configure Frontend Service
1. Add new service from repo
2. Set root directory: `frontend`
3. Set build command: `npm install && npm run build`
4. Set start command: `npm run preview -- --host 0.0.0.0 --port $PORT`

### Step 5: Set Environment Variables
```
SECRET_KEY=your-secret-key
ALLOWED_ORIGINS=https://your-frontend-url.railway.app
```

### Step 6: Deploy
Railway will automatically deploy on git push.

---

## 5. Render Deployment

### Backend Deployment

1. **Create Web Service**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New" → "Web Service"
   - Connect GitHub repository
   - Configure:
     - Name: `tire-shop-backend`
     - Root Directory: `backend`
     - Environment: `Python 3`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

2. **Add PostgreSQL**
   - Click "New" → "PostgreSQL"
   - Copy connection string

3. **Set Environment Variables**
   ```
   DATABASE_URL=<your-postgres-url>
   SECRET_KEY=your-secret-key
   ALLOWED_ORIGINS=https://your-frontend.onrender.com
   ```

### Frontend Deployment

1. **Create Static Site**
   - Click "New" → "Static Site"
   - Connect repository
   - Configure:
     - Name: `tire-shop-frontend`
     - Root Directory: `frontend`
     - Build Command: `npm install && npm run build`
     - Publish Directory: `dist`

2. **Set Environment Variables**
   ```
   VITE_API_URL=https://your-backend.onrender.com
   ```

---

## 6. Vercel + Railway

### Backend on Railway
Follow Railway deployment steps above for backend.

### Frontend on Vercel

1. **Install Vercel CLI**
```bash
npm install -g vercel
```

2. **Deploy Frontend**
```bash
cd frontend
vercel --prod
```

3. **Configure**
   - Framework Preset: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`

4. **Set Environment Variables**
   - Go to Vercel Dashboard
   - Project Settings → Environment Variables
   - Add: `VITE_API_URL=https://your-backend.railway.app`

---

## 7. Environment Variables

### Backend (.env)
```env
# Required
DATABASE_URL=postgresql://user:password@host:port/database
SECRET_KEY=your-secret-key-min-32-characters
ALLOWED_ORIGINS=http://localhost:3000,https://your-frontend.com

# Optional
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=False
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
# or
VITE_API_URL=https://your-backend-api.com
```

---

## 8. Database Migration

### Initial Setup
```bash
cd backend

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

### Seed Data
```bash
python seed_data.py
```

### Production Migration
```bash
# On Heroku
heroku run alembic upgrade head

# On Railway/Render
# Add to build command:
alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

## 9. Production Checklist

### Security
- [ ] Change SECRET_KEY to strong random value
- [ ] Set DEBUG=False
- [ ] Configure CORS properly
- [ ] Use HTTPS
- [ ] Set secure password policies
- [ ] Enable rate limiting

### Database
- [ ] Use production PostgreSQL
- [ ] Enable backups
- [ ] Set connection pooling
- [ ] Configure SSL

### Performance
- [ ] Enable caching
- [ ] Optimize database queries
- [ ] Use CDN for static files
- [ ] Enable gzip compression
- [ ] Set up monitoring

### Monitoring
- [ ] Set up error tracking (Sentry)
- [ ] Configure logging
- [ ] Set up uptime monitoring
- [ ] Enable performance monitoring

---

## 10. Troubleshooting

### Issue: Database Connection Failed
**Solution**:
- Check DATABASE_URL format
- Verify database is running
- Check firewall rules
- Ensure SSL mode is correct

### Issue: CORS Errors
**Solution**:
- Add frontend URL to ALLOWED_ORIGINS
- Check protocol (http vs https)
- Verify no trailing slashes

### Issue: Build Fails
**Solution**:
- Check Python/Node versions
- Verify all dependencies in requirements.txt/package.json
- Check for syntax errors
- Review build logs

### Issue: 502 Bad Gateway
**Solution**:
- Check if backend is running
- Verify PORT environment variable
- Check application logs
- Ensure health check endpoint works

### Issue: Static Files Not Loading
**Solution**:
- Check build output directory
- Verify static file serving configuration
- Check file permissions
- Review nginx/server configuration

---

## 11. Post-Deployment

### Create Admin User
```bash
# SSH into your server or use platform CLI
python -c "from app.core.security import get_password_hash; print(get_password_hash('your-password'))"
```

### Seed Initial Data
```bash
python seed_data.py
```

### Test Endpoints
```bash
curl https://your-api.com/health
curl https://your-api.com/docs
```

### Monitor Logs
```bash
# Heroku
heroku logs --tail

# Railway
railway logs

# Render
# View in dashboard

# Docker
docker-compose logs -f
```

---

## 12. Continuous Deployment

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to Heroku
        uses: akhileshns/heroku-deploy@v3.12.12
        with:
          heroku_api_key: ${{secrets.HEROKU_API_KEY}}
          heroku_app_name: "tire-shop-inventory"
          heroku_email: "your-email@example.com"
```

---

## 13. Backup Strategy

### Database Backups

**Heroku**:
```bash
heroku pg:backups:capture
heroku pg:backups:download
```

**Railway**:
- Automatic daily backups
- Manual backups in dashboard

**Manual Backup**:
```bash
pg_dump $DATABASE_URL > backup.sql
```

### Restore Backup
```bash
psql $DATABASE_URL < backup.sql
```

---

## 14. Scaling

### Horizontal Scaling
- Add more dynos/instances
- Use load balancer
- Enable auto-scaling

### Database Scaling
- Upgrade to larger plan
- Enable read replicas
- Use connection pooling

### Caching
- Add Redis for session storage
- Cache API responses
- Use CDN for static assets

---

## 15. Support

For deployment issues:
- Check platform documentation
- Review application logs
- Open GitHub issue
- Contact support

---

## 🎉 Deployment Complete!

Your Tire Shop Inventory Management System is now live!

**Next Steps**:
1. Test all features
2. Set up monitoring
3. Configure backups
4. Add custom domain
5. Enable SSL certificate

---

**Happy Deploying!** 🚀
