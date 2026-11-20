"""Pencatatan kejadian penting ke file log."""

import logging
from pathlib import Path

# Lokasi file log: <folder proyek>/data/app.log
FILE_LOG = Path(__file__).resolve().parent.parent / "data" / "app.log"

_logger = logging.getLogger("task_manager")
_logger.setLevel(logging.INFO)
_logger.propagate = False
# Tanpa handler file, pesan dibuang diam-diam (tidak error, tidak tercetak)
_logger.addHandler(logging.NullHandler())


def aktifkan(path=FILE_LOG):
    """Mulai mencatat ke file log. Dipanggil sekali saat program dijalankan."""
    matikan()
    path.parent.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(path, encoding="utf-8")
    handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    )
    _logger.addHandler(handler)


def matikan():
    """Hentikan pencatatan ke file dan tutup file log."""
    for handler in list(_logger.handlers):
        if isinstance(handler, logging.FileHandler):
            handler.close()
            _logger.removeHandler(handler)


def info(pesan):
    _logger.info(pesan)


def peringatan(pesan):
    _logger.warning(pesan)