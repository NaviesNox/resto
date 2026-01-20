"""Karyawan Service Module."""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.karyawan.karyawan_model import KaryawanCreate, KaryawanUpdate
from orm_models import Karyawan
""" Function untuk tambah data karyawan """
def create_karyawan(db: Session, karyawan: KaryawanCreate) -> Karyawan:
    """Create a new karyawan record in the database."""
    new_karyawan = Karyawan(**karyawan.model_dump())
    db.add(new_karyawan)
    db.commit()
    db.refresh(new_karyawan)
    return new_karyawan

""" Function untuk ambil data karyawan """
def get_all_karyawan(db: Session) -> List[Karyawan]:
    """Retrieve all karyawan records from the database."""
    return db.query(Karyawan).all()

""" Function untuk ambil data karyawan berdasarkan ID """
def get_karyawan_by_id(db: Session, karyawan_id: int) -> Optional[Karyawan]:
    """Retrieve a karyawan record by its ID."""
    return db.query(Karyawan).filter(Karyawan.id == karyawan_id).first()

""" Function untuk update data karyawan """
def update_karyawan(db: Session, karyawan_id: int, karyawan_update: KaryawanUpdate) -> Optional[Karyawan]:
    """Update an existing karyawan record."""
    karyawan = get_karyawan_by_id(db, karyawan_id)
    if not karyawan:
        return None
    update_data = karyawan_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(karyawan, key, value)
    db.commit()
    db.refresh(karyawan)
    return karyawan

""" Function untuk delete data karyawan """
def delete_karyawan(db: Session, karyawan_id: int) -> Optional[Karyawan]:
    """Delete a karyawan record from the database."""
    karyawan = get_karyawan_by_id(db, karyawan_id)
    if not karyawan:
        return None
    db.delete(karyawan)
    db.commit()
    return karyawan


