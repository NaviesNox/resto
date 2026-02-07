"""Model for the pesanan (order) in the application."""

from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from typing import Optional

class TipePesanan(str, Enum):
    dine_in = "dine_in"
    takeaway = "takeaway"

class StatusPesanan(str, Enum):
    dipesan = "dipesan"
    diproses = "diproses"
    selesai = "selesai"
    dibayar = "dibayar"
    dibatalkan = "dibatalkan"

class PesananBase(BaseModel):
    id_transaksi: int = Field(..., description="ID of the associated transaksi (transaction)", nullable=False)
    id_user: int = Field(..., description="ID of the user who placed the order", nullable=False)
    id_meja: int = Field(..., description="ID of the table associated with the order", nullable=False)
    tipe_pesanan: TipePesanan = Field(..., description="Type of the order (dine_in or takeaway)", nullable=False)
    kode_pesanan: str = Field(..., description="Unique code for the pesanan (order)", nullable=False)
    tanggal: str = Field(..., description="Date when the order was placed", nullable=False)
    status: StatusPesanan = Field(..., description="Status of the order", nullable=False)

class PesananCreate(PesananBase):
    """Model for creating a new pesanan (order)."""
    pass

class PesananUpdate(BaseModel):
    """Model for updating an existing pesanan (order)."""
    id_transaksi: Optional[int] = Field(None, description="ID of the associated transaksi (transaction)", nullable=False)
    id_user: Optional[int] = Field(None, description="ID of the user who placed the order", nullable=False)
    id_meja: Optional[int] = Field(None, description="ID of the table associated with the order", nullable=False)
    tipe_pesanan: Optional[TipePesanan] = Field(None, description="Type of the order (dine_in or takeaway)", nullable=False)
    kode_pesanan: Optional[str] = Field(None, description="Unique code for the pesanan (order)", nullable=False)
    tanggal: Optional[str] = Field(None, description="Date when the order was placed", nullable=False)
    status: Optional[StatusPesanan] = Field(None, description="Status of the order", nullable=False)    
    

class PesananDelete(BaseModel):
    """Model for deleting a pesanan (order)."""
    id: int = Field(..., description="Unique identifier for the pesanan (order) to be deleted")

class PesananResponse(PesananBase):
    """Base model for pesanan (order) in database with ID."""
    id: int = Field(..., description="Unique identifier for the pesanan (order)")

    model_config = ConfigDict({
        "from_attributes": True
    })