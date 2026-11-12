import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from src import main, tasks
from tests.helpers import siapkan_data_sementara


class TestDeadlineValid(unittest.TestCase):
    def test_format_benar(self):
        self.assertTrue(tasks.deadline_valid("2026-11-20"))
        self.assertTrue(tasks.deadline_valid("2028-02-29"))  # tahun kabisat

    def test_format_salah(self):
        for teks in ["besok", "20-11-2026", "2026-2-5", "2026/11/20", "", "2026-11-20 "]:
            with self.subTest(teks=teks):
                self.assertFalse(tasks.deadline_valid(teks))

    def test_tanggal_tidak_ada(self):
        self.assertFalse(tasks.deadline_valid("2026-02-30"))
        self.assertFalse(tasks.deadline_valid("2026-13-01"))


class TestTambahDeadlineSalah(unittest.TestCase):
    def setUp(self):
        self.path = siapkan_data_sementara(self)

    def test_tambah_tugas_menolak_deadline_salah(self):
        with self.assertRaises(ValueError):
            tasks.tambah_tugas("Laporan Basis Data", "besok")

        self.assertEqual(tasks.daftar_tugas, [])
        self.assertFalse(self.path.exists())

    def test_menu_menolak_deadline_salah(self):
        buffer = io.StringIO()
        with patch("builtins.input", side_effect=["1", "Laporan", "20-11-2026", "0"]):
            with redirect_stdout(buffer):
                main.main()

        self.assertEqual(tasks.daftar_tugas, [])
        self.assertIn("Deadline harus berformat", buffer.getvalue())


if __name__ == "__main__":
    unittest.main()