import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from src import main, tasks


class TestMenu(unittest.TestCase):
    def setUp(self):
        tasks.daftar_tugas.clear()
        tasks._id_berikutnya = 1

    def _jalankan(self, masukan):
        """Jalankan main() dengan input palsu, kembalikan teks yang dicetak."""
        buffer = io.StringIO()
        with patch("builtins.input", side_effect=masukan):
            with redirect_stdout(buffer):
                main.main()
        return buffer.getvalue()

    def test_tambah_tugas_lewat_menu(self):
        output = self._jalankan(["1", "Laporan Basis Data", "2026-11-20", "0"])

        self.assertEqual(len(tasks.daftar_tugas), 1)
        self.assertEqual(tasks.daftar_tugas[0]["judul"], "Laporan Basis Data")
        self.assertIn("berhasil ditambahkan", output)

    def test_tandai_selesai_lewat_menu(self):
        tasks.tambah_tugas("Laporan Basis Data", "2026-11-20")

        self._jalankan(["3", "1", "0"])

        self.assertTrue(tasks.daftar_tugas[0]["selesai"])

    def test_hapus_tugas_lewat_menu(self):
        tasks.tambah_tugas("Laporan Basis Data", "2026-11-20")

        self._jalankan(["4", "1", "0"])

        self.assertEqual(len(tasks.daftar_tugas), 0)

    def test_id_bukan_angka(self):
        output = self._jalankan(["3", "abc", "0"])

        self.assertIn("ID harus berupa angka.", output)

    def test_pilihan_tidak_valid(self):
        output = self._jalankan(["9", "0"])

        self.assertIn("Pilihan tidak valid", output)


if __name__ == "__main__":
    unittest.main()