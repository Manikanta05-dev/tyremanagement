from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.core.security import verify_password, create_access_token
from app.schemas.user import UserLogin, Token, UserResponse

class AuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)
    
    def login(self, credentials: UserLogin) -> Token:
        user = self.user_repo.get_by_username(credentials.username)
        
        if not user or not verify_password(credentials.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        
        access_token = create_access_token(data={"sub": user.username, "user_id": user.id})
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse.model_validate(user)
        )
