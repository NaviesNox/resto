"""Pesanan Service Module."""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.pesanan.pesanan_model import PesananCreate, PesananUpdate
from orm_models import Pesanan


def create_pesanan(db: Session, pesanan: PesananCreate) -> Pesanan:
    """
    Create a new pesanan (order) record in the database.

    Args:
        db (Session): The database session.
        pesanan (PesananCreate): The pesanan data to create.

    Returns:
        Pesanan: The created pesanan instance.
    """
    new_pesanan = Pesanan(**pesanan.model_dump())
    db.add(new_pesanan)
    db.commit()
    db.refresh(new_pesanan)
    return new_pesanan


def get_all_pesanan(db: Session) -> List[Pesanan]:
    """
    Retrieve all pesanan (order) records from the database.

    Args:
        db (Session): The database session.

    Returns:
        List[Pesanan]: A list of all pesanan instances.
    """
    return db.query(Pesanan).all()


def get_pesanan_by_id(db: Session, pesanan_id: int) -> Optional[Pesanan]:
    """
    Retrieve a pesanan (order) record by its ID.

    Args:
        db (Session): The database session.
        pesanan_id (int): The ID of the pesanan to retrieve.

    Returns:
        Optional[Pesanan]: The pesanan instance if found, None otherwise.
    """
    return db.query(Pesanan).filter(Pesanan.id == pesanan_id).first()


def update_pesanan(db: Session, pesanan_id: int, pesanan_update: PesananUpdate) -> Optional[Pesanan]:
    """
    Update an existing pesanan (order) record.

    Args:
        db (Session): The database session.
        pesanan_id (int): The ID of the pesanan to update.
        pesanan_update (PesananUpdate): The updated pesanan data.

    Returns:
        Optional[Pesanan]: The updated pesanan instance if found, None otherwise.
    """
    pesanan = get_pesanan_by_id(db, pesanan_id)
    if not pesanan:
        return None
    update_data = pesanan_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(pesanan, key, value)
    db.commit()
    db.refresh(pesanan)
    return pesanan


def delete_pesanan(db: Session, pesanan_id: int) -> Optional[Pesanan]:
    """
    Delete a pesanan (order) record from the database.

    Args:
        db (Session): The database session.
        pesanan_id (int): The ID of the pesanan to delete.

    Returns:
        Optional[Pesanan]: The deleted pesanan instance if found, None otherwise.
    """
    pesanan = get_pesanan_by_id(db, pesanan_id)
    if not pesanan:
        return None
    db.delete(pesanan)
    db.commit()
    return pesanan
