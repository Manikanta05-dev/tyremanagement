# 🌱 Seed Data Guide - Testing with Dummy Data

## Overview
This guide explains how to populate your database with realistic dummy data for testing the complete user flow.

---

## 📊 What Data Will Be Added?

### 1. Inventory (20 items)
- **MRF Tires**: 4 different sizes (145/80 R13 to 185/65 R15)
- **CEAT Tires**: 4 different sizes (145/80 R13 to 195/55 R16)
- **Apollo Tires**: 4 different sizes (145/80 R13 to 185/65 R15)
- **JK Tyre**: 3 different sizes (155/65 R14 to 185/65 R15)
- **Bridgestone**: 3 premium sizes (185/65 R15 to 205/55 R16)
- **Michelin**: 2 premium sizes (185/65 R15 to 195/55 R16)

**Total Stock**: ~350 tires across all brands

### 2. Purchase Records (10 records)
- Purchases from different suppliers (Supplier A, B, C, D)
- Dates spread over the last 30 days
- Bulk purchases matching inventory quantities
- Complete with supplier contact information

### 3. Sales Records (15 records)
- Sales to 15 different customers
- Dates spread over the last 20 days
- Mix of payment modes (Cash, UPI, Card)
- Some with discounts (Flat ₹ and Percent %)
- 1-3 items per sale
- Realistic customer names and mobile numbers

---

## 🚀 How to Seed the Database

### Method 1: Using Batch File (Easiest)
```bash
# Simply double-click or run:
seed-database.bat
```

### Method 2: Manual Command
```bash
cd backend
.venv\Scripts\activate
python seed_data.py
```

### Method 3: From Python
```python
cd backend
.venv\Scripts\activate
python
>>> from seed_data import main
>>> main()
```

---

## ⚠️ Important Notes

### Data Preservation
By default, the script **DOES NOT** clear existing data. It will add new data to what you already have.

If you want to start fresh, uncomment this line in `seed_data.py`:
```python
# Line 35 in seed_data.py
clear_existing_data(db)  # Uncomment this to clear existing data
```

### Inventory Reduction
The seed script automatically reduces inventory quantities when creating sales records, simulating real-world stock management.

---

## 🧪 Testing Scenarios

### Scenario 1: View Inventory
1. Login to the application
2. Go to **Inventory** page
3. You should see 20 different tire types
4. Check stock levels (some will be reduced due to sales)

### Scenario 2: View Sales History
1. Go to **Sales** page
2. You should see 15 sales records
3. Check different payment modes
4. Notice some sales have discounts applied

### Scenario 3: Create New Sale
1. Click **"New Sale"** button
2. Select customer details
3. Add multiple items from the seeded inventory
4. Apply a discount (Flat ₹ or Percent %)
5. Submit the sale
6. Verify stock is reduced

### Scenario 4: View Purchase History
1. Go to **Purchase** page
2. You should see 10 purchase records
3. Check supplier information
4. View purchase items

### Scenario 5: View Reports
1. Go to **Reports** page
2. Check sales analytics
3. View profit calculations
4. Analyze trends over the last 20 days

### Scenario 6: Daily Closing
1. Go to **Daily Closing** page
2. View today's sales summary
3. Check cash/UPI/card breakdowns

---

## 📋 Sample Data Details

### Sample Customers
- Rajesh Kumar (9876543210)
- Priya Sharma (9876543211)
- Amit Patel (9876543212)
- Sneha Reddy (9876543213)
- Vikram Singh (9876543214)
- ... and 10 more

### Sample Suppliers
- Supplier A (9876543210)
- Supplier B (9876543211)
- Supplier C (9876543212)
- Supplier D (9876543213)

### Price Ranges
- **Budget**: ₹2,000 - ₹3,000 (MRF, CEAT, Apollo, JK)
- **Premium**: ₹3,500 - ₹5,800 (Bridgestone, Michelin)

### Discount Examples
- **Flat**: ₹50, ₹100, ₹150, ₹200
- **Percent**: 5%, 10%, 15%, 20%

---

## 🔄 Re-seeding

If you want to re-seed with fresh data:

1. **Clear existing data** (optional):
   - Uncomment `clear_existing_data(db)` in `seed_data.py`
   
2. **Run the seed script again**:
   ```bash
   seed-database.bat
   ```

3. **Refresh your browser**

---

## 🐛 Troubleshooting

### Error: "No module named 'app'"
**Solution**: Make sure you're in the backend directory and virtual environment is activated
```bash
cd backend
.venv\Scripts\activate
python seed_data.py
```

### Error: "Database connection failed"
**Solution**: Ensure PostgreSQL is running and credentials in `.env` are correct

### Error: "Integrity constraint violation"
**Solution**: Some data might already exist. Either:
- Clear existing data first (uncomment `clear_existing_data`)
- Or modify the seed script to generate unique data

### No data appears in frontend
**Solution**: 
1. Check if backend is running
2. Refresh the browser (Ctrl+F5)
3. Check browser console for errors
4. Verify database connection

---

## 📊 Expected Results After Seeding

### Dashboard
- Total inventory value displayed
- Recent sales shown
- Low stock alerts (if any)
- Quick stats updated

### Inventory Page
- 20 tire types listed
- Various stock levels (some reduced)
- Different brands and sizes
- Mix of tubeless and tube types

### Sales Page
- 15 sales records
- Different dates over last 20 days
- Mix of payment modes
- Some with discounts

### Purchase Page
- 10 purchase records
- Different suppliers
- Bulk quantities
- Purchase dates

### Reports Page
- Sales trends visible
- Profit calculations
- Revenue analytics
- Best-selling items

---

## 🎯 Testing Checklist

After seeding, test these flows:

- [ ] View all inventory items
- [ ] Create a new sale with discount
- [ ] Verify stock reduction after sale
- [ ] View sales history
- [ ] Download invoice PDF
- [ ] Create a new purchase
- [ ] View purchase history
- [ ] Check reports and analytics
- [ ] Test daily closing
- [ ] Search and filter functionality
- [ ] Mobile responsive views
- [ ] Export data (if available)

---

## 💡 Tips

1. **Realistic Testing**: The seeded data mimics real tire shop operations
2. **Date Range**: Sales are spread over 20 days for better analytics
3. **Stock Levels**: Some items have low stock to test alerts
4. **Discounts**: Mix of flat and percentage discounts
5. **Payment Modes**: All three modes (Cash, UPI, Card) represented

---

## 🔧 Customization

Want to customize the seed data? Edit `backend/seed_data.py`:

### Add More Brands
```python
{"brand": "Goodyear", "tire_size": "195/55 R16", ...}
```

### Change Quantities
```python
"quantity": 50,  # Increase stock
```

### Add More Sales
```python
for i in range(30):  # Change from 15 to 30
```

### Adjust Discounts
```python
discount_value = random.choice([100, 200, 300, 500])
```

---

## 📝 Summary

**Command to Seed**:
```bash
seed-database.bat
```

**What You Get**:
- 20 inventory items
- 10 purchase records
- 15 sales records
- Realistic customer data
- Mix of payment modes
- Various discounts

**Time to Seed**: ~2 seconds

**Ready to Test**: Immediately after seeding!

---

## 🎉 Next Steps

1. Run the seed script
2. Refresh your browser
3. Login with: `admin` / `admin123`
4. Explore all pages
5. Test the complete user flow
6. Create new sales/purchases
7. Check reports and analytics

**Happy Testing!** 🚀
