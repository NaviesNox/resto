from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from typing import Optional, List
from datetime import datetime

# --- ENUMS (Harus Sama dengan orm_models.py) ---

class TipePesanan(str, Enum):
    dine_in = "dine-in"
    take_away = "take-away"

class StatusPesanan(str, Enum):
    baru = "baru"
    diproses = "diproses"
    siap = "siap"
    selesai = "selesai"
    batal = "batal"

# --- SCHEMAS ---

class DetailPesananSchema(BaseModel):
    id: int
    id_menu: int
    nama_menu: Optional[str] = None # Untuk kebutuhan FE menampilkan nama
    qty: int
    harga_satuan: float
    subtotal: float

    model_config = ConfigDict(from_attributes=True)

class PesananBase(BaseModel):
    id_transaksi: int
    id_user: int
    id_meja: Optional[int] = None
    tipe_pesanan: TipePesanan
    kode_pesanan: str
    tanggal: datetime
    status: StatusPesanan = StatusPesanan.baru
    catatan: Optional[str] = None

class PesananCreate(BaseModel):
    id_meja: Optional[int] = None
    tipe_pesanan: TipePesanan
    catatan: Optional[str] = None
    # detail_pesanan biasanya dikirim saat create
    items: List[dict] 

class PesananUpdate(BaseModel):
    status: Optional[StatusPesanan] = None
    id_meja: Optional[int] = None
    catatan: Optional[str] = None

class PesananResponse(PesananBase):
    id: int
    # Tambahan agar FE bisa langsung menampilkan teks tanpa mapping ID lagi
    nama_user: Optional[str] = None 
    kode_meja: Optional[str] = None
    detail_pesanan: List[DetailPesananSchema] = []

    model_config = ConfigDict(from_attributes=True)