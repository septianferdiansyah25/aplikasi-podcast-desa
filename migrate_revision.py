import sqlite3

def migrate():
    conn = sqlite3.connect('instance/podcast_desa.db')
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE podcasts ADD COLUMN jumlah_revisi INTEGER DEFAULT 0")
        conn.commit()
        print("Migrasi Berhasil: Kolom jumlah_revisi ditambahkan.")
    except sqlite3.OperationalError as e:
        print(f"Migrasi Mungkin Sudah Dilakukan: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
