import io
import json
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from src import main, tasks
from tests.helpers import siapkan_data_sementara


class TestKategori(unittest.TestCase):
    def setUp(self):
        self.path = siapkan_data_sementara(self)

    def _baca_file(self):
        with open(self.path, encoding="utf-8") as f:
            return json.load(f)

    def test_tambah_dengan_kategori(self):
        hasil = tasks.tambah_tugas("Laporan", "2026-11-20", "Basis Data")

        self.assertEqual(hasil["kategori"], "Basis Data")

    def test_kategori_default_kosong(self):
        hasil = tasks.tambah_tugas("Laporan", "2026-11-20")

        self.assertEqual(hasil["kategori"], "")

    def test_kategori_tersimpan_ke_file(self):
        tasks.tambah_tugas("Laporan", "2026-11-20", "Basis Data")

        self.assertEqual(self._baca_file()[0]["kategori"], "Basis Data")

    def test_muat_data_lama_tanpa_kategori(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump([{"id": 1, "judul": "Lama",
                        "deadline": "2026-11-20", "selesai": False}], f)

        tasks.muat_tugas()

        self.assertEqual(tasks.daftar_tugas[0]["kategori"], "")

    def test_tampil_kategori_di_tabel(self):
        tasks.tambah_tugas("Laporan", "2026-11-20", "Basis Data")
        tasks.tambah_tugas("Kuis", "2026-11-21")

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            tasks.tampilkan_tugas()
        output = buffer.getvalue()

        self.assertIn("Kategori", output)
        self.assertIn("Basis Data", output)
        self.assertIn("-", output)

    def test_menu_tambah_dengan_kategori(self):
        masukan = ["1", "Laporan", "2026-11-20", "Basis Data", "0"]
        with patch("builtins.input", side_effect=masukan):
            with redirect_stdout(io.StringIO()):
                main.main()

        self.assertEqual(tasks.daftar_tugas[0]["kategori"], "Basis Data")


if __name__ == "__main__":
    unittest.main()