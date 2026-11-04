"""Logika inti pengelolaan tugas (disimpan di memori dulu)."""

daftar_tugas = []
_id_berikutnya = 1


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
    return tugas