import customtkinter as ctk
from tkinter import messagebox

class PagePesanTiket(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, fg_color=("#ffffff", "#0f172a"))
        self.controller = controller

        # ==============================================================================
        # DATA WISATA UPDATE (Parangtritis & Merbabu diganti Karimunjawa & Tasikmadu)
        # ==============================================================================
        self.DATABASE_WISATA = {
            "Karimunjawa (Rp 250.000)": {"harga": 25000, "kuota": 8},
            "Agrowisata Tasikmadu (Rp 20.000)": {"harga": 20000, "kuota": 200},
            "Solo Safari (Rp 45.000)": {"harga": 45000, "kuota": 120},
            "Saloka Theme Park (Rp 120.000)": {"harga": 120000, "kuota": 45},
            "Candi Borobudur (Rp 50.000)": {"harga": 50000, "kuota": 15}
        }

        # Mengatur Grid Utama (Split Screen: Kiri Banner, Kanan Form)
        self.grid_columnconfigure(0, weight=1, uniform="split")
        self.grid_columnconfigure(1, weight=1, uniform="split")
        self.grid_rowconfigure(0, weight=1)

        # ==============================================================================
        # SISI KIRI: BANNER VISUAL
        # ==============================================================================
        self.banner_frame = ctk.CTkFrame(self, fg_color=("#3b82f6", "#1e3a8a"), corner_radius=0)
        self.banner_frame.grid(row=0, column=0, sticky="nsew")
        self.buat_konten_banner()

        # ==============================================================================
        # SISI KANAN: FORMULIR BOOKING TIKET ONLINE
        # ==============================================================================
        self.form_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.form_container.grid(row=0, column=1, sticky="nsew", padx=40, pady=30)
        
        # Icon atas form
        self.icon_top = ctk.CTkLabel(
            self.form_container, text="🎫", font=ctk.CTkFont(size=36),
            fg_color=("#edf2ff", "#1e293b"), width=64, height=64, corner_radius=32
        )
        self.icon_top.pack(pady=(10, 5))

        # Judul Utama Form
        self.lbl_form_title = ctk.CTkLabel(
            self.form_container, text="Booking Tiket Online", 
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"), text_color=("#0f172a", "#f8fafc")
        )
        self.lbl_form_title.pack(pady=2)

        self.lbl_form_sub = ctk.CTkLabel(
            self.form_container, text="Isi formulir di bawah untuk pemesanan tiket wisata", 
            font=ctk.CTkFont(family="Segoe UI", size=13), text_color=("#64748b", "#94a3b8")
        )
        self.lbl_form_sub.pack(pady=(0, 25))

        # ----------------------------------------------------------------------
        # INPUT 1: PILIH DESTINASI WISATA
        # ----------------------------------------------------------------------
        self.buat_section_label("Pilih Destinasi Wisata")
        
        self.opt_destinasi = ctk.CTkOptionMenu(
            self.form_container,
            values=list(self.DATABASE_WISATA.keys()),
            font=ctk.CTkFont(family="Segoe UI", size=14),
            height=46,
            fg_color=("#ffffff", "#1e293b"),
            text_color=("#0f172a", "#f8fafc"),
            button_color=("#e2e8f0", "#334155"),
            button_hover_color=("#cbd5e1", "#475569"),
            corner_radius=10,
            command=self.update_total_bayar
        )
        self.opt_destinasi.pack(fill="x", pady=(0, 15))

        # ----------------------------------------------------------------------
        # INPUT 2: JUMLAH TIKET
        # ----------------------------------------------------------------------
        self.buat_section_label("Jumlah Tiket")
        
        self.counter_frame = ctk.CTkFrame(self.form_container, fg_color="transparent")
        self.counter_frame.pack(fill="x", pady=(0, 4))

        self.btn_minus = ctk.CTkButton(
            self.counter_frame, text="−", width=46, height=44, corner_radius=10,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color=("#f1f5f9", "#1e293b"), text_color=("#0f172a", "#f8fafc"),
            hover_color=("#e2e8f0", "#334155"), command=self.kurangi_tiket
        )
        self.btn_minus.pack(side="left")

        self.jumlah_tiket = 1
        self.lbl_jumlah = ctk.CTkLabel(
            self.counter_frame, text=str(self.jumlah_tiket), 
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            text_color=("#0f172a", "#f8fafc"), width=120
        )
        self.lbl_jumlah.pack(side="left", padx=10, fill="x", expand=True)

        self.btn_plus = ctk.CTkButton(
            self.counter_frame, text="+", width=46, height=44, corner_radius=10,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color=("#f1f5f9", "#1e293b"), text_color=("#0f172a", "#f8fafc"),
            hover_color=("#e2e8f0", "#334155"), command=self.tambah_tiket
        )
        self.btn_plus.pack(side="right")

        # Info sisa kuota live
        self.lbl_sisa_kuota = ctk.CTkLabel(
            self.form_container, text="🕒 Tersedia: -- tiket",
            font=ctk.CTkFont(family="Segoe UI", size=11), text_color="#64748b"
        )
        self.lbl_sisa_kuota.pack(anchor="w", pady=(0, 15))

        # ----------------------------------------------------------------------
        # INPUT 3: METODE PEMBAYARAN
        # ----------------------------------------------------------------------
        self.buat_section_label("Metode Pembayaran")
        
        self.opt_pembayaran = ctk.CTkOptionMenu(
            self.form_container,
            values=["QRIS (Otomatis Lunas)", "Transfer Bank (Manual)", "E-Wallet (Dana/OVO)"],
            font=ctk.CTkFont(family="Segoe UI", size=14),
            height=46,
            fg_color=("#ffffff", "#1e293b"),
            text_color=("#0f172a", "#f8fafc"),
            button_color=("#e2e8f0", "#334155"),
            button_hover_color=("#cbd5e1", "#475569"),
            corner_radius=10
        )
        self.opt_pembayaran.pack(fill="x", pady=(0, 20))

        # ----------------------------------------------------------------------
        # AREA SUMMARY: TOTAL BAYAR
        # ----------------------------------------------------------------------
        self.total_card = ctk.CTkFrame(
            self.form_container, fg_color=("#edf2ff", "#131b2e"), height=60, corner_radius=12,
            border_width=1, border_color=("#dbeafe", "#1e293b")
        )
        self.total_card.pack(fill="x", pady=(0, 25))
        
        self.lbl_total_title = ctk.CTkLabel(
            self.total_card, text="Total Bayar", 
            font=ctk.CTkFont(family="Segoe UI", size=14), text_color=("#4f46e5", "#93c5fd")
        )
        self.lbl_total_title.place(relx=0.06, rely=0.5, anchor="w")

        self.lbl_total_harga = ctk.CTkLabel(
            self.total_card, text="Rp 0", 
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"), text_color=("#4f46e5", "#38bdf8")
        )
        self.lbl_total_harga.place(relx=0.94, rely=0.5, anchor="e")

        # ----------------------------------------------------------------------
        # TOMBOL AKSI UTAMA
        # ----------------------------------------------------------------------
        self.btn_submit = ctk.CTkButton(
            self.form_container,
            text="✨  Konfirmasi & Pesan Tiket",
            height=48, corner_radius=12,
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            fg_color="#5a51e6", text_color="white", hover_color="#4338ca",
            command=self.proses_simpan_booking
        )
        self.btn_submit.pack(fill="x", pady=(0, 10))

        self.lbl_lock_info = ctk.CTkLabel(
            self.form_container, text="🔒 Data Anda aman dan terenkripsi",
            font=ctk.CTkFont(family="Segoe UI", size=11), text_color="#94a3b8"
        )
        self.lbl_lock_info.pack(pady=2)

        # Me-load data awal otomatis
        self.update_total_bayar()

    def buat_konten_banner(self):
        badge = ctk.CTkLabel(
            self.banner_frame, text="🌴 Jelajahi Keindahan Indonesia",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            fg_color="white", text_color="#2563eb", corner_radius=20, padx=12, height=24
        )
        badge.pack(anchor="w", padx=40, pady=(60, 0))

        lbl_main = ctk.CTkLabel(
            self.banner_frame, text="Wujudkan Liburan\nImpianmu",
            font=ctk.CTkFont(family="Segoe UI", size=36, weight="bold"),
            text_color="white", justify="left"
        )
        lbl_main.pack(anchor="w", padx=40, pady=(15, 0))

        lbl_desc = ctk.CTkLabel(
            self.banner_frame, 
            text="Pesan tiket wisata favorit Anda dengan mudah,\ncepat, dan aman tanpa antre.",
            font=ctk.CTkFont(family="Segoe UI", size=14), text_color="#e0f2fe", justify="left"
        )
        lbl_desc.pack(anchor="w", padx=40, pady=(10, 0))

        footer_box = ctk.CTkFrame(self.banner_frame, fg_color=("white", "#1e293b"), corner_radius=16, height=80)
        footer_box.pack(fill="x", side="bottom", padx=30, pady=40)
        footer_box.grid_columnconfigure((0, 1, 2), weight=1)
        
        items = [("🛡️ Aman", "Transaksi Terjamin"), ("⚡ Cepat", "Proses Instant"), ("🎧 24/7", "Layanan Bantuan")]
        for i, (judul, sub) in enumerate(items):
            f_item = ctk.CTkFrame(footer_box, fg_color="transparent")
            f_item.grid(row=0, column=i, padx=5, pady=12, sticky="nsew")
            ctk.CTkLabel(f_item, text=judul, font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), text_color=("#0f172a", "#f8fafc")).pack(anchor="center")
            ctk.CTkLabel(f_item, text=sub, font=ctk.CTkFont(family="Segoe UI", size=10), text_color="#64748b").pack(anchor="center")

    def buat_section_label(self, text):
        lbl = ctk.CTkLabel(
            self.form_container, text=text,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), text_color=("#334155", "#cbd5e1")
        )
        lbl.pack(anchor="w", pady=(10, 4))

    def kurangi_tiket(self):
        if self.jumlah_tiket > 1:
            self.jumlah_tiket -= 1
            self.lbl_jumlah.configure(text=str(self.jumlah_tiket))
            self.update_total_bayar()

    def tambah_tiket(self):
        pilihan = self.opt_destinasi.get()
        max_kuota = self.DATABASE_WISATA[pilihan]["kuota"]
        
        if self.jumlah_tiket < max_kuota:
            self.jumlah_tiket += 1
            self.lbl_jumlah.configure(text=str(self.jumlah_tiket))
            self.update_total_bayar()
        else:
            messagebox.showwarning("Kuota Penuh", f"Maaf, sisa kuota live untuk destinasi ini hanya sisa {max_kuota} slot.")

    def update_total_bayar(self, event=None):
        pilihan = self.opt_destinasi.get()
        info = self.DATABASE_WISATA[pilihan]
        
        # Pengaman jika jumlah input tidak sengaja melebihi batas kuota setelah ganti destinasi
        if self.jumlah_tiket > info["kuota"]:
            self.jumlah_tiket = info["kuota"]
            self.lbl_jumlah.configure(text=str(self.jumlah_tiket))

        total = info["harga"] * self.jumlah_tiket
        self.lbl_total_harga.configure(text=f"Rp {total:,.0f}".replace(",", "."))
        self.lbl_sisa_kuota.configure(text=f"🕒 Tersedia: {info['kuota']} tiket live saat ini")

    def proses_simpan_booking(self):
        destinasi = self.opt_destinasi.get()
        metode = self.opt_pembayaran.get()
        total_harga = self.lbl_total_harga.cget("text")
        
        messagebox.showinfo(
            "Booking Berhasil 🎉", 
            f"Terima kasih, usyikkk!\nPemesanan tiket {destinasi} sebanyak {self.jumlah_tiket} slot telah berhasil diproses.\n\nTotal: {total_harga}\nMetode: {metode}"
        )

if __name__ == "__main__":
    ctk.set_appearance_mode("Light")
    
    root = ctk.CTk()
    root.title("Menu Pemesanan Tiket Dengan Banner Visual")
    root.geometry("1050x700")
    
    form_booking = PagePesanTiket(parent=root)
    form_booking.pack(fill="both", expand=True)
    
    root.mainloop()