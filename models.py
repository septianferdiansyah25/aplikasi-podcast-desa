from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

# Inisialisasi Database
db = SQLAlchemy()

class User(db.Model, UserMixin):
    """Model untuk data pengguna (Khusus Admin Desa)"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='admin') # Hanya admin yang memiliki akses login

# Narasumber model removed as it is now integrated into Podcast table

class Podcast(db.Model):
    """Model untuk data Podcast"""
    __tablename__ = 'podcasts'
    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(200), nullable=False)
    deskripsi = db.Column(db.Text)
    kategori = db.Column(db.String(50))
    tanggal = db.Column(db.Date, default=datetime.utcnow)
    script_text = db.Column(db.Text)
    file_pdf = db.Column(db.String(255)) # Menyimpan nama file PDF
    status = db.Column(db.String(20), default='draft') # 'plan', 'produksi', 'editing', 'publish', 'plan ditolak'
    catatan = db.Column(db.Text) # Untuk alasan ditolak atau revisi
    jumlah_revisi = db.Column(db.Integer, default=0) # Hitungan berapa kali direvisi
    link_video = db.Column(db.String(255)) # Link video YouTube atau lainnya
    
    # Timeline Produksi
    tanggal_plan = db.Column(db.Date)
    tanggal_produksi = db.Column(db.Date)
    tanggal_editing = db.Column(db.Date)
    tanggal_publish = db.Column(db.Date)
    
    # Data Narasumber (Langsung di tabel Podcast)
    narasumber_nama = db.Column(db.String(100), nullable=False)
    narasumber_deskripsi = db.Column(db.String(200)) # Jabatan atau Info singkat
    
    # Foreign Keys
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # narasumber_id relation removed
    
    # Relasi balik ke Admin yang membuat
    admin = db.relationship('User', backref='podcasts_created', lazy=True)
