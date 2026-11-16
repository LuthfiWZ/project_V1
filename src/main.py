"""Titik masuk aplikasi Task Manager Kuliah."""

from src.tasks import (
    PRIORITAS_VALID,
    deadline_valid,
    hapus_tugas,
    muat_tugas,
    tambah_tugas,
    tampilkan_tugas,
    tandai_selesai,
)

MENU = """
=== Task Manager Kuliah v0.11 ===
1. Tambah tugas
2. Lihat tugas
3. Tandai tugas selesai
4. Hapus tugas
0. Keluar
"""


def minta_id(pesan):
    """Minta input id dari pengguna. Kembalikan int, atau None kalau bukan angka."""
    teks = input(pesan).strip()
    if not teks.isdigit():
        print("ID harus berupa angka.")
        return None
    return int(teks)


def menu_tambah():
    judul = input("Judul tugas: ").strip()
    deadline = input("Deadline (YYYY-MM-DD): ").strip()
    if not judul or not deadline:
        print("Judul dan deadline tidak boleh kosong.")
        return
    if not deadline_valid(deadline):
        print("Deadline harus berformat YYYY-MM-DD dan tanggalnya valid.")
        return
    kategori = input("Mata kuliah (boleh kosong): ").strip()
    prioritas = input("Prioritas (tinggi/sedang/rendah, kosong = sedang): ")
    prioritas = prioritas.strip().lower() or "sedang"
    if prioritas not in PRIORITAS_VALID:
        print("Prioritas harus tinggi, sedang, atau rendah.")
        return
    tambah_tugas(judul, deadline, kategori, prioritas)
    print("Tugas berhasil ditambahkan.")


def menu_selesai():
    id_tugas = minta_id("ID tugas yang selesai: ")
    if id_tugas is None:
        return
    if tandai_selesai(id_tugas):
        print("Tugas ditandai selesai.")
    else:
        print("Tugas tidak ditemukan.")


def menu_hapus():
    id_tugas = minta_id("ID tugas yang dihapus: ")
    if id_tugas is None:
        return
    if hapus_tugas(id_tugas):
        print("Tugas berhasil dihapus.")
    else:
        print("Tugas tidak ditemukan.")


def main():
    muat_tugas()

    while True:
        print(MENU)
        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            menu_tambah()
        elif pilihan == "2":
            tampilkan_tugas()
        elif pilihan == "3":
            menu_selesai()
        elif pilihan == "4":
            menu_hapus()
        elif pilihan == "0":
            print("Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid, coba lagi.")


if __name__ == "__main__":
    main()