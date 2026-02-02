"""Menu Routes"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models.menu import menu_service
from app.models.menu.menu_model import MenuCreate, MenuUpdate, MenuResponse, MenuCreateWithFile
from typing import Optional

router = APIRouter(prefix="/menus", tags=["Menus"])
"""Ambil semua menu yang ada"""
@router.get("/", response_model=list[MenuResponse])
def list_menus(db: Session = Depends(get_db)):
    """Mengambil semua data menu."""
    return menu_service.get_all_menu(db)

"""Ambil menu by id"""
@router.get("/{id}", response_model=MenuResponse)
def get_menu(id: int, db:Session = Depends(get_db)):
    """Mengambil data menu berdasarkan id"""
    menu = menu_service.get_menu_by_id(db, id)
    if not menu: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu tidak ditemukan")
    return menu

"""Tambah menu baru"""
@router.post("/", response_model=MenuResponse, status_code=status.HTTP_201_CREATED)
def create_menu(menu: MenuCreate, db: Session = Depends(get_db)):
    """Menambahkan menu baru"""
    return menu_service.create_menu(db, menu)

"""Tambah menu dengan upload foto"""
@router.post("/upload", response_model=MenuResponse, status_code=status.HTTP_201_CREATED)
def create_menu_with_upload(
    nama_menu: str = Form(...),
    kategori: int = Form(...),
    harga: float = Form(...),
    stok: int = Form(...),
    foto: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """Menambahkan menu baru dengan upload foto"""
    try:
        menu_data = MenuCreateWithFile(
            nama_menu=nama_menu,
            kategori=kategori,
            harga=harga,
            stok=stok
        )
        return menu_service.create_menu_with_file(db, menu_data, foto)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

"""Update menu"""
@router.patch("/{id}", response_model=MenuResponse) 
def update_menu(id: int, menu_update: MenuUpdate, db: Session = Depends(get_db)):
    """Mengupdate data menu berdasarkan id"""
    menu = menu_service.get_menu_by_id(db, id)
    if not menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu tidak ditemukan")
    return menu_service.update_menu(db, id, menu_update)

"""Delete menu"""
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu(id: int, db: Session = Depends(get_db)):
    """Menghapus data menu berdasarkan id"""
    menu = menu_service.get_menu_by_id(db, id)
    if not menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu tidak ditemukan")
    menu_service.delete_menu(db, id)