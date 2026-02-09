"""Pesanan Service Module."""

from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.pesanan.pesanan_model import PesananCreate, PesananUpdate
from orm_models import Pesanan, DetailPesanan, Transaksi


def create_pesanan(db: Session, pesanan_data: PesananCreate) -> Pesanan:
    """
    Create a new pesanan (order) record along with its details.
    
    This service handles the creation of a transaction (Transaksi) first,
    then the order, and finally the nested order items.
    """
    # 1. Buat Transaksi induk terlebih dahulu
    new_transaksi = Transaksi()
    db.add(new_transaksi)
    db.flush()  # Dapatkan ID transaksi tanpa commit dulu

    # 2. Persiapkan data Pesanan
    # Kita pisahkan 'items' dari model_dump karena 'items' adalah DetailPesanan
    data = pesanan_data.model_dump(exclude={"items"})
    new_pesanan = Pesanan(
        **data,
        id_transaksi=new_transaksi.id
    )
    db.add(new_pesanan)
    db.flush()

    # 3. Tambahkan Detail Pesanan (items)
    for item in pesanan_data.items:
        detail = DetailPesanan(
            id_pesanan=new_pesanan.id,
            id_menu=item["id_menu"],
            qty=item["qty"],
            harga_satuan=item["harga_satuan"],
            subtotal=item["subtotal"]
        )
        db.add(detail)

    db.commit()
    db.refresh(new_pesanan)
    
    # Return dengan eager load agar data lengkap
    return get_pesanan_by_id(db, new_pesanan.id)


def get_all_pesanan(db: Session) -> List[Pesanan]:
    """
    Retrieve all pesanan records with joined relations for FE needs.
    """
    return db.query(Pesanan).options(
        joinedload(Pesanan.meja),
        joinedload(Pesanan.user),
        joinedload(Pesanan.detail_pesanan).joinedload(DetailPesanan.menu)
    ).all()


def get_pesanan_by_id(db: Session, pesanan_id: int) -> Optional[Pesanan]:
    """
    Retrieve a single pesanan record by its ID with full details.
    """
    return db.query(Pesanan).options(
        joinedload(Pesanan.meja),
        joinedload(Pesanan.user),
        joinedload(Pesanan.detail_pesanan).joinedload(DetailPesanan.menu)
    ).filter(Pesanan.id == pesanan_id).first()


def update_pesanan(db: Session, pesanan_id: int, pesanan_update: PesananUpdate) -> Optional[Pesanan]:
    """
    Update an existing pesanan status or other basic fields.
    """
    pesanan = db.query(Pesanan).filter(Pesanan.id == pesanan_id).first()
    if not pesanan:
        return None
        
    update_data = pesanan_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(pesanan, key, value)
        
    db.commit()
    db.refresh(pesanan)
    return get_pesanan_by_id(db, pesanan.id)


def delete_pesanan(db: Session, pesanan_id: int) -> Optional[Pesanan]:
    """
    Delete a pesanan record. Note: This will usually cascade delete 
    details if configured in ORM.
    """
    pesanan = get_pesanan_by_id(db, pesanan_id)
    if not pesanan:
        return None
        
    db.delete(pesanan)
    db.commit()
    return pesanan