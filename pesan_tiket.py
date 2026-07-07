import customtkinter as ctk
from tkinter import messagebox

# ==============================================================================
# FRAME HALAMAN: BOOKING TIKET ONLINE
# Desain ini DISAMAKAN dengan class PagePesanTiket di mainbaruuaspbo.py
# (Split banner biru + form scrollable sederhana, tanpa footer 3-kolom)
# ==============================================================================
class PagePesanTiket(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, fg_color=("#ffffff", "#0f172a"))
        self.controller = controller

        self.DATABASE_WISATA = {
            "Karimunjawa (Rp 250.000)": {"harga": 250000, "kuota": 8},
            "Agrowisata Tasikmadu (Rp 20.000)": {"harga": 20000, "kuota": 200},
            "Solo Safari (Rp 45.000)": {"harga": 45000, "kuota": 120},
            "Saloka Theme Park (Rp 120.000)": {"harga": 120000, "kuota": 45},
            "Candi Borobudur (Rp 50.000)": {"harga": 50000, "kuota": 15}
        }

        self.grid_columnconfigure(0, weight=1, uniform="split")
        self.grid_columnconfigure(1, weight=1, uniform="split")
        self.grid_rowconfigure(0, weight=1)

        # Kiri: Banner Info Visual
        bf = ctk.CTkFrame(self, fg_color=("#3b82f6", "#1e3a8a"), corner_radius=0)
        bf.grid(row=0, column=0, sticky="nsew")
        ctk.CTkLabel(bf, text="🌴 Jelajahi Keindahan Indonesia", font=ctk.CTkFont(size=11, weight="bold"), fg_color="white", text_color="#2563eb", corner_radius=20, padx=12, height=24).pack(anchor="w", padx=40, pady=(60, 0))
        ctk.CTkLabel(bf, text="Wujudkan Liburan\nImpianmu", font=ctk.CTkFont(size=36, weight="bold"), text_color="white", justify="left").pack(anchor="w", padx=40, pady=(15, 0))

        # Kanan: Formulir Pemesanan Interaktif
        fc = ctk.CTkScrollableFrame(self, fg_color="transparent")
        fc.grid(row=0, column=1, sticky="nsew", padx=40, pady=30)

        ctk.CTkLabel(fc, text="Booking Tiket Online", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(10, 20))

        self.buat_lbl(fc, "Pilih Destinasi Wisata")
        self.opt_destinasi = ctk.CTkOptionMenu(fc, values=list(self.DATABASE_WISATA.keys()), height=46, corner_radius=10, command=self.update_total_bayar)
        self.opt_destinasi.pack(fill="x", pady=(0, 15))

        self.buat_lbl(fc, "Jumlah Tiket")
        cf = ctk.CTkFrame(fc, fg_color="transparent")
        cf.pack(fill="x", pady=(0, 4))
        ctk.CTkButton(cf, text="−", width=46, height=44, corner_radius=10, font=ctk.CTkFont(size=18, weight="bold"), command=self.kurangi_tiket).pack(side="left")
        self.jumlah_tiket = 1
        self.lbl_jumlah = ctk.CTkLabel(cf, text="1", font=ctk.CTkFont(size=18, weight="bold"), width=120)
        self.lbl_jumlah.pack(side="left", padx=10, fill="x", expand=True)
        ctk.CTkButton(cf, text="+", width=46, height=44, corner_radius=10, font=ctk.CTkFont(size=18, weight="bold"), command=self.tambah_tiket).pack(side="right")

        self.lbl_sisa_kuota = ctk.CTkLabel(fc, text="🕒 Tersedia: -- tiket", font=ctk.CTkFont(size=11), text_color="#64748b")
        self.lbl_sisa_kuota.pack(anchor="w", pady=(0, 15))

        self.buat_lbl(fc, "Metode Pembayaran")
        self.opt_pay = ctk.CTkOptionMenu(fc, values=["QRIS (Otomatis Lunas)", "Transfer Bank", "E-Wallet"], height=46, corner_radius=10)
        self.opt_pay.pack(fill="x", pady=(0, 20))

        tc = ctk.CTkFrame(fc, fg_color=("#edf2ff", "#131b2e"), height=60, corner_radius=12)
        tc.pack(fill="x", pady=(0, 25))
        ctk.CTkLabel(tc, text="Total Bayar", font=ctk.CTkFont(size=14), text_color="#4f46e5").place(relx=0.06, rely=0.5, anchor="w")
        self.lbl_total_harga = ctk.CTkLabel(tc, text="Rp 0", font=ctk.CTkFont(size=20, weight="bold"), text_color="#4f46e5")
        self.lbl_total_harga.place(relx=0.94, rely=0.5, anchor="e")

        ctk.CTkButton(fc, text="✨  Konfirmasi & Pesan Tiket", height=48, corner_radius=12, font=ctk.CTkFont(size=15, weight="bold"), fg_color="#5a51e6", command=self.proses_simpan_booking).pack(fill="x")
        self.update_total_bayar()

    def buat_lbl(self, parent, text):
        ctk.CTkLabel(parent, text=text, font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(10, 4))

    def kurangi_tiket(self):
        if self.jumlah_tiket > 1:
            self.jumlah_tiket -= 1
            self.lbl_jumlah.configure(text=str(self.jumlah_tiket))
            self.update_total_bayar()

    def tambah_tiket(self):
        p = self.opt_destinasi.get()
        if self.jumlah_tiket < self.DATABASE_WISATA[p]["kuota"]:
            self.jumlah_tiket += 1
            self.lbl_jumlah.configure(text=str(self.jumlah_tiket))
            self.update_total_bayar()
        else:
            messagebox.showwarning("Penuh", "Batas sisa kuota tempat live tidak mencukupi!")

    def update_total_bayar(self, event=None):
        p = self.opt_destinasi.get()
        info = self.DATABASE_WISATA[p]
        tot = info["harga"] * self.jumlah_tiket
        self.lbl_total_harga.configure(text=f"Rp {tot:,.0f}".replace(",", "."))
        self.lbl_sisa_kuota.configure(text=f"🕒 Tersedia: {info['kuota']} tiket live saat ini")

    def proses_simpan_booking(self):
        username = getattr(self.controller, "username_aktif", None) or "Pengguna"
        messagebox.showinfo("Booking Berhasil 🎉", f"Terima kasih, {username}!\nPemesanan tiket {self.opt_destinasi.get()} sebanyak {self.jumlah_tiket} slot sukses dilakukan!")