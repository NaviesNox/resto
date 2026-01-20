"""Model for the meja (table) in the application."""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
class MejaBase(BaseModel):
    """Base model representing a meja (table) in the application."""
    kode_meja: str = Field(..., unique=True, nullable=False)
    kapasitas: int = Field(..., description="Capacity of the table", nullable=False)
    lokasi: str = Field(..., description="Location of the table", nullable=False)
    status: str = Field(..., nullable=False)

class MejaCreate(MejaBase):
    """Model for creating a new meja (table)."""
    pass

class MejaUpdate(BaseModel):
    """Model for updating an existing meja (table)."""
    kapasitas: Optional[int] = Field(None, description="Capacity of the table", nullable=False)
    lokasi: Optional[str] = Field(None, description="Location of the table", nullable=False)
    status: Optional[str] = Field(None, nullable=False)

class MejaDelete(BaseModel):
    """Model for deleting a meja (table)."""
    id: int = Field(..., description="Unique identifier for the meja (table) to be deleted")

class MejaResponse(MejaBase):
    """Base model for meja (table) in database with ID."""
    id: int = Field(..., description="Unique identifier for the meja (table)")

    model_config = ConfigDict({
        "from_attributes": True
    })