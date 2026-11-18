import unittest

from src import tasks
from tests.helpers import siapkan_data_sementara


class TestJudulKosong(unittest.TestCase):
    def setUp(self):
        self.path = siapkan_data_sementara(self)

    def test_judul_kosong_ditolak(self):
        for judul in ["", "   "]:
            with self.subTest(judul=judul):
                with self.assertRaises(ValueError):
                    tasks.tambah_tugas(judul, "2026-11-20")

        self.assertEqual(tasks.daftar_tugas, [])
        self.assertFalse(self.path.exists())

    def test_judul_dirapikan(self):
        hasil = tasks.tambah_tugas("  Laporan  ", "2026-11-20")

        self.assertEqual(hasil["judul"], "Laporan")


class TestDeadline(unittest.TestCase):
    def setUp(self):
        siapkan_data_sementara(self)

    def test_deadline_masa_lalu_diterima(self):
        # Sengaja diterima: pengguna boleh mencatat tugas yang sudah lewat
        hasil = tasks.tambah_tugas("Tugas lama", "2020-01-01")

        self.assertEqual(hasil["deadline"], "2020-01-01")

    def test_tahun_bukan_kabisat(self):
        with self.assertRaises(ValueError):
            tasks.tambah_tugas("Laporan", "2026-02-29")


class TestIdTidakDuplikat(unittest.TestCase):
    def setUp(self):
        siapkan_data_sementara(self)

    def test_id_setelah_hapus_tidak_dipakai_ulang(self):
        tasks.tambah_tugas("A", "2026-11-20")
        tasks.tambah_tugas("B", "2026-11-21")
        tasks.tambah_tugas("C", "2026-11-22")

        tasks.hapus_tugas(2)
        baru = tasks.tambah_tugas("D", "2026-11-23")

        self.assertEqual(baru["id"], 4)

    def test_id_setelah_muat_ulang_melanjutkan(self):
        tasks.tambah_tugas("A", "2026-11-20")
        tasks.tambah_tugas("B", "2026-11-21")

        tasks.muat_tugas()
        baru = tasks.tambah_tugas("C", "2026-11-22")

        self.assertEqual(baru["id"], 3)

    def test_semua_id_unik(self):
        for i in range(5):
            tasks.tambah_tugas(f"Tugas {i}", "2026-11-20")
        tasks.hapus_tugas(3)
        tasks.tambah_tugas("Baru", "2026-11-21")

        id_semua = [t["id"] for t in tasks.daftar_tugas]

        self.assertEqual(len(id_semua), len(set(id_semua)))

    def test_hapus_id_terbesar_lalu_muat_ulang(self):
        # Perilaku yang sudah kita catat di Hari 8: id terbesar bisa dipakai ulang
        tasks.tambah_tugas("A", "2026-11-20")
        tasks.tambah_tugas("B", "2026-11-21")
        tasks.hapus_tugas(2)

        tasks.muat_tugas()
        baru = tasks.tambah_tugas("C", "2026-11-22")

        self.assertEqual(baru["id"], 2)


if __name__ == "__main__":
    unittest.main()