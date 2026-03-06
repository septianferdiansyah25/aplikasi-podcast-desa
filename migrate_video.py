import sqlite3
import os

def migrate():
    # Use the same path as in app.py if possible, or relative to cwd
    db_path = 'instance/podcast_desa.db'
    if not os.path.exists(db_path):
        # Try finding it if relative path fails (common in different environments)
        db_path = 'c:/Users/septian ferdiansyah/.gemini/antigravity/scratch/aplikasi_podcast_desa/instance/podcast_desa.db'

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE podcasts ADD COLUMN link_video TEXT")
        conn.commit()
        print("Migrasi Berhasil: Kolom link_video ditambahkan.")
    except sqlite3.OperationalError as e:
        print(f"Migrasi Mungkin Sudah Dilakukan: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
