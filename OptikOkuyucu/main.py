import cv2
import pytesseract
import numpy as np
from tkinter import filedialog, Tk, Label, Button, StringVar, OptionMenu
from PIL import Image, ImageTk

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

cevap_anahtari = [0, 1, 2, 3, 4] * 10

sehirler = ["İstanbul", "Ankara", "İzmir", "Bursa", "Adana"]
kurumlar = ["Anadolu Lisesi", "Fen Lisesi", "Meslek Lisesi", "İmam Hatip", "Özel Kolej"]
kitapciklar = ["A", "B", "C", "D"]
salonlar = [str(i) for i in range(1, 21)]
belge_turleri = [
    "SRC 1", "SRC 2", "SRC 3", "SRC 4",
    "ODY 1", "ODY 2", "ODY 3", "ODY 4",
    "ÜDY 1", "ÜDY 2", "ÜDY 3", "ÜDY 4",
    "İş Makinesi"
]

def formu_oku(path):
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)[1]

    cevaplar = []
    start_y = 820
    start_x = 350
    bubble_w, bubble_h = 20, 20
    gap_x = 30

    for i in range(50):
        row_y = start_y + (i * 10)
        max_black = 0
        marked = -1
        for j in range(5):
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
    roi = image[100:400, 100:800]
    text = pytesseract.image_to_string(roi, lang="tur")
    return text

def dosya_sec():
    path = filedialog.askopenfilename(filetypes=[("JPG files", "*.jpg")])
    if not path:
        return

    cevaplar = formu_oku(path)
    dogru = sum(1 for i in range(len(cevap_anahtari)) if cevaplar[i] == cevap_anahtari[i])
    bilgi = ocr_bilgileri(path)

    sonuc = f"""
 Şehir: {sehir_var.get()}
 Kurum: {kurum_var.g()}
 Kitapçık Türü: {kitapcik_var.get()}
 Salon No: {salon_var.get()}
 Belge Türü: {belge_var.get()}

 Doğru Sayısı: {dogru}/50

 Kimlik Bilgileri:
{bilgi}
""".strip()

    sonuc_label.config(text=sonuc)

    img = Image.open(path).resize((300, 500))
    img_tk = ImageTk.PhotoImage(img)
    image_label.config(image=img_tk)
    image_label.image = img_tk

pencere = Tk()
pencere.title("Optik Okuyucu")
pencere.geometry("700x850")

# Seçim kutuları
def secim_ekle(label_text, var, secenekler):
    Label(pencere, text=label_text, font=("Arial", 12)).pack()
    OptionMenu(pencere, var, *secenekler).pack()

sehir_var = StringVar(pencere)
sehir_var.set(sehirler[0])
kurum_var = StringVar(pencere)
kurum_var.set(kurumlar[0])
kitapcik_var = StringVar(pencere)
kitapcik_var.set(kitapciklar[0])
salon_var = StringVar(pencere)
salon_var.set(salonlar[0])
belge_var = StringVar(pencere)
belge_var.set(belge_turleri[0])

secim_ekle("Şehir Seç:", sehir_var, sehirler)
secim_ekle("Kurum Seç:", kurum_var, kurumlar)
secim_ekle("Kitapçık Türü:", kitapcik_var, kitapciklar)
secim_ekle("Salon No:", salon_var, salonlar)
secim_ekle("Belge Türü:", belge_var, belge_turleri)

Button(pencere, text="Form Seç", command=dosya_sec, font=("Arial", 14)).pack(pady=10)

image_label = Label(pencere)
image_label.pack()
sonuc_label = Label(pencere, text="", font=("Arial", 11), justify="left")
sonuc_label.pack(pady=10)

pencere.mainloop()
