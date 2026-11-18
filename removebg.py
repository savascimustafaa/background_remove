import io
import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

from PIL import Image, ImageTk
from rembg import remove

# ----- Windows DPI ayarı (diğer sistemlerde sessizce atlanır) -----
try:
    import ctypes
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        ctypes.windll.user32.SetProcessDPIAware()
except Exception:
    pass

# ----- Renkler -----
ARKA_PLAN = "#0b132b"
YAZILAR = "#e0e1dd"
BUTON_RENK = "#1c2541"
BUTON_HOVER = "#3a506b"
KART_RENK = "#1c2541"


# ----- FONKSİYONLAR -----
def arka_plani_kaldir():
    girdi_dosya = filedialog.askopenfilename(
        title="Bir görüntü seçiniz",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.webp *.bmp *.tiff *.gif")],
    )
    if not girdi_dosya:
        return

    cikti_dosya = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png")],
        title="Çıktı Dosyasını Kaydet",
    )
    if not cikti_dosya:
        return

    buton_islem.config(state="disabled", text="İşleniyor...")
    # Ağır işlem ayrı thread'de çalışır, arayüz donmaz
    threading.Thread(
        target=isle, args=(girdi_dosya, cikti_dosya), daemon=True
    ).start()


def isle(girdi_dosya, cikti_dosya):
    try:
        with open(girdi_dosya, "rb") as f:
            girdi = f.read()
        sonuc = remove(girdi)
        with open(cikti_dosya, "wb") as f:
            f.write(sonuc)
        rembgapp.after(0, lambda: bitti(sonuc))
    except Exception as e:
        rembgapp.after(0, lambda err=e: hata(err))


def bitti(sonuc):
    goruntu = Image.open(io.BytesIO(sonuc))
    goruntu.thumbnail((400, 400))
    img = ImageTk.PhotoImage(goruntu)
    label_cikti.config(image=img)
    label_cikti.image = img  # referansı tut, yoksa görüntü silinir
    buton_islem.config(state="normal", text="Görsel Seç", bg=BUTON_RENK)
    messagebox.showinfo("Başarılı", "Arka plan başarıyla kaldırıldı ve kaydedildi")


def hata(e):
    buton_islem.config(state="normal", text="Görsel Seç", bg=BUTON_RENK)
    messagebox.showerror("HATA!", f"Bir Hata Oluştu: {e}")


def on_enter(e):
    if str(buton_islem["state"]) != "disabled":
        buton_islem["bg"] = BUTON_HOVER


def on_leave(e):
    if str(buton_islem["state"]) != "disabled":
        buton_islem["bg"] = BUTON_RENK


# ----- ARAYÜZ -----
rembgapp = tk.Tk()
rembgapp.title("Arka Plan Kaldırma Uygulaması")
rembgapp.geometry("750x650")
rembgapp.configure(bg=ARKA_PLAN)
rembgapp.resizable(True, True)

# İkon dosyası yoksa veya Windows değilse program çökmesin
try:
    ikon_yolu = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rembg.ico")
    rembgapp.iconbitmap(ikon_yolu)
except Exception:
    pass

# Fontlar
baslik_font = ("Segoe UI", 18, "bold")
normal_font = ("Segoe UI", 11)

# Ana frame
frame_ana = tk.Frame(rembgapp, bg=ARKA_PLAN)
frame_ana.pack(expand=True)

# Başlık
label_baslik = tk.Label(
    frame_ana,
    text="Fotoğraflardaki Arka Planı Kaldır",
    font=baslik_font,
    fg=YAZILAR,
    bg=ARKA_PLAN,
)
label_baslik.pack(pady=(20, 10))

# Açıklama
label_aciklama = tk.Label(
    frame_ana,
    text="Bir görsel seçin, arka plan otomatik olarak kaldırılır.",
    font=normal_font,
    fg="#a0aec0",
    bg=ARKA_PLAN,
)
label_aciklama.pack(pady=(0, 20))

# Buton
buton_islem = tk.Button(
    frame_ana,
    text="Görsel Seç",
    command=arka_plani_kaldir,
    font=("Segoe UI", 11, "bold"),
    bg=BUTON_RENK,
    fg=YAZILAR,
    activebackground=BUTON_HOVER,
    activeforeground="white",
    disabledforeground="#7f8c9a",
    relief="flat",
    padx=20,
    pady=10,
    cursor="hand2",
)
buton_islem.pack(pady=10)
buton_islem.bind("<Enter>", on_enter)
buton_islem.bind("<Leave>", on_leave)

# Çıktı alanı
frame_cikti = tk.Frame(frame_ana, bg=KART_RENK)
frame_cikti.pack(pady=20, padx=20, fill="both", expand=True)

label_cikti = tk.Label(frame_cikti, bg=KART_RENK)
label_cikti.pack(expand=True)

rembgapp.mainloop()