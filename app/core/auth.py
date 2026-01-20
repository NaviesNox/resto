"""Authentication Core Module and JWT Handling"""
from datetime import datetime, timedelta
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from orm_models import User
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core.deps import get_db
from orm_models import UserRole
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

class TokenData(BaseModel):
    user_id:int
    role: Optional[UserRole] = None

def create_access_token(data: dict, expires_delta: Optional[timedelta]= None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str = Depends(oauth2_scheme)) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        role: str = payload.get("role")
        if user_id is None or role is None:
            raise credentials_exception

        return TokenData(user_id=user_id, role=role)
    except JWTError:
        raise credentials_exception
    
def get_current_user(token_data: TokenData = Depends(verify_token), db: Session = Depends(get_db)) -> User:
    user = db.query(User).filter(User.id == token_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

    
def require_role(required_role: UserRole):
    def role_dependency(curent_user: User = Depends(get_current_user)):
        if curent_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Role mu ga boleh masuk sini"
            )
        return curent_user
    return role_dependency

