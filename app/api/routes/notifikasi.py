from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.notifikasi import Notifikasi
from app.schemas.notifikasi import NotifikasiRead

router = APIRouter(prefix='/notifikasi', tags=['notifikasi'])


@router.get('/{user_id}', response_model=list[NotifikasiRead])
def list_notifikasi(user_id: int, db: Session = Depends(get_db)):
    items = db.query(Notifikasi).filter(Notifikasi.user_id == user_id).order_by(Notifikasi.created_at.desc()).all()
    return items


@router.patch('/{notifikasi_id}/read')
def mark_read(notifikasi_id: int, db: Session = Depends(get_db)):
    item = db.query(Notifikasi).filter(Notifikasi.id == notifikasi_id).first()
    if not item:
        raise HTTPException(status_code=404, detail='Notifikasi tidak ditemukan')
    item.dibaca = True
    db.commit()
    return {'message': 'Notifikasi ditandai sudah dibaca'}
