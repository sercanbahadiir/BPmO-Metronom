import tkinter as tk
from tkinter import messagebox
import serial
import threading
import time

# Arduino seri port ayarı (kendine göre değiştir, örneğin 'COM8')
PORT = 'COM8'

try:
    arduino = serial.Serial(PORT, 9600, timeout=1)
    time.sleep(2)
except serial.SerialException:
    messagebox.showerror("Bağlantı Hatası", f"Arduino'ya bağlanılamadı! Port: {PORT}")
    exit()

running = False

def veri_okuma_thread():
    while running:
        try:
            satir = arduino.readline().decode().strip()
            if satir.startswith("BPM:"):
                bpm_degeri = satir.split(":")[1]
                label_mevcut_bpm.config(text=f"Mevcut BPM: {bpm_degeri}")
        except:
            pass
        time.sleep(0.1)

def baslat():
    global running
    if running:
        messagebox.showinfo("Uyarı", "Metronom zaten çalışıyor.")
        return

    bpm = entry_bpm.get()
    inc = entry_inc.get()
    per = entry_per.get()
    direction = direction_var.get()

    if not (bpm.isdigit() and inc.isdigit() and per.isdigit()):
        messagebox.showerror("Hatalı Giriş", "Lütfen tüm alanlara geçerli sayılar girin.")
        return

    veri = f"{bpm},{inc},{per},{direction}\n"
    arduino.write(veri.encode())
    time.sleep(0.1)
    arduino.write(b"START\n")

    running = True
    threading.Thread(target=veri_okuma_thread, daemon=True).start()

def durdur():
    global running
    if not running:
        messagebox.showinfo("Uyarı", "Metronom zaten durdu.")
        return
    arduino.write(b"STOP\n")
    running = False
    label_mevcut_bpm.config(text="Mevcut BPM: -")

def bitir():
    global running
    if running:
        arduino.write(b"STOP\n")
        running = False
    arduino.write(b"EXIT\n")
    arduino.close()
    pencere.destroy()

# ---------- Tkinter GUI ----------

pencere = tk.Tk()
pencere.title("Arduino Metronom Kontrol")
pencere.geometry("320x450")

# Başlangıç BPM
tk.Label(pencere, text="Başlangıç BPM").pack(pady=(10, 0))
entry_bpm = tk.Entry(pencere)
entry_bpm.insert(0, "60")
entry_bpm.pack()

# Artış Miktarı
tk.Label(pencere, text="Artış Miktarı (BPM)").pack(pady=(10, 0))
entry_inc = tk.Entry(pencere)
entry_inc.insert(0, "4")
entry_inc.pack()

# Artış Periyodu
tk.Label(pencere, text="Artış Periyodu (vuruş)").pack(pady=(10, 0))
entry_per = tk.Entry(pencere)
entry_per.insert(0, "16")
entry_per.pack()

# Hızlanma/Yavaşlama Seçimi
tk.Label(pencere, text="Hız Değişim Yönü").pack(pady=(10, 0))
direction_var = tk.StringVar(value="up")  # default 'up'

frame_dir = tk.Frame(pencere)
frame_dir.pack()

tk.Radiobutton(frame_dir, text="Hızlanma (Artır)", variable=direction_var, value="up").pack(side=tk.LEFT, padx=10)
tk.Radiobutton(frame_dir, text="Yavaşlama (Azalt)", variable=direction_var, value="down").pack(side=tk.LEFT, padx=10)

# Mevcut BPM
label_mevcut_bpm = tk.Label(pencere, text="Mevcut BPM: -", font=("Arial", 14))
label_mevcut_bpm.pack(pady=15)

# Butonlar
btn_frame = tk.Frame(pencere)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Başlat", width=10, command=baslat).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Durdur", width=10, command=durdur).grid(row=0, column=1, padx=5)
tk.Button(pencere, text="Bitir", width=30, command=bitir).pack(pady=20)

pencere.protocol("WM_DELETE_WINDOW", bitir)
pencere.mainloop()
