import io
import json
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from src import main, tasks
from tests.helpers import siapkan_data_sementara


class TestMuatTugas(unittest.TestCase):
    def setUp(self):
        self.path = siapkan_data_sementara(self)

    def _tulis_file(self, data):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f)

    def test_file_tidak_ada(self):
        tasks.muat_tugas()

        self.assertEqual(tasks.daftar_tugas, [])
        self.assertEqual(tasks._id_berikutnya, 1)

    def test_muat_data_dari_file(self):
        self._tulis_file([
            {"id": 1, "judul": "Laporan Basis Data",
             "deadline": "2026-11-20", "selesai": True},
        ])

        tasks.muat_tugas()

        self.assertEqual(len(tasks.daftar_tugas), 1)
        self.assertEqual(tasks.daftar_tugas[0]["judul"], "Laporan Basis Data")
        self.assertTrue(tasks.daftar_tugas[0]["selesai"])

    def test_id_berikutnya_melanjutkan_id_terbesar(self):
        self._tulis_file([
            {"id": 1, "judul": "A", "deadline": "2026-11-20", "selesai": False},
            {"id": 3, "judul": "B", "deadline": "2026-11-21", "selesai": False},
        ])

        tasks.muat_tugas()
        baru = tasks.tambah_tugas("C", "2026-11-22")

        self.assertEqual(baru["id"], 4)

    def test_file_rusak_mulai_kosong(self):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write("ini bukan json")

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            tasks.muat_tugas()

        self.assertEqual(tasks.daftar_tugas, [])
        self.assertIn("Peringatan", buffer.getvalue())

    def test_main_memuat_data_saat_dibuka(self):
        self._tulis_file([
            {"id": 1, "judul": "Laporan Basis Data",
             "deadline": "2026-11-20", "selesai": False},
        ])

        buffer = io.StringIO()
        with patch("builtins.input", side_effect=["2", "0"]):
            with redirect_stdout(buffer):
                main.main()

        self.assertIn("Laporan Basis Data", buffer.getvalue())


if __name__ == "__main__":
    unittest.main()