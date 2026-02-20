from fpdf import FPDF
import os
import unicodedata

def clean_text_for_pdf(text):
    """
    Fungsi Paling Ampuh untuk membersihkan teks agar bersahabat dengan PDF.
    """
    if not text:
        return ""
    if not isinstance(text, str):
        text = str(text)
    
    # 1. Normalisasi karakter (mengubah ’ menjadi ' biasa, dll)
    # NFKD memecah karakter spesial, lalu kita encode ke ascii untuk membuang yang aneh
    normalized = unicodedata.normalize('NFKD', text)
    ascii_bytes = normalized.encode('ascii', 'ignore')
    text = ascii_bytes.decode('ascii')
    
    # 2. Tambahan manual untuk sisa-sisa karakter Latin-1 yang didukung PDF tapi lolos dari ascii
    # Tapi untuk cari aman, kita pakai latin-1 ignore saja
    return text.encode('latin-1', 'ignore').decode('latin-1')

def generate_podcast_pdf(podcast, narasumber_nama):
    # TANDANYA KALO KODINGAN BARU JALAN (Cek di Jendela Hitam)
    print("\n" + "*"*60)
    print("  >>> MENJALANKAN SISTEM PDF VERSI 4.0 (ANTI-UNICODE) <<<")
    print(f"  >>> JUDUL PODCAST: {podcast.judul[:30]}...")
    print("*"*60 + "\n")
    
    pdf = FPDF()
    # Matikan kompresi jika perlu, tapi default saja dulu
    pdf.add_page()
    
    # Bersihkan input
    c_judul = clean_text_for_pdf(podcast.judul)
    c_ns_nama = clean_text_for_pdf(narasumber_nama)
    c_ns_desc = clean_text_for_pdf(podcast.narasumber_deskripsi)
    c_script = clean_text_for_pdf(podcast.script_text)
    c_kat = clean_text_for_pdf(podcast.kategori)
    
    # Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"Script Podcast: {c_judul}", ln=True, align='C')
    pdf.ln(5)
    
    # Info
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Tanggal: {podcast.tanggal}", ln=True)
    pdf.cell(0, 10, f"Kategori: {c_kat}", ln=True)
    pdf.cell(0, 10, f"Narasumber: {c_ns_nama}", ln=True)
    if c_ns_desc:
        pdf.set_font("Arial", 'I', 10)
        pdf.cell(0, 10, f"({c_ns_desc})", ln=True)
    pdf.ln(10)
    
    # Script
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Isi Script:", ln=True)
    pdf.ln(2)
    pdf.set_font("Arial", size=11)
    
    # Multi_cell
    pdf.multi_cell(0, 7, c_script)
    
    # Simpan
    filename = f"podcast_{podcast.id}.pdf"
    filepath = os.path.join('static', 'pdf', filename)
    
    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))
        
    pdf.output(filepath)
    return filename

def generate_timeline_pdf(p):
    """
    Menghasilkan PDF Laporan Timeline Produksi untuk satu podcast tertentu.
    """
    pdf = FPDF()
    pdf.add_page()
    
    # Clean text
    judul = clean_text_for_pdf(p.judul)
    kategori = clean_text_for_pdf(p.kategori)
    narsum = clean_text_for_pdf(p.narasumber_nama)
    catatan = clean_text_for_pdf(p.catatan) if p.catatan else "-"
    
    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 15, "LAPORAN TIMELINE PRODUKSI PODCAST", ln=True, align='C')
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"Judul: {judul}", ln=True, align='C')
    pdf.ln(10)
    
    # Informasi Dasar
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(40, 8, "Kategori", border=0)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 8, f": {kategori}", ln=True)
    
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(40, 8, "Narasumber", border=0)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 8, f": {narsum}", ln=True)
    
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(40, 8, "Status Terakhir", border=0)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 8, f": {p.status.upper()}", ln=True)

    if p.jumlah_revisi > 0:
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(40, 8, "Status Revisi", border=0)
        pdf.set_font("Arial", '', 11)
        pdf.cell(0, 8, f": Direvisi {p.jumlah_revisi} kali", ln=True)
    pdf.ln(10)
    
    # Table Header Timeline
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(95, 10, " Tahapan Produksi", border=1, fill=True)
    pdf.cell(95, 10, " Tanggal Dicapai", border=1, fill=True, align='C')
    pdf.ln()
    
    # Table Body
    pdf.set_font("Arial", '', 11)
    stages = [
        ("1. Tahap Planning", p.tanggal_plan),
        ("2. Tahap Produksi", p.tanggal_produksi),
        ("3. Tahap Editing", p.tanggal_editing),
        ("4. Tahap Publish", p.tanggal_publish)
    ]
    
    for stage, date in stages:
        pdf.cell(95, 10, f" {stage}", border=1)
        date_str = date.strftime('%d %B %Y') if date else "-"
        pdf.cell(95, 10, f" {date_str}", border=1, align='C')
        pdf.ln()
    
    pdf.ln(10)
    
    # Catatan / Keterangan
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, "Catatan / Review:", ln=True)
    pdf.set_font("Arial", 'I', 11)
    pdf.multi_cell(0, 8, catatan)
    
    # Footer
    pdf.set_y(-30)
    pdf.set_font("Arial", 'I', 8)
    pdf.cell(0, 10, f"Dicetak otomatis oleh Sistem Podcast Desa pada: {os.popen('date /t').read().strip()}", align='C')

    # Save
    filename = f"report_{p.id}.pdf"
    filepath = os.path.join('static', 'pdf', filename)
    pdf.output(filepath)
    return filename
