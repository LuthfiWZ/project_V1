"""Logika inti pengelolaan tugas (disimpan di memori dan file JSON)."""

from pathlib import Path

from src import logger, storage, tampilan
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
    logger.info(f"Data dimuat: {len(daftar_tugas)} tugas")


def tambah_tugas(judul, deadline, kategori="", prioritas="sedang"):
    """Tambah tugas baru dan kembalikan tugas tersebut.

    judul     : nama tugas, contoh "Laporan Basis Data"
    deadline  : string tanggal format YYYY-MM-DD, contoh "2026-11-20"
    kategori  : mata kuliah (opsional), contoh "Basis Data"
    prioritas : "tinggi", "sedang" (default), atau "rendah"

    Melempar ValueError kalau judul kosong, atau deadline/prioritas tidak valid.
    """
    global _id_berikutnya

    judul = judul.strip()
    if not judul:
        raise ValueError("Judul tidak boleh kosong.")
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
    logger.info(f"Tugas ditambahkan: id={tugas['id']}, judul={judul}")
    return tugas


def ubah_tugas(
    id_tugas,
    judul=None,
    deadline=None,
    kategori=None,
    prioritas=None,
    selesai=None,
):
    """Ubah field tugas. Field yang bernilai None tidak diubah.

    Mengembalikan tugas yang diubah, atau None kalau id tidak ditemukan.
    Melempar ValueError kalau ada nilai yang tidak valid. Semua nilai
    divalidasi dulu, jadi kalau ada yang salah, tidak ada yang berubah.
    """
    target = None
    for tugas in daftar_tugas:
        if tugas["id"] == id_tugas:
            target = tugas
            break
    if target is None:
        logger.peringatan(f"Ubah gagal: id={id_tugas} tidak ditemukan")
        return None

    if judul is not None:
        judul = judul.strip()
        if not judul:
            raise ValueError("Judul tidak boleh kosong.")
    if deadline is not None and not deadline_valid(deadline):
        raise ValueError("Deadline harus berformat YYYY-MM-DD dan tanggalnya valid.")
    if prioritas is not None and prioritas not in PRIORITAS_VALID:
        raise ValueError("Prioritas harus tinggi, sedang, atau rendah.")
    if selesai is not None and not isinstance(selesai, bool):
        raise ValueError("Selesai harus true atau false.")

    if judul is not None:
        target["judul"] = judul
    if deadline is not None:
        target["deadline"] = deadline
    if kategori is not None:
        target["kategori"] = kategori.strip()
    if prioritas is not None:
        target["prioritas"] = prioritas
    if selesai is not None:
        target["selesai"] = selesai

    simpan_tugas()
    logger.info(f"Tugas diubah: id={id_tugas}")
    return target


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
            logger.info(f"Tugas ditandai selesai: id={id_tugas}")
            return tugas
    logger.peringatan(f"Tandai selesai gagal: id={id_tugas} tidak ditemukan")
    return None


def hapus_tugas(id_tugas):
    """Hapus tugas dengan id tertentu.

    Mengembalikan tugas yang dihapus, atau None kalau id tidak ditemukan.
    """
    for tugas in daftar_tugas:
        if tugas["id"] == id_tugas:
            daftar_tugas.remove(tugas)
            simpan_tugas()
            logger.info(f"Tugas dihapus: id={id_tugas}")
            return tugas
    logger.peringatan(f"Hapus gagal: id={id_tugas} tidak ditemukan")
    return None