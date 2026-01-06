from sqlalchemy import Column, Integer, String, ForeignKey, Time, DateTime, Enum, Float, Text
from sqlalchemy.orm import relationship, declarative_base
import enum
from datetime import datetime
from app.core.database import Base

metadata = Base.metadata

class StatusMeja(enum.Enum):
    tersedia = "tersedia"
    booked = "booked"


class UserRole(enum.Enum):
    admin = "admin"
    pramusaji = "pramusaji"


class KategoriMenu(enum.Enum):
    makanan = "makanan"
    minuman = "minuman"
    makanan_ringan = "makanan_ringan"


class StatusPesanan(enum.Enum):
    dipesan = "dipesan"
    diproses = "diproses"
    selesai = "selesai"
    dibayar = "dibayar"
    dibatalkan = "dibatalkan"


class TipePesanan(enum.Enum):
    dine_in = "dine_in"
    takeaway = "takeaway"


class MetodePembayaran(enum.Enum):
    cash = "cash"
    qris = "qris"



class Meja(Base):
    __tablename__ = "meja"

    id = Column(Integer, primary_key=True, index=True)
    kode_meja = Column(String, unique=True, nullable=False)
    kapasitas = Column(Integer, nullable=False)
    lokasi = Column(String, nullable=False)
    status = Column(Enum(StatusMeja), default=StatusMeja.tersedia, nullable=False)

    pesanan = relationship("Pesanan", back_populates="meja")

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    nama = Column(String, nullable=False)
    no_telp = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.pramusaji, nullable=False)

    pesanan = relationship("Pesanan", back_populates="user")



class Menu(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, index=True)
    nama_menu = Column(String, unique=True, nullable=False)
    harga = Column(Float, nullable=False)
    stok = Column(Integer, nullable=False)
    kategori = Column(Enum(KategoriMenu), nullable=False)

    detail_pesanan = relationship("DetailPesanan", back_populates="menu")

class Transaksi(Base):
    __tablename__ = "transaksi"

    id = Column(Integer, primary_key=True, index=True)
    waktu = Column(DateTime, default=datetime.utcnow, nullable=False)

    pesanan = relationship("Pesanan", back_populates="transaksi")
    pembayaran = relationship("Pembayaran", back_populates="transaksi", uselist=False)


class Pesanan(Base):
    __tablename__ = "pesanan"

    id = Column(Integer, primary_key=True, index=True)

    id_transaksi = Column(Integer, ForeignKey("transaksi.id"), nullable=False)
    id_user = Column(Integer, ForeignKey("user.id"), nullable=False)
    id_meja = Column(Integer, ForeignKey("meja.id"), nullable=True)

    tipe_pesanan = Column(Enum(TipePesanan), nullable=False)
    kode_pesanan = Column(String, unique=True, nullable=False)

    tanggal = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(Enum(StatusPesanan), default=StatusPesanan.dipesan, nullable=False)
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
    id_pesanan = Column(Integer, ForeignKey("pesanan.id"), unique=True)
    metode = Column(Enum(MetodePembayaran), nullable=False)
    total = Column(Float, nullable=False)
    waktu_bayar = Column(DateTime, default=datetime.now)
    status = Column(String, default="lunas")
