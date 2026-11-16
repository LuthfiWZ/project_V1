import io
import json
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from src import main, tasks
from tests.helpers import siapkan_data_sementara


class TestPrioritas(unittest.TestCase):
    def setUp(self):
        self.path = siapkan_data_sementara(self)

    def _baca_file(self):
        with open(self.path, encoding="utf-8") as f:
            return json.load(f)

    def _jalankan_menu(self, masukan):
        buffer = io.StringIO()
        with patch("builtins.input", side_effect=masukan):
            with redirect_stdout(buffer):
                main.main()
        return buffer.getvalue()

    def test_prioritas_default_sedang(self):
        hasil = tasks.tambah_tugas("Laporan", "2026-11-20")

        self.assertEqual(hasil["prioritas"], "sedang")

    def test_tambah_dengan_prioritas_tinggi(self):
        hasil = tasks.tambah_tugas("Laporan", "2026-11-20", "Basis Data", "tinggi")

        self.assertEqual(hasil["prioritas"], "tinggi")

    def test_prioritas_tidak_valid_ditolak(self):
        with self.assertRaises(ValueError):
            tasks.tambah_tugas("Laporan", "2026-11-20", "", "penting")

        self.assertEqual(tasks.daftar_tugas, [])

    def test_prioritas_tersimpan_ke_file(self):
        tasks.tambah_tugas("Laporan", "2026-11-20", "", "rendah")

        self.assertEqual(self._baca_file()[0]["prioritas"], "rendah")

    def test_muat_data_lama_tanpa_prioritas(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump([{"id": 1, "judul": "Lama", "kategori": "",
                        "deadline": "2026-11-20", "selesai": False}], f)

        tasks.muat_tugas()

        self.assertEqual(tasks.daftar_tugas[0]["prioritas"], "sedang")

    def test_tampil_prioritas_di_tabel(self):
        tasks.tambah_tugas("Laporan", "2026-11-20", "", "tinggi")

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            tasks.tampilkan_tugas()
        output = buffer.getvalue()

        self.assertIn("Prioritas", output)
        self.assertIn("tinggi", output)

    def test_menu_tambah_dengan_prioritas(self):
        self._jalankan_menu(["1", "Laporan", "2026-11-20", "", "TINGGI", "0"])

        self.assertEqual(tasks.daftar_tugas[0]["prioritas"], "tinggi")

    def test_menu_menolak_prioritas_salah(self):
        output = self._jalankan_menu(["1", "Laporan", "2026-11-20", "", "penting", "0"])

        self.assertEqual(tasks.daftar_tugas, [])
        self.assertIn("Prioritas harus", output)


if __name__ == "__main__":
    unittest.main()