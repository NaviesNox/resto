"""Transaksi Service Module."""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.transaksi.transaksi_model import TransaksiCreate, TransaksiUpdate
from orm_models import Transaksi


def create_transaksi(db: Session, transaksi: TransaksiCreate) -> Transaksi:
    """
    Create a new transaksi (transaction) record in the database.

    Args:
        db (Session): The database session.
        transaksi (TransaksiCreate): The transaksi data to create.

    Returns:
        Transaksi: The created transaksi instance.
    """
    new_transaksi = Transaksi(**transaksi.model_dump())
    db.add(new_transaksi)
    db.commit()
    db.refresh(new_transaksi)
    return new_transaksi


def get_all_transaksi(db: Session) -> List[Transaksi]:
    """
    Retrieve all transaksi (transaction) records from the database.

    Args:
        db (Session): The database session.

    Returns:
        List[Transaksi]: A list of all transaksi instances.
    """
    return db.query(Transaksi).all()


def get_transaksi_by_id(db: Session, transaksi_id: int) -> Optional[Transaksi]:
    """
    Retrieve a transaksi (transaction) record by its ID.

    Args:
        db (Session): The database session.
        transaksi_id (int): The ID of the transaksi to retrieve.

    Returns:
        Optional[Transaksi]: The transaksi instance if found, None otherwise.
    """
    return db.query(Transaksi).filter(Transaksi.id == transaksi_id).first()


def update_transaksi(db: Session, transaksi_id: int, transaksi_update: TransaksiUpdate) -> Optional[Transaksi]:
    """
    Update an existing transaksi (transaction) record.

    Args:
        db (Session): The database session.
        transaksi_id (int): The ID of the transaksi to update.
        transaksi_update (TransaksiUpdate): The updated transaksi data.

    Returns:
        Optional[Transaksi]: The updated transaksi instance if found, None otherwise.
    """
    transaksi = get_transaksi_by_id(db, transaksi_id)
    if not transaksi:
        return None
    update_data = transaksi_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(transaksi, key, value)
    db.commit()
    db.refresh(transaksi)
    return transaksi


def delete_transaksi(db: Session, transaksi_id: int) -> Optional[Transaksi]:
    """
    Delete a transaksi (transaction) record from the database.

    Args:
        db (Session): The database session.
        transaksi_id (int): The ID of the transaksi to delete.

    Returns:
        Optional[Transaksi]: The deleted transaksi instance if found, None otherwise.
    """
    transaksi = get_transaksi_by_id(db, transaksi_id)
    if not transaksi:
        return None
    db.delete(transaksi)
    db.commit()
    return transaksi
