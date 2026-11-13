"""Logika inti pengelolaan tugas (disimpan di memori dan file JSON)."""

import json
import re
from datetime import datetime
from pathlib import Path

# Lokasi file data: <folder proyek>/data/tasks.json
FILE_DATA = Path(__file__).resolve().parent.parent / "data" / "tasks.json"

daftar_tugas = []
_id_berikutnya = 1


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


def simpan_tugas():
    """Tulis seluruh daftar tugas ke file JSON."""
    FILE_DATA.parent.mkdir(parents=True, exist_ok=True)
    with open(FILE_DATA, "w", encoding="utf-8") as f:
        json.dump(daftar_tugas, f, ensure_ascii=False, indent=2)


def muat_tugas():
    """Baca daftar tugas dari file JSON ke memori.

    - File belum ada: mulai dengan daftar kosong.
    - File rusak (bukan JSON valid): tampilkan peringatan, mulai kosong.
    - Data lama tanpa kategori diberi kategori kosong.
    - id berikutnya dihitung dari id terbesar yang ada + 1.
    """
    global _id_berikutnya

    daftar_tugas.clear()
    _id_berikutnya = 1

    if not FILE_DATA.exists():
        return

    try:
        with open(FILE_DATA, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("Peringatan: file data rusak, mulai dengan daftar kosong.")
        return

    for tugas in data:
        tugas.setdefault("kategori", "")
    daftar_tugas.extend(data)
    if daftar_tugas:
        _id_berikutnya = max(tugas["id"] for tugas in daftar_tugas) + 1


def tambah_tugas(judul, deadline, kategori=""):
    """Tambah tugas baru dan kembalikan tugas tersebut.

    judul    : nama tugas, contoh "Laporan Basis Data"
    deadline : string tanggal format YYYY-MM-DD, contoh "2026-11-20"
    kategori : mata kuliah (opsional), contoh "Basis Data"

    Melempar ValueError kalau format deadline salah.
    """
    global _id_berikutnya

    if not deadline_valid(deadline):
        raise ValueError("Deadline harus berformat YYYY-MM-DD dan tanggalnya valid.")

    tugas = {
        "id": _id_berikutnya,
        "judul": judul,
        "kategori": kategori,
        "deadline": deadline,
        "selesai": False,
    }
    daftar_tugas.append(tugas)
    _id_berikutnya += 1
    simpan_tugas()
    return tugas


def tampilkan_tugas():
    """Cetak semua tugas dalam bentuk tabel sederhana."""
    if not daftar_tugas:
        print("Belum ada tugas.")
        return

    print(f"{'No':<4}{'Judul':<24}{'Kategori':<16}{'Deadline':<12}Status")
    print("-" * 63)
    for tugas in daftar_tugas:
        status = "Selesai" if tugas["selesai"] else "Belum"
        kategori = tugas.get("kategori") or "-"
        print(
            f"{tugas['id']:<4}{tugas['judul']:<24}{kategori:<16}"
            f"{tugas['deadline']:<12}{status}"
        )


def tandai_selesai(id_tugas):
    """Tandai tugas dengan id tertentu sebagai selesai.

    Mengembalikan tugas yang diubah, atau None kalau id tidak ditemukan.
    """
    for tugas in daftar_tugas:
        if tugas["id"] == id_tugas:
            tugas["selesai"] = True
            simpan_tugas()
            return tugas
    return None


def hapus_tugas(id_tugas):
    """Hapus tugas dengan id tertentu.

    Mengembalikan tugas yang dihapus, atau None kalau id tidak ditemukan.
    """
    for tugas in daftar_tugas:
        if tugas["id"] == id_tugas:
            daftar_tugas.remove(tugas)
            simpan_tugas()
            return tugas
    return None