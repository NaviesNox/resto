from sqlalchemy.orm import Session
from app.core.security import verify_password
from orm_models import User

def authenticate_pramuSaji(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    # cek password hash
    if not verify_password(password, user.password):
        return None
    return user

def authenticate_admin(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    # cek role staff
    if user.role not in ["admin"]:
        return None
    return user