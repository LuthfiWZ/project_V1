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
            return tugas
    return None