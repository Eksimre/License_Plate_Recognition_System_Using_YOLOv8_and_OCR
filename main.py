# Okunan plakanın ve diğer verilerin veri tabanına işlenmesi.
# Kullanılan kütüphaneler.
import sqlite3                      # SQLite veri tabanı işlemleri.
from datetime import datetime       # Tarih-saat işlemleri.
from plate_read import plaka_okut   # Okunan plakanın çekilmesi.

# Araç giriş fonksiyonu.
def arac_giris_yap(giris_plaka):
    now = datetime.now()                      # Şu anki tarih ve saat.
    zaman = now.strftime("%d-%m-%Y %H:%M:%S") # Formatlı hale getir.

    conn = sqlite3.connect('database.db') # Veri tabanına bağlan.
    cursor = conn.cursor()                # Cursor (imleç) oluştur.

    # Giriş kaydını Arac_girisi_cikis tablosuna ekle.
    cursor.execute("INSERT INTO Arac_girisi_cikis (arac_plaka, giris_zamani) VALUES (?,?)", (giris_plaka, zaman))
    
    conn.commit()    # Verileri kalıcı hale getir.
    conn.close()     # Veri tabanı ile bağlantıyı kes.
    
# Araç çıkış fonksiyonu.
def arac_cikis_yap(cikis_plaka):
    now = datetime.now()                      # Çıkış zamanı.
    zaman = now.strftime("%d-%m-%Y %H:%M:%S") # Formatlı hale getir.

    conn = sqlite3.connect('database.db') # Veri tabanına bağlan.
    cursor = conn.cursor()                # Cursor (imleç) oluştur.  

    # Giriş kaydı var mı kontrol et. 
    cursor.execute("SELECT arac_plaka, giris_zamani FROM Arac_girisi_cikis")
    records = cursor.fetchall()
    # Kayıtlar arasında gez.
    for row in records:
        if row[0] == cikis_plaka:
            # Girş ve çıkış zamnını al ve farkı bul.
            giris_dt = datetime.strptime(row[1], "%d-%m-%Y %H:%M:%S")
            cikis_dt = datetime.strptime(zaman, "%d-%m-%Y %H:%M:%S")
            gecen_sure = cikis_dt - giris_dt
            gecen_sure_dt = gecen_sure.total_seconds()

            # Giriş tablosunu çıkış zamanı ile güncelle.
            cursor.execute("UPDATE Arac_girisi_cikis SET cikis_zamani = ?, gecirilen_sure = ? WHERE arac_plaka = ?", (zaman, gecen_sure_dt, row[0]))

            # Arşive verinin son halini ekleyelim.
            cursor.execute("INSERT INTO Arsiv (arac_plaka, giris_zamani, cikis_zamani, gecirilen_sure) VALUES (?,?,?,?)", (row[0], row[1], zaman, gecen_sure_dt))
 
            # Araç çıkış yapıp arşive eklendik sonra ana tablodaki veriyi anlık, günlük veya haftalık olarak silebiliriz.
            # Proje test aşamsında olduğu için anlık siliyorum.
            cursor.execute("DELETE FROM Arac_girisi_cikis WHERE arac_plaka = ?", (row[0],))
      
            break # döngüden çık.
        else:
            print("plaka yok") # Plaka eşleşmezse bilgi ver.

    conn.commit()    # Verileri kalıcı hale getir.
    conn.close()     # Veri tabanı ile bağlantıyı kes.

def kayit_getir():
    pass

# Çalıştır
if __name__ == "__main__":
    """
    Program buradan başlar.
    - Önce kamera açılır ve OCR yapılır.
    - Sonra okunan plakalar veri tabanına kaydedilir.
    """
    # Kamerayı aç ve plakaları oku
    giris_plaka, cikis_plaka = plaka_okut()

    # Eğer giriş plakası varsa, veri tabanına giriş kaydını yaz.
    if giris_plaka:
        arac_giris_yap(giris_plaka)

    # Eğer çıkış plakası varsa, çıkışı kaydet.
    if cikis_plaka:
        arac_cikis_yap(cikis_plaka)



