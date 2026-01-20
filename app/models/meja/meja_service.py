"""Meja Service Module."""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.meja.meja_model import MejaCreate, MejaUpdate
from orm_models import Meja


def create_meja(db: Session, meja: MejaCreate) -> Meja:
    """
    Create a new meja (table) record in the database.

    Args:
        db (Session): The database session.
        meja (MejaCreate): The meja data to create.

    Returns:
        Meja: The created meja instance.
    """
    new_meja = Meja(**meja.model_dump())
    db.add(new_meja)
    db.commit()
    db.refresh(new_meja)
    return new_meja


def get_all_meja(db: Session) -> List[Meja]:
    """
    Retrieve all meja (table) records from the database.

    Args:
        db (Session): The database session.

    Returns:
        List[Meja]: A list of all meja instances.
    """
    return db.query(Meja).all()


def get_meja_by_id(db: Session, meja_id: int) -> Optional[Meja]:
    """
    Retrieve a meja (table) record by its ID.

    Args:
        db (Session): The database session.
        meja_id (int): The ID of the meja to retrieve.

    Returns:
        Optional[Meja]: The meja instance if found, None otherwise.
    """
    return db.query(Meja).filter(Meja.id == meja_id).first()


def update_meja(db: Session, meja_id: int, meja_update: MejaUpdate) -> Optional[Meja]:
    """
    Update an existing meja (table) record.

    Args:
        db (Session): The database session.
        meja_id (int): The ID of the meja to update.
        meja_update (MejaUpdate): The updated meja data.

    Returns:
        Optional[Meja]: The updated meja instance if found, None otherwise.
    """
    meja = get_meja_by_id(db, meja_id)
    if not meja:
        return None
    update_data = meja_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(meja, key, value)
    db.commit()
    db.refresh(meja)
    return meja


def delete_meja(db: Session, meja_id: int) -> Optional[Meja]:
    """
    Delete a meja (table) record from the database.

    Args:
        db (Session): The database session.
        meja_id (int): The ID of the meja to delete.

    Returns:
        Optional[Meja]: The deleted meja instance if found, None otherwise.
    """
    meja = get_meja_by_id(db, meja_id)
    if not meja:
        return None
    db.delete(meja)
    db.commit()
    return meja
