"""
Reset database - Drop all tables and recreate with current schema
"""
from app.core.database import Base, engine
from app.models import *  # Import all models
from sqlalchemy import text

def reset_database():
    print("Dropping all tables with CASCADE...")
    # Drop all tables using CASCADE to handle dependencies
    with engine.connect() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))
        conn.commit()
    print("✓ All tables dropped")
    
    print("Creating tables with new schema...")
    Base.metadata.create_all(bind=engine)
    print("✓ All tables created")
    
    print("\nDatabase reset complete!")
    print("Run 'python init_db.py' to create admin user")

if __name__ == "__main__":
    confirm = input("This will DELETE all data. Are you sure? (yes/no): ")
    if confirm.lower() == "yes":
        reset_database()
    else:
        print("Operation cancelled")
