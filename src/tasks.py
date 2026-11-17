"""Logika inti pengelolaan tugas (disimpan di memori dan file JSON)."""

from pathlib import Path

from src import storage, tampilan
from src.validasi import PRIORITAS_VALID, STATUS_VALID, deadline_valid

# Lokasi file data: <folder proyek>/data/tasks.json
FILE_DATA = Path(__file__).resolve().parent.parent / "data" / "tasks.json"

daftar_tugas = []
_id_berikutnya = 1


def simpan_tugas():
    """Tulis seluruh daftar tugas ke file JSON."""
    storage.tulis_json(FILE_DATA, daftar_tugas)


def muat_tugas():
    """Baca daftar tugas dari file JSON ke memori.

    - Data lama tanpa kategori diberi kategori kosong.
    - Data lama tanpa prioritas diberi prioritas "sedang".
    - id berikutnya dihitung dari id terbesar yang ada + 1.
    """
    global _id_berikutnya

    daftar_tugas.clear()
    _id_berikutnya = 1

    data = storage.baca_json(FILE_DATA)
    for tugas in data:
        tugas.setdefault("kategori", "")
        tugas.setdefault("prioritas", "sedang")
    daftar_tugas.extend(data)
    if daftar_tugas:
        _id_berikutnya = max(tugas["id"] for tugas in daftar_tugas) + 1


def tambah_tugas(judul, deadline, kategori="", prioritas="sedang"):
    """Tambah tugas baru dan kembalikan tugas tersebut.

    judul     : nama tugas, contoh "Laporan Basis Data"
    deadline  : string tanggal format YYYY-MM-DD, contoh "2026-11-20"
    kategori  : mata kuliah (opsional), contoh "Basis Data"
    prioritas : "tinggi", "sedang" (default), atau "rendah"

    Melempar ValueError kalau deadline atau prioritas tidak valid.
    """
    global _id_berikutnya

    if not deadline_valid(deadline):
        raise ValueError("Deadline harus berformat YYYY-MM-DD dan tanggalnya valid.")
    if prioritas not in PRIORITAS_VALID:
        raise ValueError("Prioritas harus tinggi, sedang, atau rendah.")

    tugas = {
        "id": _id_berikutnya,
        "judul": judul,
        "kategori": kategori,
        "prioritas": prioritas,
        "deadline": deadline,
        "selesai": False,
    }
    daftar_tugas.append(tugas)
    _id_berikutnya += 1
    simpan_tugas()
    return tugas


def cari_tugas(kata):
    """Kembalikan tugas yang judulnya mengandung kata (tanpa peduli huruf besar/kecil)."""
    kata = kata.strip().lower()
    return [t for t in daftar_tugas if kata in t["judul"].lower()]


def filter_tugas(kategori="", prioritas="", status=""):
    """Kembalikan tugas yang cocok dengan semua syarat yang diisi.

    kategori  : nama mata kuliah (tanpa peduli huruf besar/kecil), kosong = semua
    prioritas : "tinggi"/"sedang"/"rendah", kosong = semua
    status    : "selesai"/"belum", kosong = semua
    """
    hasil = []
    for tugas in daftar_tugas:
        if kategori and tugas.get("kategori", "").lower() != kategori.strip().lower():
            continue
        if prioritas and tugas.get("prioritas", "sedang") != prioritas:
            continue
        if status == "selesai" and not tugas["selesai"]:
            continue
        if status == "belum" and tugas["selesai"]:
            continue
        hasil.append(tugas)
    return hasil


def tampilkan_tugas(daftar=None):
    """Cetak tugas sebagai tabel. Tanpa argumen: cetak semua tugas."""
    tampilan.cetak_tabel(daftar_tugas if daftar is None else daftar)


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