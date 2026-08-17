from __future__ import annotations

from datetime import date, timedelta

from app.core.database import SessionLocal, engine, Base
from app.models.harga_histori import HargaHistori
from app.models.notifikasi import Notifikasi
from app.models.produk import Produk
from app.models.transaksi import Transaksi
from app.models.user import User

Base.metadata.create_all(bind=engine)

db = SessionLocal()

def drop_if_exists():
    db.query(Notifikasi).delete()
    db.query(Transaksi).delete()
    db.query(Produk).delete()
    db.query(HargaHistori).delete()
    db.query(User).delete()
    db.commit()


def seed_users():
    users = [
        User(id=1, nama='Pak Budi', role='petani', lokasi_lat=-6.9, lokasi_lng=107.6, nomor_hp='08123456789'),
        User(id=2, nama='Ibu Sari', role='petani', lokasi_lat=-6.92, lokasi_lng=107.58, nomor_hp='08132456789'),
        User(id=3, nama='Pak Rudi', role='petani', lokasi_lat=-6.95, lokasi_lng=107.7, nomor_hp='08143256789'),
        User(id=4, nama='Distributor Jaya', role='distributor', lokasi_lat=-6.87, lokasi_lng=107.59, nomor_hp='08123400011'),
        User(id=5, nama='Konsumen Urban', role='konsumen', lokasi_lat=-6.94, lokasi_lng=107.64, nomor_hp='08123411122'),
    ]
    db.add_all(users)
    db.commit()


def seed_histori_harga():
    kategori_data = {
        'cabai rawit': [24000, 25000, 25500, 26000, 27000, 28000, 28600, 29500, 31000, 32000, 33000, 34000, 35500, 36000],
        'tomat': [18000, 18500, 19000, 19500, 20000, 21000, 21500, 22000, 22500, 22800, 23200, 23800, 24500, 25000],
        'jagung manis': [14000, 14500, 14800, 15000, 15300, 15500, 16000, 16200, 17000, 17200, 17800, 18000, 18300, 18500],
        'sawi hijau': [9000, 9200, 9300, 9500, 9700, 9900, 10100, 10300, 10400, 10800, 11000, 11200, 11500, 11800],
        'kentang': [17000, 17000, 17500, 18000, 18500, 19000, 19200, 19500, 19800, 20000, 20800, 21200, 21400, 22000],
        'buncis': [15000, 15800, 16000, 16500, 17000, 17500, 17800, 18000, 18500, 18800, 19200, 19600, 20000, 21000],
    }

    for kategori, prices in kategori_data.items():
        start = date.today() - timedelta(days=len(prices) - 1)
        for i, price in enumerate(prices):
            db.add(HargaHistori(produk_kategori=kategori, tanggal=start + timedelta(days=i), harga_pasar=price))
    db.commit()


def seed_produk():
    products = [
        Produk(id=1, petani_id=1, nama_produk='Cabai Rawit', kategori='cabai rawit', jumlah_kg=68, tanggal_panen=date.today() - timedelta(days=3), umur_simpan_hari=5, harga_jual=42000, status='tersedia'),
        Produk(id=2, petani_id=2, nama_produk='Tomat', kategori='tomat', jumlah_kg=140, tanggal_panen=date.today() - timedelta(days=5), umur_simpan_hari=7, harga_jual=34000, status='tersedia'),
        Produk(id=3, petani_id=1, nama_produk='Jagung Manis', kategori='jagung manis', jumlah_kg=90, tanggal_panen=date.today() - timedelta(days=2), umur_simpan_hari=6, harga_jual=16000, status='tersedia'),
        Produk(id=4, petani_id=3, nama_produk='Sawi Hijau', kategori='sawi hijau', jumlah_kg=52, tanggal_panen=date.today() - timedelta(days=4), umur_simpan_hari=5, harga_jual=12000, status='tersedia'),
        Produk(id=5, petani_id=2, nama_produk='Kentang', kategori='kentang', jumlah_kg=120, tanggal_panen=date.today() - timedelta(days=6), umur_simpan_hari=8, harga_jual=21000, status='tersedia'),
        Produk(id=6, petani_id=1, nama_produk='Buncis', kategori='buncis', jumlah_kg=78, tanggal_panen=date.today() - timedelta(days=2), umur_simpan_hari=5, harga_jual=18000, status='tersedia'),
        Produk(id=7, petani_id=3, nama_produk='Timun', kategori='timun', jumlah_kg=62, tanggal_panen=date.today() - timedelta(days=3), umur_simpan_hari=7, harga_jual=13800, status='tersedia'),
    ]
    db.add_all(products)
    db.commit()


def seed_transaksi():
    transaksi = [
        Transaksi(id=1, produk_id=1, pembeli_id=4, jumlah_kg=20, harga_petani=30000, harga_distributor=35000, harga_akhir=42000, tanggal=date.today() - timedelta(days=1)),
        Transaksi(id=2, produk_id=3, pembeli_id=5, jumlah_kg=12, harga_petani=12000, harga_distributor=14500, harga_akhir=17000, tanggal=date.today() - timedelta(days=2)),
    ]
    db.add_all(transaksi)
    db.commit()


def seed_notifikasi():
    from datetime import datetime, timezone

    notif = [
        Notifikasi(id=1, user_id=1, tipe='waste_alert', pesan='Cabai rawit mendekati masa optimal jual. Segera buat penawaran.', dibaca=False, created_at=datetime.now(timezone.utc)),
        Notifikasi(id=2, user_id=4, tipe='matching', pesan='Produk tomat baru cocok dengan kebutuhan distributor Anda.', dibaca=False, created_at=datetime.now(timezone.utc)),
    ]
    db.add_all(notif)
    db.commit()


def main():
    drop_if_exists()
    seed_users()
    seed_histori_harga()
    seed_produk()
    seed_transaksi()
    seed_notifikasi()
    print('Seed data berhasil dibuat.')


if __name__ == '__main__':
    main()
