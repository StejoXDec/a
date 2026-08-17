from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class FreshnessResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    produk_id: int
    skor: float
    sisa_hari: float
    status: str
    harga_diskon: float | None = None
    penjelasan: str


class HargaPrediksi(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    kategori: str
    harga_rekomendasi: float
    tren: str
    data_7_hari: list[float]
    penjelasan: str


class MatchingResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    produk_id: int
    nama_produk: str
    petani_id: int
    jarak_km: float
    prioritas: float
    alasan: str


class JejakTransaksi(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    transaksi_id: int
    petani: float
    distributor: float
    konsumen: float
    persentase_petani: float
    persentase_distributor: float
    persentase_konsumen: float
