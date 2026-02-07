"""Detail Pesanan Routes Module."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.pesanan.detail_pesanan.detail_pesanan_service import (
    create_detail_pesanan,
    get_all_detail_pesanan,
    update_detail_pesanan,
    delete_detail_pesanan,
    get_detail_pesanan_by_id
)
from app.models.pesanan.detail_pesanan.detail_pesanan_model import (
    DetailPesananCreate,
    DetailPesananUpdate,
    DetailPesananResponse,
)
from app.core.deps import get_db
router = APIRouter(
    prefix="/detail-pesanan",
    tags=["Detail Pesanan"],
)

"""Detail Pesanan Routes Create"""
@router.post("/", response_model=DetailPesananResponse)
def create_detail_pesanan_route(detail_pesanan: DetailPesananCreate, db:
    Session = Depends(get_db)):
    """Create a new detail pesanan."""
    return create_detail_pesanan(db, detail_pesanan)

@router.get("/", response_model=list[DetailPesananResponse])
def read_detail_pesanan(db: Session = Depends(get_db)):
    """Read all detail pesanan."""
    return get_all_detail_pesanan(db)

@router.put("/{detail_pesanan_id}", response_model=DetailPesananResponse)
def update_detail_pesanan_route(detail_pesanan_id: int, detail_pesanan
    : DetailPesananUpdate, db: Session = Depends(get_db)):
    """Update a detail pesanan by ID."""
    return update_detail_pesanan(db, detail_pesanan_id, detail_pesanan)

@router.delete("/{detail_pesanan_id}")
def delete_detail_pesanan_route(detail_pesanan_id: int, db: Session =
    Depends(get_db)):
    delete_detail_pesanan(db, detail_pesanan_id)
    return {"message": "Detail Pesanan deleted successfully"}

@router.get("/{detail_pesanan_id}", response_model=DetailPesananResponse)
def read_detail_pesanan_by_id(detail_pesanan_id: int, db: Session
    = Depends(get_db)):
    return get_detail_pesanan_by_id(db, detail_pesanan_id)

