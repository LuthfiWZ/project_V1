"""Logika inti pengelolaan tugas (disimpan di memori dan file JSON)."""

import json
import re
from datetime import datetime
from pathlib import Path

# Lokasi file data: <folder proyek>/data/tasks.json
FILE_DATA = Path(__file__).resolve().parent.parent / "data" / "tasks.json"

PRIORITAS_VALID = ("tinggi", "sedang", "rendah")
STATUS_VALID = ("selesai", "belum")

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
    - Data lama tanpa prioritas diberi prioritas "sedang".
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
    """Kembalikan daftar tugas yang judulnya mengandung kata (tanpa peduli huruf besar/kecil)."""
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
    """Cetak tugas dalam bentuk tabel sederhana.

    Tanpa argumen: cetak semua tugas. Dengan argumen: cetak daftar itu saja.
    """
    if daftar is None:
        daftar = daftar_tugas

    if not daftar:
        print("Belum ada tugas.")
        return

    print(
        f"{'No':<4}{'Judul':<22}{'Kategori':<14}"
        f"{'Prioritas':<10}{'Deadline':<12}Status"
    )
    print("-" * 69)
    for tugas in daftar:
        status = "Selesai" if tugas["selesai"] else "Belum"
        kategori = tugas.get("kategori") or "-"
        prioritas = tugas.get("prioritas", "sedang")
        print(
            f"{tugas['id']:<4}{tugas['judul']:<22}{kategori:<14}"
            f"{prioritas:<10}{tugas['deadline']:<12}{status}"
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