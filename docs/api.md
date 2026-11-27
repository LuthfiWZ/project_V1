# Dokumentasi API Task Manager Kuliah

Base URL (lokal): `http://127.0.0.1:5000`

Semua request dan respons memakai format JSON. Untuk request dengan body
(POST dan PUT), kirim header `Content-Type: application/json`.

## Menjalankan server
```
pip install -r requirements.txt
python -m src.api
```

## Bentuk data tugas
```json
{
  "id": 1,
  "judul": "Laporan Basis Data",
  "kategori": "Basis Data",
  "prioritas": "tinggi",
  "deadline": "2026-11-30",
  "selesai": false
}
```

| Field | Tipe | Keterangan |
|---|---|---|
| id | angka | Dibuat otomatis, tidak bisa diubah |
| judul | teks | Wajib, tidak boleh kosong |
| kategori | teks | Opsional, nama mata kuliah |
| prioritas | teks | `tinggi`, `sedang` (default), atau `rendah` |
| deadline | teks | Wajib, format `YYYY-MM-DD` dan tanggalnya harus valid |
| selesai | boolean | `false` saat dibuat |

## Ringkasan endpoint

| Method | Endpoint | Fungsi |
|---|---|---|
| GET | /tugas | Lihat semua tugas |
| GET | /tugas/{id} | Lihat satu tugas |
| POST | /tugas | Tambah tugas |
| PUT | /tugas/{id} | Ubah tugas |
| DELETE | /tugas/{id} | Hapus tugas |

## GET /tugas
Mengembalikan semua tugas.

Respons `200 OK`:
```json
[
  {
    "id": 1,
    "judul": "Laporan Basis Data",
    "kategori": "Basis Data",
    "prioritas": "tinggi",
    "deadline": "2026-11-30",
    "selesai": false
  }
]
```
Kalau belum ada tugas, hasilnya `[]`.

## GET /tugas/{id}
Mengembalikan satu tugas.

- `200 OK`: objek tugas.
- `404 Not Found`: `{"error": "Tugas tidak ditemukan."}`

## POST /tugas
Menambah tugas baru.

Body:
```json
{
  "judul": "Laporan Basis Data",
  "deadline": "2026-11-30",
  "kategori": "Basis Data",
  "prioritas": "tinggi"
}
```
`judul` dan `deadline` wajib. `kategori` dan `prioritas` opsional.

- `201 Created`: objek tugas yang baru dibuat.
- `400 Bad Request`: body bukan JSON object, field wajib hilang, tipe data
  salah, deadline tidak valid, atau prioritas tidak valid.

Contoh error:
```json
{"error": "Deadline harus berformat YYYY-MM-DD dan tanggalnya valid."}
```

## PUT /tugas/{id}
Mengubah satu atau lebih field. Field yang tidak dikirim tidak berubah.
Field yang boleh diubah: `judul`, `deadline`, `kategori`, `prioritas`, `selesai`.

Body (contoh menandai selesai):
```json
{"selesai": true}
```

- `200 OK`: objek tugas setelah diubah.
- `400 Bad Request`: body kosong, ada field yang tidak dikenal (misalnya `id`),
  tipe data salah, atau nilai tidak valid. Kalau ada satu nilai yang salah,
  tidak ada field yang berubah.
- `404 Not Found`: id tidak ditemukan.

## DELETE /tugas/{id}
Menghapus tugas.

- `200 OK`: objek tugas yang dihapus.
- `404 Not Found`: id tidak ditemukan.

Id tugas yang dihapus tidak digeser. Tugas lain tetap memakai id-nya.

## Contoh pemakaian (PowerShell)
```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5000/tugas -ContentType "application/json" -Body '{"judul":"Laporan","deadline":"2026-11-30"}'
Invoke-RestMethod http://127.0.0.1:5000/tugas/1
Invoke-RestMethod -Method Put -Uri http://127.0.0.1:5000/tugas/1 -ContentType "application/json" -Body '{"selesai":true}'
Invoke-RestMethod -Method Delete -Uri http://127.0.0.1:5000/tugas/1
```

## Contoh pemakaian (curl, Linux/macOS)
```bash
curl -X POST http://127.0.0.1:5000/tugas \
  -H "Content-Type: application/json" \
  -d '{"judul":"Laporan","deadline":"2026-11-30"}'
curl http://127.0.0.1:5000/tugas/1
```