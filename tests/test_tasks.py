import unittest

from src import tasks


class TestTambahTugas(unittest.TestCase):
    def setUp(self):
        # Kosongkan data sebelum tiap test supaya test saling independen
        tasks.daftar_tugas.clear()
        tasks._id_berikutnya = 1

    def test_tambah_tugas_menyimpan_data(self):
        hasil = tasks.tambah_tugas("Laporan Basis Data", "2026-11-20")

        self.assertEqual(len(tasks.daftar_tugas), 1)
        self.assertEqual(hasil["id"], 1)
        self.assertEqual(hasil["judul"], "Laporan Basis Data")
        self.assertEqual(hasil["deadline"], "2026-11-20")
        self.assertFalse(hasil["selesai"])


if __name__ == "__main__":
    unittest.main()