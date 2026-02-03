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
    manager = "manager"
    kasir = "kasir"


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

class statusUser(enum.Enum):
    active = "active"
    inactive = "inactive"



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
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.pramusaji, nullable=False)
    status = Column(Enum(statusUser), default=statusUser.active, nullable=True)
    id_karyawan = Column(Integer, ForeignKey("karyawan.id"), nullable=True)

    pesanan = relationship("Pesanan", back_populates="user")
    karyawan = relationship("Karyawan", back_populates="user", uselist=False)  # Tambahkan ini untuk akses ke Karyawan

    @property
    def nama(self):
        """Expose employee name as `nama` for serializers/response models."""
        return self.karyawan.nama_karyawan if self.karyawan else None

    @property
    def no_telp(self):
        """Expose employee phone as `no_telp` for serializers/response models."""
        return self.karyawan.no_hp if self.karyawan else None

class Karyawan(Base):
    __tablename__ = "karyawan"
    id = Column(Integer, primary_key=True, index=True)
    nama_karyawan = Column(String, nullable=False)
    no_hp = Column(String, nullable=False)
    alamat = Column(String, nullable=False)

    user = relationship("User", back_populates="karyawan", uselist=False)  # Ubah backref ke back_populates

class KategoriMenu(Base):
    __tablename__ = "kategori_menu"

    id = Column(Integer, primary_key=True, index=True)
    nama_kategori = Column(String, unique=True, nullable=False)

    menu = relationship("Menu", back_populates="kategori_obj")  # Ubah backref ke back_populates dan sesuaikan nama

class Menu(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, index=True)
    nama_menu = Column(String, unique=True, nullable=False)
    harga = Column(Float, nullable=False)
    stok = Column(Integer, nullable=False)
    id_kategori_menu = Column(Integer, ForeignKey("kategori_menu.id"), nullable=False)  # Tetap sebagai Column
    deskripsi = Column(Text, nullable=True)
    detail_pesanan = relationship("DetailPesanan", back_populates="menu")
    kategori_obj = relationship("KategoriMenu", back_populates="menu")  # Rename dari kategori_menu untuk hindari konflik
    update_stok_harian = relationship("updateStokHarian", back_populates="menu")  # Tambahkan back_populates

    @property
    def kategori(self):
        """Expose the category id as `kategori` for serializers/response models."""
        return self.id_kategori_menu

class updateStokHarian(Base):
    __tablename__ = "update_stok_harian"

    id = Column(Integer, primary_key=True, index=True)
    id_menu = Column(Integer, ForeignKey("menu.id"), nullable=False)
    jumlah_porsi = Column(Integer, nullable=False)
    tanggal_update = Column(DateTime, default=datetime.now, nullable=False)

    menu = relationship("Menu", back_populates="update_stok_harian")  # Tambahkan back_populates

class Transaksi(Base):
    __tablename__ = "transaksi"

    id = Column(Integer, primary_key=True, index=True)
    waktu = Column(DateTime, default=datetime.now, nullable=False)

    pesanan = relationship("Pesanan", back_populates="transaksi", uselist=False)  # Tambahkan uselist=False jika one-to-one
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
    id_transaksi = Column(Integer, ForeignKey("transaksi.id"), unique=True, nullable=False)

    metode = Column(Enum(MetodePembayaran), nullable=False)
    total = Column(Float, nullable=False)
    waktu_bayar = Column(DateTime, default=datetime.now , nullable=False)
    status = Column(String, default="lunas")

    transaksi = relationship("Transaksi", back_populates="pembayaran")

