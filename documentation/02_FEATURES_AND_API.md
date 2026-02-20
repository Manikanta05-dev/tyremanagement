# 📚 Features & API Documentation - v2.0

## Table of Contents
1. [Complete Feature List](#complete-feature-list)
2. [API Endpoints](#api-endpoints)
3. [Database Schema](#database-schema)
4. [Business Workflows](#business-workflows)
5. [Feature Details](#feature-details)

---

## Complete Feature List

### 🔐 Authentication & Security
- ✅ JWT token-based authentication
- ✅ Bcrypt password hashing
- ✅ Role-based access (Admin/Staff)
- ✅ Protected API endpoints
- ✅ Protected frontend routes
- ✅ Token expiration handling
- ✅ Secure session management

### 📦 Inventory Management
- ✅ Add/Edit/Delete tire inventory
- ✅ Track brand, size, type (Tube/Tubeless)
- ✅ Monitor stock levels
- ✅ Purchase & selling price tracking
- ✅ Supplier information
- ✅ Search & filter functionality
- ✅ Low stock alerts (< 5 quantity)
- ✅ Automatic stock updates on sales/purchases

### 🛒 Purchase Management (NEW v2.0)
- ✅ Record purchase entries
- ✅ Track supplier information
- ✅ Monitor purchase quantities & prices
- ✅ Payment status (Paid/Pending)
- ✅ Purchase date tracking
- ✅ Auto increase inventory stock
- ✅ Complete purchase history
- ✅ Update/Delete purchase records

### 💰 Sales & Billing
- ✅ Create multi-item sales bills
- ✅ Customer information capture
- ✅ Multiple payment modes (Cash/UPI/Card)
- ✅ Auto-generated invoice IDs (INV{YYYYMMDD}{0001})
- ✅ Real-time total calculation
- ✅ Stock validation before sale
- ✅ Complete sales history
- ✅ Prevent overselling

### 📄 GST Invoice Generation (NEW v2.0)
- ✅ Professional PDF invoice generation
- ✅ GST-compliant format
- ✅ Shop details with GSTIN
- ✅ CGST (9%) + SGST (9%) calculation
- ✅ Grand total with taxes
- ✅ Downloadable PDF format
- ✅ Professional styling (A4 layout)

### 💎 Profit Calculation (NEW v2.0)
- ✅ Automatic profit per sale
- ✅ Daily profit tracking
- ✅ Monthly profit tracking
- ✅ Total profit overview
- ✅ Profit margin calculation
- ✅ Cost vs revenue analysis
- ✅ Dashboard profit cards

### 📋 Daily Closing Report (NEW v2.0)
- ✅ End-of-day summary
- ✅ Total sales & profit
- ✅ Payment mode breakdown (Cash/UPI/Card)
- ✅ Total items sold count
- ✅ Transaction count
- ✅ Average transaction value
- ✅ Profit margin percentage
- ✅ Historical reports

### 📱 WhatsApp Integration (NEW v2.0)
- ✅ Send invoice via WhatsApp
- ✅ Twilio API integration
- ✅ Automatic mobile formatting
- ✅ PDF attachment support
- ✅ One-click sending
- ✅ Success/failure notifications

### 📊 Dashboard Analytics
- ✅ Today's sales & profit
- ✅ Monthly revenue & profit
- ✅ Low stock count & alerts
- ✅ Total inventory value
- ✅ Sales trend chart (7 days)
- ✅ Low stock items list
- ✅ Real-time data updates

### 📈 Reports
- ✅ Sales report with date filter
- ✅ Inventory report
- ✅ Low stock identification
- ✅ Purchase reports
- ✅ Profit reports
- ✅ Daily closing reports
- ✅ Export-ready format

---

## API Endpoints

### Base URL
```
http://localhost:8000
```

### Authentication Required
All endpoints except `/auth/login` require JWT token in header:
```
Authorization: Bearer <your_token>
```

---

### 🔐 Authentication (1 endpoint)

#### POST /auth/login
Login to get access token.

**Request:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@tireshop.com",
    "full_name": "Admin User",
    "role": "admin"
  }
}
```

---

### 📦 Inventory Management (5 endpoints)

#### GET /inventory/all
Get all inventory items with optional search and pagination.

**Query Parameters:**
- `skip` (optional): Number to skip (default: 0)
- `limit` (optional): Max items (default: 100)
- `search` (optional): Search by brand or size

**Response:**
```json
[
  {
    "id": 1,
    "brand": "MRF",
    "tire_size": "195/65R15",
    "tire_type": "tubeless",
    "quantity": 25,
    "purchase_price": 3500.00,
    "selling_price": 4500.00,
    "supplier_id": null,
    "supplier_name": null,
    "purchase_date": "2024-01-15"
  }
]
```

#### GET /inventory/{id}
Get specific inventory item.

#### POST /inventory/add
Add new tire to inventory.

**Request:**
```json
{
  "brand": "MRF",
  "tire_size": "195/65R15",
  "tire_type": "tubeless",
  "quantity": 25,
  "purchase_price": 3500.00,
  "selling_price": 4500.00,
  "supplier_id": null,
  "purchase_date": "2024-01-15"
}
```

#### PUT /inventory/update/{id}
Update existing inventory item.

#### DELETE /inventory/delete/{id}
Delete inventory item.

---

### 🛒 Purchase Management (5 endpoints - NEW)

#### POST /purchase/add
Add new purchase entry.

**Request:**
```json
{
  "supplier_name": "ABC Tires",
  "tire_id": 1,
  "quantity": 10,
  "purchase_price": 3500.00,
  "purchase_date": "2024-02-19",
  "payment_status": "paid"
}
```

**Response:**
```json
{
  "id": 1,
  "supplier_name": "ABC Tires",
  "tire_id": 1,
  "quantity": 10,
  "purchase_price": 3500.00,
  "total_amount": 35000.00,
  "purchase_date": "2024-02-19",
  "payment_status": "paid",
  "tire_brand": "MRF",
  "tire_size": "195/65R15"
}
```

#### GET /purchase/all
Get all purchases with pagination.

#### GET /purchase/{id}
Get specific purchase.

#### PUT /purchase/update/{id}
Update purchase record.

#### DELETE /purchase/delete/{id}
Delete purchase record.

---

### 💰 Sales Management (3 endpoints)

#### POST /sales/create
Create new sale.

**Request:**
```json
{
  "customer_name": "John Doe",
  "customer_mobile": "9876543210",
  "payment_mode": "cash",
  "items": [
    {
      "tire_id": 1,
      "quantity": 2
    }
  ]
}
```

**Response:**
```json
{
  "id": 1,
  "invoice_id": "INV202402190001",
  "customer_name": "John Doe",
  "customer_mobile": "9876543210",
  "total_amount": 9000.00,
  "payment_mode": "cash",
  "sale_date": "2024-02-19T10:30:00",
  "items": [
    {
      "id": 1,
      "tire_id": 1,
      "quantity": 2,
      "unit_price": 4500.00,
      "total_price": 9000.00,
      "tire_brand": "MRF",
      "tire_size": "195/65R15"
    }
  ]
}
```

#### GET /sales/history
Get sales history with pagination.

**Query Parameters:**
- `skip` (optional): Number to skip
- `limit` (optional): Max items

#### GET /sales/{id}
Get specific sale details.

---

### 📄 Invoice Generation (2 endpoints - NEW)

#### GET /invoice/generate/{sale_id}
Generate and download GST invoice PDF.

**Response:** PDF file download

**Invoice Contains:**
- Shop details with GSTIN
- Customer information
- Itemized billing
- CGST (9%) + SGST (9%)
- Grand total

#### POST /invoice/send-whatsapp/{sale_id}
Send invoice via WhatsApp.

**Query Parameters:**
- `customer_mobile`: Customer's mobile number

**Response:**
```json
{
  "success": true,
  "message": "Invoice sent successfully via WhatsApp",
  "message_sid": "SM..."
}
```

---

### 💎 Profit Tracking (3 endpoints - NEW)

#### GET /profit/summary
Get profit summary (daily, monthly, total).

**Response:**
```json
{
  "daily_profit": 2000.00,
  "monthly_profit": 45000.00,
  "total_profit": 125000.00
}
```

#### GET /profit/details
Get profit details for each sale.

**Query Parameters:**
- `skip` (optional)
- `limit` (optional)

**Response:**
```json
[
  {
    "sale_id": 1,
    "invoice_id": "INV202402190001",
    "customer_name": "John Doe",
    "total_amount": 9000.00,
    "total_cost": 7000.00,
    "profit": 2000.00,
    "sale_date": "2024-02-19"
  }
]
```

#### GET /profit/daily-closing
Generate daily closing report.

**Query Parameters:**
- `report_date` (optional): Date for report (default: today)

**Response:**
```json
{
  "date": "2024-02-19",
  "total_sales": 45000.00,
  "total_profit": 8000.00,
  "cash_sales": 20000.00,
  "upi_sales": 15000.00,
  "card_sales": 10000.00,
  "total_items_sold": 25,
  "total_transactions": 8
}
```

---

### 📊 Dashboard (1 endpoint)

#### GET /dashboard/summary
Get complete dashboard data.

**Response:**
```json
{
  "summary": {
    "total_sales_today": 13500.00,
    "total_monthly_revenue": 125000.00,
    "low_stock_count": 3,
    "total_inventory_value": 450000.00,
    "total_items": 45,
    "daily_profit": 2500.00,
    "monthly_profit": 28000.00
  },
  "low_stock_items": [
    {
      "id": 5,
      "brand": "Apollo",
      "tire_size": "185/70R14",
      "quantity": 3
    }
  ],
  "sales_chart": [
    {
      "date": "2024-02-19",
      "amount": 13500.00
    }
  ]
}
```

---

### 📈 Reports (2 endpoints)

#### GET /reports/sales
Get sales report for date range.

**Query Parameters:**
- `start_date` (required): Start date (YYYY-MM-DD)
- `end_date` (required): End date (YYYY-MM-DD)

#### GET /reports/inventory
Get complete inventory report.

---

## Database Schema

### Tables Overview

```
users
├── id (PK)
├── username (unique)
├── email (unique)
├── hashed_password
├── full_name
└── role (admin/staff)

suppliers
├── id (PK)
├── name
├── contact_person
├── phone
├── email
└── address

tire_inventory
├── id (PK)
├── brand
├── tire_size
├── tire_type (tube/tubeless)
├── quantity
├── purchase_price
├── selling_price
├── supplier_id (FK → suppliers)
└── purchase_date

purchases (NEW v2.0)
├── id (PK)
├── supplier_name
├── tire_id (FK → tire_inventory)
├── quantity
├── purchase_price
├── total_amount
├── purchase_date
└── payment_status (paid/pending)

sales
├── id (PK)
├── invoice_id (unique)
├── customer_name
├── customer_mobile
├── total_amount
├── payment_mode (cash/upi/card)
└── sale_date

sales_items
├── id (PK)
├── sale_id (FK → sales)
├── tire_id (FK → tire_inventory)
├── quantity
├── unit_price
└── total_price
```

### Relationships

- **tire_inventory** → **supplier** (Many-to-One)
- **tire_inventory** → **purchases** (One-to-Many)
- **tire_inventory** → **sales_items** (One-to-Many)
- **sales** → **sales_items** (One-to-Many)

---

## Business Workflows

### 1. Purchase Workflow

```
1. Supplier delivers tires
   ↓
2. Go to Purchase page
   ↓
3. Add purchase entry
   - Select tire
   - Enter quantity & price
   - Set payment status
   ↓
4. Save purchase
   ↓
5. ✅ Inventory automatically increases
   ↓
6. Track in purchase history
```

### 2. Sales Workflow

```
1. Customer requests tires
   ↓
2. Go to Sales page
   ↓
3. Create new sale
   - Enter customer details
   - Add items to bill
   - Select payment mode
   ↓
4. System validates stock
   ↓
5. Calculate total with GST
   ↓
6. Complete sale
   ↓
7. ✅ Stock automatically decreases
   ↓
8. Invoice generated
   ↓
9. Download PDF or Send WhatsApp
```

### 3. Daily Closing Workflow

```
1. End of business day
   ↓
2. Go to Daily Closing page
   ↓
3. Generate report
   ↓
4. Review:
   - Total sales
   - Total profit
   - Payment breakdown
   - Items sold
   ↓
5. Match cash with report
   ↓
6. Print for records
   ↓
7. ✅ Day closed
```

---

## Feature Details

### Profit Calculation Formula

```
For each sale:
  Cost = Sum of (Purchase Price × Quantity) for all items
  Revenue = Total Sale Amount
  Profit = Revenue - Cost
  Profit Margin = (Profit / Revenue) × 100

Daily Profit = Sum of all profits for today
Monthly Profit = Sum of all profits for current month
```

### Invoice ID Generation

```
Format: INV{YYYYMMDD}{0001}

Examples:
- INV202402190001 (First invoice of Feb 19, 2024)
- INV202402190002 (Second invoice of same day)
- INV202402200001 (First invoice of Feb 20, 2024)
```

### GST Calculation

```
Subtotal = Sum of (Unit Price × Quantity)
CGST = Subtotal × 9%
SGST = Subtotal × 9%
Grand Total = Subtotal + CGST + SGST

Example:
Subtotal: ₹10,000
CGST (9%): ₹900
SGST (9%): ₹900
Grand Total: ₹11,800
```

### Low Stock Alert Logic

```
if (tire.quantity < 5) {
  Show warning badge
  Include in low stock list
  Display on dashboard
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Insufficient stock for MRF 195/65R15. Available: 2"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid authentication credentials"
}
```

### 404 Not Found
```json
{
  "detail": "Inventory item not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "quantity"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## Interactive API Documentation

Visit **http://localhost:8000/docs** for:
- Complete API reference
- Try API calls directly
- View request/response schemas
- Test authentication
- Download OpenAPI spec

---

**Complete API documentation for all 21 endpoints!** 📚
