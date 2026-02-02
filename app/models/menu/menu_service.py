"""Menu Service Module."""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.menu.menu_model import MenuCreate, MenuUpdate, MenuCreateWithFile
from orm_models import Menu
import os
from pathlib import Path
from fastapi import UploadFile


def create_menu(db: Session, menu: MenuCreate) -> Menu:
    """
    Create a new menu item record in the database.

    Args:
        db (Session): The database session.
        menu (MenuCreate): The menu data to create.

    Returns:
        Menu: The created menu instance.
    """
    new_menu = Menu(**menu.model_dump())
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    return new_menu


def get_all_menu(db: Session) -> List[Menu]:
    """
    Retrieve all menu item records from the database.

    Args:
        db (Session): The database session.

    Returns:
        List[Menu]: A list of all menu instances.
    """
    return db.query(Menu).all()


def get_menu_by_id(db: Session, menu_id: int) -> Optional[Menu]:
    """
    Retrieve a menu item record by its ID.

    Args:
        db (Session): The database session.
        menu_id (int): The ID of the menu to retrieve.

    Returns:
        Optional[Menu]: The menu instance if found, None otherwise.
    """
    return db.query(Menu).filter(Menu.id == menu_id).first()


def update_menu(db: Session, menu_id: int, menu_update: MenuUpdate) -> Optional[Menu]:
    """
    Update an existing menu item record.

    Args:
        db (Session): The database session.
        menu_id (int): The ID of the menu to update.
        menu_update (MenuUpdate): The updated menu data.

    Returns:
        Optional[Menu]: The updated menu instance if found, None otherwise.
    """
    menu = get_menu_by_id(db, menu_id)
    if not menu:
        return None
    update_data = menu_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(menu, key, value)
    db.commit()
    db.refresh(menu)
    return menu


def delete_menu(db: Session, menu_id: int) -> Optional[Menu]:
    """
    Delete a menu item record from the database.

    Args:
        db (Session): The database session.
        menu_id (int): The ID of the menu to delete.

    Returns:
        Optional[Menu]: The deleted menu instance if found, None otherwise.
    """
    menu = get_menu_by_id(db, menu_id)
    if not menu:
        return None
    db.delete(menu)
    db.commit()
    return menu


def save_upload_file(file: UploadFile, destination_folder: str = "uploads/menu") -> str:
    """
    Save uploaded file to the filesystem.

    Args:
        file (UploadFile): The uploaded file object.
        destination_folder (str): The folder path to save the file.

    Returns:
        str: The filename that was saved.

    Raises:
        ValueError: If file type is not allowed.
    """
    # Define allowed file extensions
    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
    
    # Create destination folder if it doesn't exist
    Path(destination_folder).mkdir(parents=True, exist_ok=True)
    
    # Check file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"File type {file_ext} is not allowed. Allowed types: {ALLOWED_EXTENSIONS}")
    
    # Create unique filename with timestamp
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
    filename = timestamp + file.filename
    filepath = os.path.join(destination_folder, filename)
    
    # Save file
    with open(filepath, "wb") as buffer:
        buffer.write(file.file.read())
    
    return filename


def create_menu_with_file(db: Session, menu_data: MenuCreateWithFile, file: Optional[UploadFile] = None) -> Menu:
    """
    Create a new menu item with optional file upload.

    Args:
        db (Session): The database session.
        menu_data (MenuCreateWithFile): The menu data to create.
        file (Optional[UploadFile]): The uploaded file for the menu photo.

    Returns:
        Menu: The created menu instance.

    Raises:
        ValueError: If file validation fails.
    """
    # Save file if provided
    foto_filename = None
    if file:
        foto_filename = save_upload_file(file)
    
    # Create menu object
    new_menu = Menu(
        nama_menu=menu_data.nama_menu,
        kategori=menu_data.kategori,
        harga=menu_data.harga,
        stok=menu_data.stok,
        id_kategori_menu=menu_data.kategori,
        foto=foto_filename
    )
    
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    return new_menu
