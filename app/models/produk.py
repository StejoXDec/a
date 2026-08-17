from __future__ import annotations

from datetime import date

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Produk(Base):
    __tablename__ = 'produk'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    petani_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    nama_produk: Mapped[str] = mapped_column(String, nullable=False)
    kategori: Mapped[str] = mapped_column(String, nullable=False)
    jumlah_kg: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    tanggal_panen: Mapped[date] = mapped_column(Date, nullable=False)
    umur_simpan_hari: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    harga_jual: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    status: Mapped[str] = mapped_column(String, nullable=False, default='tersedia')
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
