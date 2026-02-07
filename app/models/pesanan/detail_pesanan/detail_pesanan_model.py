"""Model for the detail_pesanan (order details) in the application."""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class DetailPesananBase(BaseModel):
    """Base model representing a detail_pesanan (order details) in the application."""
    id_pesanan: int = Field(..., description="ID of the associated pesanan (order)", nullable=False)
    id_menu: int = Field(..., description="ID of the associated menu item", nullable=False)
    qty: int = Field(..., description="Quantity of the menu item ordered", nullable=False)
    harga_satuan: float = Field(..., description="Unit price of the menu item", nullable=False)
    subtotal: float = Field(..., description="Subtotal price for the menu item ordered", nullable=False)

class DetailPesananCreate(DetailPesananBase):
    """Model for creating a new detail_pesanan (order details)."""
    pass

class DetailPesananUpdate(BaseModel):
    """Model for updating an existing detail_pesanan (order details)."""
    id_pesanan: Optional[int] = Field(None, description="ID of the associated pesanan (order)", nullable=False)
    id_menu: Optional[int] = Field(None, description="ID of the associated menu item", nullable=False)
    qty: Optional[int] = Field(None, description="Quantity of the menu item ordered", nullable=False)
    harga_satuan: Optional[float] = Field(None, description="Unit price of the menu item", nullable=False)
    subtotal: Optional[float] = Field(None, description="Subtotal price for the menu item ordered", nullable=False)

class DetailPesananDelete(BaseModel):
    """Model for deleting a detail_pesanan (order details)."""
    id: int = Field(..., description="Unique identifier for the detail_pesanan (order details) to be deleted")

class DetailPesananResponse(DetailPesananBase):
    """Base model for detail_pesanan (order details) in database with ID."""
    id: int = Field(..., description="Unique identifier for the detail_pesanan (order details)")

    model_config = ConfigDict({
        "from_attributes": True
    })