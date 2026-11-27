"""REST API Task Manager Kuliah (Flask)."""

from flask import Flask, jsonify, request

from src import logger, tasks

FIELD_UBAH = {"judul", "deadline", "kategori", "prioritas", "selesai"}
FIELD_TEKS = ("judul", "deadline", "kategori", "prioritas")


def _galat(pesan, kode=400):
    return jsonify({"error": pesan}), kode


def create_app():
    """Buat aplikasi Flask. Dipisah jadi fungsi supaya mudah dites."""
    app = Flask(__name__)
    app.json.ensure_ascii = False

    @app.get("/tugas")
    def daftar_semua():
        return jsonify(tasks.daftar_tugas)

    @app.get("/tugas/<int:id_tugas>")
    def satu_tugas(id_tugas):
        for tugas in tasks.daftar_tugas:
            if tugas["id"] == id_tugas:
                return jsonify(tugas)
        return _galat("Tugas tidak ditemukan.", 404)

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

    @app.put("/tugas/<int:id_tugas>")
    def ubah(id_tugas):
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return _galat("Body harus berupa JSON object.")
        if not data:
            return _galat("Tidak ada field yang diubah.")

        asing = set(data) - FIELD_UBAH
        if asing:
            return _galat(f"Field tidak dikenal: {', '.join(sorted(asing))}.")
        for nama in FIELD_TEKS:
            if nama in data and not isinstance(data[nama], str):
                return _galat(f"Field {nama} harus berupa teks.")
        if "selesai" in data and not isinstance(data["selesai"], bool):
            return _galat("Field selesai harus true atau false.")

        try:
            tugas = tasks.ubah_tugas(id_tugas, **data)
        except ValueError as galat:
            return _galat(str(galat))

        if tugas is None:
            return _galat("Tugas tidak ditemukan.", 404)
        return jsonify(tugas)

    @app.delete("/tugas/<int:id_tugas>")
    def hapus(id_tugas):
        tugas = tasks.hapus_tugas(id_tugas)
        if tugas is None:
            return _galat("Tugas tidak ditemukan.", 404)
        return jsonify(tugas)

    return app


if __name__ == "__main__":
    logger.aktifkan()
    tasks.muat_tugas()
    create_app().run(port=5000)