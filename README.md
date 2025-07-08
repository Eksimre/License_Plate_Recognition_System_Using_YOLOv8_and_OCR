# 🚗 YOLOv8 ve OCR Kullanarak Araç Plaka Tanıma ve Kayıt Sistemi

Bu proje, Python, YOLOv8 ve Tesseract OCR kullanarak gerçek zamanlı araç plakası tespiti ve tanıma işlemi gerçekleştirir. Kameradan canlı görüntü alır, plakayı tespit eder, OCR ile yazıya çevirir ve giriş-çıkış bilgilerini SQLite veri tabanına kaydeder.

---

## 🎯 Özellikler

✅ **Gerçek Zamanlı Plaka Tespiti**  
- USB kamera veya laptop kamerasından görüntü alır.  
- YOLOv8 modeli ile plakayı algılar.

✅ **OCR ile Plaka Okuma**  
- Tesseract OCR kullanarak plakadaki yazıyı tanır.  
- Gereksiz karakterleri otomatik temizler.

✅ **Giriş - Çıkış Takibi**  
- `g` tuşu ile giriş kaydı oluşturur.  
- `ç` tuşu ile çıkış kaydı oluşturur.  
- Giriş ve çıkış arasındaki süreyi hesaplar.

✅ **SQLite Veri Tabanı**  
- Anlık giriş kayıtları `Arac_girisi_cikis` tablosunda tutulur.  
- Çıkış yapıldığında kayıt `Arsiv` tablosuna taşınır.
---

- Plaka tespiti, interneten bulduğum önceden eğitimiş bir model ile yapılıyor (license_plate_detector.pt).
- Gerekli kütüphaneler kurulduktan sonra "create_database.py" çalıştırılarak veri tabanı oluşturulur.
- Pc'ye bağlı bir webcam var ise "main.py" dosyası çalıştırılır ve araç plaksı tespit edilmeye başlar.

---
- Örnek giris data
![Multiple_choice_picture](https://r.resimlink.com/7mw16zn.png)

---
- Örnek çıkış data
![Multiple_choice_picture](https://r.resimlink.com/sRYtPga3zGv.png)
