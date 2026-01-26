"""Service for managing kategori menu items in the application."""
from sqlalchemy.orm import Session
from app.models.kategori_menu.kategori_menu_model import (
    KategoriMenuCreate,
    KategoriMenuUpdate,
    KategoriMenuDelete,
    KategoriMenuResponse,
)
from orm_models import KategoriMenu
def create_kategori_menu(db: Session, kategori_menu: KategoriMenuCreate) -> KategoriMenuResponse:
    """Create a new kategori menu item."""
    db_kategori_menu = KategoriMenu(nama_kategori=kategori_menu.nama_kategori)
    db.add(db_kategori_menu)
    db.commit()
    db.refresh(db_kategori_menu)
    return KategoriMenuResponse.from_orm(db_kategori_menu)

def get_kategori_menu(db: Session, kategori_menu_id: int) -> KategoriMenuResponse:
    """Retrieve a kategori menu item by its ID."""
    db_kategori_menu = db.query(KategoriMenu).filter(KategoriMenu.id == kategori_menu_id).first()
    if db_kategori_menu is None:
        return None
    return KategoriMenuResponse.from_orm(db_kategori_menu)

def update_kategori_menu(db: Session, kategori_menu_id: int, kategori_menu: KategoriMenuUpdate) -> KategoriMenuResponse:
    """Update an existing kategori menu item."""
    db_kategori_menu = db.query(KategoriMenu).filter(KategoriMenu.id == kategori_menu_id).first()
    if db_kategori_menu is None:
        return None
    if kategori_menu.nama_kategori is not None:
        db_kategori_menu.nama_kategori = kategori_menu.nama_kategori
    db.commit()
    db.refresh(db_kategori_menu)
    return KategoriMenuResponse.from_orm(db_kategori_menu)

def delete_kategori_menu(db: Session, kategori_menu_id: int) -> bool:
    """Delete a kategori menu item by its ID."""
    db_kategori_menu = db.query(KategoriMenu).filter(KategoriMenu.id == kategori_menu_id).first()
    if db_kategori_menu is None:
        return False
    db.delete(db_kategori_menu)
    db.commit()
    return True

def list_kategori_menus(db: Session) -> list[KategoriMenuResponse]:
    """List all kategori menu items."""
    db_kategori_menus = db.query(KategoriMenu).all()
    return [KategoriMenuResponse.from_orm(kategori_menu) for kategori_menu in db_kategori_menus]

