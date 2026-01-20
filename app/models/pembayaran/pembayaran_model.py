"""Model for the pembayaran (payment) in the application."""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class PembayaranBase(BaseModel):
    """Base model representing a pembayaran (payment) in the application."""
    metode_pembayaran: str = Field(..., nullable=False)
    jumlah_bayar: float = Field(..., description="Amount paid", nullable=False)
    status_pembayaran: str = Field(..., nullable=False)

class PembayaranCreate(PembayaranBase):
    """Model for creating a new pembayaran (payment)."""
    pass

class PembayaranUpdate(BaseModel):
    """Model for updating an existing pembayaran (payment)."""
    metode_pembayaran: Optional[str] = Field(None, nullable=False)
    jumlah_bayar: Optional[float] = Field(None, description="Amount paid", nullable=False)
    status_pembayaran: Optional[str] = Field(None, nullable=False)

class PembayaranDelete(BaseModel):
    """Model for deleting a pembayaran (payment)."""
    id: int = Field(..., description="Unique identifier for the pembayaran (payment) to be deleted")

class PembayaranResponse(PembayaranBase):
    """Base model for pembayaran (payment) in database with ID."""
    id: int = Field(..., description="Unique identifier for the pembayaran (payment)")

    model_config = ConfigDict({
        "from_attributes": True
    })