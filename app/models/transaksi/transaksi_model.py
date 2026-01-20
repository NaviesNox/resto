"""Model for the transaksi (transaction) in the application."""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
class TransaksiBase(BaseModel):
    """Base model representing a transaksi (transaction) in the application."""
    id_pesanan: int = Field(..., description="ID of the associated pesanan (order)", nullable=False)
    id_meja: int = Field(..., description="ID of the associated meja (table)", nullable=False)
    total_bayar: float = Field(..., description="Total amount paid in the transaction", nullable=False)
    tanggal_transaksi: str = Field(..., description="Date of the transaction", nullable=False)

class TransaksiCreate(TransaksiBase):
    """Model for creating a new transaksi (transaction)."""
    pass

class TransaksiUpdate(BaseModel):
    """Model for updating an existing transaksi (transaction)."""
    id_pesanan: Optional[int] = Field(None, description="ID of the associated pesanan (order)", nullable=False)
    id_meja: Optional[int] = Field(None, description="ID of the associated meja (table)", nullable=False)
    total_bayar: Optional[float] = Field(None, description="Total amount paid in the transaction", nullable=False)
    tanggal_transaksi: Optional[str] = Field(None, description="Date of the transaction", nullable=False)

class TransaksiDelete(BaseModel):
    """Model for deleting a transaksi (transaction)."""
    id: int = Field(..., description="Unique identifier for the transaksi (transaction) to be deleted")

class TransaksiResponse(TransaksiBase):
    """Base model for transaksi (transaction) in database with ID."""
    id: int = Field(..., description="Unique identifier for the transaksi (transaction)")

    model_config = ConfigDict({
        "from_attributes": True
    })
    