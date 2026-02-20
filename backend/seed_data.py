"""
Seed script to populate the database with dummy data for testing
Run this script to add sample inventory and sales data
"""

import sys
from pathlib import Path

# Add the backend directory to the path
sys.path.append(str(Path(__file__).parent))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.inventory import TireInventory
from app.models.sales import Sales, SalesItem, PaymentMode
from app.models.purchase import Purchase, PaymentStatus
from app.models.user import User
from app.core.security import get_password_hash
from datetime import datetime, timedelta
import random

def clear_existing_data(db: Session):
    """Clear existing data (optional - comment out if you want to keep existing data)"""
    print("🗑️  Clearing existing data...")
    db.query(SalesItem).delete()
    db.query(Sales).delete()
    db.query(Purchase).delete()
    db.query(TireInventory).delete()
    db.commit()
    print("✅ Existing data cleared")

def seed_inventory(db: Session):
    """Add sample tire inventory"""
    print("\n📦 Adding inventory data...")
    
    tire_data = [
        # MRF Tires
        {"brand": "MRF", "tire_size": "145/80 R13", "tire_type": "tubeless", "quantity": 25, "purchase_price": 2000, "selling_price": 2500, "purchase_date": "2024-01-15"},
        {"brand": "MRF", "tire_size": "155/65 R14", "tire_type": "tubeless", "quantity": 30, "purchase_price": 2200, "selling_price": 2800, "purchase_date": "2024-01-16"},
        {"brand": "MRF", "tire_size": "175/70 R14", "tire_type": "tubeless", "quantity": 20, "purchase_price": 2500, "selling_price": 3200, "purchase_date": "2024-01-17"},
        {"brand": "MRF", "tire_size": "185/65 R15", "tire_type": "tubeless", "quantity": 15, "purchase_price": 3000, "selling_price": 3800, "purchase_date": "2024-01-18"},
        
        # CEAT Tires
        {"brand": "CEAT", "tire_size": "145/80 R13", "tire_type": "tubeless", "quantity": 22, "purchase_price": 1950, "selling_price": 2450, "purchase_date": "2024-01-19"},
        {"brand": "CEAT", "tire_size": "155/65 R14", "tire_type": "tubeless", "quantity": 28, "purchase_price": 2150, "selling_price": 2750, "purchase_date": "2024-01-20"},
        {"brand": "CEAT", "tire_size": "175/70 R14", "tire_type": "tube", "quantity": 18, "purchase_price": 2400, "selling_price": 3100, "purchase_date": "2024-01-21"},
        {"brand": "CEAT", "tire_size": "195/55 R16", "tire_type": "tubeless", "quantity": 12, "purchase_price": 3500, "selling_price": 4500, "purchase_date": "2024-01-22"},
        
        # Apollo Tires
        {"brand": "Apollo", "tire_size": "145/80 R13", "tire_type": "tubeless", "quantity": 20, "purchase_price": 2050, "selling_price": 2550, "purchase_date": "2024-01-23"},
        {"brand": "Apollo", "tire_size": "155/65 R14", "tire_type": "tubeless", "quantity": 25, "purchase_price": 2250, "selling_price": 2850, "purchase_date": "2024-01-24"},
        {"brand": "Apollo", "tire_size": "175/70 R14", "tire_type": "tube", "quantity": 16, "purchase_price": 2450, "selling_price": 3150, "purchase_date": "2024-01-25"},
        {"brand": "Apollo", "tire_size": "185/65 R15", "tire_type": "tubeless", "quantity": 14, "purchase_price": 2950, "selling_price": 3750, "purchase_date": "2024-01-26"},
        
        # JK Tyre
        {"brand": "JK Tyre", "tire_size": "155/65 R14", "tire_type": "tubeless", "quantity": 24, "purchase_price": 2100, "selling_price": 2700, "purchase_date": "2024-01-27"},
        {"brand": "JK Tyre", "tire_size": "175/70 R14", "tire_type": "tubeless", "quantity": 19, "purchase_price": 2400, "selling_price": 3100, "purchase_date": "2024-01-28"},
        {"brand": "JK Tyre", "tire_size": "185/65 R15", "tire_type": "tubeless", "quantity": 13, "purchase_price": 2900, "selling_price": 3700, "purchase_date": "2024-01-29"},
        
        # Bridgestone (Premium)
        {"brand": "Bridgestone", "tire_size": "185/65 R15", "tire_type": "tubeless", "quantity": 10, "purchase_price": 3500, "selling_price": 4500, "purchase_date": "2024-01-30"},
        {"brand": "Bridgestone", "tire_size": "195/55 R16", "tire_type": "tubeless", "quantity": 8, "purchase_price": 4000, "selling_price": 5200, "purchase_date": "2024-01-31"},
        {"brand": "Bridgestone", "tire_size": "205/55 R16", "tire_type": "tubeless", "quantity": 6, "purchase_price": 4500, "selling_price": 5800, "purchase_date": "2024-02-01"},
        
        # Michelin (Premium)
        {"brand": "Michelin", "tire_size": "185/65 R15", "tire_type": "tubeless", "quantity": 8, "purchase_price": 3800, "selling_price": 4900, "purchase_date": "2024-02-02"},
        {"brand": "Michelin", "tire_size": "195/55 R16", "tire_type": "tubeless", "quantity": 7, "purchase_price": 4300, "selling_price": 5600, "purchase_date": "2024-02-03"},
    ]
    
    tires = []
    for data in tire_data:
        tire = TireInventory(**data)
        db.add(tire)
        tires.append(tire)
    
    db.commit()
    print(f"✅ Added {len(tires)} tire inventory items")
    return tires

def seed_purchases(db: Session, tires):
    """Add sample purchase records"""
    print("\n🛒 Adding purchase data...")
    
    # Create purchases for the first 10 tires
    purchases_data = []
    for i, tire in enumerate(tires[:10]):
        purchase_date = datetime.now() - timedelta(days=30-i)
        purchase = Purchase(
            supplier_name=f"Supplier {random.choice(['A', 'B', 'C', 'D'])}",
            total_amount=tire.purchase_price * tire.quantity,
            purchase_date=purchase_date.date(),
            payment_status=random.choice([PaymentStatus.PAID, PaymentStatus.PENDING])
        )
        db.add(purchase)
        purchases_data.append(purchase)
    
    db.commit()
    print(f"✅ Added {len(purchases_data)} purchase records")
    return purchases_data

def seed_sales(db: Session, tires):
    """Add sample sales records"""
    print("\n💰 Adding sales data...")
    
    customer_names = [
        "Rajesh Kumar", "Priya Sharma", "Amit Patel", "Sneha Reddy", "Vikram Singh",
        "Anita Desai", "Rahul Verma", "Pooja Gupta", "Sanjay Mehta", "Kavita Joshi",
        "Arjun Nair", "Deepika Iyer", "Manoj Rao", "Sunita Pillai", "Karthik Menon"
    ]
    
    payment_modes = [PaymentMode.CASH, PaymentMode.UPI, PaymentMode.CARD]
    
    sales_data = []
    invoice_counter = 1
    
    # Create 15 sales over the last 20 days
    for i in range(15):
        sale_date = datetime.now() - timedelta(days=20-i)
        customer_name = random.choice(customer_names)
        customer_mobile = f"98765{43210+i:05d}"
        payment_mode = random.choice(payment_modes)
        
        # Randomly select 1-3 tires for this sale
        num_items = random.randint(1, 3)
        selected_tires = random.sample([t for t in tires if t.quantity > 0], min(num_items, len(tires)))
        
        # Calculate subtotal
        subtotal = 0
        for tire in selected_tires:
            qty = random.randint(1, 2)
            subtotal += tire.selling_price * qty
        
        # Apply discount randomly (50% chance)
        discount_type = None
        discount_value = 0
        discount_amount = 0
        
        if random.random() > 0.5:
            if random.random() > 0.5:
                # Flat discount
                discount_type = "flat"
                discount_value = random.choice([50, 100, 150, 200])
                discount_amount = discount_value
            else:
                # Percentage discount
                discount_type = "percent"
                discount_value = random.choice([5, 10, 15, 20])
                discount_amount = (subtotal * discount_value) / 100
        
        total_amount = subtotal - discount_amount
        
        # Create sale
        sale = Sales(
            invoice_id=f"INV-{sale_date.strftime('%Y%m%d')}-{invoice_counter:03d}",
            customer_name=customer_name,
            customer_mobile=customer_mobile,
            subtotal=subtotal,
            discount_type=discount_type,
            discount_value=discount_value,
            discount_amount=discount_amount,
            total_amount=total_amount,
            notes=f"Sale to {customer_name}" if random.random() > 0.7 else None,
            payment_mode=payment_mode,
            sale_date=sale_date
        )
        db.add(sale)
        db.flush()
        
        # Add sale items
        for tire in selected_tires:
            qty = random.randint(1, 2)
            sale_item = SalesItem(
                sale_id=sale.id,
                tire_id=tire.id,
                quantity=qty,
                unit_price=tire.selling_price,
                total_price=tire.selling_price * qty
            )
            db.add(sale_item)
            
            # Reduce inventory
            tire.quantity -= qty
        
        sales_data.append(sale)
        invoice_counter += 1
    
    db.commit()
    print(f"✅ Added {len(sales_data)} sales records")
    return sales_data

def main():
    """Main seeding function"""
    print("\n" + "="*60)
    print("🌱 SEEDING DATABASE WITH DUMMY DATA")
    print("="*60)
    
    db = SessionLocal()
    
    try:
        # Optional: Clear existing data (comment out if you want to keep existing data)
        # clear_existing_data(db)
        
        # Seed data
        tires = seed_inventory(db)
        purchases = seed_purchases(db, tires)
        sales = seed_sales(db, tires)
        
        print("\n" + "="*60)
        print("✅ DATABASE SEEDING COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"\n📊 Summary:")
        print(f"   • Inventory Items: {len(tires)}")
        print(f"   • Purchase Records: {len(purchases)}")
        print(f"   • Sales Records: {len(sales)}")
        print(f"\n🚀 You can now test the application with realistic data!")
        print(f"   Frontend: http://localhost:3000")
        print(f"   Login: admin / admin123")
        print("\n" + "="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
