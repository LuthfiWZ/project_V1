import io
import json
import unittest
from contextlib import redirect_stdout

from src import tasks
from tests.helpers import siapkan_data_sementara


class TestTambahTugas(unittest.TestCase):
    def setUp(self):
        siapkan_data_sementara(self)

    def test_tambah_tugas_menyimpan_data(self):
        hasil = tasks.tambah_tugas("Laporan Basis Data", "2026-11-20")

        self.assertEqual(len(tasks.daftar_tugas), 1)
        self.assertEqual(hasil["id"], 1)
        self.assertEqual(hasil["judul"], "Laporan Basis Data")
        self.assertEqual(hasil["deadline"], "2026-11-20")
        self.assertFalse(hasil["selesai"])


class TestTampilkanTugas(unittest.TestCase):
    def setUp(self):
        siapkan_data_sementara(self)

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
        siapkan_data_sementara(self)

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


class TestHapusTugas(unittest.TestCase):
    def setUp(self):
        siapkan_data_sementara(self)

    def test_hapus_tugas_menghilangkan_data(self):
        tasks.tambah_tugas("Laporan Basis Data", "2026-11-20")
        tasks.tambah_tugas("Presentasi Jaringan", "2026-11-25")

        hasil = tasks.hapus_tugas(1)

        self.assertEqual(hasil["judul"], "Laporan Basis Data")
        self.assertEqual(len(tasks.daftar_tugas), 1)
        self.assertEqual(tasks.daftar_tugas[0]["judul"], "Presentasi Jaringan")

    def test_hapus_tugas_id_tidak_ditemukan(self):
        tasks.tambah_tugas("Laporan Basis Data", "2026-11-20")

        hasil = tasks.hapus_tugas(99)

        self.assertIsNone(hasil)
        self.assertEqual(len(tasks.daftar_tugas), 1)


class TestSimpanTugas(unittest.TestCase):
    def setUp(self):
        self.path = siapkan_data_sementara(self)

    def _baca_file(self):
        with open(self.path, encoding="utf-8") as f:
            return json.load(f)

    def test_tambah_tugas_tersimpan_ke_file(self):
        tasks.tambah_tugas("Laporan Basis Data", "2026-11-20")

        isi = self._baca_file()

        self.assertEqual(len(isi), 1)
        self.assertEqual(isi[0]["judul"], "Laporan Basis Data")
        self.assertFalse(isi[0]["selesai"])

    def test_tandai_selesai_tersimpan_ke_file(self):
        tasks.tambah_tugas("Laporan Basis Data", "2026-11-20")

        tasks.tandai_selesai(1)

        self.assertTrue(self._baca_file()[0]["selesai"])

    def test_hapus_tugas_tersimpan_ke_file(self):
        tasks.tambah_tugas("Laporan Basis Data", "2026-11-20")
        tasks.tambah_tugas("Presentasi Jaringan", "2026-11-25")

        tasks.hapus_tugas(1)

        isi = self._baca_file()
        self.assertEqual(len(isi), 1)
        self.assertEqual(isi[0]["judul"], "Presentasi Jaringan")


if __name__ == "__main__":
    unittest.main()