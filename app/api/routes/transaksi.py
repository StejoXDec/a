from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.transaksi import Transaksi
from app.schemas.ai import JejakTransaksi

router = APIRouter(prefix='/transaksi', tags=['transaksi'])


@router.get('/{transaksi_id}/jejak', response_model=JejakTransaksi)
def jejak_transaksi(transaksi_id: int, db: Session = Depends(get_db)):
    transaksi = db.query(Transaksi).filter(Transaksi.id == transaksi_id).first()
    if not transaksi:
        raise HTTPException(status_code=404, detail='Transaksi tidak ditemukan')

    total = transaksi.harga_akhir
    petani = transaksi.harga_petani
    distributor = transaksi.harga_distributor or (total - petani) * 0.5
    konsumen = total
    persentase_petani = (petani / total) * 100 if total else 0
    persentase_distributor = (distributor / total) * 100 if total else 0
    persentase_konsumen = (konsumen / total) * 100 if total else 0

    return JejakTransaksi(
        transaksi_id=transaksi.id,
        petani=petani,
        distributor=distributor,
        konsumen=konsumen,
        persentase_petani=round(persentase_petani, 2),
        persentase_distributor=round(persentase_distributor, 2),
        persentase_konsumen=round(persentase_konsumen, 2),
    )
