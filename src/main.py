"""Titik masuk aplikasi Task Manager Kuliah."""

from src.tasks import (
    PRIORITAS_VALID,
    STATUS_VALID,
    cari_tugas,
    deadline_valid,
    filter_tugas,
    hapus_tugas,
    muat_tugas,
    tambah_tugas,
    tampilkan_tugas,
    tandai_selesai,
)

MENU = """
=== Task Manager Kuliah v0.12 ===
1. Tambah tugas
2. Lihat tugas
3. Tandai tugas selesai
4. Hapus tugas
5. Cari tugas
6. Filter tugas
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


def menu_cari():
    kata = input("Kata kunci judul: ").strip()
    if not kata:
        print("Kata kunci tidak boleh kosong.")
        return
    hasil = cari_tugas(kata)
    if not hasil:
        print("Tidak ada tugas yang cocok.")
        return
    tampilkan_tugas(hasil)


def menu_filter():
    kategori = input("Mata kuliah (kosong = semua): ").strip()
    prioritas = input("Prioritas (tinggi/sedang/rendah, kosong = semua): ")
    prioritas = prioritas.strip().lower()
    status = input("Status (selesai/belum, kosong = semua): ").strip().lower()

    if prioritas and prioritas not in PRIORITAS_VALID:
        print("Prioritas harus tinggi, sedang, atau rendah.")
        return
    if status and status not in STATUS_VALID:
        print("Status harus selesai atau belum.")
        return

    hasil = filter_tugas(kategori, prioritas, status)
    if not hasil:
        print("Tidak ada tugas yang cocok.")
        return
    tampilkan_tugas(hasil)


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
        elif pilihan == "5":
            menu_cari()
        elif pilihan == "6":
            menu_filter()
        elif pilihan == "0":
            print("Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid, coba lagi.")


if __name__ == "__main__":
    main()