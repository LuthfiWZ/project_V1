"""Tampilan tabel tugas di terminal."""


def cetak_tabel(daftar):
    """Cetak daftar tugas dalam bentuk tabel sederhana."""
    if not daftar:
        print("Belum ada tugas.")
        return

    print(
        f"{'No':<4}{'Judul':<22}{'Kategori':<14}"
        f"{'Prioritas':<10}{'Deadline':<12}Status"
    )
    print("-" * 69)
    for tugas in daftar:
        status = "Selesai" if tugas["selesai"] else "Belum"
        kategori = tugas.get("kategori") or "-"
        prioritas = tugas.get("prioritas", "sedang")
        print(
            f"{tugas['id']:<4}{tugas['judul']:<22}{kategori:<14}"
            f"{prioritas:<10}{tugas['deadline']:<12}{status}"
        )