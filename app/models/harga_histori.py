from __future__ import annotations

from datetime import date

from sqlalchemy import Date, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class HargaHistori(Base):
    __tablename__ = 'harga_histori'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    produk_kategori: Mapped[str] = mapped_column(String, nullable=False)
    tanggal: Mapped[date] = mapped_column(Date, nullable=False)
    harga_pasar: Mapped[float] = mapped_column(Float, nullable=False)
