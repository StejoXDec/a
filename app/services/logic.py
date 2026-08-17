from __future__ import annotations

from datetime import date, datetime, timedelta


def calculate_freshness_score(panen_date: date, umur_simpan_hari: int, now: date | None = None) -> tuple[float, float, str]:
    now = now or date.today()
    days_since = max((now - panen_date).days, 0)
    sisa_hari = max(umur_simpan_hari - days_since, 0)
    skor = (sisa_hari / umur_simpan_hari) * 100 if umur_simpan_hari else 0
    if skor > 60:
        status = 'segar'
    elif skor >= 25:
        status = 'perlu_segera'
    else:
        status = 'risiko_tinggi'
    return round(skor, 2), round(sisa_hari, 2), status


def get_status_label(skor: float) -> str:
    if skor > 60:
        return 'segar'
    if skor >= 25:
        return 'perlu_segera'
    return 'risiko_tinggi'


def calculate_prediction(historical_prices: list[float], trend_bias: float = 0.0) -> tuple[float, str, list[float], str]:
    if not historical_prices:
        return 0.0, 'stabil', [], 'Belum tersedia data historis.'

    latest = historical_prices[-1]
    avg_7 = sum(historical_prices) / len(historical_prices)
    change_pct = ((latest - avg_7) / avg_7) * 100 if avg_7 else 0
    adjusted = latest * (1 + (change_pct / 100) + (trend_bias / 100))
    if abs(change_pct) < 3:
        tren = 'stabil'
    elif change_pct > 0:
        tren = 'naik'
    else:
        tren = 'turun'

    trend_word = 'naik' if tren == 'naik' else 'turun' if tren == 'turun' else 'stabil'
    penjelasan = (
        f'Harga saat ini {latest:,.0f} diproyeksikan menjadi {adjusted:,.0f} karena '
        f'trend pasar {trend_word} dibanding rata-rata 7 hari terakhir.'
    )
    return round(adjusted, 2), tren, historical_prices, penjelasan


def distance_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    import math

    r = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lng2 - lng1)
    a = (math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(r * c, 2)
