from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Float, Text
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from app.core.database import Base

# --- ENUMS ---

class StatusMeja(enum.Enum):
    tersedia = "tersedia"
    terisi = "terisi"
    kosong = "kosong" # Sesuai dengan fetchAvailableMeja di frontend

class UserRole(enum.Enum):
    admin = "admin"
    pramusaji = "pramusaji"
    manager = "manager"
    kasir = "kasir"

class StatusPesanan(enum.Enum):
    # Disesuaikan dengan filterStatus di Vue: baru, diproses, siap, selesai, batal
    baru = "baru"
    diproses = "diproses"
    siap = "siap"
    selesai = "selesai"
    batal = "batal"

class TipePesanan(enum.Enum):
    dine_in = "dine-in" # Disesuaikan dengan value di Vue <option value="dine-in">
    take_away = "take-away"

class MetodePembayaran(enum.Enum):
    cash = "cash"
    qris = "qris"

class StatusUser(enum.Enum):
    active = "active"
    inactive = "inactive"

# --- TABLES ---

class Meja(Base):
    __tablename__ = "meja"
    id = Column(Integer, primary_key=True, index=True)
    kode_meja = Column(String, unique=True, nullable=False)
    kapasitas = Column(Integer, nullable=False)
    lokasi = Column(String, nullable=False)
    status = Column(Enum(StatusMeja), default=StatusMeja.tersedia, nullable=False)
    
    pesanan = relationship("Pesanan", back_populates="meja")

class Karyawan(Base):
    __tablename__ = "karyawan"
    id = Column(Integer, primary_key=True, index=True)
    nama_karyawan = Column(String, nullable=False)
    no_hp = Column(String, nullable=False)
    alamat = Column(String, nullable=False)
    user = relationship("User", back_populates="karyawan", uselist=False)

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.pramusaji, nullable=False)
    status = Column(Enum(StatusUser), default=StatusUser.active, nullable=True)
    id_karyawan = Column(Integer, ForeignKey("karyawan.id"), nullable=True)

    karyawan = relationship("Karyawan", back_populates="user")
    pesanan = relationship("Pesanan", back_populates="user")

class KategoriMenu(Base):
    __tablename__ = "kategori_menu"
    id = Column(Integer, primary_key=True, index=True)
    nama_kategori = Column(String, unique=True, nullable=False)
    menu = relationship("Menu", back_populates="kategori_obj")

class Menu(Base):
    __tablename__ = "menu"
    id = Column(Integer, primary_key=True, index=True)
    nama_menu = Column(String, unique=True, nullable=False)
    harga = Column(Float, nullable=False)
    stok = Column(Integer, nullable=False)
    id_kategori_menu = Column(Integer, ForeignKey("kategori_menu.id"), nullable=False)
    deskripsi = Column(Text, nullable=True)
    
    @property
    def kategori(self):
        return self.id_kategori_menu

    kategori_obj = relationship("KategoriMenu", back_populates="menu")
    detail_pesanan = relationship("DetailPesanan", back_populates="menu")
    update_stok_harian = relationship("UpdateStokHarian", back_populates="menu")

class UpdateStokHarian(Base):
    __tablename__ = "update_stok_harian"
    id = Column(Integer, primary_key=True, index=True)
    id_menu = Column(Integer, ForeignKey("menu.id"), nullable=False)
    jumlah_porsi = Column(Integer, nullable=False)
    tanggal_update = Column(DateTime, default=datetime.now, nullable=False)
    menu = relationship("Menu", back_populates="update_stok_harian")

class Transaksi(Base):
    __tablename__ = "transaksi"
    id = Column(Integer, primary_key=True, index=True)
    waktu = Column(DateTime, default=datetime.now, nullable=False)
    pesanan = relationship("Pesanan", back_populates="transaksi", uselist=False)
    pembayaran = relationship("Pembayaran", back_populates="transaksi", uselist=False)

class Pesanan(Base):
    __tablename__ = "pesanan"
    id = Column(Integer, primary_key=True, index=True)
    id_transaksi = Column(Integer, ForeignKey("transaksi.id"), nullable=False)
    id_user = Column(Integer, ForeignKey("user.id"), nullable=False)
    id_meja = Column(Integer, ForeignKey("meja.id"), nullable=True)
    
    tipe_pesanan = Column(Enum(TipePesanan), nullable=False)
    kode_pesanan = Column(String, unique=True, nullable=False)
    tanggal = Column(DateTime, default=datetime.now, nullable=False)
    status = Column(Enum(StatusPesanan), default=StatusPesanan.baru, nullable=False)
    catatan = Column(Text)

    transaksi = relationship("Transaksi", back_populates="pesanan")
    user = relationship("User", back_populates="pesanan")
    meja = relationship("Meja", back_populates="pesanan")
    detail_pesanan = relationship("DetailPesanan", back_populates="pesanan")

class DetailPesanan(Base):
    __tablename__ = "detail_pesanan"
    id = Column(Integer, primary_key=True, index=True)
    id_pesanan = Column(Integer, ForeignKey("pesanan.id"), nullable=False)
    id_menu = Column(Integer, ForeignKey("menu.id"), nullable=False)
    qty = Column(Integer, nullable=False)
    harga_satuan = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

    pesanan = relationship("Pesanan", back_populates="detail_pesanan")
    menu = relationship("Menu", back_populates="detail_pesanan")

class Pembayaran(Base):
    __tablename__ = "pembayaran"
    id = Column(Integer, primary_key=True)
    id_transaksi = Column(Integer, ForeignKey("transaksi.id"), unique=True, nullable=False)
    metode = Column(Enum(MetodePembayaran), nullable=False)
    total = Column(Float, nullable=False)
    waktu_bayar = Column(DateTime, default=datetime.now, nullable=False)
    status = Column(String, default="lunas")
    transaksi = relationship("Transaksi", back_populates="pembayaran")