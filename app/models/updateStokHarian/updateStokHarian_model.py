"""Model updateStokHarian"""

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

class UpdateStokHarianBase(BaseModel):
    """Model representing an updateStokHarian (daily stock update)."""
    id_menu: int = Field(..., description="ID of the menu item", nullable=False)
    jumlah_porsi: int = Field(..., description="Number of portions updated", nullable=False)
    tanggal_update: datetime = Field(default_factory=datetime.now, description="Date and time of the update", nullable=False)

class UpdateStokHarianCreate(UpdateStokHarianBase):
    """Model for creating a new updateStokHarian."""
    pass

class UpdateStokHarianUpdate(BaseModel):
    """Model for updating an existing updateStokHarian."""
    id_menu: Optional[int] = Field(None, description="ID of the menu item", nullable=False)
    jumlah_porsi: Optional[int] = Field(None, description="Number of portions updated", nullable=False)
    tanggal_update: Optional[datetime] = Field(None, description="Date and time of the update", nullable=False)

class UpdateStokHarianResponse(UpdateStokHarianBase):
    """Model representing an updateStokHarian in the database with ID."""
    id: int = Field(..., description="Unique identifier for the updateStokHarian")

    model_config = ConfigDict(
        from_attributes=True
    )
