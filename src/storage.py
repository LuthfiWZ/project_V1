"""Baca dan tulis data tugas ke file JSON."""

import json

from src import logger


def tulis_json(path, data):
    """Tulis data ke file JSON, buat folder kalau belum ada."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def baca_json(path):
    """Baca data dari file JSON.

    - File belum ada: kembalikan list kosong.
    - File rusak atau bentuk isinya salah: tampilkan peringatan,
      catat ke log, kembalikan list kosong.
    """
    if not path.exists():
        return []

    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        logger.peringatan(f"File data bukan JSON valid: {path}")
        print("Peringatan: file data rusak, mulai dengan daftar kosong.")
        return []

    if not isinstance(data, list) or not all(
        isinstance(t, dict) and "id" in t for t in data
    ):
        logger.peringatan(f"Bentuk isi file data tidak sesuai: {path}")
        print("Peringatan: file data rusak, mulai dengan daftar kosong.")
        return []

    return data