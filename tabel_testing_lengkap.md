# Tabel Black Box Testing (Positive & Negative)

Berikut adalah tabel pengujian Black Box yang dibagi menjadi skenario **Positive** (menguji fungsi normal) dan **Negative** (menguji penanganan kesalahan).

| No | Pengujian | Fitur / Skenario Pengujian | Input Data | Hasil yang Diharapkan | Hasil Pengujian | Keterangan |
|:--:| --- | --- | --- | --- | :---: | --- |
| **1** | **Positive** | Login Admin dengan akun valid | Email: `admin@desa.id`<br>Pass: `admin123` | Sistem berhasil login dan masuk ke Dashboard. | **Sesuai** | Akses Diterima |
| **2** | **Negative** | Login Admin dengan password salah | Email: `admin@desa.id`<br>Pass: `salah123` | Sistem menolak akses dan menampilkan pesan error. | **Sesuai** | Keamanan OK |
| **3** | **Negative** | Login Admin dengan field kosong | Email: (kosong)<br>Pass: (kosong) | Sistem memberikan peringatan bahwa field harus diisi. | **Sesuai** | Validasi OK |
| **4** | **Positive** | Tambah Podcast (Data Lengkap) | Judul, Kategori, Script diisi lengkap | Data tersimpan dan file PDF otomatis ter-generate. | **Sesuai** | Fitur Berjalan |
| **5** | **Negative** | Tambah Podcast (Tanpa Judul) | Judul: (kosong)<br>Lainnya: diisi | Sistem menolak simpan (karena field judul mandatory/NOT NULL). | **Sesuai** | Validasi OK |
| **6** | **Positive** | Pencarian Podcast (Data Ada) | Kata kunci: "Vaksin" | Menampilkan hasil podcast yang berkaitan dengan vaksin. | **Sesuai** | Fitur Berjalan |
| **7** | **Negative** | Pencarian Podcast (Data Tidak Ada) | Kata kunci: "zxzx123" | Menampilkan pesan "Podcast tidak ditemukan". | **Sesuai** | Penanganan OK |
| **8** | **Negative** | Akses Dashboard Tanpa Login | Memasukkan URL `/admin` langsung | Sistem otomatis me-redirect (mengalihkan) ke halaman Login. | **Sesuai** | Proteksi OK |
| **9** | **Positive** | Generate & Download PDF | Klik tombol Download PDF | File berhasil diunduh dalam format `.pdf` yang valid. | **Sesuai** | Output Valid |
| **10** | **Positive** | Update Status Produksi | Mengubah dari 'Draft' ke 'Publish' | Status di database berubah dan muncul di halaman depan warga. | **Sesuai** | Workflow OK |
