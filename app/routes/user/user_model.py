"""User model for the application."""

from pydantic import BaseModel,  Field, ConfigDict
from typing import Optional

class Userbase(BaseModel):
    """User model representing a user in the application."""

    
    username: str = Field(..., unique=True, nullable=False)
    nama: str = Field(..., description="Full name of the user", nullable=False)
    no_telp: str = Field(..., description="Phone number of the user", nullable=False)
    password: str = Field(..., nullable=False)
    role: str = Field(..., nullable=False)


class UserCreate(Userbase):
    """Model for creating a new user."""
    pass

class UserUpdate(BaseModel):
    """Model for updating an existing user."""
    nama: Optional[str] = Field(None, description="Full name of the user", nullable=False)
    no_telp: Optional[str] = Field(None, description="Phone number of the user", nullable=False)
    password: Optional[str] = Field(None, nullable=False)

class UserDelete(BaseModel):
    """Model for deleting a user."""
    id: int = Field(..., description="Unique identifier for the user to be deleted")

class UserResponse(Userbase):
    """Base model for user in database with ID."""
    id: int = Field(..., description="Unique identifier for the user")



    model_config = ConfigDict({
        "from_attributes": True
    })
