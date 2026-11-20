import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from src import logger, tasks
from tests.helpers import siapkan_data_sementara


class TestLogging(unittest.TestCase):
    def setUp(self):
        self.path_data = siapkan_data_sementara(self)

        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.path_log = Path(folder.name) / "app.log"

        logger.aktifkan(self.path_log)
        # Dijalankan sebelum folder dihapus (cleanup berjalan terbalik)
        self.addCleanup(logger.matikan)

    def _isi_log(self):
        return self.path_log.read_text(encoding="utf-8")

    def test_tambah_tugas_tercatat(self):
        tasks.tambah_tugas("Laporan", "2026-11-20")

        isi = self._isi_log()
        self.assertIn("[INFO]", isi)
        self.assertIn("Tugas ditambahkan: id=1, judul=Laporan", isi)

    def test_tandai_selesai_tercatat(self):
        tasks.tambah_tugas("Laporan", "2026-11-20")

        tasks.tandai_selesai(1)

        self.assertIn("Tugas ditandai selesai: id=1", self._isi_log())

    def test_hapus_tercatat(self):
        tasks.tambah_tugas("Laporan", "2026-11-20")

        tasks.hapus_tugas(1)

        self.assertIn("Tugas dihapus: id=1", self._isi_log())

    def test_hapus_id_tidak_ditemukan_jadi_peringatan(self):
        tasks.hapus_tugas(99)

        isi = self._isi_log()
        self.assertIn("[WARNING]", isi)
        self.assertIn("Hapus gagal: id=99", isi)

    def test_tandai_id_tidak_ditemukan_jadi_peringatan(self):
        tasks.tandai_selesai(99)

        isi = self._isi_log()
        self.assertIn("[WARNING]", isi)
        self.assertIn("Tandai selesai gagal: id=99", isi)

    def test_file_data_rusak_tercatat(self):
        self.path_data.write_text("bukan json", encoding="utf-8")

        with redirect_stdout(io.StringIO()):
            tasks.muat_tugas()

        self.assertEqual(tasks.daftar_tugas, [])
        self.assertIn("bukan JSON valid", self._isi_log())

    def test_isi_file_bukan_daftar_tugas(self):
        self.path_data.write_text('{"a": 1}', encoding="utf-8")

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            tasks.muat_tugas()

        self.assertEqual(tasks.daftar_tugas, [])
        self.assertIn("Peringatan", buffer.getvalue())
        self.assertIn("Bentuk isi file data tidak sesuai", self._isi_log())

    def test_tanpa_log_aktif_tetap_aman(self):
        logger.matikan()

        hasil = tasks.tambah_tugas("Laporan", "2026-11-20")

        self.assertEqual(hasil["id"], 1)


if __name__ == "__main__":
    unittest.main()