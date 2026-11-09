"""Titik masuk aplikasi Task Manager Kuliah."""

from src.tasks import (
    hapus_tugas,
    tambah_tugas,
    tampilkan_tugas,
    tandai_selesai,
)


def main():
    print("Task Manager Kuliah v0.5")
    tambah_tugas("Laporan Basis Data", "2026-11-20")
    tambah_tugas("Presentasi Jaringan", "2026-11-25")
    tambah_tugas("Kuis Algoritma", "2026-11-27")

    tandai_selesai(1)

    print("\nSebelum hapus:")
    tampilkan_tugas()

    hapus_tugas(2)

    print("\nSetelah tugas 2 dihapus:")
    tampilkan_tugas()


if __name__ == "__main__":
    main()