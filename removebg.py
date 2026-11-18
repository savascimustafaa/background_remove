from tkinter import *              # * yaptığımız zaman tkinter içindeki her şeyi dahil ediyoruz
from tkinter import filedialog, messagebox
from rembg import remove 
from PIL import Image, ImageTk
import io
import ctypes

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    ctypes.windll.user32.SetProcessDPIAware()

#-----FONKSİYONLAR-----
def arka_planı_kaldir():
    try:
        #kullanıcıdan dosya seçmesini isteyelim
        girdi_dosya = filedialog.askopenfilename(
            title="Bir görüntü seçiniz",
            filetypes=[("Image files","*.jpg *.jpeg *.png")] #kabul edilen dosya tiplerini belirtir.
        )
        if not girdi_dosya:
            return
        cikti_dosya = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
            title="Çıktı Dosyasını Kaydet"
        )
        if not cikti_dosya:
            return
        
        #görüntü oku ve arka planı kaldır
        with open (girdi_dosya, "rb") as dosya:
            girdi = dosya.read() #dosyaları byte cinsinden okuyoruz
        sonuc = remove(girdi) #arkaplanı burada kaldırıyoruz #remove rembg modülünün bir elemanı
        
        #sonucu kaydet
        with open(cikti_dosya, "wb") as dosya:
            dosya.write(sonuc) #işlenmiş görüntüyü yeni dosyaya yazar
        
        # çıktı görüntüsünü bir önizleme ekle
        sonuc_goruntu = Image.open(io.BytesIO(sonuc)) #çıktıyı belekte açar
        sonuc_goruntu.thumbnail((400, 400))
        sonuc_img = ImageTk.PhotoImage(sonuc_goruntu)
        label_cikti.config(image = sonuc_img)
        label_cikti.image = sonuc_img
        messagebox.showinfo("Başarılı","Arkaplan başarıyla kaldırıldı ve kayıt edildi")
    except Exception as e:
        messagebox.showerror("HATA!",f"Bir Hata Oluştu: {e}")

#-----Renk Seçimleri-----
arka_plan = "#0b132b"
yazilar = "#e0e1dd"
buton_renk = "#1c2541"
buton_hover = "#3a506b"

#arayüz kodlama
rembgapp = Tk()
rembgapp.title("Arka Plan Kaldırma Uygulaması")
rembgapp.geometry("750x650")
rembgapp.configure(bg=arka_plan)
rembgapp.resizable(1, 1)
rembgapp.iconbitmap("rembg.ico")


# Fontlar
baslik_font = ("Segoe UI", 18, "bold")
normal_font = ("Segoe UI", 11)

# ANA FRAME (kart hissi verir)
frame_ana = Frame(rembgapp, bg=arka_plan)
frame_ana.pack(expand=True)

# başlık
label_baslik = Label(
    frame_ana,
    text="Fotoğraflardaki Arka Planı Kaldır",
    font=baslik_font,
    fg=yazilar,
    bg=arka_plan
)
label_baslik.pack(pady=(20, 10))

# açıklama (premium hissi artırır)
label_aciklama = Label(
    frame_ana,
    text="Bir görsel seçin, arka plan otomatik olarak kaldırılır.",
    font=normal_font,
    fg="#a0aec0",
    bg=arka_plan
)
label_aciklama.pack(pady=(0, 20))

# BUTON
buton_islem = Button(
    frame_ana,
    text="Görsel Seç",
    command=arka_planı_kaldir,
    font=("Segoe UI", 11, "bold"),
    bg=buton_renk,
    fg=yazilar,
    activebackground=buton_hover,
    activeforeground="white",
    relief="flat",
    padx=20,
    pady=10,
    cursor="hand2"
)
buton_islem.pack(pady=10)

# HOVER efekti
def on_enter(e):
    buton_islem["bg"] = buton_hover

def on_leave(e):
    buton_islem["bg"] = buton_renk

buton_islem.bind("<Enter>", on_enter)
buton_islem.bind("<Leave>", on_leave)

# çıktı alanı (kart gibi)
frame_cikti = Frame(frame_ana, bg="#1c2541")
frame_cikti.pack(pady=20, padx=20, fill="both", expand=True)

label_cikti = Label(frame_cikti, bg="#1c2541")
label_cikti.pack(expand=True)

rembgapp.mainloop()