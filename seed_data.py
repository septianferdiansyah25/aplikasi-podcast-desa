from app import app, db
from models import User, Podcast
from werkzeug.security import generate_password_hash
from datetime import datetime
from utils import generate_podcast_pdf
import os

def seed():
    with app.app_context():
        # 1. Hapus data lama dan buat baru sesuai struktur revisi
        db.drop_all()
        db.create_all()

        # 2. Tambah Admin (sudah ada di app.py sebenarnya tapi kita pastikan)
        admin = User.query.filter_by(email='admin@desa.id').first()
        if not admin:
            admin = User(
                nama="Administrator Desa",
                email="admin@desa.id",
                password_hash=generate_password_hash("admin123"),
                role="admin"
            )
            db.session.add(admin)
            db.session.commit()

        # 3. Tambah Podcast (Narasumber langsung diketik)
        p1 = Podcast(
            judul="Pentingnya Vaksinasi PIN Polio",
            deskripsi="Sosialisasi mengenai pekan imunisasi nasional polio untuk anak usia 0-7 tahun di desa kita.",
            kategori="Sosialisasi",
            tanggal=datetime.now(),
            script_text="""
HOST: Halo warga desa sekalian! Selamat datang di Podcast Desa Digital.
HARI INI: Kita kedatangan narasumber spesial, Dr. Andi Wijaya.
DOKTER: Halo warga, penting sekali bagi putra-putri kita mendapatkan vaksin polio...
[Isi Script Lanjutan...]
Pemberian vaksin akan dilaksanakan di Balai Desa besok pagi pukul 08.00 WIB.
Pastikan membawa buku KIA. Terima kasih!
""",
            status="publish",
            admin_id=admin.id,
            narasumber_nama="Dr. Andi Wijaya",
            narasumber_deskripsi="Kepala Puskesmas - Dinas Kesehatan"
        )
        
        p2 = Podcast(
            judul="Strategi Pemasaran Produk UMKM via TikTok",
            deskripsi="Tips dan trik meningkatkan penjualan produk kerajinan desa melalui media sosial modern.",
            kategori="Ekonomi",
            tanggal=datetime.now(),
            script_text="""
HOST: Bagaimana produk kerajinan kita bisa bersaing di kancah nasional?
IBU SITI: Kuncinya adalah visualisasi dan storytelling di media sosial.
Kita harus berani membuat konten video pendek di TikTok...
[Tips 1: Pencahayaan yang baik]
[Tips 2: Musik yang trending]
Semoga bermanfaat bagi para pelaku UMKM di desa kita!
""",
            status="publish",
            admin_id=admin.id,
            narasumber_nama="Ibu Siti Aminah",
            narasumber_deskripsi="Ketua UMKM Desa - Paguyuban Kreatif"
        )
        
        db.session.add_all([p1, p2])
        db.session.commit()

        # 4. Generate PDF untuk data dummy
        p1.file_pdf = generate_podcast_pdf(p1, p1.narasumber_nama)
        p2.file_pdf = generate_podcast_pdf(p2, p2.narasumber_nama)
        db.session.commit()

        print("Seeding completed successfully!")

if __name__ == '__main__':
    seed()
