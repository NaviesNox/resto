"""Model for the menu in the application."""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class MenuBase(BaseModel):
    """Base model representing a menu item in the application."""
    nama_menu: str = Field(...)
    kategori: int = Field(...)
    harga: float = Field(..., description="Price of the menu item")
    stok: int = Field(..., description="Stock of the menu item")

class MenuCreate(MenuBase):
    """Model for creating a new menu item."""
    pass

class MenuUpdate(BaseModel):
    """Model for updating an existing menu item."""
    nama_menu: Optional[str] = None
    kategori: Optional[int] = None
    harga: Optional[float] = None
    stok: Optional[int] = None

class MenuDelete(BaseModel):
    """Model for deleting a menu item."""
    id: int = Field(..., description="Unique identifier for the menu item to be deleted")

class MenuResponse(MenuBase):
    """Base model for menu item in database with ID."""
    id: int = Field(..., description="Unique identifier for the menu item")

    model_config = ConfigDict(from_attributes=True)