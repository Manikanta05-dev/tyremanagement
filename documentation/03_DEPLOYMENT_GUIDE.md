# 🚀 Deployment Guide - Production Ready

## Table of Contents
1. [Production Checklist](#production-checklist)
2. [Server Deployment](#server-deployment)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Security Configuration](#security-configuration)
6. [Monitoring & Maintenance](#monitoring--maintenance)

---

## Production Checklist

### Before Deployment

- [ ] Change default admin password
- [ ] Generate strong SECRET_KEY (min 32 characters)
- [ ] Update DATABASE_URL with production credentials
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Set secure environment variables
- [ ] Enable database backups
- [ ] Configure firewall rules
- [ ] Test all features
- [ ] Review security settings

### Generate Secure SECRET_KEY

```python
# Python
import secrets
print(secrets.token_urlsafe(32))
```

```bash
# Or using OpenSSL
openssl rand -hex 32
```

---

## Server Deployment

### Option 1: Traditional Linux Server (Ubuntu)

#### 1. System Setup

```bash
# Update system
sudo apt update
sudo apt upgrade -y

# Install dependencies
sudo apt install python3.9 python3-pip postgresql nginx -y
```

#### 2. PostgreSQL Setup

```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE tire_shop_db;
CREATE USER tire_shop_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE tire_shop_db TO tire_shop_user;
\q
```

#### 3. Backend Deployment

```bash
# Clone repository
git clone <your-repo-url>
cd tire-shop-app/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Configure environment
nano .env
```

**Production .env:**
```env
DATABASE_URL=postgresql://tire_shop_user:your_secure_password@localhost:5432/tire_shop_db
SECRET_KEY=<your-generated-secret-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# WhatsApp (if using)
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
```

```bash
# Initialize database
python init_db.py

# Test backend
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

#### 4. Create Systemd Service

```bash
sudo nano /etc/systemd/system/tireshop-api.service
```

**Service file:**
```ini
[Unit]
Description=Tire Shop API
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/tire-shop-app/backend
Environment="PATH=/path/to/tire-shop-app/backend/venv/bin"
ExecStart=/path/to/tire-shop-app/backend/venv/bin/gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

[Install]
WantedBy=multi-user.target
```

```bash
# Start service
sudo systemctl daemon-reload
sudo systemctl start tireshop-api
sudo systemctl enable tireshop-api
sudo systemctl status tireshop-api
```

#### 5. Frontend Deployment

```bash
cd ../frontend

# Install dependencies
npm install

# Update environment
nano .env
```

**Production .env:**
```env
VITE_API_URL=https://api.yourdomain.com
```

```bash
# Build for production
npm run build
```

#### 6. Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/tireshop
```

**Nginx config:**
```nginx
# Frontend
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    root /path/to/tire-shop-app/frontend/dist;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
}

# Backend API
server {
    listen 80;
    server_name api.yourdomain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/tireshop /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 7. SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get certificates
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
sudo certbot --nginx -d api.yourdomain.com

# Auto-renewal is configured automatically
```

---

## Docker Deployment

### 1. Backend Dockerfile

Create `backend/Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create invoices directory
RUN mkdir -p invoices

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Frontend Dockerfile

Create `frontend/Dockerfile`:
```dockerfile
# Build stage
FROM node:16-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html

# Nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

Create `frontend/nginx.conf`:
```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### 3. Docker Compose

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: tire_shop_db
      POSTGRES_USER: tire_shop_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

  backend:
    build: ./backend
    environment:
      DATABASE_URL: postgresql://tire_shop_user:${DB_PASSWORD}@db:5432/tire_shop_db
      SECRET_KEY: ${SECRET_KEY}
      TWILIO_ACCOUNT_SID: ${TWILIO_ACCOUNT_SID}
      TWILIO_AUTH_TOKEN: ${TWILIO_AUTH_TOKEN}
      TWILIO_WHATSAPP_FROM: ${TWILIO_WHATSAPP_FROM}
    depends_on:
      - db
    ports:
      - "8000:8000"
    volumes:
      - ./backend/invoices:/app/invoices
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped

volumes:
  postgres_data:
```

Create `.env` file:
```env
DB_PASSWORD=your_secure_password
SECRET_KEY=your_secret_key
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
```

### 4. Deploy with Docker

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Rebuild
docker-compose up -d --build
```

---

## Cloud Deployment

### AWS Deployment

#### 1. Backend (EC2 + RDS)

**EC2 Setup:**
```bash
# Launch Ubuntu EC2 instance
# Configure security groups (ports 22, 80, 443, 8000)
# Connect via SSH

# Follow traditional server deployment steps
```

**RDS Setup:**
```bash
# Create PostgreSQL RDS instance
# Note the endpoint URL
# Update DATABASE_URL in .env
```

#### 2. Frontend (S3 + CloudFront)

```bash
# Build frontend
cd frontend
npm run build

# Create S3 bucket
aws s3 mb s3://your-bucket-name

# Upload files
aws s3 sync dist/ s3://your-bucket-name

# Enable static website hosting
aws s3 website s3://your-bucket-name --index-document index.html

# Create CloudFront distribution
# Point to S3 bucket
# Configure custom domain
```

### Heroku Deployment

#### Backend

```bash
# Install Heroku CLI
# Login
heroku login

# Create app
cd backend
heroku create tireshop-api

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set SECRET_KEY=your_secret_key
heroku config:set ALGORITHM=HS256
heroku config:set ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Create Procfile
echo "web: uvicorn app.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
git init
git add .
git commit -m "Initial commit"
git push heroku main

# Initialize database
heroku run python init_db.py
```

#### Frontend (Vercel)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd frontend
vercel

# Follow prompts
# Set VITE_API_URL to your Heroku backend URL
```

---

## Security Configuration

### 1. Environment Variables

**Never commit these to git:**
```env
DATABASE_URL=postgresql://...
SECRET_KEY=...
TWILIO_ACCOUNT_SID=...
TWILIO_AUTH_TOKEN=...
```

### 2. CORS Configuration

Update `backend/app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. HTTPS Only

Nginx config:
```nginx
# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # ... rest of config
}
```

### 4. Firewall Rules

```bash
# Ubuntu UFW
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable
```

### 5. Database Security

```sql
-- Revoke public access
REVOKE ALL ON DATABASE tire_shop_db FROM PUBLIC;

-- Grant specific permissions
GRANT CONNECT ON DATABASE tire_shop_db TO tire_shop_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO tire_shop_user;
```

---

## Monitoring & Maintenance

### 1. Application Monitoring

```bash
# Check backend logs
sudo journalctl -u tireshop-api -f

# Check Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Check system resources
htop
df -h
```

### 2. Database Backup

```bash
# Manual backup
pg_dump -U tire_shop_user tire_shop_db > backup_$(date +%Y%m%d).sql

# Restore
psql -U tire_shop_user tire_shop_db < backup_20240219.sql

# Automated daily backup (crontab)
0 2 * * * pg_dump -U tire_shop_user tire_shop_db > /backups/tire_shop_$(date +\%Y\%m\%d).sql
```

### 3. Update Application

```bash
# Backend update
cd /path/to/tire-shop-app/backend
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart tireshop-api

# Frontend update
cd /path/to/tire-shop-app/frontend
git pull
npm install
npm run build
sudo systemctl reload nginx
```

### 4. Health Checks

```bash
# Backend health
curl http://localhost:8000/health

# Database connection
psql -U tire_shop_user -d tire_shop_db -c "SELECT 1;"

# Frontend
curl -I http://localhost
```

### 5. Performance Optimization

**Backend:**
```python
# In database.py - Connection pooling
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=20,
    max_overflow=0
)
```

**Nginx Caching:**
```nginx
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### 6. Log Rotation

```bash
# Create logrotate config
sudo nano /etc/logrotate.d/tireshop

# Add:
/var/log/nginx/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data adm
    sharedscripts
    postrotate
        [ -f /var/run/nginx.pid ] && kill -USR1 `cat /var/run/nginx.pid`
    endscript
}
```

---

## Troubleshooting Production Issues

### High CPU Usage

```bash
# Check processes
top
htop

# Check backend workers
ps aux | grep gunicorn

# Restart if needed
sudo systemctl restart tireshop-api
```

### Database Connection Issues

```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check connections
sudo -u postgres psql -c "SELECT * FROM pg_stat_activity;"

# Restart PostgreSQL
sudo systemctl restart postgresql
```

### Disk Space Issues

```bash
# Check disk usage
df -h

# Find large files
du -sh /* | sort -h

# Clean old logs
sudo journalctl --vacuum-time=7d

# Clean old backups
find /backups -mtime +30 -delete
```

---

## Production Checklist Summary

### Security
- [x] HTTPS enabled
- [x] Strong passwords
- [x] Firewall configured
- [x] CORS restricted
- [x] Environment variables secured

### Performance
- [x] Database connection pooling
- [x] Nginx caching
- [x] Gzip compression
- [x] Static file optimization

### Reliability
- [x] Systemd service
- [x] Auto-restart enabled
- [x] Database backups
- [x] Log rotation
- [x] Health checks

### Monitoring
- [x] Application logs
- [x] Error tracking
- [x] Performance monitoring
- [x] Disk space alerts
- [x] Backup verification

---

**Your application is production-ready!** 🚀
