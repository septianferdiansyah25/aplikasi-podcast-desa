import random
from app import app, db
from models import User, Podcast
from utils import generate_podcast_pdf
from datetime import datetime, timedelta

def create_bulk_data():
    with app.app_context():
        # Pastikan ada admin
        admin = User.query.filter_by(role='admin').first()
        if not admin:
            print("Admin tidak ditemukan. Jalankan aplikasi dulu untuk membuat admin default.")
            return

        categories = ["Berita Desa", "Sosialisasi", "Inspirasi", "Budaya", "Ekonomi"]
        narasumber_pool = [
            ("Bapak Ahmad", "Ketua RW 01"),
            ("Ibu Siti", "Ketua PKK"),
            ("Pak Budi", "Petani Milenial"),
            ("dr. Laila", "Kepala Puskesmas"),
            ("Bapak Heru", "Babinsa Desa"),
            ("Ibu Ratna", "Guru SD"),
            ("Pak Mamat", "Pengusaha Keripik"),
            ("Teh Rina", "Karang Taruna")
        ]

        templates = {
            "Berita Desa": [
                "Laporan Mingguan Desa", "Update Pembangunan Jembatan", 
                "Rincian Dana Desa", "Jadwal Posyandu Terkini", "Berita Kerja Bakti"
            ],
            "Sosialisasi": [
                "Pentingnya Kebersihan", "Aturan Baru Parkir Desa", 
                "Sosialisasi Pajak Bumi", "Bahaya Narkoba Bagi Remaja", "Pilah Sampah Sejak Diri"
            ],
            "Inspirasi": [
                "Sukses Budidaya Ikan", "Kisah Juara Lomba Desa", 
                "Pemuda Kreatif Sagara", "Inspirasi Warung Modern", "Menabung Untuk Masa Depan"
            ],
            "Budaya": [
                "Melestarikan Pencak Silat", "Sejarah Asal Usul Desa", 
                "Ragam Batik Sagara", "Seni Calung Kembali Rama", "Wayang Golek Malam Minggu"
            ],
            "Ekonomi": [
                "Tips UMKM Berkembang", "Pasar Kaget Hari Minggu", 
                "Pinjaman Modal Desa", "Koperasi Maju Bersama", "Cara Jualan Online Warga"
            ]
        }

        print("Memulai proses seeding bulk data...")
        
        for cat in categories:
            print(f">> Menambahkan 5 data untuk kategori: {cat}")
            for i in range(1, 6):
                ns_nama, ns_desc = random.choice(narasumber_pool)
                judul = f"{templates[cat][i-1]} #{i}"
                tanggal = datetime.now().date() - timedelta(days=random.randint(0, 30))
                
                script_text = f"""
Selamat pagi warga desa sekalian! 
Selamat datang kembali di Podcast Desa kita tercinta.

Hari ini kita akan berbincang mengenai {judul}. 
Topik ini sangat menarik karena berkaitan langsung dengan kesejahteraan kita di desa.

Nama saya adalah {ns_nama} selaku {ns_desc}. 
Saya ingin menyampaikan bahwa {judul} ini bertujuan untuk kemajuan bersama.

Pesan saya: "Mari kita gotong royong dan terus berinovasi untuk masa depan desa yang lebih cerah."

Terima kasih telah mendengarkan, sampai jumpa di episode selanjutnya!
                """
                
                p = Podcast(
                    judul=judul,
                    deskripsi=f"Informasi lengkap mengenai {judul} untuk seluruh warga desa.",
                    kategori=cat,
                    tanggal=tanggal,
                    script_text=script_text.strip(),
                    status='publish',
                    admin_id=admin.id,
                    narasumber_nama=ns_nama,
                    narasumber_deskripsi=ns_desc
                )
                
                db.session.add(p)
                db.session.commit() # Commit ID dulu
                
                # Generate PDF
                p.file_pdf = generate_podcast_pdf(p, ns_nama)
                db.session.commit()
                
                print(f"   [OK] {judul} berhasil dibuat.")

        print("\nSukses! 25 data dummy berhasil ditambahkan.")

if __name__ == "__main__":
    create_bulk_data()
