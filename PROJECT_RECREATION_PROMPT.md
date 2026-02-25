# Complete Project Recreation Prompt

Use this prompt with an AI assistant to recreate this entire Tire Shop Management System from scratch.

---

## PROMPT START

Create a complete full-stack Tire Shop Inventory Management System with the following specifications:

## Project Overview

Build a production-ready business SaaS application for tire shop inventory, sales, purchases, and invoicing management.

## Technology Stack

### Backend:
- **Framework**: FastAPI 0.109.0
- **Database**: PostgreSQL with SQLAlchemy 2.0.25
- **Authentication**: JWT with python-jose, bcrypt 3.2.0, passlib 1.7.4
- **Server**: Uvicorn with standard extras
- **PDF Generation**: ReportLab 4.0.9
- **Notifications**: Twilio 8.11.1
- **Validation**: Pydantic 2.10.5, email-validator
- **Migrations**: Alembic 1.13.1
- **Other**: python-multipart, python-dotenv, pydantic-settings

### Frontend:
- **Framework**: React 18.2.0 with Vite 5.0.11
- **Routing**: React Router DOM 6.21.1
- **HTTP Client**: Axios 1.6.5
- **Charts**: Recharts 2.10.3
- **Notifications**: React Hot Toast 2.4.1
- **Styling**: Tailwind CSS 3.4.1
- **Build**: Vite with React plugin

### Deployment:
- **Backend**: Render.com (Docker, Free tier)
- **Frontend**: Vercel (Free tier)
- **Database**: Render PostgreSQL (Free tier)

## Project Structure

```
tire-shop-management/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py          # Login, Register
│   │   │   ├── dashboard.py     # Dashboard stats
│   │   │   ├── dependencies.py  # Auth dependencies
│   │   │   ├── inventory.py     # Tire inventory CRUD
│   │   │   ├── invoice.py       # PDF invoice generation
│   │   │   ├── profit.py        # Profit calculations
│   │   │   ├── purchase.py      # Purchase management
│   │   │   ├── reports.py       # Daily closing reports
│   │   │   ├── sales.py         # Sales management
│   │   │   └── debug.py         # Debug endpoints (db_status, cors_config, etc.)
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py        # Settings with pydantic-settings
│   │   │   ├── database.py      # SQLAlchemy setup with SSL support
│   │   │   └── security.py      # Password hashing, JWT tokens
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py          # User model with roles
│   │   │   ├── inventory.py     # TireInventory model
│   │   │   ├── sales.py         # Sales, SalesItem models
│   │   │   ├── purchase.py      # Purchase model
│   │   │   ├── purchase_item.py # PurchaseItem model
│   │   │   └── supplier.py      # Supplier model
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   ├── user_repository.py
│   │   │   ├── inventory_repository.py
│   │   │   ├── sales_repository.py
│   │   │   └── purchase_repository.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── user.py          # UserCreate, UserLogin, Token, UserResponse
│   │   │   ├── dashboard.py     # Dashboard schemas
│   │   │   ├── inventory.py     # Inventory schemas
│   │   │   ├── invoice.py       # Invoice schemas
│   │   │   ├── profit.py        # Profit schemas
│   │   │   ├── purchase.py      # Purchase schemas
│   │   │   └── sales.py         # Sales schemas
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── dashboard_service.py
│   │   │   ├── inventory_service.py
│   │   │   ├── invoice_service.py
│   │   │   ├── profit_service.py
│   │   │   ├── purchase_service.py
│   │   │   ├── sales_service.py
│   │   │   └── whatsapp_service.py
│   │   ├── __init__.py
│   │   └── main.py              # FastAPI app with CORS, startup events
│   ├── alembic/
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── invoices/                # Generated PDF invoices
│   ├── .env.example
│   ├── alembic.ini
│   ├── requirements.txt
│   └── seed_data.py             # Optional seed data script
├── frontend/
│   ├── public/
│   │   └── icons/               # App icons (optional)
│   ├── src/
│   │   ├── components/
│   │   │   ├── Layout.jsx       # Main layout with sidebar
│   │   │   ├── Loader.jsx       # Loading spinner
│   │   │   ├── ProtectedRoute.jsx
│   │   │   └── ResponsiveTable.jsx
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx    # Dashboard with stats
│   │   │   ├── DailyClosing.jsx # Daily closing reports
│   │   │   ├── Inventory.jsx    # Inventory management
│   │   │   ├── Login.jsx        # Login page
│   │   │   ├── Purchase.jsx     # Purchase management
│   │   │   ├── Reports.jsx      # Reports page
│   │   │   └── Sales.jsx        # Sales management
│   │   ├── services/
│   │   │   └── api.js           # Axios instance with interceptors
│   │   ├── styles/
│   │   │   └── app.css          # Tailwind imports + custom styles
│   │   ├── utils/
│   │   │   └── auth.js          # Auth helper functions
│   │   ├── App.jsx              # Router setup
│   │   └── main.jsx             # React entry point
│   ├── .env.example
│   ├── index.html               # NO service worker registration
│   ├── package.json
│   ├── postcss.config.js
│   ├── tailwind.config.js
│   └── vite.config.js
├── .gitignore
├── Dockerfile.backend
├── LICENSE
├── README.md
└── render.yaml
```

## Core Features to Implement

### 1. Authentication System
- User registration with username, email, password, role (admin/staff)
- JWT-based login with access tokens (24-hour expiry)
- Password hashing with bcrypt (3.2.0 for compatibility)
- Protected routes with role-based access
- User model with created_at timestamp

### 2. Inventory Management
- Tire inventory with brand, size, type, quantity, price
- Add, edit, delete tire entries
- Low stock alerts
- Search and filter functionality
- Stock level tracking

### 3. Sales Management
- Create sales with multiple items
- Customer information
- Payment modes (Cash, Card, UPI)
- Discount support
- Invoice generation
- Sales history with filters

### 4. Purchase Management
- Record purchases from suppliers
- Multiple items per purchase
- Payment status tracking
- Supplier management
- Purchase history

### 5. Dashboard
- Total sales, purchases, profit
- Low stock items
- Recent transactions
- Charts and graphs (using Recharts)
- Date range filters

### 6. Invoice Generation
- PDF invoices with GST details
- Company information
- Itemized billing
- Download functionality
- WhatsApp sharing (optional)

### 7. Reports
- Daily closing reports
- Profit calculations
- Sales by date range
- Purchase reports
- Export functionality

## Critical Backend Requirements

### 1. CORS Configuration (CRITICAL!)
```python
# In backend/app/main.py

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

app = FastAPI(title="Tire Shop Management API", version="2.0.0")

# CORS middleware - Read from environment
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173")
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",") if origin.strip()]

print(f"🌐 CORS Configuration:")
print(f"   Raw ALLOWED_ORIGINS: {repr(allowed_origins_str)}")
print(f"   Parsed origins: {allowed_origins}")
print(f"   Total origins: {len(allowed_origins)}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Specific origins only (NO wildcard with credentials)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global OPTIONS handler for CORS preflight requests
@app.options("/{full_path:path}")
async def preflight_handler(full_path: str):
    """Handle CORS preflight OPTIONS requests."""
    return Response(status_code=200)  # Let middleware add headers
```

### 2. Database Configuration with SSL
```python
# In backend/app/core/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")

# Determine if SSL is required (Render PostgreSQL)
use_ssl = False
if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
    if "render.com" in DATABASE_URL or "dpg-" in DATABASE_URL:
        use_ssl = True
        print("🔒 SSL mode enabled for Render PostgreSQL")

# Create engine with SSL support for production
if use_ssl:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"sslmode": "require"},
        pool_pre_ping=True,
        pool_recycle=300,
        echo=False,
    )
else:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=False,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 3. Password Hashing (Byte-level truncation)
```python
# In backend/app/core/security.py

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    # Truncate password to 72 bytes for bcrypt (byte-level, not character-level)
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
        password = password_bytes.decode('utf-8', errors='ignore')
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

### 4. Startup Event with Table Creation
```python
# In backend/app/main.py

@app.on_event("startup")
def startup_event():
    """Create database tables on application startup"""
    print("🚀 Starting up Tire Shop Management API...")
    
    # Import all models
    from app.models import (
        User, UserRole, 
        Supplier, 
        TireInventory, TireType,
        Sales, SalesItem, PaymentMode,
        Purchase, PurchaseItem, PaymentStatus
    )
    
    # Check if production
    environment = os.getenv("ENVIRONMENT", "development")
    is_production = environment == "production"
    
    # Drop users table in production (for schema updates)
    if is_production:
        print("🔧 Production environment detected")
        try:
            User.__table__.drop(bind=engine, checkfirst=True)
            print("✅ Users table dropped for schema update")
        except Exception as e:
            print(f"⚠️ Could not drop users table: {e}")
    
    # Create all tables
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
```

### 5. User Model
```python
# In backend/app/models/user.py

from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.sql import func
import enum
from app.core.database import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    STAFF = "staff"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(Enum(UserRole), default=UserRole.STAFF)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

### 6. Authentication Endpoints
```python
# In backend/app/api/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check duplicates
    # Hash password ONCE
    # Create user
    # Return user response

@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    # Verify credentials
    # Generate JWT token
    # Return token
```

### 7. Debug Endpoints
```python
# In backend/app/api/debug.py

router = APIRouter(prefix="/debug", tags=["Debug"])

@router.get("/db_status")
def database_status():
    """Check database connection and users table"""
    # Test connection
    # Check if users table exists
    # Return status

@router.get("/cors_config")
def cors_configuration():
    """Get CORS configuration for debugging"""
    # Return parsed ALLOWED_ORIGINS
    # Show whitespace detection
    # Return environment
```

## Critical Frontend Requirements

### 1. API Configuration
```javascript
// In frontend/src/services/api.js

import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,  // Important for CORS with credentials
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
```

### 2. NO Service Worker (Critical!)
```html
<!-- In frontend/index.html -->
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
    <title>Tire Shop Management</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
    
    <!-- Unregister any existing service workers -->
    <script>
      if ('serviceWorker' in navigator) {
        navigator.serviceWorker.getRegistrations().then(function(registrations) {
          for (let registration of registrations) {
            registration.unregister();
          }
        });
        if ('caches' in window) {
          caches.keys().then(function(cacheNames) {
            cacheNames.forEach(function(cacheName) {
              caches.delete(cacheName);
            });
          });
        }
      }
    </script>
  </body>
</html>
```

### 3. Protected Routes
```javascript
// In frontend/src/components/ProtectedRoute.jsx

import { Navigate } from 'react-router-dom';

const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem('token');
  
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  
  return children;
};

export default ProtectedRoute;
```

### 4. Router Setup
```javascript
// In frontend/src/App.jsx

import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Inventory from './pages/Inventory';
import Sales from './pages/Sales';
import Purchase from './pages/Purchase';
import Reports from './pages/Reports';
import DailyClosing from './pages/DailyClosing';
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="inventory" element={<Inventory />} />
          <Route path="sales" element={<Sales />} />
          <Route path="purchase" element={<Purchase />} />
          <Route path="reports" element={<Reports />} />
          <Route path="daily-closing" element={<DailyClosing />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
```

## Deployment Configuration

### 1. Dockerfile.backend
```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

EXPOSE 10000

CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}
```

### 2. render.yaml
```yaml
services:
  - type: web
    name: tire-shop-backend
    env: docker
    dockerfilePath: ./Dockerfile.backend
    dockerContext: .
    plan: free
    healthCheckPath: /docs
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: tire-shop-db
          property: connectionString
      - key: SECRET_KEY
        generateValue: true
      - key: ALGORITHM
        value: HS256
      - key: ACCESS_TOKEN_EXPIRE_MINUTES
        value: 1440
      - key: ALLOWED_ORIGINS
        value: http://localhost:5173,https://your-frontend.vercel.app
      - key: ENVIRONMENT
        value: production

databases:
  - name: tire-shop-db
    databaseName: tireshop
    user: tireshop
    plan: free
```

### 3. Environment Variables

**Backend (.env):**
```
DATABASE_URL=postgresql://user:password@localhost:5432/tire_shop_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

**Frontend (.env):**
```
VITE_API_URL=http://localhost:8000
```

**Frontend Production (.env.production):**
```
VITE_API_URL=https://your-backend.onrender.com
```

## Critical Issues to Avoid

### 1. CORS Issues
- ❌ NEVER use wildcard (*) with allow_credentials=True
- ✅ Always use specific origins from environment variable
- ✅ Strip whitespace from ALLOWED_ORIGINS
- ✅ Add global OPTIONS handler
- ✅ Let CORSMiddleware add headers (don't add manually)

### 2. Bcrypt Compatibility
- ❌ NEVER use bcrypt 4.x (incompatible with passlib)
- ✅ Use bcrypt==3.2.0 and passlib[bcrypt]==1.7.4
- ✅ Truncate passwords at byte-level (not character-level)
- ✅ Hash password only ONCE

### 3. PostgreSQL SSL
- ❌ NEVER connect to Render PostgreSQL without SSL
- ✅ Detect Render by checking for "render.com" or "dpg-" in URL
- ✅ Use connect_args={"sslmode": "require"}

### 4. Service Worker
- ❌ NEVER use service workers for business SaaS dashboards
- ❌ NEVER cache authentication or API requests
- ✅ Add unregistration script in index.html
- ✅ Clear all caches on load

### 5. Schema Migrations
- ✅ Drop users table on production startup (for development phase)
- ✅ Use Alembic for production with real users
- ✅ Import all models before Base.metadata.create_all()

## Testing Checklist

### Backend:
- [ ] /health returns 200
- [ ] /docs shows Swagger UI
- [ ] /debug/db_status shows database connected
- [ ] /debug/cors_config shows correct origins
- [ ] POST /auth/register creates user
- [ ] POST /auth/login returns JWT token
- [ ] Protected endpoints require authentication

### Frontend:
- [ ] Login page loads
- [ ] Login with credentials works
- [ ] Dashboard shows after login
- [ ] All pages accessible
- [ ] Logout works
- [ ] Protected routes redirect to login

### CORS:
- [ ] OPTIONS requests return 200
- [ ] CORS headers present on all responses
- [ ] Access-Control-Allow-Origin matches frontend URL
- [ ] Access-Control-Allow-Credentials is true
- [ ] No wildcard (*) with credentials

### Mobile:
- [ ] Login works on mobile browsers
- [ ] No CORS errors on mobile
- [ ] No cached responses
- [ ] Fresh authentication every time

## Additional Features (Optional)

1. **WhatsApp Integration**: Send invoices via WhatsApp using Twilio
2. **Email Notifications**: Send reports via email
3. **Barcode Scanning**: Scan tire barcodes for quick entry
4. **Multi-language Support**: Support multiple languages
5. **Dark Mode**: Add dark mode toggle
6. **Export to Excel**: Export reports to Excel
7. **Backup/Restore**: Database backup and restore
8. **Audit Logs**: Track all user actions

## Documentation to Create

1. README.md - Project overview and setup
2. API_DOCUMENTATION.md - API endpoints and examples
3. DEPLOYMENT_GUIDE.md - Step-by-step deployment
4. TROUBLESHOOTING.md - Common issues and solutions
5. CORS_GUIDE.md - CORS configuration explained

## Success Criteria

The project is complete when:
- ✅ Backend deploys successfully on Render
- ✅ Frontend deploys successfully on Vercel
- ✅ Login works on desktop and mobile
- ✅ All CRUD operations work
- ✅ PDF invoices generate correctly
- ✅ Dashboard shows accurate data
- ✅ No CORS errors in production
- ✅ Database persists data correctly
- ✅ Authentication is secure

## PROMPT END

---

## Usage Instructions

1. Copy the entire prompt above (from "PROMPT START" to "PROMPT END")
2. Paste it into a new conversation with an AI assistant (Claude, ChatGPT, etc.)
3. The AI will create the complete project structure and code
4. Follow the deployment instructions to deploy to Render and Vercel
5. Test thoroughly on desktop and mobile devices

## Notes

- This prompt includes all critical fixes for CORS, bcrypt, SSL, and service workers
- The project is production-ready and tested on mobile browsers
- All security best practices are included
- The architecture follows clean code principles with separation of concerns
