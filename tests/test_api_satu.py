import unittest
from pathlib import Path

from src import tasks
from src.api import create_app
from tests.helpers import siapkan_data_sementara

FILE_DOKUMENTASI = Path(__file__).resolve().parent.parent / "docs" / "api.md"


class TestGetSatuTugas(unittest.TestCase):
    def setUp(self):
        siapkan_data_sementara(self)
        self.client = create_app().test_client()
        tasks.tambah_tugas("Laporan", "2026-11-20", "Basis Data", "tinggi")
        tasks.tambah_tugas("Kuis", "2026-11-27")

    def test_ambil_satu_tugas(self):
        respons = self.client.get("/tugas/2")

        self.assertEqual(respons.status_code, 200)
        data = respons.get_json()
        self.assertEqual(data["id"], 2)
        self.assertEqual(data["judul"], "Kuis")

    def test_id_tidak_ditemukan(self):
        respons = self.client.get("/tugas/99")

        self.assertEqual(respons.status_code, 404)
        self.assertIn("error", respons.get_json())

    def test_id_bukan_angka(self):
        respons = self.client.get("/tugas/abc")

        self.assertEqual(respons.status_code, 404)


class TestDokumentasi(unittest.TestCase):
    def test_dokumentasi_menyebut_semua_endpoint(self):
        isi = FILE_DOKUMENTASI.read_text(encoding="utf-8")

        for bagian in [
            "## GET /tugas",
            "## GET /tugas/{id}",
            "## POST /tugas",
            "## PUT /tugas/{id}",
            "## DELETE /tugas/{id}",
        ]:
            with self.subTest(bagian=bagian):
                self.assertIn(bagian, isi)


if __name__ == "__main__":
    unittest.main()