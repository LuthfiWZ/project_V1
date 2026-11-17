"""Baca dan tulis data tugas ke file JSON."""

import json


def tulis_json(path, data):
    """Tulis data ke file JSON, buat folder kalau belum ada."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def baca_json(path):
    """Baca data dari file JSON.

    - File belum ada: kembalikan list kosong.
    - File rusak: tampilkan peringatan, kembalikan list kosong.
    """
    if not path.exists():
        return []
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Peringatan: file data rusak, mulai dengan daftar kosong.")
        return []