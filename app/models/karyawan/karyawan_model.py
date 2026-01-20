"""Mode karyawan"""

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
import enum

class KaryawanBase(BaseModel):
    """Model representing a karyawan (employee)."""
    nama_karyawan: str = Field(..., description="Full name of the employee", nullable=False)
    no_hp: str = Field(..., description="Phone number of the employee", nullable=False)
    alamat: str = Field(..., description="Address of the employee", nullable=False)

class KaryawanCreate(KaryawanBase):
    """Model for creating a new karyawan."""
    pass

class KaryawanUpdate(BaseModel):
    """Model for updating an existing karyawan."""
    nama_karyawan: Optional[str] = Field(None, description="Full name of the employee", nullable=False)
    no_hp: Optional[str] = Field(None, description="Phone number of the employee", nullable=False)
    alamat: Optional[str] = Field(None, description="Address of the employee", nullable=False)

class KaryawanResponse(KaryawanBase):
    """Model representing a karyawan in the database with ID."""
    id: int = Field(..., description="Unique identifier for the karyawan")

    model_config = ConfigDict(  
        from_attributes = True
    )