"""Pesanan ROutes"""

from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.models.pesanan.pesanan_service import (
    create_pesanan,
    get_all_pesanan,
    update_pesanan,
    delete_pesanan,
    get_pesanan_by_id
)
from app.models.pesanan.pesanan_model import (
    PesananCreate,
    PesananUpdate,
    PesananResponse,
)
from app.core.deps import get_db
from fastapi import Depends, HTTPException

router = APIRouter(
    prefix="/pesanan",
    tags=["Pesanan"],
)
"""Pesanan Routes"""
@router.post("/", response_model=PesananResponse)
def create_pesanan_route(pesanan: PesananCreate, db: Session = Depends(get_db)):
    """Create a new pesanan."""
    return create_pesanan(db, pesanan)

@router.get("/", response_model=list[PesananResponse])
def read_pesanan(db: Session = Depends(get_db)):
    """Read all pesanan."""
    return get_all_pesanan(db)

@router.put("/{pesanan_id}", response_model=PesananResponse)
def update_pesanan_route(pesanan_id: int, pesanan: PesananUpdate, db: Session = Depends(get_db)):
    """Update a pesanan by ID."""
    return update_pesanan(db, pesanan_id, pesanan)

@router.delete("/{pesanan_id}")
def delete_pesanan_route(pesanan_id: int, db: Session = Depends(get_db)):
    delete_pesanan(db, pesanan_id)
    return {"message": "Pesanan deleted successfully"}

@router.get("/{pesanan_id}", response_model=PesananResponse)
def read_pesanan_by_id(pesanan_id: int, db: Session = Depends(get_db)):
    return get_pesanan_by_id(db, pesanan_id)