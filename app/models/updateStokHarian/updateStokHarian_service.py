"""UpdateStokHarian Service Module."""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.updateStokHarian.updateStokHarian_model import UpdateStokHarianCreate, UpdateStokHarianUpdate
from orm_models import updateStokHarian


def create_update_stok_harian(db: Session, update_stok: UpdateStokHarianCreate) -> updateStokHarian:
    """
    Create a new updateStokHarian (daily stock update) record in the database.

    Args:
        db (Session): The database session.
        update_stok (UpdateStokHarianCreate): The updateStokHarian data to create.

    Returns:
        updateStokHarian: The created updateStokHarian instance.
    """
    new_update_stok = updateStokHarian(**update_stok.model_dump())
    db.add(new_update_stok)
    db.commit()
    db.refresh(new_update_stok)
    return new_update_stok


def get_all_update_stok_harian(db: Session) -> List[updateStokHarian]:
    """
    Retrieve all updateStokHarian (daily stock update) records from the database.

    Args:
        db (Session): The database session.

    Returns:
        List[updateStokHarian]: A list of all updateStokHarian instances.
    """
    return db.query(updateStokHarian).all()


def get_update_stok_harian_by_id(db: Session, update_stok_id: int) -> Optional[updateStokHarian]:
    """
    Retrieve a updateStokHarian (daily stock update) record by its ID.

    Args:
        db (Session): The database session.
        update_stok_id (int): The ID of the updateStokHarian to retrieve.

    Returns:
        Optional[updateStokHarian]: The updateStokHarian instance if found, None otherwise.
    """
    return db.query(updateStokHarian).filter(updateStokHarian.id == update_stok_id).first()


def update_update_stok_harian(db: Session, update_stok_id: int, update_stok_update: UpdateStokHarianUpdate) -> Optional[updateStokHarian]:
    """
    Update an existing updateStokHarian (daily stock update) record.

    Args:
        db (Session): The database session.
        update_stok_id (int): The ID of the updateStokHarian to update.
        update_stok_update (UpdateStokHarianUpdate): The updated updateStokHarian data.

    Returns:
        Optional[updateStokHarian]: The updated updateStokHarian instance if found, None otherwise.
    """
    update_stok = get_update_stok_harian_by_id(db, update_stok_id)
    if not update_stok:
        return None
    update_data = update_stok_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(update_stok, key, value)
    db.commit()
    db.refresh(update_stok)
    return update_stok


def delete_update_stok_harian(db: Session, update_stok_id: int) -> Optional[updateStokHarian]:
    """
    Delete a updateStokHarian (daily stock update) record from the database.

    Args:
        db (Session): The database session.
        update_stok_id (int): The ID of the updateStokHarian to delete.

    Returns:
        Optional[updateStokHarian]: The deleted updateStokHarian instance if found, None otherwise.
    """
    update_stok = get_update_stok_harian_by_id(db, update_stok_id)
    if not update_stok:
        return None
    db.delete(update_stok)
    db.commit()
    return update_stok
