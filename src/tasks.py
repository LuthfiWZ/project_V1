"""Logika inti pengelolaan tugas (disimpan di memori dan file JSON)."""

import json
from pathlib import Path

# Lokasi file data: <folder proyek>/data/tasks.json
FILE_DATA = Path(__file__).resolve().parent.parent / "data" / "tasks.json"

daftar_tugas = []
_id_berikutnya = 1


def simpan_tugas():
    """Tulis seluruh daftar tugas ke file JSON."""
    FILE_DATA.parent.mkdir(parents=True, exist_ok=True)
    with open(FILE_DATA, "w", encoding="utf-8") as f:
        json.dump(daftar_tugas, f, ensure_ascii=False, indent=2)


def tambah_tugas(judul, deadline):
    """Tambah tugas baru dan kembalikan tugas tersebut.

    judul    : nama tugas, contoh "Laporan Basis Data"
    deadline : string tanggal format YYYY-MM-DD, contoh "2026-11-20"
    """
    global _id_berikutnya

    tugas = {
        "id": _id_berikutnya,
        "judul": judul,
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

    print(f"{'No':<4}{'Judul':<30}{'Deadline':<12}Status")
    print("-" * 53)
    for tugas in daftar_tugas:
        status = "Selesai" if tugas["selesai"] else "Belum"
        print(f"{tugas['id']:<4}{tugas['judul']:<30}{tugas['deadline']:<12}{status}")


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