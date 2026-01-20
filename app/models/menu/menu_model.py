"""Model for the menu in the application."""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class MenuBase(BaseModel):
    """Base model representing a menu item in the application."""
    nama_menu: str = Field(..., unique=True, nullable=False)
    kategori: str = Field(..., nullable=False)
    harga: float = Field(..., description="Price of the menu item", nullable=False)
    stok: int = Field(..., description="Stock of the menu item", nullable=False)

class MenuCreate(MenuBase):
    """Model for creating a new menu item."""
    pass

class MenuUpdate(BaseModel):
    """Model for updating an existing menu item."""
    nama_menu: Optional[str] = Field(None, unique=True, nullable=False)
    kategori: Optional[str] = Field(None, nullable=False)
    harga: Optional[float] = Field(None, description="Price of the menu item", nullable=False)
    stok: Optional[int] = Field(None, description="Stock of the menu item", nullable=False)

class MenuDelete(BaseModel):
    """Model for deleting a menu item."""
    id: int = Field(..., description="Unique identifier for the menu item to be deleted")

class MenuResponse(MenuBase):
    """Base model for menu item in database with ID."""
    id: int = Field(..., description="Unique identifier for the menu item")

    model_config = ConfigDict({
        "from_attributes": True
    })