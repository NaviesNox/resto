from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.auth import create_access_token
from app.core.deps import get_db
from fastapi.security import  OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.models.user import user_service
from app.routes.auth import auth_service
from app.models.user.user_model import UserRegis, UserResponse


router = APIRouter(prefix="/auth", tags=["Auth"])

class LoginRequest(BaseModel):
    username: str
    password: str

""" ================= UNIVERSAL LOGIN ================= """
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Universal login untuk Swagger (Customer & Staff)."""
    print("Login hit")
    # coba login sebagai pramuSaji
    user = auth_service.authenticate_pramuSaji(db, form_data.username, form_data.password)
    if user:
        token = create_access_token({"user_id": str(user.id), "role": "pramusaji"})
        return {"access_token": token, "token_type": "bearer"}

    # coba login sebagai admin
    user = auth_service.authenticate_admin(db, form_data.username, form_data.password)
    if user:
        token = create_access_token({"user_id": str(user.id), "role": user.role.value})
        return {"access_token": token, "token_type": "bearer"}

    raise HTTPException(status_code=401, detail="Invalid username or password")


@router.post("/register", response_model=UserResponse, status_code=201)
def register_user(user: UserRegis, db: Session = Depends(get_db)):
    return user_service.create_register(db, user)