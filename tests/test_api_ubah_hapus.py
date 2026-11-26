import json
import unittest

from src import tasks
from src.api import create_app
from tests.helpers import siapkan_data_sementara


class DasarApi(unittest.TestCase):
    def setUp(self):
        self.path = siapkan_data_sementara(self)
        self.client = create_app().test_client()
        tasks.tambah_tugas("Laporan", "2026-11-20", "Basis Data", "tinggi")
        tasks.tambah_tugas("Kuis", "2026-11-27")

    def _isi_file(self):
        with open(self.path, encoding="utf-8") as f:
            return json.load(f)


class TestPut(DasarApi):
    def test_ubah_judul(self):
        respons = self.client.put("/tugas/1", json={"judul": "Laporan Akhir"})

        self.assertEqual(respons.status_code, 200)
        self.assertEqual(respons.get_json()["judul"], "Laporan Akhir")
        self.assertEqual(tasks.daftar_tugas[0]["judul"], "Laporan Akhir")
        self.assertEqual(tasks.daftar_tugas[0]["deadline"], "2026-11-20")

    def test_tandai_selesai(self):
        respons = self.client.put("/tugas/1", json={"selesai": True})

        self.assertEqual(respons.status_code, 200)
        self.assertTrue(respons.get_json()["selesai"])

    def test_ubah_banyak_field(self):
        respons = self.client.put(
            "/tugas/2",
            json={"deadline": "2026-12-01", "kategori": " Algoritma ",
                  "prioritas": "rendah"},
        )

        data = respons.get_json()
        self.assertEqual(respons.status_code, 200)
        self.assertEqual(data["deadline"], "2026-12-01")
        self.assertEqual(data["kategori"], "Algoritma")
        self.assertEqual(data["prioritas"], "rendah")

    def test_perubahan_tersimpan_ke_file(self):
        self.client.put("/tugas/1", json={"selesai": True})

        self.assertTrue(self._isi_file()[0]["selesai"])

    def test_id_tidak_ditemukan(self):
        respons = self.client.put("/tugas/99", json={"selesai": True})

        self.assertEqual(respons.status_code, 404)
        self.assertIn("error", respons.get_json())

    def test_bukan_json(self):
        respons = self.client.put("/tugas/1", data="bukan json")

        self.assertEqual(respons.status_code, 400)

    def test_body_kosong(self):
        respons = self.client.put("/tugas/1", json={})

        self.assertEqual(respons.status_code, 400)

    def test_field_tidak_dikenal(self):
        respons = self.client.put("/tugas/1", json={"id": 5})

        self.assertEqual(respons.status_code, 400)
        self.assertIn("id", respons.get_json()["error"])
        self.assertEqual(tasks.daftar_tugas[0]["id"], 1)

    def test_deadline_salah_tidak_mengubah_apa_pun(self):
        respons = self.client.put(
            "/tugas/1", json={"judul": "Baru", "deadline": "besok"}
        )

        self.assertEqual(respons.status_code, 400)
        self.assertEqual(tasks.daftar_tugas[0]["judul"], "Laporan")
        self.assertEqual(tasks.daftar_tugas[0]["deadline"], "2026-11-20")

    def test_prioritas_salah(self):
        respons = self.client.put("/tugas/1", json={"prioritas": "penting"})

        self.assertEqual(respons.status_code, 400)
        self.assertEqual(tasks.daftar_tugas[0]["prioritas"], "tinggi")

    def test_selesai_bukan_boolean(self):
        for nilai in ["ya", 1, None]:
            with self.subTest(nilai=nilai):
                respons = self.client.put("/tugas/1", json={"selesai": nilai})
                self.assertEqual(respons.status_code, 400)

        self.assertFalse(tasks.daftar_tugas[0]["selesai"])

    def test_judul_kosong(self):
        respons = self.client.put("/tugas/1", json={"judul": "   "})

        self.assertEqual(respons.status_code, 400)
        self.assertEqual(tasks.daftar_tugas[0]["judul"], "Laporan")


class TestDelete(DasarApi):
    def test_hapus_berhasil(self):
        respons = self.client.delete("/tugas/1")

        self.assertEqual(respons.status_code, 200)
        self.assertEqual(respons.get_json()["judul"], "Laporan")
        self.assertEqual(len(tasks.daftar_tugas), 1)

    def test_hapus_hanya_tugas_itu(self):
        self.client.delete("/tugas/1")

        self.assertEqual([t["id"] for t in tasks.daftar_tugas], [2])

    def test_hapus_tersimpan_ke_file(self):
        self.client.delete("/tugas/1")

        self.assertEqual([t["id"] for t in self._isi_file()], [2])

    def test_hapus_id_tidak_ditemukan(self):
        respons = self.client.delete("/tugas/99")

        self.assertEqual(respons.status_code, 404)
        self.assertEqual(len(tasks.daftar_tugas), 2)


if __name__ == "__main__":
    unittest.main() 