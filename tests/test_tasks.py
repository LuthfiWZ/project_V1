import io
import unittest
from contextlib import redirect_stdout

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


class TestTampilkanTugas(unittest.TestCase):
    def setUp(self):
        tasks.daftar_tugas.clear()
        tasks._id_berikutnya = 1

    def _tangkap_output(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            tasks.tampilkan_tugas()
        return buffer.getvalue()

    def test_tampilkan_saat_kosong(self):
        output = self._tangkap_output()
        self.assertIn("Belum ada tugas.", output)

    def test_tampilkan_berisi_data_tugas(self):
        tasks.tambah_tugas("Laporan Basis Data", "2026-11-20")
        output = self._tangkap_output()

        self.assertIn("Laporan Basis Data", output)
        self.assertIn("2026-11-20", output)
        self.assertIn("Belum", output)


class TestTandaiSelesai(unittest.TestCase):
    def setUp(self):
        tasks.daftar_tugas.clear()
        tasks._id_berikutnya = 1

    def test_tandai_selesai_mengubah_status(self):
        tasks.tambah_tugas("Laporan Basis Data", "2026-11-20")

        hasil = tasks.tandai_selesai(1)

        self.assertTrue(hasil["selesai"])
        self.assertTrue(tasks.daftar_tugas[0]["selesai"])

    def test_tandai_selesai_id_tidak_ditemukan(self):
        tasks.tambah_tugas("Laporan Basis Data", "2026-11-20")

        hasil = tasks.tandai_selesai(99)

        self.assertIsNone(hasil)
        self.assertFalse(tasks.daftar_tugas[0]["selesai"])


if __name__ == "__main__":
    unittest.main()