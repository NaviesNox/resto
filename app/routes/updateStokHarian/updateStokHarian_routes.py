"""Routes for updating daily stock  """

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.updateStokHarian.updateStokHarian_service import (
    create_update_stok_harian,
    get_all_update_stok_harian,
    get_update_stok_harian_by_id,
    update_update_stok_harian,
    delete_update_stok_harian,

)
from app.models.updateStokHarian.updateStokHarian_model import (    
    UpdateStokHarianUpdate,
    UpdateStokHarianResponse,
    UpdateStokHarianCreate,
    UpdateStokHarianInDB

)

from app.core.deps import get_db
router = APIRouter(
    prefix="/update_stok_harian",
    tags=["Update Stok Harian"],
)

@router.post("/", response_model=UpdateStokHarianResponse)
def create_stok_harian_route(
    update_stok_harian_data: UpdateStokHarianUpdate,
    db: Session = Depends(get_db),
):
    """Route untuk membuat update stok harian baru."""
    return create_update_stok_harian(db, update_stok_harian_data)

@router.get("/", response_model=list[UpdateStokHarianResponse])
def list_stok_harian_route(
    db: Session = Depends(get_db),
):
    """Route untuk mendapatkan semua data stok harian."""
    return get_all_update_stok_harian(db)


@router.get("/{update_stok_harian_id}", response_model=UpdateStokHarianResponse)
def get_stok_harian_route(
    update_stok_harian_id: int,
    db: Session = Depends(get_db),
):
    """Route untuk mendapatkan stok harian berdasarkan ID."""
    db_update_stok_harian = get_update_stok_harian_by_id(db, update_stok_harian_id)
    if db_update_stok_harian is None:
        raise HTTPException(status_code=404, detail="Update Stok Harian tidak ditemukan")
    return db_update_stok_harian


@router.put("/{update_stok_harian_id}", response_model=UpdateStokHarianResponse)
def update_stok_harian_route(
    update_stok_harian_id: int,
    update_stok_harian_data: UpdateStokHarianUpdate,
    db: Session = Depends(get_db),
):
    """Route untuk memperbarui stok harian berdasarkan ID."""
    db_update_stok_harian = update_update_stok_harian(db, update_stok_harian_id, update_stok_harian_data)
    if db_update_stok_harian is None:
        raise HTTPException(status_code=404, detail="Update Stok Harian tidak ditemukan")
    return db_update_stok_harian

@router.delete("/{update_stok_harian_id}")
def delete_stok_harian_route(
    update_stok_harian_id: int,
    db: Session = Depends(get_db),
):
    """Route untuk menghapus stok harian berdasarkan ID."""
    success = delete_update_stok_harian(db, update_stok_harian_id)
    if not success:
        raise HTTPException(status_code=404, detail="Update Stok Harian tidak ditemukan")
    return {"message": "Update Stok Harian berhasil dihapus"}

