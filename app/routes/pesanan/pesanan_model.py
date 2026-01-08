"""Model for the pesanan (order) in the application."""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class PesananBase(BaseModel):
    id_user: int = Field(..., description="ID of the user who placed the order", nullable=False)
    tanggal_pesanan: str = Field(..., description="Date when the order was placed", nullable=False)
    total_harga: float = Field(..., description="Total price of the order", nullable=False)
    status: str = Field(..., description="Status of the order (e.g., pending, completed)", nullable=False)

class PesananCreate(PesananBase):
    """Model for creating a new pesanan (order)."""
    pass

class PesananUpdate(BaseModel):
    """Model for updating an existing pesanan (order)."""
    id_user: Optional[int] = Field(None, description="ID of the user who placed the order", nullable=False)
    tanggal_pesanan: Optional[str] = Field(None, description="Date when the order was placed", nullable=False)
    total_harga: Optional[float] = Field(None, description="Total price of the order", nullable=False)
    status: Optional[str] = Field(None, description="Status of the order (e.g., pending, completed)", nullable=False)

class PesananDelete(BaseModel):
    """Model for deleting a pesanan (order)."""
    id: int = Field(..., description="Unique identifier for the pesanan (order) to be deleted")

class PesananResponse(PesananBase):
    """Base model for pesanan (order) in database with ID."""
    id: int = Field(..., description="Unique identifier for the pesanan (order)")

    model_config = ConfigDict({
        "from_attributes": True
    })