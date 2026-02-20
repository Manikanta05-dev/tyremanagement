from sqlalchemy.orm import Session
from typing import Optional
from app.models.user import User
from app.core.security import get_password_hash

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()
    
    def create(self, username: str, password: str, **kwargs) -> User:
        hashed_password = get_password_hash(password)
        user = User(username=username, hashed_password=hashed_password, **kwargs)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
