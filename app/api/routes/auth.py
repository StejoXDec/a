from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/register', response_model=UserRead)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    user = User(
        nama=payload.nama,
        role=payload.role,
        lokasi_lat=payload.lokasi_lat,
        lokasi_lng=payload.lokasi_lng,
        nomor_hp=payload.nomor_hp,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post('/login')
def login_user(payload: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.nama == payload.nama, User.role == payload.role).first()
    if not user:
        raise HTTPException(status_code=404, detail='User tidak ditemukan')
    return {'message': 'Login berhasil', 'user_id': user.id, 'role': user.role}
