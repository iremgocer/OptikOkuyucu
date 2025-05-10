import cv2
import pytesseract
import numpy as np
from tkinter import filedialog, Tk, Label, Button
from PIL import Image, ImageTk

# Tesseract yolu (Windows'ta değiştir)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Cevap anahtarı (örnek olarak A, B, C, D, E = 0,1,2,3,4)
cevap_anahtari = [0, 1, 2, 3, 4] * 10  # 50 soru

def formu_oku(path):
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)[1]

    cevaplar = []
    start_y = 820  # Cevap kutularının yaklaşık Y başlangıcı
    start_x = 350  # Sol başlangıç
    bubble_w, bubble_h = 20, 20  # Baloncuk boyutları
    gap_x = 30  # Seçenekler arası mesafe

    for i in range(50):  # 50 soru
        row_y = start_y + (i * 10)  # Her soru biraz aşağı kayar
        max_black = 0
        marked = -1
        for j in range(5):  # A B C D E
            x = start_x + j * gap_x
            bubble = thresh[row_y:row_y + bubble_h, x:x + bubble_w]
            black = cv2.countNonZero(bubble)
            if black > max_black and black > 30:
                max_black = black
                marked = j
        cevaplar.append(marked)

    return cevaplar

def ocr_bilgileri(path):
    image = cv2.imread(path)
    roi = image[100:400, 100:800]  # Kimlik bilgileri alanı
    text = pytesseract.image_to_string(roi, lang="tur")
    return text

def dosya_sec():
    path = filedialog.askopenfilename(filetypes=[("JPG files", "*.jpg")])
    if not path:
        return

    cevaplar = formu_oku(path)
    dogru = sum(1 for i in range(len(cevap_anahtari)) if cevaplar[i] == cevap_anahtari[i])
    bilgi = ocr_bilgileri(path)

    sonuc = f"Doğru Sayısı: {dogru}/50\n\nKimlik Bilgileri:\n{bilgi}"
    sonuc_label.config(text=sonuc)

    img = Image.open(path).resize((300, 500))
    img_tk = ImageTk.PhotoImage(img)
    image_label.config(image=img_tk)
    image_label.image = img_tk

# GUI başlat
pencere = Tk()
pencere.title("Basit Optik Okuyucu")
pencere.geometry("600x600")

Button(pencere, text="Form Seç", command=dosya_sec, font=("Arial", 14)).pack(pady=10)
image_label = Label(pencere)
image_label.pack()
sonuc_label = Label(pencere, text="", font=("Arial", 12), justify="left")
sonuc_label.pack(pady=10)

pencere.mainloop()
