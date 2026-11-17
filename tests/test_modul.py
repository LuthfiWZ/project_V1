import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from src import storage, tampilan, validasi


class TestStorage(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.path = Path(folder.name) / "sub" / "data.json"

    def test_tulis_lalu_baca(self):
        storage.tulis_json(self.path, [{"id": 1}])

        self.assertEqual(storage.baca_json(self.path), [{"id": 1}])

    def test_baca_file_tidak_ada(self):
        self.assertEqual(storage.baca_json(self.path), [])

    def test_baca_file_rusak(self):
        self.path.parent.mkdir(parents=True)
        self.path.write_text("bukan json", encoding="utf-8")

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            hasil = storage.baca_json(self.path)

        self.assertEqual(hasil, [])
        self.assertIn("Peringatan", buffer.getvalue())


class TestTampilan(unittest.TestCase):
    def _cetak(self, daftar):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            tampilan.cetak_tabel(daftar)
        return buffer.getvalue()

    def test_cetak_kosong(self):
        self.assertIn("Belum ada tugas.", self._cetak([]))

    def test_cetak_berisi(self):
        output = self._cetak([{
            "id": 1, "judul": "Laporan", "kategori": "", "prioritas": "tinggi",
            "deadline": "2026-11-20", "selesai": True,
        }])

        self.assertIn("Laporan", output)
        self.assertIn("Selesai", output)
        self.assertIn("-", output)


if __name__ == "__main__":
    unittest.main()