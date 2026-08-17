from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Transaksi(Base):
    __tablename__ = 'transaksi'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    produk_id: Mapped[int] = mapped_column(ForeignKey('produk.id'), nullable=False)
    pembeli_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    jumlah_kg: Mapped[float] = mapped_column(Float, nullable=False)
    harga_petani: Mapped[float] = mapped_column(Float, nullable=False)
    harga_distributor: Mapped[float] = mapped_column(Float, nullable=True)
    harga_akhir: Mapped[float] = mapped_column(Float, nullable=False)
    tanggal: Mapped[datetime] = mapped_column(DateTime, nullable=False)
