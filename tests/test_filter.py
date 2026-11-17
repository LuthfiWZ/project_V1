import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from src import main, tasks
from tests.helpers import siapkan_data_sementara


class DasarTest(unittest.TestCase):
    def setUp(self):
        siapkan_data_sementara(self)
        tasks.tambah_tugas("Laporan Basis Data", "2026-11-20", "Basis Data", "tinggi")
        tasks.tambah_tugas("Kuis Algoritma", "2026-11-27", "Algoritma", "sedang")
        tasks.tambah_tugas("Presentasi Jaringan", "2026-11-25", "Jaringan", "rendah")
        tasks.tandai_selesai(1)

    def _jalankan_menu(self, masukan):
        buffer = io.StringIO()
        with patch("builtins.input", side_effect=masukan):
            with redirect_stdout(buffer):
                main.main()
        return buffer.getvalue()


class TestCariTugas(DasarTest):
    def test_cari_menemukan_judul(self):
        hasil = tasks.cari_tugas("kuis")

        self.assertEqual([t["id"] for t in hasil], [2])

    def test_cari_tidak_peduli_huruf_besar(self):
        hasil = tasks.cari_tugas("LAPORAN")

        self.assertEqual(len(hasil), 1)
        self.assertEqual(hasil[0]["judul"], "Laporan Basis Data")

    def test_cari_tidak_ketemu(self):
        self.assertEqual(tasks.cari_tugas("zzz"), [])


class TestFilterTugas(DasarTest):
    def test_filter_kategori(self):
        hasil = tasks.filter_tugas(kategori="basis data")

        self.assertEqual([t["id"] for t in hasil], [1])

    def test_filter_prioritas(self):
        hasil = tasks.filter_tugas(prioritas="rendah")

        self.assertEqual([t["id"] for t in hasil], [3])

    def test_filter_status(self):
        selesai = tasks.filter_tugas(status="selesai")
        belum = tasks.filter_tugas(status="belum")

        self.assertEqual([t["id"] for t in selesai], [1])
        self.assertEqual([t["id"] for t in belum], [2, 3])

    def test_filter_gabungan(self):
        hasil = tasks.filter_tugas(prioritas="sedang", status="belum")

        self.assertEqual([t["id"] for t in hasil], [2])

    def test_filter_tanpa_syarat_mengembalikan_semua(self):
        self.assertEqual(len(tasks.filter_tugas()), 3)


class TestMenuCariFilter(DasarTest):
    def test_menu_cari(self):
        output = self._jalankan_menu(["5", "basis", "0"])

        self.assertIn("Laporan Basis Data", output)
        self.assertNotIn("Kuis Algoritma", output)

    def test_menu_cari_kosong(self):
        output = self._jalankan_menu(["5", "", "0"])

        self.assertIn("Kata kunci tidak boleh kosong.", output)

    def test_menu_filter(self):
        output = self._jalankan_menu(["6", "", "tinggi", "", "0"])

        self.assertIn("Laporan Basis Data", output)
        self.assertNotIn("Kuis Algoritma", output)

    def test_menu_filter_prioritas_salah(self):
        output = self._jalankan_menu(["6", "", "penting", "", "0"])

        self.assertIn("Prioritas harus", output)


if __name__ == "__main__":
    unittest.main()