"""
Initialize database with admin user on startup
"""
from app.core.database import SessionLocal
from app.models.user import User, UserRole
from passlib.context import CryptContext

def init_admin():
    db = SessionLocal()
    try:
        # Check if admin already exists
        existing_admin = db.query(User).filter(User.username == "admin").first()
        if existing_admin:
            print("✅ Admin user already exists")
            return
        
        # Create admin user
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hashed = pwd_context.hash("admin")
        
        admin_user = User(
            username="admin",
            email="admin@example.com",
            full_name="Admin User",
            role=UserRole.ADMIN,
            hashed_password=hashed
        )
        
        db.add(admin_user)
        db.commit()
        
        print("✅ Admin user created: username=admin, password=admin")
        
    except Exception as e:
        print(f"⚠️ Could not create admin user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_admin()
