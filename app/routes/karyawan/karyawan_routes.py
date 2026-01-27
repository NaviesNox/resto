""" Karyawan Routes """
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models.karyawan import karyawan_service
from app.models.karyawan.karyawan_model import KaryawanCreate, KaryawanUpdate, KaryawanResponse as Karyawan

router = APIRouter(prefix="/karyawan", tags=["Karyawan"])
"""ambil semua karyawan"""
@router.get("/", response_model=list[Karyawan])
def list_karyawan(db: Session = Depends(get_db)):
    """Mengambil semua data karyawan."""
    return karyawan_service.get_all_karyawan(db)

"""ambil karyawan by id"""
@router.get("/{id}", response_model=Karyawan)
def get_karyawan(id: int, db: Session = Depends(get_db)):
    """Mengambil data karyawan berdasarkan ID."""
    karyawan = karyawan_service.get_karyawan_by_id(db, id)
    if not karyawan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Karyawan not found")
    return karyawan

"""tambah karyawan"""
@router.post("/", response_model=Karyawan, status_code=status.HTTP_201_CREATED)
def create_karyawan(karyawan: KaryawanCreate, db: Session = Depends(get_db)):
    return karyawan_service.create_karyawan(db, karyawan)

"""update karyawan"""
@router.patch("/{id}", response_model=Karyawan)
def update_karyawan(id: int, karyawan_update: KaryawanUpdate, db: Session = Depends(get_db)):
    karyawan = karyawan_service.get_karyawan_by_id(db, id)
    if not karyawan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Karyawan not found")
    return karyawan_service.update_karyawan(db, id, karyawan_update)

"""delete karyawan"""
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_karyawan(id: int, db: Session = Depends(get_db)):
    karyawan = karyawan_service.get_karyawan_by_id(db, id)
    if not karyawan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Karyawan not found")
    karyawan_service.delete_karyawan(db, id)
    return None

