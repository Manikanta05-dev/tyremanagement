"""
Migration script to add discount fields to sales table
Run this after updating the models
"""
from sqlalchemy import text
from app.core.database import engine

def migrate():
    with engine.connect() as conn:
        # Add new columns to sales table
        try:
            conn.execute(text("ALTER TABLE sales ADD COLUMN IF NOT EXISTS subtotal FLOAT DEFAULT 0"))
            conn.execute(text("ALTER TABLE sales ADD COLUMN IF NOT EXISTS discount_type VARCHAR"))
            conn.execute(text("ALTER TABLE sales ADD COLUMN IF NOT EXISTS discount_value FLOAT DEFAULT 0"))
            conn.execute(text("ALTER TABLE sales ADD COLUMN IF NOT EXISTS discount_amount FLOAT DEFAULT 0"))
            conn.execute(text("ALTER TABLE sales ADD COLUMN IF NOT EXISTS notes VARCHAR"))
            
            # Update existing records - set subtotal = total_amount for old records
            conn.execute(text("UPDATE sales SET subtotal = total_amount WHERE subtotal = 0 OR subtotal IS NULL"))
            
            conn.commit()
            print("✓ Migration completed successfully!")
            print("  - Added subtotal column")
            print("  - Added discount_type column")
            print("  - Added discount_value column")
            print("  - Added discount_amount column")
            print("  - Added notes column")
            print("  - Updated existing records")
        except Exception as e:
            print(f"Migration error: {e}")
            conn.rollback()

if __name__ == "__main__":
    print("Running sales discount migration...")
    migrate()
