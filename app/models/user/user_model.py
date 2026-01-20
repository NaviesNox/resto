"""User model for the application."""

import email
from pydantic import BaseModel,  Field, ConfigDict, EmailStr
from typing import Optional
import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    pramusaji = "pramusaji"
    manager = "manager"
    kasir = "kasir"

class statusUser(str, enum.Enum):
    active = "active"
    inactive = "inactive"


class Userbase(BaseModel):
    """User model representing a user in the application."""

    
    username: str = Field(..., unique=True, nullable=False)
    nama: str = Field(..., description="Full name of the user", nullable=False)
    no_telp: str = Field(..., description="Phone number of the user", nullable=False)
    role: UserRole = Field(..., nullable=False)
    email: EmailStr = Field(..., unique=True, nullable=False)
    status: statusUser = Field(default=statusUser.active, nullable=False)
    id_karyawan: int = Field(..., description="ID of the associated employee", nullable=True)

class UserCreate(Userbase):
    """Model for creating a new user."""    
    password: str = Field(..., nullable=False)
    pass

class UserRegis(BaseModel):
    """Model for user registration."""
    username: str = Field(..., unique=True, nullable=False)
    nama: str = Field(..., description="Full name of the user", nullable=False)
    no_telp: str = Field(..., description="Phone number of the user", nullable=False)
    password: str = Field(..., nullable=False)
    email: EmailStr = Field(..., unique=True, nullable=True)
    role: UserRole = Field(default=UserRole.pramusaji, nullable=False)
    status: statusUser = Field(default=statusUser.active, nullable=True)
    id_karyawan: Optional[int] = Field(None, description="ID of the associated employee", nullable=True)

    

class UserUpdate(BaseModel):
    """Model for updating an existing user."""
    username: Optional[str] = Field(None, unique=True, nullable=False)
    nama: Optional[str] = Field(None, description="Full name of the user", nullable=False)
    no_telp: Optional[str] = Field(None, description="Phone number of the user", nullable=False)
    password: Optional[str] = Field(None, nullable=False)
    role: Optional[UserRole] = Field(None, nullable=False)


class UserDelete(BaseModel):
    """Model for deleting a user."""
    id: int = Field(..., description="Unique identifier for the user to be deleted")

class UserResponse(Userbase):
    """Base model for user in database with ID."""
    id: int = Field(..., description="Unique identifier for the user")



    model_config = ConfigDict({
        "from_attributes": True
    })
