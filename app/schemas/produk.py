from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field, ConfigDict


class ProdukCreate(BaseModel):
    petani_id: int
    nama_produk: str
    kategori: str
    jumlah_kg: float = Field(..., gt=0)
    tanggal_panen: date
    umur_simpan_hari: int = Field(..., gt=0)
    harga_jual: float = Field(..., gt=0)
    status: str = 'tersedia'


class ProdukRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    petani_id: int
    nama_produk: str
    kategori: str
    jumlah_kg: float
    tanggal_panen: date
    umur_simpan_hari: int
    harga_jual: float
    status: str
