"""Trasaksi Routes"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.transaksi.transaksi_service import (
    create_transaksi,
    get_all_transaksi,
    update_transaksi,
    delete_transaksi,
    get_transaksi_by_id
)   
from app.models.transaksi.transaksi_model import (
    TransaksiCreate,
    TransaksiUpdate,
    TransaksiResponse,
)
from app.core.deps import get_db

router = APIRouter(
    prefix="/transaksi",
    tags=["Transaksi"],
)


@router.post("/", response_model=TransaksiResponse)
def create_transaksi_route(
    trasaksi: TransaksiCreate,
    db: Session = Depends(get_db),
):
    """Route untuk membuat transaksi baru."""
    return create_transaksi(db, trasaksi)


@router.get("/{transaksi_id}", response_model=TransaksiResponse)
def get_transaksi_route(
    transaksi_id: int,
    db: Session = Depends(get_db),
):
    """Route untuk mendapatkan transaksi berdasarkan ID."""
    db_transaksi = get_transaksi_by_id(db, transaksi_id)
    if db_transaksi is None:
        raise HTTPException(status_code=404, detail="Transaksi tidak ditemukan")
    return db_transaksi

@router.put("/{transaksi_id}", response_model=TransaksiResponse)
def update_transaksi_route(
    transaksi_id: int,
    transaksi: TransaksiUpdate,
    db: Session = Depends(get_db),
):
    """Route untuk memperbarui transaksi berdasarkan
    ID."""
    db_transaksi = update_transaksi(db, transaksi_id, transaksi)
    if db_transaksi is None:
        raise HTTPException(status_code=404, detail="Transaksi tidak ditemukan")
    return db_transaksi

@router.delete("/{transaksi_id}")
def delete_transaksi_route(
    transaksi_id: int,
    db: Session = Depends(get_db),
):
    """Route untuk menghapus transaksi berdasarkan ID."""
    success = delete_transaksi(db, transaksi_id)
    if not success:
        raise HTTPException(status_code=404, detail="Transaksi tidak ditemukan")
    
    return {"detail": "Transaksi berhasil dihapus"}

@router.get("/", response_model=list[TransaksiResponse])
def list_transaksis_route(
    db: Session = Depends(get_db),
):
    """Route untuk mendapatkan daftar semua transaksi."""
    return get_all_transaksi(db)

