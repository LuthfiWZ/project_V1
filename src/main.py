"""Titik masuk aplikasi Task Manager Kuliah."""

from src.tasks import tambah_tugas, tampilkan_tugas, tandai_selesai


def main():
    print("Task Manager Kuliah v0.4")
    tambah_tugas("Laporan Basis Data", "2026-11-20")
    tambah_tugas("Presentasi Jaringan", "2026-11-25")

    print("\nSebelum ditandai selesai:")
    tampilkan_tugas()

    tandai_selesai(1)

    print("\nSetelah tugas 1 ditandai selesai:")
    tampilkan_tugas()


if __name__ == "__main__":
    main()