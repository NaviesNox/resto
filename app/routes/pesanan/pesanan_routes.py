"""Pesanan ROutes"""

from fastapi import APIRouter
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.auth import get_current_user
from app.models.pesanan.pesanan_service import (
    create_pesanan,
    get_all_pesanan,
    update_pesanan,
    delete_pesanan,
    get_pesanan_by_id
)
from app.models.pesanan.pesanan_model import (
    CreatePesananRequest,
    PesananCreate,
    PesananUpdate,
    PesananResponse,
    StatusPesanan,
)
from app.core.deps import get_db
from fastapi import Depends, HTTPException

from orm_models import DetailPesanan, Meja, Menu, Pesanan, StatusMeja, TipePesanan, Transaksi

router = APIRouter(
    prefix="/pesanan",
    tags=["Pesanan"],
)
"""Pesanan Routes"""
@router.post("/", response_model=PesananResponse)
def create_pesanan_route(pesanan: PesananCreate, db: Session = Depends(get_db)):
    """Create a new pesanan."""
    return create_pesanan(db, pesanan)

@router.post("/buat")
def buat_pesanan(req: CreatePesananRequest, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    
    # 1. Validasi items tidak kosong
    if not req.items:
        raise HTTPException(status_code=400, detail="Minimal 1 item")
    
    # 2. Validasi meja jika dine-in
    if req.tipe_pesanan == "dine-in":
        if not req.id_meja:
            raise HTTPException(status_code=400, detail="Meja wajib untuk dine-in")
        meja = db.query(Meja).filter(Meja.id == req.id_meja).first()
        if not meja or meja.status != StatusMeja.tersedia:
            raise HTTPException(status_code=400, detail="Meja tidak tersedia")
    
    # 3. Validasi stok semua menu dulu sebelum insert apapun
    for item in req.items:
        menu = db.query(Menu).filter(Menu.id == item.id_menu).first()
        if not menu:
            raise HTTPException(status_code=404, detail=f"Menu id {item.id_menu} tidak ditemukan")
        if menu.stok < item.qty:
            raise HTTPException(status_code=400, detail=f"Stok {menu.nama_menu} tidak cukup")
    
    try:
        # 4. Buat transaksi
        transaksi = Transaksi(waktu=datetime.now())
        db.add(transaksi)
        db.flush()  # dapat transaksi.id tanpa commit
        
        # 5. Generate kode pesanan
        kode = f"PES-{datetime.now().strftime('%Y%m%d%H%M%S')}-{transaksi.id}"
        
        # 6. Buat pesanan
        pesanan = Pesanan(
            id_transaksi=transaksi.id,
            id_user=current_user.id,
            id_meja=req.id_meja,
            tipe_pesanan=TipePesanan(req.tipe_pesanan),
            kode_pesanan=kode,
            tanggal=datetime.now(),
            status=StatusPesanan.baru,
            catatan=req.catatan
        )
        db.add(pesanan)
        db.flush()  # dapat pesanan.id
        
        # 7. Buat detail pesanan + kurangi stok
        for item in req.items:
            detail = DetailPesanan(
                id_pesanan=pesanan.id,
                id_menu=item.id_menu,
                qty=item.qty,
                harga_satuan=item.harga_satuan,
                subtotal=item.qty * item.harga_satuan
            )
            db.add(detail)
            
            # Kurangi stok
            menu = db.query(Menu).filter(Menu.id == item.id_menu).first()
            menu.stok -= item.qty
        
        # 8. Update meja jika dine-in
        if req.tipe_pesanan == "dine-in" and req.id_meja:
            meja = db.query(Meja).filter(Meja.id == req.id_meja).first()
            meja.status = StatusMeja.terisi
        
        # 9. Commit semuanya sekaligus (atomic)
        db.commit()
        db.refresh(pesanan)
        
        return {
            "message": "Pesanan berhasil dibuat",
            "transaksi_id": transaksi.id,
            "pesanan_id": pesanan.id,
            "kode_pesanan": kode
        }
        
    except Exception as e:
        db.rollback()  # Kalau gagal, SEMUA dibatalkan
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=list[PesananResponse])
def read_pesanan(db: Session = Depends(get_db)):
    """Read all pesanan."""
    return get_all_pesanan(db)

@router.put("/{pesanan_id}", response_model=PesananResponse)
def update_pesanan_route(pesanan_id: int, pesanan: PesananUpdate, db: Session = Depends(get_db)):
    """Update a pesanan by ID."""
    return update_pesanan(db, pesanan_id, pesanan)

@router.delete("/{pesanan_id}")
def delete_pesanan_route(pesanan_id: int, db: Session = Depends(get_db)):
    delete_pesanan(db, pesanan_id)
    return {"message": "Pesanan deleted successfully"}

@router.get("/{pesanan_id}", response_model=PesananResponse)
def read_pesanan_by_id(pesanan_id: int, db: Session = Depends(get_db)):
    return get_pesanan_by_id(db, pesanan_id)