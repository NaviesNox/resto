"""Model for the detail_pesanan (order details) in the application."""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class DetailPesananBase(BaseModel):
    """Base model representing a detail_pesanan (order details) in the application."""
    id_pesanan: int = Field(..., description="ID of the associated pesanan (order)")
    id_menu: int = Field(..., description="ID of the associated menu item")
    qty: int = Field(..., description="Quantity of the menu item ordered")
    harga_satuan: float = Field(..., description="Unit price of the menu item")
    subtotal: float = Field(..., description="Subtotal price for the menu item ordered")

class DetailPesananCreate(DetailPesananBase):
    """Model for creating a new detail_pesanan (order details)."""
    pass

class DetailPesananUpdate(BaseModel):
    """Model for updating an existing detail_pesanan (order details)."""
    id_pesanan: Optional[int] = Field(None, description="ID of the associated pesanan (order)")
    id_menu: Optional[int] = Field(None, description="ID of the associated menu item")
    qty: Optional[int] = Field(None, description="Quantity of the menu item ordered")
    harga_satuan: Optional[float] = Field(None, description="Unit price of the menu item")
    subtotal: Optional[float] = Field(None, description="Subtotal price for the menu item ordered")

class DetailPesananDelete(BaseModel):
    """Model for deleting a detail_pesanan (order details)."""
    id: int = Field(..., description="Unique identifier for the detail_pesanan to be deleted")

class DetailPesananResponse(DetailPesananBase):
    """Model for detail_pesanan response, including ID and helper fields for FE."""
    id: int = Field(..., description="Unique identifier for the detail_pesanan")
    nama_menu: Optional[str] = Field(None, description="Name of the menu item for display purposes")

    model_config = ConfigDict(from_attributes=True)