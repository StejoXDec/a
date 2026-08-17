from __future__ import annotations

from pydantic import BaseModel, Field, ConfigDict


class UserCreate(BaseModel):
    nama: str = Field(..., min_length=1)
    role: str
    lokasi_lat: float
    lokasi_lng: float
    nomor_hp: str | None = None


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nama: str
    role: str
    lokasi_lat: float
    lokasi_lng: float
    nomor_hp: str | None = None
