from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NotifikasiRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    tipe: str
    pesan: str
    dibaca: bool
    created_at: datetime
