"""Routes untuk kategori menu."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.kategori_menu.kategori_menu_service import (
    create_kategori_menu,
    get_kategori_menu,
    update_kategori_menu,
    delete_kategori_menu,
    list_kategori_menus,
)
from app.models.kategori_menu.kategori_menu_model import (
    KategoriMenuCreate,
    KategoriMenuUpdate,
    KategoriMenuResponse,
)
from app.core.deps import get_db
router = APIRouter(
    prefix="/kategori_menu",
    tags=["Kategori Menu"],
)

@router.post("/", response_model=KategoriMenuResponse)
def create_kategori_menu_route(
    kategori_menu: KategoriMenuCreate,
    db: Session = Depends(get_db),
):
    """Route untuk membuat kategori menu baru."""
    return create_kategori_menu(db, kategori_menu)

@router.get("/{kategori_menu_id}", response_model=KategoriMenuResponse)
def get_kategori_menu_route(
    kategori_menu_id: int,
    db: Session = Depends(get_db),
):
    """Route untuk mendapatkan kategori menu berdasarkan ID."""
    db_kategori_menu = get_kategori_menu(db, kategori_menu_id)
    if db_kategori_menu is None:
        raise HTTPException(status_code=404, detail="Kategori menu tidak ditemukan")
    return db_kategori_menu

@router.put("/{kategori_menu_id}", response_model=KategoriMenuResponse)
def update_kategori_menu_route(
    kategori_menu_id: int,
    kategori_menu: KategoriMenuUpdate,
    db: Session = Depends(get_db),
):
    """Route untuk memperbarui kategori menu berdasarkan ID."""
    db_kategori_menu = update_kategori_menu(db, kategori_menu_id, kategori_menu)
    if db_kategori_menu is None:
        raise HTTPException(status_code=404, detail="Kategori menu tidak ditemukan")
    return db_kategori_menu

@router.delete("/{kategori_menu_id}")
def delete_kategori_menu_route(
    kategori_menu_id: int,
    db: Session = Depends(get_db),
):
    """Route untuk menghapus kategori menu berdasarkan ID."""
    success = delete_kategori_menu(db, kategori_menu_id)
    if not success:
        raise HTTPException(status_code=404, detail="Kategori menu tidak ditemukan")
    return {"detail": "Kategori menu berhasil dihapus"}

@router.get("/", response_model=list[KategoriMenuResponse])
def list_kategori_menus_route(
    db: Session = Depends(get_db),
):
    """Route untuk mendapatkan daftar semua kategori menu."""
    return list_kategori_menus(db)

