"""
Script to create an admin user directly in the database
Run this once after deployment to create the first admin user
"""
import sys
from app.core.database import SessionLocal
from app.models.user import User, UserRole

def create_admin():
    db = SessionLocal()
    try:
        # Check if admin already exists
        existing_admin = db.query(User).filter(User.username == "admin").first()
        if existing_admin:
            print("❌ Admin user already exists!")
            return
        
        # Create admin user with simple password hashing
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        # Use short password to avoid bcrypt 72 byte limit
        password = "admin"
        hashed = pwd_context.hash(password)
        
        admin_user = User(
            username="admin",
            email="admin@example.com",
            full_name="Admin User",
            role=UserRole.ADMIN,
            hashed_password=hashed
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("✅ Admin user created successfully!")
        print(f"   Username: admin")
        print(f"   Password: admin")
        print(f"   Role: {admin_user.role}")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
