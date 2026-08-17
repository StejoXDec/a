from __future__ import annotations

from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.harga_histori import HargaHistori
from app.models.notifikasi import Notifikasi
from app.models.produk import Produk
from app.models.user import User
from app.schemas.ai import FreshnessResult, HargaPrediksi, MatchingResult
from app.schemas.produk import ProdukCreate, ProdukRead
from app.services.logic import calculate_freshness_score, calculate_prediction, distance_km

router = APIRouter(prefix='/produk', tags=['produk'])


@router.post('', response_model=ProdukRead)
def create_produk(payload: ProdukCreate, db: Session = Depends(get_db)):
    if not db.query(User).filter(User.id == payload.petani_id).first():
        raise HTTPException(status_code=404, detail='Petani tidak ditemukan')

    produk = Produk(**payload.model_dump())
    db.add(produk)
    db.commit()
    db.refresh(produk)
    return produk


@router.get('', response_model=list[ProdukRead])
def list_produk(
    kategori: str | None = None,
    status: str | None = None,
    radius_km: float | None = None,
    user_id: int | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Produk)
    if kategori:
        query = query.filter(Produk.kategori == kategori)
    if status:
        query = query.filter(Produk.status == status)
    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail='User tidak ditemukan')
        max_radius = radius_km or settings.default_radius_km
        produk_list = query.all()
        filtered = []
        for produk in produk_list:
            petani = db.query(User).filter(User.id == produk.petani_id).first()
            if petani:
                jarak = distance_km(user.lokasi_lat, user.lokasi_lng, petani.lokasi_lat, petani.lokasi_lng)
                if jarak <= max_radius:
                    filtered.append(produk)
        return filtered
    return query.all()


@router.get('/{produk_id}', response_model=ProdukRead)
def get_produk_by_id(produk_id: int, db: Session = Depends(get_db)):
    produk = db.query(Produk).filter(Produk.id == produk_id).first()
    if not produk:
        raise HTTPException(status_code=404, detail='Produk tidak ditemukan')
    return produk


@router.patch('/{produk_id}')
def update_produk(produk_id: int, payload: dict, db: Session = Depends(get_db)):
    produk = db.query(Produk).filter(Produk.id == produk_id).first()
    if not produk:
        raise HTTPException(status_code=404, detail='Produk tidak ditemukan')
    for key, value in payload.items():
        setattr(produk, key, value)
    db.commit()
    return {'message': 'Produk berhasil diupdate'}


@router.get('/{produk_id}/freshness', response_model=FreshnessResult)
def freshness_produk(produk_id: int, db: Session = Depends(get_db)):
    produk = db.query(Produk).filter(Produk.id == produk_id).first()
    if not produk:
        raise HTTPException(status_code=404, detail='Produk tidak ditemukan')

    skor, sisa_hari, status = calculate_freshness_score(produk.tanggal_panen, produk.umur_simpan_hari)
    if status == 'risiko_tinggi':
        diskon = settings.discount_rate
        produk.harga_jual = round(produk.harga_jual * (1 - diskon), 2)
        notif = Notifikasi(
            user_id=produk.petani_id,
            tipe='waste_alert',
            pesan=f'{produk.nama_produk} masuk kategori risiko tinggi dan didiskon {diskon * 100:.0f}% untuk mencegah pembusukan.',
            dibaca=False,
        )
        db.add(notif)
        db.commit()
        harga_diskon = produk.harga_jual
    else:
        harga_diskon = None

    penjelasan = {
        'segar': f'{produk.nama_produk} masih dalam masa optimal penjualan dengan {skor}% freshness.',
        'perlu_segera': f'{produk.nama_produk} perlu segera dijual karena sisa waktu optimal tinggal {sisa_hari} hari.',
        'risiko_tinggi': f'{produk.nama_produk} mendekati masa kadaluarsa; produk perlu dipercepat penjualannya untuk menekan pemborosan.'
    }[status]

    return FreshnessResult(
        produk_id=produk.id,
        skor=skor,
        sisa_hari=sisa_hari,
        status=status,
        harga_diskon=harga_diskon,
        penjelasan=penjelasan,
    )


@router.get('/kategori/{kategori}/prediksi-harga', response_model=HargaPrediksi)
def prediksi_harga(kategori: str, db: Session = Depends(get_db)):
    hari_ini = date.today()
    seven_days = [hari_ini - timedelta(days=i) for i in range(7)]
    data = []
    for d in reversed(seven_days):
        rec = db.query(HargaHistori).filter(HargaHistori.produk_kategori == kategori, HargaHistori.tanggal == d).first()
        data.append(rec.harga_pasar if rec else 0)

    if len(data) < 2:
        data = [20000, 20500, 21000, 21300, 22000, 21800, 22500]

    historical = [float(x) for x in data if x > 0]
    rekom, tren, _, penjelasan = calculate_prediction(historical)
    return HargaPrediksi(
        kategori=kategori,
        harga_rekomendasi=rekom,
        tren=tren,
        data_7_hari=historical,
        penjelasan=penjelasan,
    )


@router.get('/matching/{user_id}', response_model=list[MatchingResult])
def matching_produk(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User tidak ditemukan')

    produk_list = db.query(Produk).filter(Produk.status == 'tersedia').all()
    hasil = []
    for produk in produk_list:
        petani = db.query(User).filter(User.id == produk.petani_id).first()
        if not petani:
            continue
        jarak = distance_km(user.lokasi_lat, user.lokasi_lng, petani.lokasi_lat, petani.lokasi_lng)
        skor, _, status = calculate_freshness_score(produk.tanggal_panen, produk.umur_simpan_hari)
        prioritas = 100 - jarak * 2
        if status == 'risiko_tinggi':
            prioritas += 35
        elif status == 'perlu_segera':
            prioritas += 18
        alasan = f'{produk.nama_produk} dekat dengan lokasi Anda dan masuk status {status}.'
        hasil.append({
            'produk_id': produk.id,
            'nama_produk': produk.nama_produk,
            'petani_id': produk.petani_id,
            'jarak_km': jarak,
            'prioritas': round(prioritas, 2),
            'alasan': alasan,
        })

    return sorted(hasil, key=lambda x: (-x['prioritas'], x['jarak_km']))
