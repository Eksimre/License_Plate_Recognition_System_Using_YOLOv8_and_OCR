# veri tabanı oluşturuyoruz, giren ve çıkan araçların plakaları bu veri tabanına saklanacak.
# Zamanla kayıt sayısı çok fazla olacağı için 2 tablo oluşturuyorum. 1. tablo içindeki kayıt, araç çıktıktan sonar silinecek, 1. tablodaki yükü azaltmış olacağım.
# 2. tablo bütün kayıtları arşivleyecek.
import sqlite3 # SQLite veritabanı modülü
import os      # Dosya işlemleri için modül

# Veri tabanı oluşturma foksiyonu
def create_database():
    # Aynı klasörde daha önce oluşturulmuş bir veritabanı varsa onu sil.
    # Deneme projesi olduğu için her çalıştırmada temiz bir veritabanı ile başlanır.
    # Proje başladığında bu satırlar iptal edilir.
    if os.path.exists("database.db"):
        os.remove("database.db")

    # Veri tabanını oluştur ve bağlantı kur.
    conn = sqlite3.connect("database.db") # Veritabanı dosyasını oluşturur.
    cursor = conn.cursor() # SQL kodlarını çalıştırmak için bir imleç oluştur (cursor).
    return conn, cursor # Veri bağlantısı ve imleci fonksiyon dışında döndür.

# Plaka hareketleri tablolarını oluşturan fonksiyon.
def create_table(cursor):
    # Araç giriş tablosu.
    cursor.execute("""
        CREATE TABLE Arac_girisi_cikis(
            id INTEGER PRIMARY KEY,
            arac_plaka VARCHAR(255) NOT NULL,
            giris_zamani TEXT,
            cikis_zamani TEXT,
            gecirilen_sure TEXT
        )
    """)
    # Arşiv tablosu. 
    cursor.execute("""
        CREATE TABLE Arsiv(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            arac_plaka VARCHAR(255) NOT NULL,
            giris_zamani TEXT NOT NULL,
            cikis_zamani TEXT NOT NULL,
            gecirilen_sure TEXT NOT NULL   
        )
    """)
    
# Veri tabanı oluşturma ve tablo kurma işlemini başlatan ana fonksiyon.   
def run():
    # Veri tabanını oluştur.
    conn, cursor = create_database()
    try:
        create_table(cursor) # Tabloları oluşturur.
        conn.commit()        # Değişiklikleri kaydet.
    except sqlite3.OperationalError as e:
        print("Hata:", e)    # Hata mesajını ekrana yaz.
    finally:
        conn.close()         # Bağlantıyı kapat.

# Programı çalıştır.
run()

