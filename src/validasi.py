"""Aturan validasi data tugas."""

import re
from datetime import datetime

PRIORITAS_VALID = ("tinggi", "sedang", "rendah")
STATUS_VALID = ("selesai", "belum")


def deadline_valid(teks):
    """Cek apakah teks berformat YYYY-MM-DD dan tanggalnya benar-benar ada.

    Contoh valid  : "2026-11-20"
    Contoh salah  : "besok", "20-11-2026", "2026-2-5", "2026-02-30"
    """
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", teks):
        return False
    try:
        datetime.strptime(teks, "%Y-%m-%d")
    except ValueError:
        return False
    return True