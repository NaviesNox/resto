"""DetailPesanan Service Module."""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.pesanan.detail_pesanan.detail_pesanan_model import DetailPesananCreate, DetailPesananUpdate
from orm_models import DetailPesanan


def create_detail_pesanan(db: Session, detail_pesanan: DetailPesananCreate) -> DetailPesanan:
    """
    Create a new detail_pesanan (order details) record in the database.

    Args:
        db (Session): The database session.
        detail_pesanan (DetailPesananCreate): The detail_pesanan data to create.

    Returns:
        DetailPesanan: The created detail_pesanan instance.
    """
    new_detail_pesanan = DetailPesanan(**detail_pesanan.model_dump())
    db.add(new_detail_pesanan)
    db.commit()
    db.refresh(new_detail_pesanan)
    return new_detail_pesanan


def get_all_detail_pesanan(db: Session) -> List[DetailPesanan]:
    """
    Retrieve all detail_pesanan (order details) records from the database.

    Args:
        db (Session): The database session.

    Returns:
        List[DetailPesanan]: A list of all detail_pesanan instances.
    """
    return db.query(DetailPesanan).all()


def get_detail_pesanan_by_id(db: Session, detail_pesanan_id: int) -> Optional[DetailPesanan]:
    """
    Retrieve a detail_pesanan (order details) record by its ID.

    Args:
        db (Session): The database session.
        detail_pesanan_id (int): The ID of the detail_pesanan to retrieve.

    Returns:
        Optional[DetailPesanan]: The detail_pesanan instance if found, None otherwise.
    """
    return db.query(DetailPesanan).filter(DetailPesanan.id == detail_pesanan_id).first()


def update_detail_pesanan(db: Session, detail_pesanan_id: int, detail_pesanan_update: DetailPesananUpdate) -> Optional[DetailPesanan]:
    """
    Update an existing detail_pesanan (order details) record.

    Args:
        db (Session): The database session.
        detail_pesanan_id (int): The ID of the detail_pesanan to update.
        detail_pesanan_update (DetailPesananUpdate): The updated detail_pesanan data.

    Returns:
        Optional[DetailPesanan]: The updated detail_pesanan instance if found, None otherwise.
    """
    detail_pesanan = get_detail_pesanan_by_id(db, detail_pesanan_id)
    if not detail_pesanan:
        return None
    update_data = detail_pesanan_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(detail_pesanan, key, value)
    db.commit()
    db.refresh(detail_pesanan)
    return detail_pesanan


def delete_detail_pesanan(db: Session, detail_pesanan_id: int) -> Optional[DetailPesanan]:
    """
    Delete a detail_pesanan (order details) record from the database.

    Args:
        db (Session): The database session.
        detail_pesanan_id (int): The ID of the detail_pesanan to delete.

    Returns:
        Optional[DetailPesanan]: The deleted detail_pesanan instance if found, None otherwise.
    """
    detail_pesanan = get_detail_pesanan_by_id(db, detail_pesanan_id)
    if not detail_pesanan:
        return None
    db.delete(detail_pesanan)
    db.commit()
    return detail_pesanan
