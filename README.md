# 🚗 Tire Shop Inventory Management System

A modern, full-stack inventory management system designed specifically for tire retail shops. Built with FastAPI (Python) backend and React (Vite) frontend.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![React](https://img.shields.io/badge/react-18.2-blue.svg)
![FastAPI](https://img.shields.io/badge/fastapi-0.109-green.svg)

---

## ✨ Features

### 🛒 Sales & Billing
- Multi-item billing interface
- Discount system (Flat ₹ and Percentage %)
- Real-time calculations (Subtotal → Discount → Total)
- Multiple payment modes (Cash, UPI, Card)
- Invoice generation (PDF)
- WhatsApp invoice sharing
- Stock auto-reduction

### 📦 Inventory Management
- Complete tire inventory tracking
- Brand, size, and type categorization
- Stock level monitoring
- Low stock alerts
- Purchase price and selling price tracking
- Tubeless/Tube type support

### 🛍️ Purchase Management
- Supplier management
- Purchase order tracking
- Payment status monitoring
- Purchase history

### 📊 Reports & Analytics
- Sales trends and analytics
- Profit calculations
- Revenue tracking
- Best-selling items analysis
- Daily closing reports

### 🔐 Security
- JWT token authentication
- Token expiry validation
- Secure route protection
- Password hashing (bcrypt)
- Role-based access control

### 📱 Mobile Responsive
- Touch-friendly UI (44px touch targets)
- Mobile-optimized layouts
- Bottom navigation for mobile
- No horizontal scroll
- Responsive design for all devices

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+
- PostgreSQL 14+

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/tire-shop-inventory.git
cd tire-shop-inventory
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your database credentials

# Run migrations (if using Alembic)
# alembic upgrade head

# Start backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 4. Access Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 5. Default Login
```
Username: admin
Password: admin123
```

---

## 📦 Installation Scripts

### Windows
```bash
# Start both servers
start-dev.bat

# Start backend only
start-backend.bat

# Start frontend only
start-frontend.bat

# Seed database with dummy data
seed-database.bat
```

### Linux/Mac
```bash
# Make scripts executable
chmod +x *.sh

# Start both servers
./start-dev.sh

# Seed database
./seed-database.sh
```

---

## 🗄️ Database Setup

### PostgreSQL Setup
1. Install PostgreSQL 14+
2. Create database:
```sql
CREATE DATABASE tire_shop_db;
CREATE USER tire_shop_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE tire_shop_db TO tire_shop_user;
```

3. Update `.env` file:
```env
DATABASE_URL=postgresql://tire_shop_user:your_password@localhost:5432/tire_shop_db
SECRET_KEY=your-secret-key-here
```

### Seed Dummy Data
```bash
cd backend
python seed_data.py
```

This will add:
- 20 tire inventory items
- 10 purchase records
- 15 sales records

---

## 📁 Project Structure

```
tire-shop-inventory/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Core functionality (auth, database)
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   └── services/     # Business logic
│   ├── .env.example      # Environment variables template
│   ├── requirements.txt  # Python dependencies
│   └── seed_data.py      # Database seeding script
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API services
│   │   ├── styles/       # CSS styles
│   │   └── utils/        # Utility functions
│   ├── package.json      # Node dependencies
│   └── vite.config.js    # Vite configuration
├── documentation/        # Project documentation
├── .gitignore
├── README.md
└── LICENSE
```

---

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI 0.109
- **Database**: PostgreSQL 14+
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt
- **Validation**: Pydantic v2
- **CORS**: FastAPI CORS middleware

### Frontend
- **Framework**: React 18.2
- **Build Tool**: Vite 5.0
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **Notifications**: React Hot Toast
- **Styling**: Custom CSS (Mobile-first)

### Database Schema
- Users (Authentication)
- Tire Inventory
- Sales & Sales Items
- Purchases
- Daily Closing Reports

---

## 🔧 Configuration

### Backend Configuration (.env)
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/tire_shop_db

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Frontend Configuration (vite.config.js)
```javascript
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    host: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
```

---

## 📚 API Documentation

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration

### Inventory
- `GET /inventory/all` - Get all inventory
- `POST /inventory/` - Add new tire
- `PUT /inventory/{id}` - Update tire
- `DELETE /inventory/{id}` - Delete tire

### Sales
- `GET /sales/history` - Get sales history
- `POST /sales/` - Create new sale
- `GET /sales/{id}` - Get sale details

### Purchase
- `GET /purchase/history` - Get purchase history
- `POST /purchase/` - Create new purchase

### Reports
- `GET /reports/sales-summary` - Sales summary
- `GET /reports/profit-analysis` - Profit analysis

Full API documentation available at: http://localhost:8000/docs

---

## 🧪 Testing

### Run Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Test with Dummy Data
1. Run seed script: `seed-database.bat`
2. Login with: `admin` / `admin123`
3. Test all features with realistic data

---

## 🚢 Deployment

### Backend Deployment (Heroku/Railway/Render)

1. **Prepare for deployment**:
```bash
# Ensure requirements.txt is up to date
pip freeze > requirements.txt
```

2. **Create Procfile**:
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

3. **Set environment variables** on your hosting platform

4. **Deploy**:
```bash
git push heroku main
```

### Frontend Deployment (Vercel/Netlify)

1. **Build for production**:
```bash
cd frontend
npm run build
```

2. **Deploy to Vercel**:
```bash
vercel --prod
```

3. **Update API URL** in production environment

---

## 📖 Documentation

- [Getting Started](documentation/01_GETTING_STARTED.md)
- [Critical Fixes Implemented](CRITICAL_FIXES_IMPLEMENTED.md)
- [Quick Test Guide](QUICK_TEST_GUIDE.md)
- [Seed Data Guide](SEED_DATA_GUIDE.md)
- [PostgreSQL Installation](INSTALL_POSTGRESQL.md)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Your Name** - *Initial work* - [YourGitHub](https://github.com/yourusername)

---

## 🙏 Acknowledgments

- FastAPI for the amazing backend framework
- React team for the frontend library
- PostgreSQL for the robust database
- All contributors and testers

---

## 📞 Support

For support, email your-email@example.com or open an issue on GitHub.

---

## 🗺️ Roadmap

- [ ] Multi-user support with roles
- [ ] Advanced reporting with charts
- [ ] Email notifications
- [ ] SMS integration
- [ ] Barcode scanning
- [ ] Multi-branch support
- [ ] Mobile app (React Native)
- [ ] Inventory forecasting
- [ ] Customer loyalty program
- [ ] Integration with accounting software

---

## 📊 Project Status

**Status**: ✅ Production Ready

**Version**: 2.0.0

**Last Updated**: February 2026

---

## 🎯 Key Features Implemented

✅ Multi-item billing with discount  
✅ JWT authentication with token validation  
✅ Mobile-responsive UI  
✅ Real-time stock management  
✅ Invoice generation  
✅ Sales analytics  
✅ Purchase tracking  
✅ Daily closing reports  

---

**Made with ❤️ for tire shop owners**
