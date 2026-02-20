# 📖 Upgrade Guide & Quick Reference - v2.0

## Table of Contents
1. [Version 2.0 Upgrade](#version-20-upgrade)
2. [What's New](#whats-new)
3. [Quick Reference](#quick-reference)
4. [Sample Data](#sample-data)
5. [Common Tasks](#common-tasks)
6. [FAQ](#faq)

---

## Version 2.0 Upgrade

### 🎉 Major Features Added

**From v1.0 to v2.0 - 5 Enterprise Features:**

1. **🛒 Purchase Management** - Track all tire purchases
2. **📄 GST Invoice PDF** - Professional invoice generation
3. **💎 Profit Calculation** - Automatic profit tracking
4. **📋 Daily Closing Report** - End-of-day summaries
5. **📱 WhatsApp Integration** - Send invoices instantly

### Upgrade Steps

#### 1. Update Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**New packages:**
- `reportlab==4.0.9` - PDF generation
- `twilio==8.11.1` - WhatsApp integration

#### 2. Update Environment Variables

Add to `backend/.env` (optional for WhatsApp):
```env
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
```

#### 3. Database Migration

No manual migration needed! The new `purchases` table will be created automatically on first run.

#### 4. Restart Services

```bash
# Backend
cd backend
uvicorn app.main:app --reload

# Frontend (no changes needed)
cd frontend
npm run dev
```

### Backward Compatibility

✅ **All v1.0 features work unchanged**
✅ **Existing data preserved**
✅ **No breaking changes**
✅ **Seamless upgrade**

---

## What's New

### New Pages

#### 1. Purchase Page
- **Location:** Main menu → Purchase
- **Purpose:** Record tire purchases from suppliers
- **Features:**
  - Add purchase entries
  - Track supplier information
  - Monitor payment status
  - Auto increase inventory
  - View purchase history

#### 2. Daily Closing Page
- **Location:** Main menu → Daily Closing
- **Purpose:** Generate end-of-day business reports
- **Features:**
  - Total sales & profit
  - Payment breakdown
  - Items sold count
  - Transaction statistics
  - Historical reports

### Enhanced Pages

#### Dashboard
- **New:** Today's Profit card (green)
- **New:** Monthly Profit card (blue)
- **Updated:** 5 cards instead of 4

#### Sales Page
- **New:** 📄 PDF button - Download invoice
- **New:** 📱 WhatsApp button - Send invoice
- **Enhanced:** Action buttons for each sale

### New API Endpoints

**Total: 21 endpoints** (was 13)

**Purchase Management (5):**
- POST /purchase/add
- GET /purchase/all
- GET /purchase/{id}
- PUT /purchase/update/{id}
- DELETE /purchase/delete/{id}

**Invoice (2):**
- GET /invoice/generate/{sale_id}
- POST /invoice/send-whatsapp/{sale_id}

**Profit (3):**
- GET /profit/summary
- GET /profit/details
- GET /profit/daily-closing

---

## Quick Reference

### Common Commands

#### Start Application
```bash
# Backend
cd backend
venv\Scripts\activate  # Windows
uvicorn app.main:app --reload

# Frontend
cd frontend
npm run dev
```

#### Database Operations
```bash
# Connect
psql -U postgres -d tire_shop_db

# Backup
pg_dump -U postgres tire_shop_db > backup.sql

# Restore
psql -U postgres tire_shop_db < backup.sql

# View tables
\dt

# Exit
\q
```

#### Check Status
```bash
# Backend health
curl http://localhost:8000/health

# View API docs
# Open: http://localhost:8000/docs

# Frontend
# Open: http://localhost:3000
```

### Keyboard Shortcuts

**In Application:**
- `Ctrl + K` - Quick search (if implemented)
- `Esc` - Close modals
- `Enter` - Submit forms

**In Browser:**
- `F12` - Open developer tools
- `Ctrl + Shift + R` - Hard refresh
- `Ctrl + +/-` - Zoom in/out

### Default Credentials

```
Username: admin
Password: admin123
```

⚠️ **Change in production!**

---

## Sample Data

### Sample Tire Inventory

```json
{
  "brand": "MRF",
  "tire_size": "195/65R15",
  "tire_type": "tubeless",
  "quantity": 25,
  "purchase_price": 3500,
  "selling_price": 4500,
  "purchase_date": "2024-02-19"
}
```

```json
{
  "brand": "Apollo",
  "tire_size": "185/70R14",
  "tire_type": "tube",
  "quantity": 15,
  "purchase_price": 2800,
  "selling_price": 3500,
  "purchase_date": "2024-02-19"
}
```

```json
{
  "brand": "Bridgestone",
  "tire_size": "205/55R16",
  "tire_type": "tubeless",
  "quantity": 20,
  "purchase_price": 4200,
  "selling_price": 5500,
  "purchase_date": "2024-02-19"
}
```

### Sample Purchase

```json
{
  "supplier_name": "ABC Tires Pvt Ltd",
  "tire_id": 1,
  "quantity": 10,
  "purchase_price": 3500,
  "purchase_date": "2024-02-19",
  "payment_status": "paid"
}
```

### Sample Sale

```json
{
  "customer_name": "John Doe",
  "customer_mobile": "9876543210",
  "payment_mode": "cash",
  "items": [
    {
      "tire_id": 1,
      "quantity": 2
    },
    {
      "tire_id": 2,
      "quantity": 1
    }
  ]
}
```

---

## Common Tasks

### Task 1: Add New Tire to Inventory

```
1. Login to application
2. Go to "Inventory" page
3. Click "+ Add New Tire"
4. Fill in details:
   - Brand: MRF
   - Size: 195/65R15
   - Type: Tubeless
   - Quantity: 25
   - Purchase Price: 3500
   - Selling Price: 4500
   - Date: Today
5. Click "Add"
6. ✅ Tire added to inventory
```

### Task 2: Record a Purchase

```
1. Go to "Purchase" page
2. Click "+ Add Purchase"
3. Fill in details:
   - Supplier: ABC Tires
   - Select Tire: MRF 195/65R15
   - Quantity: 10
   - Purchase Price: 3500
   - Payment Status: Paid
   - Date: Today
4. Click "Add Purchase"
5. ✅ Inventory automatically increases by 10
```

### Task 3: Create a Sale

```
1. Go to "Sales" page
2. Click "+ New Sale"
3. Enter customer details:
   - Name: John Doe
   - Mobile: 9876543210
   - Payment: Cash
4. Add items:
   - Select tire: MRF 195/65R15
   - Quantity: 2
   - Click "Add"
5. Review total
6. Click "Create Sale"
7. ✅ Sale created, stock reduced
```

### Task 4: Download Invoice

```
1. Go to "Sales" page
2. Find the sale in history
3. Click "📄 PDF" button
4. ✅ Invoice downloads as PDF
```

### Task 5: Send Invoice via WhatsApp

```
1. Go to "Sales" page
2. Find the sale
3. Click "📱 WhatsApp" button
4. ✅ Invoice sent to customer's WhatsApp
```

### Task 6: Generate Daily Closing Report

```
1. Go to "Daily Closing" page
2. Select date (defaults to today)
3. Click "Generate Report"
4. Review:
   - Total Sales
   - Total Profit
   - Payment Breakdown
   - Items Sold
5. Click "Print" if needed
6. ✅ Report generated
```

### Task 7: Check Profit

```
1. Go to "Dashboard"
2. View profit cards:
   - Today's Profit (green card)
   - Monthly Profit (blue card)
3. ✅ Profit visible at a glance
```

### Task 8: Search Inventory

```
1. Go to "Inventory" page
2. Use search box at top
3. Type brand or size (e.g., "MRF" or "195")
4. ✅ Results filter in real-time
```

### Task 9: Update Stock

```
1. Go to "Inventory" page
2. Find the tire
3. Click "Edit"
4. Update quantity or prices
5. Click "Update"
6. ✅ Stock updated
```

### Task 10: View Low Stock Items

```
1. Go to "Dashboard"
2. Check "Low Stock Alert" card
3. Scroll down to "Low Stock Items" section
4. ✅ See all items with quantity < 5
```

---

## FAQ

### General Questions

**Q: What's the difference between v1.0 and v2.0?**
A: v2.0 adds 5 major features: Purchase Management, GST Invoice PDF, Profit Calculation, Daily Closing Reports, and WhatsApp Integration.

**Q: Will my existing data be lost?**
A: No! All existing data is preserved. The upgrade is backward compatible.

**Q: Do I need to configure WhatsApp?**
A: No, it's optional. You can still download and manually share invoices without WhatsApp.

**Q: How accurate is profit calculation?**
A: 100% accurate based on purchase and selling prices in the system.

**Q: Can I customize the invoice?**
A: Yes! Edit `backend/app/services/invoice_service.py` to customize shop details and layout.

### Technical Questions

**Q: What database does it use?**
A: PostgreSQL 13 or higher.

**Q: Can I use MySQL instead?**
A: Not recommended. The system is optimized for PostgreSQL.

**Q: How do I change the admin password?**
A: Currently, you need to update it directly in the database. User management UI coming in future version.

**Q: Can I run this on Windows?**
A: Yes! The setup instructions include Windows commands.

**Q: What's the minimum server requirement?**
A: 2GB RAM, 2 CPU cores, 20GB storage for small shops. Scale up for larger operations.

**Q: How many concurrent users can it handle?**
A: With proper configuration, 50-100 concurrent users easily.

### Feature Questions

**Q: Can I export reports to Excel?**
A: Not built-in yet, but you can copy data from reports. Excel export coming in future version.

**Q: Does it support multiple shops?**
A: Not currently. It's designed for single shop operation.

**Q: Can I add custom fields?**
A: Yes, but requires code modification. Contact for customization.

**Q: Is there a mobile app?**
A: The web interface is mobile-responsive. Native app coming in future.

**Q: Can I integrate with accounting software?**
A: Not built-in, but possible through API integration.

### Troubleshooting

**Q: Invoice PDF not generating?**
A: Check if `invoices/` folder exists in backend directory.

**Q: WhatsApp not working?**
A: Verify Twilio credentials in `.env` file and check account balance.

**Q: Profit showing zero?**
A: Ensure purchase prices are recorded in inventory before making sales.

**Q: Low stock alerts not showing?**
A: Check if any items have quantity < 5.

**Q: Can't login?**
A: Use default credentials: admin/admin123. Check if backend is running.

---

## Business Workflows

### Daily Operations

**Morning:**
1. Check Dashboard for yesterday's performance
2. Review low stock items
3. Plan purchases if needed

**During Day:**
1. Record purchases as they arrive
2. Create sales as customers buy
3. Download/send invoices
4. Monitor stock levels

**Evening:**
1. Generate daily closing report
2. Match cash with report
3. Review profit for the day
4. Plan for tomorrow

### Weekly Operations

1. Review weekly sales trends
2. Analyze profit margins
3. Identify best-selling items
4. Check pending payments
5. Plan inventory purchases

### Monthly Operations

1. Generate monthly sales report
2. Calculate monthly profit
3. Review inventory turnover
4. Analyze payment modes
5. Plan for next month

---

## Formulas & Calculations

### Profit Calculation
```
Cost = Purchase Price × Quantity
Revenue = Selling Price × Quantity
Profit = Revenue - Cost
Profit Margin = (Profit / Revenue) × 100
```

### GST Calculation
```
Subtotal = Sum of all items
CGST = Subtotal × 9%
SGST = Subtotal × 9%
Total GST = CGST + SGST
Grand Total = Subtotal + Total GST
```

### Inventory Value
```
Item Value = Selling Price × Quantity
Total Inventory Value = Sum of all item values
```

### Average Transaction
```
Average = Total Sales / Number of Transactions
```

---

## Project Structure

```
tire-shop-app/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints (21 endpoints)
│   │   ├── core/         # Config, database, security
│   │   ├── models/       # Database models (6 tables)
│   │   ├── repositories/ # Data access layer
│   │   ├── schemas/      # Request/response schemas
│   │   ├── services/     # Business logic (8 services)
│   │   └── main.py       # Application entry
│   ├── alembic/          # Database migrations
│   ├── invoices/         # Generated PDF invoices
│   ├── init_db.py        # Database initialization
│   └── requirements.txt  # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/   # Reusable components
│   │   ├── pages/        # 7 pages
│   │   ├── services/     # API integration
│   │   └── utils/        # Helper functions
│   └── package.json      # Node dependencies
│
└── documentation/        # This folder
    ├── 01_GETTING_STARTED.md
    ├── 02_FEATURES_AND_API.md
    ├── 03_DEPLOYMENT_GUIDE.md
    └── 04_UPGRADE_AND_REFERENCE.md
```

---

## Version History

### v2.0.0 (Current)
- ✅ Purchase Management
- ✅ GST Invoice PDF Generation
- ✅ Profit Calculation Engine
- ✅ Daily Closing Reports
- ✅ WhatsApp Integration
- ✅ Enhanced Dashboard
- ✅ 21 API endpoints

### v1.0.0
- ✅ JWT Authentication
- ✅ Inventory Management
- ✅ Sales & Billing
- ✅ Dashboard Analytics
- ✅ Reports Generation
- ✅ 13 API endpoints

---

## Support & Resources

### Documentation
- **Getting Started:** 01_GETTING_STARTED.md
- **Features & API:** 02_FEATURES_AND_API.md
- **Deployment:** 03_DEPLOYMENT_GUIDE.md
- **This File:** 04_UPGRADE_AND_REFERENCE.md

### Online Resources
- **API Docs:** http://localhost:8000/docs
- **FastAPI:** https://fastapi.tiangolo.com/
- **React:** https://react.dev/
- **Tailwind CSS:** https://tailwindcss.com/
- **PostgreSQL:** https://www.postgresql.org/docs/

### Getting Help
1. Check documentation files
2. Review API documentation
3. Check console logs (F12)
4. Verify all services running
5. Review error messages

---

## Tips & Best Practices

### For Vendors

1. **Record purchases immediately** - Don't wait
2. **Generate invoices for all sales** - Professional image
3. **Check daily closing every evening** - Stay on top
4. **Review profit margins regularly** - Optimize pricing
5. **Keep low stock alerts monitored** - Avoid stock-outs

### For Developers

1. **Use virtual environment** - Isolate dependencies
2. **Keep .env secure** - Never commit to git
3. **Backup database regularly** - Prevent data loss
4. **Monitor logs** - Catch issues early
5. **Test before deploying** - Avoid production issues

### For System Administrators

1. **Enable HTTPS** - Security first
2. **Configure firewall** - Restrict access
3. **Set up monitoring** - Know system health
4. **Automate backups** - Daily at minimum
5. **Keep system updated** - Security patches

---

## Keyboard Shortcuts & Tips

### Browser
- `Ctrl + Shift + R` - Hard refresh (clear cache)
- `F12` - Developer tools
- `Ctrl + F` - Find on page

### Application
- `Esc` - Close modals
- `Enter` - Submit forms
- `Tab` - Navigate form fields

### Development
- `Ctrl + C` - Stop server
- `Ctrl + Z` - Undo
- `Ctrl + Shift + P` - Command palette (VS Code)

---

## Glossary

**API** - Application Programming Interface
**CGST** - Central Goods and Services Tax
**CRUD** - Create, Read, Update, Delete
**GST** - Goods and Services Tax
**GSTIN** - GST Identification Number
**JWT** - JSON Web Token
**ORM** - Object-Relational Mapping
**PDF** - Portable Document Format
**REST** - Representational State Transfer
**SGST** - State Goods and Services Tax
**SQL** - Structured Query Language
**SSL** - Secure Sockets Layer
**UPI** - Unified Payments Interface

---

## Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Can't login | Check backend is running, use admin/admin123 |
| Database error | Verify PostgreSQL running, check credentials |
| Port in use | Kill process or use different port |
| Module not found | Run pip install -r requirements.txt |
| Invoice not generating | Check invoices/ folder exists |
| WhatsApp not working | Verify Twilio credentials in .env |
| Profit showing zero | Record purchase prices before sales |
| Low stock not showing | Check items with quantity < 5 |

---

**Complete reference guide for Tire Shop Management System v2.0!** 📖

**You're all set to manage your business efficiently!** 🚀
