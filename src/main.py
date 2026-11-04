"""Titik masuk aplikasi Task Manager Kuliah."""

from src.tasks import tambah_tugas, daftar_tugas


def main():
    print("Task Manager Kuliah v0.2")
    tambah_tugas("Laporan Basis Data", "2026-11-20")
    print(f"Tugas tersimpan: {daftar_tugas}")


if __name__ == "__main__":
    main()