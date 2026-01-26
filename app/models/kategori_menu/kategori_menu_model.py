"""Kategori Menu Model"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional 

class KategoriMenuBase(BaseModel):
    """Base model representing a kategori menu item in the application."""
    nama_kategori: str = Field(..., unique=True, nullable=False)


class KategoriMenuCreate(KategoriMenuBase):
    """Model for creating a new kategori menu item."""
    pass

class KategoriMenuUpdate(BaseModel):
    """Model for updating an existing kategori menu item."""
    nama_kategori: Optional[str] = Field(None, unique=True, nullable=False)


class KategoriMenuDelete(BaseModel):
    """Model for deleting a kategori menu item."""
    id: int = Field(..., description="Unique identifier for the kategori menu item to be deleted")

class KategoriMenuResponse(KategoriMenuBase):
    """Base model for kategori menu item in database with ID."""
    id: int = Field(..., description="Unique identifier for the kategori menu item")

    model_config = ConfigDict({
        "from_attributes": True
    })