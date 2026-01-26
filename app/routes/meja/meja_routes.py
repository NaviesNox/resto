"""Meja Routes"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models.meja import meja_service
from app.models.meja.meja_model import MejaCreate, MejaUpdate, MejaResponse

router = APIRouter(prefix="/mejas", tags=["Mejas"])
"""ambil semua meja"""
@router.get("/", response_model=list[MejaResponse])
def list_mejas(db: Session = Depends(get_db)):
    """Mengambil semua data meja."""
    return meja_service.get_all_meja(db)

"""ambil meja by id"""
@router.get("/{id}", response_model=MejaResponse)
def get_meja(id: int, db: Session = Depends(get_db)):
    """Mengambil data meja berdasarkan ID."""
    meja = meja_service.get_meja_by_id(db, id)
    if not meja:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meja not found")
    return meja

"""tambah meja"""
@router.post("/", response_model=MejaResponse, status_code=status.HTTP_201_CREATED)
def create_meja(meja: MejaCreate, db: Session = Depends(get_db)):    
    return meja_service.create_meja(db, meja)

"""update meja"""
@router.patch("/{id}", response_model=MejaResponse)
def update_meja(id: int, meja_update: MejaUpdate, db: Session = Depends(get_db)):
    meja = meja_service.get_meja_by_id(db, id)
    if not meja:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meja not found")
    return meja_service.update_meja(db, id, meja_update)

"""delete meja"""
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_meja(id: int, db: Session = Depends(get_db)):
    meja = meja_service.get_meja_by_id(db, id)
    if not meja:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meja not found")
    meja_service.delete_meja(db, id)


