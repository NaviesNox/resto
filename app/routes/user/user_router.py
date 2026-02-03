"""User Router"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models.user import user_service
from app.models.user.user_model import UserCreate, UserUpdate, UserResponse
from orm_models import User, UserRole
from app.core.auth import require_role, get_current_user


router = APIRouter(prefix="/users", tags=["Users"])
"""ambil semua user"""
@router.get("/", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db),
               user: User = Depends(require_role(UserRole.admin))):
    """Mengambil semua data user. Hanya untuk admin."""
    return user_service.get_all_user(db)

"""Get Profile of user that login"""
@router.get("/profile/", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

"""Update Profile of user that login"""
@router.patch("/profile/", response_model=UserResponse)
def update_profile(user_update: UserUpdate,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)): 
    return user_service.update_user(db, current_user.id, user_update)

"""ambol user by id"""
@router.get("/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db),
             admin_user: User = Depends(require_role(UserRole.admin))):
    """Mengambil data user berdasarkan ID. Hanya untuk admin."""
    user = user_service.get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


"""tambah user"""
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db),
                admin_user: User = Depends(require_role(UserRole.admin))):

    return user_service.create_user(db, user)

"""update user"""
@router.patch("/{id}", response_model=UserResponse)
def update_user(id: int, user_update: UserUpdate, db: Session = Depends(get_db),
                admin_user: User = Depends(require_role(UserRole.admin))):
    user = user_service.get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user_service.update_user(db, id, user_update)

"""delete user"""
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db),
                admin_user: User = Depends(require_role(UserRole.admin))):
    user = user_service.get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user_service.delete_user(db, id)
    return None   
 