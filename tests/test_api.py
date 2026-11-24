import json
import unittest

from src import tasks
from src.api import create_app
from tests.helpers import siapkan_data_sementara


class TestApi(unittest.TestCase):
    def setUp(self):
        self.path = siapkan_data_sementara(self)
        self.client = create_app().test_client()

    def test_get_kosong(self):
        respons = self.client.get("/tugas")

        self.assertEqual(respons.status_code, 200)
        self.assertEqual(respons.get_json(), [])

    def test_get_berisi(self):
        tasks.tambah_tugas("Laporan", "2026-11-20", "Basis Data", "tinggi")

        respons = self.client.get("/tugas")

        data = respons.get_json()
        self.assertEqual(respons.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["judul"], "Laporan")
        self.assertEqual(data[0]["prioritas"], "tinggi")

    def test_post_berhasil(self):
        respons = self.client.post(
            "/tugas",
            json={"judul": "Laporan", "deadline": "2026-11-20",
                  "kategori": "Basis Data", "prioritas": "tinggi"},
        )

        self.assertEqual(respons.status_code, 201)
        data = respons.get_json()
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["kategori"], "Basis Data")
        self.assertFalse(data["selesai"])
        self.assertEqual(len(tasks.daftar_tugas), 1)

    def test_post_memakai_nilai_default(self):
        respons = self.client.post(
            "/tugas", json={"judul": "Laporan", "deadline": "2026-11-20"}
        )

        data = respons.get_json()
        self.assertEqual(respons.status_code, 201)
        self.assertEqual(data["kategori"], "")
        self.assertEqual(data["prioritas"], "sedang")

    def test_post_tersimpan_ke_file(self):
        self.client.post(
            "/tugas", json={"judul": "Laporan", "deadline": "2026-11-20"}
        )

        with open(self.path, encoding="utf-8") as f:
            isi = json.load(f)
        self.assertEqual(isi[0]["judul"], "Laporan")

    def test_post_bukan_json(self):
        respons = self.client.post("/tugas", data="bukan json")

        self.assertEqual(respons.status_code, 400)
        self.assertIn("error", respons.get_json())
        self.assertEqual(tasks.daftar_tugas, [])

    def test_post_field_wajib_hilang(self):
        respons = self.client.post("/tugas", json={"judul": "Laporan"})

        self.assertEqual(respons.status_code, 400)
        self.assertEqual(tasks.daftar_tugas, [])

    def test_post_deadline_salah(self):
        respons = self.client.post(
            "/tugas", json={"judul": "Laporan", "deadline": "besok"}
        )

        self.assertEqual(respons.status_code, 400)
        self.assertIn("Deadline", respons.get_json()["error"])
        self.assertEqual(tasks.daftar_tugas, [])

    def test_post_prioritas_salah(self):
        respons = self.client.post(
            "/tugas",
            json={"judul": "Laporan", "deadline": "2026-11-20",
                  "prioritas": "penting"},
        )

        self.assertEqual(respons.status_code, 400)
        self.assertIn("Prioritas", respons.get_json()["error"])

    def test_post_tipe_data_salah(self):
        respons = self.client.post(
            "/tugas", json={"judul": 123, "deadline": "2026-11-20"}
        )

        self.assertEqual(respons.status_code, 400)
        self.assertEqual(tasks.daftar_tugas, [])


if __name__ == "__main__":
    unittest.main()