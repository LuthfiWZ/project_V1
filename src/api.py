"""REST API Task Manager Kuliah (Flask)."""

from flask import Flask, jsonify, request

from src import logger, tasks


def _galat(pesan, kode=400):
    return jsonify({"error": pesan}), kode


def create_app():
    """Buat aplikasi Flask. Dipisah jadi fungsi supaya mudah dites."""
    app = Flask(__name__)
    app.json.ensure_ascii = False

    @app.get("/tugas")
    def daftar_semua():
        return jsonify(tasks.daftar_tugas)

    @app.post("/tugas")
    def tambah():
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return _galat("Body harus berupa JSON object.")

        judul = data.get("judul")
        deadline = data.get("deadline")
        kategori = data.get("kategori", "")
        prioritas = data.get("prioritas", "sedang")

        if not isinstance(judul, str) or not isinstance(deadline, str):
            return _galat("Field judul dan deadline wajib diisi (teks).")
        if not isinstance(kategori, str) or not isinstance(prioritas, str):
            return _galat("Field kategori dan prioritas harus berupa teks.")

        try:
            tugas = tasks.tambah_tugas(judul, deadline, kategori.strip(), prioritas)
        except ValueError as galat:
            return _galat(str(galat))

        return jsonify(tugas), 201

    return app


if __name__ == "__main__":
    logger.aktifkan()
    tasks.muat_tugas()
    create_app().run(port=5000)