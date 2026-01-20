"""Pembayaran Service Module."""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.pembayaran.pembayaran_model import PembayaranCreate, PembayaranUpdate
from orm_models import Pembayaran


def create_pembayaran(db: Session, pembayaran: PembayaranCreate) -> Pembayaran:
    """
    Create a new pembayaran (payment) record in the database.

    Args:
        db (Session): The database session.
        pembayaran (PembayaranCreate): The pembayaran data to create.

    Returns:
        Pembayaran: The created pembayaran instance.
    """
    new_pembayaran = Pembayaran(**pembayaran.model_dump())
    db.add(new_pembayaran)
    db.commit()
    db.refresh(new_pembayaran)
    return new_pembayaran


def get_all_pembayaran(db: Session) -> List[Pembayaran]:
    """
    Retrieve all pembayaran (payment) records from the database.

    Args:
        db (Session): The database session.

    Returns:
        List[Pembayaran]: A list of all pembayaran instances.
    """
    return db.query(Pembayaran).all()


def get_pembayaran_by_id(db: Session, pembayaran_id: int) -> Optional[Pembayaran]:
    """
    Retrieve a pembayaran (payment) record by its ID.

    Args:
        db (Session): The database session.
        pembayaran_id (int): The ID of the pembayaran to retrieve.

    Returns:
        Optional[Pembayaran]: The pembayaran instance if found, None otherwise.
    """
    return db.query(Pembayaran).filter(Pembayaran.id == pembayaran_id).first()


def update_pembayaran(db: Session, pembayaran_id: int, pembayaran_update: PembayaranUpdate) -> Optional[Pembayaran]:
    """
    Update an existing pembayaran (payment) record.

    Args:
        db (Session): The database session.
        pembayaran_id (int): The ID of the pembayaran to update.
        pembayaran_update (PembayaranUpdate): The updated pembayaran data.

    Returns:
        Optional[Pembayaran]: The updated pembayaran instance if found, None otherwise.
    """
    pembayaran = get_pembayaran_by_id(db, pembayaran_id)
    if not pembayaran:
        return None
    update_data = pembayaran_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(pembayaran, key, value)
    db.commit()
    db.refresh(pembayaran)
    return pembayaran


def delete_pembayaran(db: Session, pembayaran_id: int) -> Optional[Pembayaran]:
    """
    Delete a pembayaran (payment) record from the database.

    Args:
        db (Session): The database session.
        pembayaran_id (int): The ID of the pembayaran to delete.

    Returns:
        Optional[Pembayaran]: The deleted pembayaran instance if found, None otherwise.
    """
    pembayaran = get_pembayaran_by_id(db, pembayaran_id)
    if not pembayaran:
        return None
    db.delete(pembayaran)
    db.commit()
    return pembayaran
