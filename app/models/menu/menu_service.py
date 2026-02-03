"""Menu Service Module."""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.menu.menu_model import MenuCreate, MenuUpdate
from orm_models import Menu


def create_menu(db: Session, menu: MenuCreate) -> Menu:
    """
    Create a new menu item record in the database.

    Args:
        db (Session): The database session.
        menu (MenuCreate): The menu data to create.

    Returns:
        Menu: The created menu instance.
    """
    menu_data = menu.model_dump()
    menu_data['id_kategori_menu'] = menu_data.pop('kategori')
    new_menu = Menu(**menu_data)
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
    if 'kategori' in update_data:
        update_data['id_kategori_menu'] = update_data.pop('kategori')
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
