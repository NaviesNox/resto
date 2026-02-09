"""DetailPesanan Service Module."""

from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.pesanan.detail_pesanan.detail_pesanan_model import DetailPesananCreate, DetailPesananUpdate
from orm_models import DetailPesanan


def create_detail_pesanan(db: Session, detail_pesanan: DetailPesananCreate) -> DetailPesanan:
    """
    Create a new detail_pesanan (order details) record in the database.
    """
    new_detail_pesanan = DetailPesanan(**detail_pesanan.model_dump())
    db.add(new_detail_pesanan)
    db.commit()
    db.refresh(new_detail_pesanan)
    
    # Mengembalikan dengan informasi menu untuk kebutuhan UI
    return get_detail_pesanan_by_id(db, new_detail_pesanan.id)


def get_all_detail_pesanan(db: Session) -> List[DetailPesanan]:
    """
    Retrieve all detail_pesanan records with menu information.
    """
    return db.query(DetailPesanan).options(
        joinedload(DetailPesanan.menu)
    ).all()


def get_detail_pesanan_by_id(db: Session, detail_pesanan_id: int) -> Optional[DetailPesanan]:
    """
    Retrieve a detail_pesanan record by its ID with menu information.
    """
    return db.query(DetailPesanan).options(
        joinedload(DetailPesanan.menu)
    ).filter(DetailPesanan.id == detail_pesanan_id).first()


def update_detail_pesanan(db: Session, detail_pesanan_id: int, detail_pesanan_update: DetailPesananUpdate) -> Optional[DetailPesanan]:
    """
    Update an existing detail_pesanan record.
    """
    detail_pesanan = db.query(DetailPesanan).filter(DetailPesanan.id == detail_pesanan_id).first()
    if not detail_pesanan:
        return None
        
    update_data = detail_pesanan_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(detail_pesanan, key, value)
        
    db.commit()
    db.refresh(detail_pesanan)
    return get_detail_pesanan_by_id(db, detail_pesanan.id)


def delete_detail_pesanan(db: Session, detail_pesanan_id: int) -> Optional[DetailPesanan]:
    """
    Delete a detail_pesanan record.
    """
    detail_pesanan = get_detail_pesanan_by_id(db, detail_pesanan_id)
    if not detail_pesanan:
        return None
        
    db.delete(detail_pesanan)
    db.commit()
    return detail_pesanan