import os
from flask import Flask, render_template, redirect, url_for, request, flash, session, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Podcast
from utils import generate_podcast_pdf, generate_timeline_pdf
from datetime import datetime

# Konfigurasi Aplikasi Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'podcast-desa-secret-key-12345' # Ganti dengan yang lebih aman di produksi
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///podcast_desa.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inisialisasi Database dan Login Manager
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# --- Inisialisasi Database saat Start ---
with app.app_context():
    db.create_all()
    # Membuat Default Admin jika belum ada
    if not User.query.filter_by(role='admin').first():
        admin = User(
            nama="Administrator Desa",
            email="admin@desa.id",
            password_hash=generate_password_hash("admin123"),
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()
        print("Default Admin Created: admin@desa.id / admin123")

# --- Rute Autentikasi --- #

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard' if current_user.role == 'admin' else 'user_home'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash(f'Selamat datang, {user.nama}!', 'success')
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('user_home'))
        else:
            flash('Login gagal. Email atau password salah.', 'danger')
    return render_template('auth/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Anda telah logout.', 'info')
    return redirect(url_for('user_home'))

# --- Rute Admin (Panel Pengelolaan) --- #

@app.route('/admin')
@login_required
def admin_dashboard():
    # Proteksi Role Admin
    if current_user.role != 'admin':
        return redirect(url_for('user_home'))
    
    q = request.args.get('q', '')
    status = request.args.get('status', '')
    
    query = Podcast.query
    
    if q:
        query = query.filter(Podcast.judul.contains(q))
    if status:
        query = query.filter_by(status=status)
        
    # Hitung Statistik per Tahap
    total_podcast = Podcast.query.count()
    total_plan = Podcast.query.filter_by(status='plan').count()
    total_produksi = Podcast.query.filter_by(status='produksi').count()
    total_editing = Podcast.query.filter_by(status='editing').count()
    total_publish = Podcast.query.filter_by(status='publish').count()
    total_rejected = Podcast.query.filter_by(status='plan ditolak').count()
    total_returned = Podcast.query.filter_by(status='dikembalikan').count()
    
    podcasts = query.order_by(Podcast.id.desc()).all()
    
    return render_template('admin/dashboard.html', 
                           total_podcast=total_podcast, 
                           total_plan=total_plan,
                           total_produksi=total_produksi,
                           total_editing=total_editing,
                           total_publish=total_publish,
                           total_rejected=total_rejected,
                           total_returned=total_returned,
                           podcasts=podcasts,
                           q=q,
                           current_status=status)

# Narasumber routes removed

# Kelola Podcast
@app.route('/admin/podcast')
@login_required
def admin_podcast():
    if current_user.role != 'admin': return redirect(url_for('user_home'))
    list_podcast = Podcast.query.all()
    return render_template('admin/podcast/index.html', list_podcast=list_podcast)

@app.route('/admin/podcast/add', methods=['GET', 'POST'])
@login_required
def add_podcast():
    if current_user.role != 'admin': return redirect(url_for('user_home'))
    if request.method == 'POST':
        p = Podcast(
            judul=request.form.get('judul'),
            deskripsi=request.form.get('deskripsi'),
            kategori=request.form.get('kategori'),
            tanggal=datetime.strptime(request.form.get('tanggal'), '%Y-%m-%d').date(),
            script_text=request.form.get('script_text'),
            status=request.form.get('status'),
            catatan=request.form.get('catatan'),
            admin_id=current_user.id,
            narasumber_nama=request.form.get('narasumber_nama'),
            narasumber_deskripsi=request.form.get('narasumber_deskripsi'),
            link_video=request.form.get('link_video')
        )
        
        # Set initial timeline date
        today = datetime.now().date()
        if p.status == 'plan': p.tanggal_plan = today
        elif p.status == 'produksi': p.tanggal_produksi = today
        elif p.status == 'editing': p.tanggal_editing = today
        elif p.status == 'publish': p.tanggal_publish = today
        
        db.session.add(p)
        db.session.commit()
        
        # Generate PDF otomatis setelah simpan database
        p.file_pdf = generate_podcast_pdf(p, p.narasumber_nama)
        db.session.commit()
        
        flash('Podcast baru berhasil ditambahkan.', 'success')
        return redirect(url_for('admin_podcast'))
    return render_template('admin/podcast/add.html', now_date=datetime.now().strftime('%Y-%m-%d'))

@app.route('/admin/podcast/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_podcast(id):
    if current_user.role != 'admin': return redirect(url_for('user_home'))
    p = db.get_or_404(Podcast, id)
    if request.method == 'POST':
        p.judul = request.form.get('judul')
        p.deskripsi = request.form.get('deskripsi')
        p.kategori = request.form.get('kategori')
        p.tanggal = datetime.strptime(request.form.get('tanggal'), '%Y-%m-%d').date()
        p.script_text = request.form.get('script_text')
        
        new_status = request.form.get('status')
        if p.status != new_status:
            today = datetime.now().date()
            if new_status == 'plan':
                p.tanggal_plan = today
                p.tanggal_produksi = p.tanggal_editing = p.tanggal_publish = None
            elif new_status == 'produksi':
                p.tanggal_produksi = today
                p.tanggal_editing = p.tanggal_publish = None
            elif new_status == 'editing':
                p.tanggal_editing = today
                p.tanggal_publish = None
            elif new_status == 'publish':
                p.tanggal_publish = today
            elif new_status == 'dikembalikan':
                p.jumlah_revisi += 1
                # Reset tanggal tahap saat ini karena dikembalikan untuk diperbaiki
                if p.status == 'publish': p.tanggal_publish = None
                elif p.status == 'editing': p.tanggal_editing = None
                elif p.status == 'produksi': p.tanggal_produksi = None
                elif p.status == 'plan': p.tanggal_plan = None
            
        p.status = new_status
        p.catatan = request.form.get('catatan')
        p.narasumber_nama = request.form.get('narasumber_nama')
        p.narasumber_deskripsi = request.form.get('narasumber_deskripsi')
        p.link_video = request.form.get('link_video')
        
        # Regenerate PDF saat edit
        p.file_pdf = generate_podcast_pdf(p, p.narasumber_nama)
        
        db.session.commit()
        flash('Podcast diperbarui.', 'success')
        return redirect(url_for('admin_podcast'))
    return render_template('admin/podcast/edit.html', p=p)

@app.route('/admin/podcast/delete/<int:id>')
@login_required
def delete_podcast(id):
    if current_user.role != 'admin': return redirect(url_for('user_home'))
    p = db.get_or_404(Podcast, id)
    # Hapus file PDF (opsional untuk menjaga storage)
    pdf_path = os.path.join('static', 'pdf', p.file_pdf)
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
        
    db.session.delete(p)
    db.session.commit()
    flash('Podcast berhasil dihapus.', 'success')
    return redirect(url_for('admin_podcast'))

# Laporan Timeline Produksi
@app.route('/admin/laporan')
@login_required
def admin_report():
    if current_user.role != 'admin': return redirect(url_for('user_home'))
    
    q = request.args.get('q', '')
    status = request.args.get('status', '')
    
    query = Podcast.query
    if q:
        query = query.filter(Podcast.judul.contains(q))
    if status:
        query = query.filter_by(status=status)
        
    podcasts = query.order_by(Podcast.id.desc()).all()
    
    return render_template('admin/report.html', 
                           podcasts=podcasts, 
                           q=q, 
                           current_status=status)

@app.route('/admin/podcast/report-pdf/<int:id>')
@login_required
def report_pdf(id):
    if current_user.role != 'admin': return redirect(url_for('user_home'))
    p = db.get_or_404(Podcast, id)
    filename = generate_timeline_pdf(p)
    return send_from_directory(os.path.join(app.root_path, 'static', 'pdf'), filename)

@app.route('/admin/podcast/export/<string:type>')
@login_required
def export_podcast(type):
    if current_user.role != 'admin': return redirect(url_for('user_home'))
    
    ids_str = request.args.get('ids', '')
    if not ids_str:
        flash('Tidak ada data yang dipilih.', 'warning')
        return redirect(url_for('admin_dashboard'))
        
    ids = [int(i) for i in ids_str.split(',')]
    podcasts = Podcast.query.filter(Podcast.id.in_(ids)).all()
    
    from utils import generate_multiselect_pdf, generate_multiselect_excel
    
    if type == 'pdf':
        filename = generate_multiselect_pdf(podcasts)
    else:
        flash('Tipe ekspor tidak valid.', 'danger')
        return redirect(url_for('admin_dashboard'))
        
    return send_from_directory(os.path.join(app.root_path, 'static', 'pdf'), filename, as_attachment=True)

# Kelola User
@app.route('/admin/users')
@login_required
def admin_users():
    if current_user.role != 'admin': return redirect(url_for('user_home'))
    list_user = User.query.all()
    return render_template('admin/users/index.html', list_user=list_user)

# --- Rute User (Masyarakat) --- #

@app.route('/')
def user_home():
    q = request.args.get('q', '')
    cat = request.args.get('cat', '')
    
    podcasts_query = Podcast.query.filter_by(status='publish')
    
    if q:
        podcasts_query = podcasts_query.filter(Podcast.judul.contains(q))
    if cat:
        podcasts_query = podcasts_query.filter_by(kategori=cat)
        
    podcasts = podcasts_query.order_by(Podcast.tanggal.desc()).all()
    
    # Ambil list kategori unik hanya dari podcast yang sudah publish
    categories = db.session.query(Podcast.kategori).filter(Podcast.status == 'publish').distinct().all()
    categories = [c[0] for c in categories if c[0]]
    
    return render_template('user/index.html', podcasts=podcasts, categories=categories, q=q, current_cat=cat)

@app.route('/podcast/<int:id>')
def podcast_detail(id):
    p = db.get_or_404(Podcast, id)
    # Pastikan podcast dipublish atau user adalah admin
    if p.status != 'publish':
        if not (current_user.is_authenticated and current_user.role == 'admin'):
            flash('Podcast belum dipublikasikan.', 'warning')
            return redirect(url_for('user_home'))
            
    return render_template('user/detail.html', p=p)

@app.route('/download/<filename>')
@login_required
def download_pdf(filename):
    """Fungsi untuk melayani download file PDF"""
    return send_from_directory(os.path.join(app.root_path, 'static', 'pdf'), filename)

if __name__ == '__main__':
    app.run(debug=True)
