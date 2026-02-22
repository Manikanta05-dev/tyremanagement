# Tire Shop Management System

A full-stack inventory management system for tire shops with sales tracking, purchase management, and GST invoice generation.

## Tech Stack

**Frontend:** React + Vite  
**Backend:** FastAPI + Python  
**Database:** PostgreSQL  

## Features

- 📦 Inventory Management
- 💰 Sales Tracking
- 🛒 Purchase Orders
- 📄 GST Invoice Generation
- 📊 Dashboard & Reports
- 👥 User Authentication
- 📱 Mobile Responsive

## Local Development

### Prerequisites
- Python 3.12+
- Node.js 18+
- PostgreSQL 14+

### Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Deployment

**Frontend:** Vercel  
**Backend:** Render  
**Database:** Render PostgreSQL  

See deployment instructions below.

## License

MIT
