# Aplikasi Podcast Desa

Aplikasi manajemen podcast digital untuk desa, memungkinkan pengelolaan script, narasumber, dan timeline produksi serta publikasi konten podcast ke masyarakat.

## Fitur Utama
- **Dashboard Admin**: Ringkasan data podcast.
- **Manajemen Podcast**: CRUD data podcast dan narasumber.
- **Timeline Produksi**: Pelacakan status produksi (Planning, Produksi, Editing, Publish).
- **Generator PDF**: Cetak script podcast otomatis ke format PDF.
- **Halaman Publik**: Daftar podcast yang sudah dipublikasikan untuk warga.

## Teknologi
- **Backend**: Flask (Python)
- **Database**: SQLAlchemy (SQLite)
- **Frontend**: Bootstrap & Jinja2
- **PDF Engine**: FPDF

## Cara Menjalankan
1. Instal dependensi:
   ```bash
   pip install -r requirements.txt
   ```
2. Jalankan aplikasi:
   ```bash
   python app.py
   ```
3. Buka browser di `http://127.0.0.1:5000`
