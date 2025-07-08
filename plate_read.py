# Okuma için kullanacağımız kütüphaneler.
from ultralytics import YOLO # YOLOv8 modelini yüklemek ve plaka tespiti.
import cv2                   # Görüntü işleme ve webcam erişimi.
import pytesseract           # OCR yazı tanıma ve okuma.
import re                    # Okunan karakterlerin düzenlenmesi.

# Yolo modelini yükleme.
# Önceden hazırlanmış plaka tespit modeli.
model = YOLO("license_plate_detector.pt")

# Tesseract OCR motoru, görüntü işleme için.
# Bilgisayarda Tesseract kurulu olmalı ve yolu bilmemiz gerekiyor.
pytesseract.pytesseract.tesseract_cmd = r"C:/Tesseract-OCR/tesseract.exe"

# Fonksiyonu oluşturuyoruz.
def plaka_okut():
    # Webcam başlat.
    cap = cv2.VideoCapture(0)
    # Webcam başlatılmaz ise uyarı ver.
    if not cap.isOpened():
        print("Webcam açılamadı!")
        return None, None

    # Giriş ve çıkış plakalarının kayıt edileceği değişenler.
    text_giris = None
    text_cikis = None

    # Bir while döngüsü kuruyoruz. 
    while True:
        ret, frame = cap.read()          # Kameradan görüntü al.
        if not ret:                      # Okuma başarısız ise uyarı ver.
            print("Görüntü alınamadı!")
            break

        # Modeli görüntüye uygula
        result = model.predict(source=frame, # O anki kareyi input oalrak verir.
                               conf=0.3)     # %30 güven skoru olan tahminleri al.
          
        # Predict() çıktısı bir liste döndürür.
        # Tüm sonuçlardan ilkini al.
        result = result[0]

        # Tespit edilen kutuları al (xmin, ymin, xmax, ymax) kordinatlar, numpy array'e çevir.
        boxes = result.boxes.xyxy.cpu().numpy()

        # # Her tespit edilen kutu için çerçeve çiz.
        for box in boxes:
            xmin, ymin, xmax, ymax = box.astype(int)                        # Kutu koordinatlarını tam sayıya çevir.
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0,255,0), 2)  # Kutuyu yeşil çerçeveyle çiz.

        # Ekranda görüntüyü göster.
        cv2.imshow("Plaka Tespiti", frame)
        
        # Klavye girişi.
        key = cv2.waitKey(1) & 0xFF

        # "q" tuşuna basılırsa çıkış yap
        if key == ord("q"):
            break

        # "g" tuşuna basılırsa araç girişi için plakayı kırp ve oku.
        if key == ord("g"):
            if len(boxes) == 0: # Görüntü yoksa uyarı ver.
                print("Plaka tespit edilemedi.")
            else:
                xmin, ymin, xmax, ymax = boxes[0].astype(int)     # koordinatları tam sayıya çevirir (çünkü piksel değerleri tam sayı olmalı).
                cropped = frame[ymin:ymax, xmin:xmax]             # Plakayı görüntüden kırpar (crop) — sadece plakanın olduğu alan alınır.
                gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)  # Kırpılan plaka resmi griye çevrilir (siyah-beyaz hâle gelir).
                raw_giris = pytesseract.image_to_string(gray, lang="eng").replace(" ", "") # OCR kütüphanesiyle plaka metni okunur.
                text_giris = "".join(re.findall(r"[A-Z0-9]", raw_giris.upper()))           # Sadece büyük harfler (A-Z) ve rakamlar (0-9) alınır.
                print("Giriş plakası:", text_giris)

        # "ç" tuşuna basılırsa araç çıkışı için plakayı kırp ve oku.
        if key == ord("ç"):
            if len(boxes) == 0: # Görüntü yoksa uyarı ver.
                print("Plaka tespit edilemedi.")
            else:
                xmin, ymin, xmax, ymax = boxes[0].astype(int)     # koordinatları tam sayıya çevirir (çünkü piksel değerleri tam sayı olmalı).
                cropped = frame[ymin:ymax, xmin:xmax]             # Plakayı görüntüden kırpar (crop) — sadece plakanın olduğu alan alınır.
                gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)  # Kırpılan plaka resmi griye çevrilir (siyah-beyaz hâle gelir).
                raw_cikis = pytesseract.image_to_string(gray, lang="eng").replace(" ", "") # OCR kütüphanesiyle plaka metni okunur.
                text_cikis = "".join(re.findall(r"[A-Z0-9]", raw_cikis.upper()))           # Sadece büyük harfler (A-Z) ve rakamlar (0-9) alınır.
                print("Çıkış plakası:", text_cikis)

        # Giriş veya çıkış herhangi birisi okunduysa döngüyü bitir.
        if text_giris or text_cikis:
            break

    cap.release()           # Kamera bağlantısını kapat.
    cv2.destroyAllWindows() # Açılan pencereyi kapat.

    # Alınan plakayı döndür.
    return text_giris, text_cikis 