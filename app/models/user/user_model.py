"""User model for the application."""

from pydantic import BaseModel, Field, ConfigDict, EmailStr, computed_field
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
    role: UserRole = Field(..., nullable=False)
    email: EmailStr = Field(..., unique=True, nullable=False)
    status: statusUser = Field(default=statusUser.active, nullable=False)
    id_karyawan: int = Field(..., description="ID of the associated employee", nullable=False)

class UserCreate(Userbase):
    """Model for creating a new user."""    
    password: str = Field(..., nullable=False)
    pass

class UserRegis(BaseModel):
    """Model for user registration."""
    username: str = Field(..., unique=True, nullable=False)
    password: str = Field(..., nullable=False)
    email: EmailStr = Field(..., unique=True, nullable=True)
    role: UserRole = Field(default=UserRole.pramusaji, nullable=False)
    status: statusUser = Field(default=statusUser.active, nullable=True)
    id_karyawan: int = Field(..., description="ID of the associated employee", nullable=False)

    

class UserUpdate(BaseModel):
    """Model for updating an existing user."""
    username: Optional[str] = Field(None, unique=True, nullable=False)
    password: Optional[str] = Field(None, nullable=False)
    role: Optional[UserRole] = Field(None, nullable=False)


class UserDelete(BaseModel):
    """Model for deleting a user."""
    id: int = Field(..., description="Unique identifier for the user to be deleted")

class UserResponse(BaseModel):
    """Model for user response."""
    id: int = Field(..., description="Unique identifier for the user")
    username: str = Field(..., unique=True, nullable=False)
    email: EmailStr = Field(..., unique=True, nullable=True)
    role: UserRole = Field(..., nullable=False)
    email: EmailStr = Field(..., nullable=False)
    status: statusUser = Field(default=statusUser.active, nullable=False)
    id_karyawan: Optional[int] = Field(None, description="ID of the associated employee", nullable=True)

    model_config = ConfigDict({
        "from_attributes": True
    })

    status: statusUser = Field(..., nullable=True)
    id_karyawan: int = Field(..., description="ID of the associated employee", nullable=False)

    model_config = ConfigDict(from_attributes=True)
    