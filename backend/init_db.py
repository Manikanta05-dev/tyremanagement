"""
Initialize database with default admin user
Run this script after creating the database and running migrations
"""
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models import User, UserRole
from app.core.security import get_password_hash

def init_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if admin user exists
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin = User(
                username="admin",
                email="admin@tireshop.com",
                hashed_password=get_password_hash("admin123"),
                full_name="Admin User",
                role=UserRole.ADMIN
            )
            db.add(admin)
            db.commit()
            print("✓ Admin user created successfully")
            print("  Username: admin")
            print("  Password: admin123")
        else:
            print("✓ Admin user already exists")
    finally:
        db.close()

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database initialization complete!")
