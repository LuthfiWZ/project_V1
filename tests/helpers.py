"""Fungsi bantu untuk test."""

import tempfile
from pathlib import Path
from unittest.mock import patch

from src import tasks


def siapkan_data_sementara(test_case):
    """Reset data di memori dan arahkan penyimpanan ke folder sementara.

    Dipanggil di setUp() setiap test. Folder sementara dihapus otomatis
    setelah test selesai. Mengembalikan path file JSON sementara.
    """
    tasks.daftar_tugas.clear()
    tasks._id_berikutnya = 1

    folder = tempfile.TemporaryDirectory()
    test_case.addCleanup(folder.cleanup)

    path = Path(folder.name) / "tasks.json"
    pengganti = patch.object(tasks, "FILE_DATA", path)
    pengganti.start()
    test_case.addCleanup(pengganti.stop)
    return path