# 🚀 Getting Started - Tire Shop Management System v2.0

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Quick Start (5 Minutes)](#quick-start-5-minutes)
4. [Detailed Setup](#detailed-setup)
5. [First Steps](#first-steps)
6. [Troubleshooting](#troubleshooting)

---

## Overview

A **production-ready** full-stack tire shop management system with enterprise features:

- 🔐 JWT Authentication
- 📦 Inventory Management
- 🛒 Purchase Tracking
- 💰 Sales & Billing
- 📄 GST Invoice PDF Generation
- 💎 Profit Calculation
- 📋 Daily Closing Reports
- 📱 WhatsApp Integration
- 📊 Dashboard Analytics

**Tech Stack:**
- Backend: FastAPI + PostgreSQL + SQLAlchemy
- Frontend: React + Vite + Tailwind CSS
- PDF: ReportLab
- WhatsApp: Twilio API

---

## Prerequisites

### Required Software
- **Python 3.9+** - Backend runtime
- **Node.js 16+** - Frontend runtime
- **PostgreSQL 13+** - Database

### Check Installations
```bash
# Check Python
python --version

# Check Node.js
node --version

# Check PostgreSQL
psql --version
```

---

## Quick Start (5 Minutes)

### Step 1: Create Database (1 minute)
```bash
# Open PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE tire_shop_db;

# Exit
\q
```

### Step 2: Backend Setup (2 minutes)
```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Update .env file with your PostgreSQL password
# Edit backend/.env and change 'password' to your actual password

# Initialize database with admin user
python init_db.py

# Start backend
uvicorn app.main:app --reload
```

✅ Backend running at: **http://localhost:8000**
📚 API Docs: **http://localhost:8000/docs**

### Step 3: Frontend Setup (2 minutes)
Open a **NEW terminal**:
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start frontend
npm run dev
```

✅ Frontend running at: **http://localhost:3000**

### Step 4: Login & Test
1. Open browser: **http://localhost:3000**
2. Login with:
   - **Username:** `admin`
   - **Password:** `admin123`
3. Start using the application!

---

## Detailed Setup

### Backend Configuration

#### 1. Environment Variables
Edit `backend/.env`:
```env
# Database
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/tire_shop_db

# Security
SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# WhatsApp (Optional)
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
```

#### 2. Database Initialization
```bash
cd backend
python init_db.py
```

This creates:
- Default admin user (admin/admin123)
- All database tables
- Required indexes

#### 3. Start Backend
```bash
# Development mode
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or use the batch file (Windows)
start-backend.bat
```

### Frontend Configuration

#### 1. Environment Variables
Edit `frontend/.env`:
```env
VITE_API_URL=http://localhost:8000
```

#### 2. Start Frontend
```bash
cd frontend
npm run dev

# Or use the batch file (Windows)
start-frontend.bat
```

### WhatsApp Setup (Optional)

#### 1. Create Twilio Account
- Visit: https://www.twilio.com/
- Sign up for free trial
- Get Account SID and Auth Token

#### 2. Enable WhatsApp
- Go to Twilio Console
- Enable WhatsApp Sandbox
- Get WhatsApp number

#### 3. Configure
Add credentials to `backend/.env`:
```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
```

---

## First Steps

### 1. Add Inventory (2 minutes)
1. Go to **Inventory** page
2. Click **+ Add New Tire**
3. Fill in details:
   - Brand: MRF
   - Size: 195/65R15
   - Type: Tubeless
   - Quantity: 25
   - Purchase Price: 3500
   - Selling Price: 4500
   - Date: Today
4. Click **Add**

### 2. Record Purchase (2 minutes)
1. Go to **Purchase** page
2. Click **+ Add Purchase**
3. Fill in details:
   - Supplier: ABC Tires
   - Select Tire: MRF 195/65R15
   - Quantity: 10
   - Purchase Price: 3500
   - Payment Status: Paid
4. Click **Add Purchase**
5. ✅ Inventory automatically increases!

### 3. Create Sale (3 minutes)
1. Go to **Sales** page
2. Click **+ New Sale**
3. Enter customer details:
   - Name: John Doe
   - Mobile: 9876543210
   - Payment: Cash
4. Add items:
   - Select tire
   - Enter quantity
   - Click **Add**
5. Click **Create Sale**
6. ✅ Invoice generated!

### 4. Download Invoice (1 minute)
1. On Sales page
2. Find the sale
3. Click **📄 PDF** button
4. Invoice downloads automatically

### 5. Send via WhatsApp (1 minute)
1. On Sales page
2. Click **📱 WhatsApp** button
3. Invoice sent to customer!

### 6. Check Dashboard (1 minute)
1. Go to **Dashboard**
2. See:
   - Today's Sales
   - Today's Profit
   - Monthly Revenue
   - Monthly Profit
   - Low Stock Alerts

### 7. Daily Closing (2 minutes)
1. Go to **Daily Closing** page
2. Select date (defaults to today)
3. Click **Generate Report**
4. See complete summary:
   - Total Sales
   - Total Profit
   - Payment breakdown
   - Items sold

---

## Troubleshooting

### Database Connection Error

**Problem:** Cannot connect to database

**Solutions:**
```bash
# 1. Check if PostgreSQL is running
# Windows: Check Services for PostgreSQL

# 2. Verify database exists
psql -U postgres -l

# 3. Check credentials in .env
# Make sure password is correct

# 4. Test connection
psql -U postgres -d tire_shop_db
```

### Port Already in Use

**Problem:** Port 8000 or 3000 already in use

**Solutions:**
```bash
# Find process using port 8000 (Backend)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Find process using port 3000 (Frontend)
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Module Not Found

**Problem:** Import errors or missing modules

**Solutions:**
```bash
# Backend
cd backend
pip install -r requirements.txt --force-reinstall

# Frontend
cd frontend
npm install --force
```

### WhatsApp Not Working

**Problem:** WhatsApp messages not sending

**Solutions:**
1. Check Twilio credentials in `.env`
2. Verify Twilio account is active
3. Check Twilio balance
4. Verify WhatsApp sandbox is enabled
5. Test with your own number first

### Invoice Not Generating

**Problem:** PDF download fails

**Solutions:**
```bash
# 1. Check if invoices folder exists
cd backend
mkdir invoices

# 2. Verify ReportLab is installed
pip install reportlab

# 3. Check file permissions
# Ensure backend can write to invoices folder
```

### Profit Showing Zero

**Problem:** Profit calculations are zero

**Solutions:**
1. Ensure purchase prices are recorded in inventory
2. Record purchases before making sales
3. Check that purchase_price field is not null
4. Verify profit calculation in dashboard

---

## Quick Commands Reference

### Backend Commands
```bash
# Start backend
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload

# Initialize database
python init_db.py

# View API docs
# Open: http://localhost:8000/docs
```

### Frontend Commands
```bash
# Start frontend
cd frontend
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Database Commands
```bash
# Connect to database
psql -U postgres -d tire_shop_db

# List tables
\dt

# View users
SELECT * FROM users;

# View inventory
SELECT * FROM tire_inventory;

# Exit
\q
```

---

## Default Credentials

**Admin Login:**
- Username: `admin`
- Password: `admin123`

⚠️ **Important:** Change the default password after first login in production!

---

## Next Steps

1. ✅ Complete setup
2. ✅ Login successfully
3. ✅ Add sample inventory
4. ✅ Record a purchase
5. ✅ Create a sale
6. ✅ Download invoice
7. ✅ Check dashboard
8. ✅ Generate daily closing

**Ready to manage your tire shop like a pro!** 🚀

---

## Support Resources

- **API Documentation:** http://localhost:8000/docs
- **Interactive API Testing:** http://localhost:8000/docs
- **Check Console Logs:** F12 in browser
- **Backend Logs:** Terminal running uvicorn
- **Frontend Logs:** Terminal running npm

---

## Production Deployment

For production deployment instructions, see:
- **02_FEATURES_AND_API.md** - Complete feature list
- **03_DEPLOYMENT_GUIDE.md** - Production deployment

---

**Setup Complete! Start managing your business efficiently.** ✅
