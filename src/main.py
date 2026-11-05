"""Titik masuk aplikasi Task Manager Kuliah."""

from src.tasks import tambah_tugas, tampilkan_tugas


def main():
    print("Task Manager Kuliah v0.3")
    tambah_tugas("Laporan Basis Data", "2026-11-20")
    tambah_tugas("Presentasi Jaringan", "2026-11-25")
    tampilkan_tugas()


if __name__ == "__main__":
    main()