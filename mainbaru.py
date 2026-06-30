import customtkinter as ctk
from tkinter import messagebox
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ==============================================================================
# 1. APPLICATION CONTROLLER (PENGENDALI UTAMA WINDOW & NAVIGASI SIDEBAR)
# ==============================================================================
class AplikasiUtama(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("WisataApps - Manajemen Tracking & Booking Tiket")
        self.geometry("1280(x)760")
        self.minsize(1100, 650)
        
        # Sesuai mockup: Light Mode Cerah Elegan
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        # Layout Split Utama (Kolom 0: Sidebar, Kolom 1: Halaman Konten)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = None
        self.tombol_menu_list = {}

        # Frame Utama Wadah Pergantian Halaman
        self.container_halaman = ctk.CTkFrame(self, fg_color="transparent")
        self.container_halaman.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.container_halaman.grid_rowconfigure(0, weight=1)
        self.container_halaman.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Mendaftarkan seluruh kelas halaman ke dalam sistem penumpukan frame (Raise Page)
        for PageClass in (PageLogin, PageRegister, PageDashboardUtama, PageDestinasi, 
                          PagePesanTiket, PageRiwayatTiket, PageProfilAkun, PageLogout):
            page_name = PageClass.__name__
            frame = PageClass(parent=self.container_halaman, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Jalankan program langsung ke frame Login awal
        self.show_frame("PageLogin")

    def show_frame(self, page_name):
        """Mengangkat frame ke paling atas dan mengatur status kemunculan sidebar"""
        frame = self.frames[page_name]
        frame.tkraise()

        if page_name in ["PageLogin", "PageRegister"]:
            self.sembunyikan_sidebar()
        else:
            self.tampilkan_sidebar()
            self.sorot_tombol_aktif(page_name)

    def tampilkan_sidebar(self):
        if self.sidebar_frame is not None:
            return
            
        self.grid_columnconfigure(0, weight=2, minsize=240)
        self.sidebar_frame = ctk.CTkFrame(self, fg_color=("#ffffff", "#1e293b"), corner_radius=0, border_width=1, border_color=("#e2e8f0", "#334155"))
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        # Bagian Atas Sidebar: Logo Brand
        brand_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        brand_frame.pack(fill="x", padx=20, pady=(25, 20))
        ctk.CTkLabel(brand_frame, text="🌴", font=ctk.CTkFont(size=28)).pack(side="left", padx=(5, 10))
        ctk.CTkLabel(brand_frame, text="WisataApps", font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"), text_color="#2563eb").pack(side="left")

        # Item Daftar Tombol Menu Navigasi Sesuai Alur Gambar Mockup
        menu_items = [
            ("🏠 Dashboard Utama", "PageDashboardUtama"),
            ("🗺️ Destinasi Wisata", "PageDestinasi"),
            ("🎫 Pesan Tiket Online", "PagePesanTiket"),
            ("📋 Riwayat Pesanan", "PageRiwayatTiket"),
            ("👤 Profil Akun", "PageProfilAkun"),
            ("🚪 Keluar Aplikasi", "PageLogout")
        ]

        for text, target_frame in menu_items:
            btn = ctk.CTkButton(
                self.sidebar_frame, text=text, height=42, anchor="w", corner_radius=10,
                font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
                fg_color="transparent", text_color=("#475569", "#cbd5e1"),
                hover_color=("#f1f5f9", "#334155"),
                command=lambda tf=target_frame: self.show_frame(tf)
            )
            btn.pack(fill="x", padx=15, pady=4)
            self.tombol_menu_list[target_frame] = btn

        # Banner Promo/Dekorasi Tambahan di bawah Sidebar
        promo_card = ctk.CTkFrame(self.sidebar_frame, fg_color=("#edf2ff", "#131b2e"), corner_radius=14)
        promo_card.pack(fill="x", side="bottom", padx=15, pady=20)
        ctk.CTkLabel(promo_card, text="Liburan Seru\nMenanti Anda!", font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), text_color="#4f46e5", justify="left").pack(anchor="w", padx=15, pady=(12, 4))
        ctk.CTkLabel(promo_card, text="Pesan tiket pariwisata\nterfavorit sekarang juga.", font=ctk.CTkFont(family="Segoe UI", size=10), text_color="#64748b", justify="left").pack(anchor="w", padx=15, pady=(0, 12))

    def sembunyikan_sidebar(self):
        if self.sidebar_frame is not None:
            self.sidebar_frame.destroy()
            self.sidebar_frame = None
            self.tombol_menu_list.clear()
            self.grid_columnconfigure(0, weight=0, minsize=0)

    def sorot_tombol_aktif(self, page_name):
        for target_frame, btn_obj in self.tombol_menu_list.items():
            if target_frame == page_name:
                btn_obj.configure(fg_color="#5a51e6", text_color="white", hover_color="#4338ca")
            else:
                btn_obj.configure(fg_color="transparent", text_color=("#475569", "#cbd5e1"), hover_color=("#f1f5f9", "#334155"))


# ==============================================================================
# 2. FRAME HALAMAN: LOGIN
# ==============================================================================
class PageLogin(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color=("#f8fafc", "#0f172a"))
        
        box = ctk.CTkFrame(self, width=420, height=520, corner_radius=20, fg_color=("#ffffff", "#1e293b"), border_width=1, border_color=("#e2e8f0", "#334155"))
        box.place(relx=0.5, rely=0.5, anchor="center")
        box.pack_propagate(False)
        
        ctk.CTkLabel(box, text="🔒 Login Akun", font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold")).pack(pady=(40, 30))
        
        ctk.CTkLabel(box, text="Username", font=ctk.CTkFont(size=11, weight="bold"), text_color="gray").pack(anchor="w", padx=45)
        self.entry_user = ctk.CTkEntry(box, width=330, height=40, placeholder_text="Masukkan nama pengguna...")
        self.entry_user.pack(pady=(2, 15))
        
        ctk.CTkLabel(box, text="Password", font=ctk.CTkFont(size=11, weight="bold"), text_color="gray").pack(anchor="w", padx=45)
        self.entry_pass = ctk.CTkEntry(box, width=330, height=40, placeholder_text="Masukkan kata sandi...", show="*")
        self.entry_pass.pack(pady=(2, 25))
        
        btn_login = ctk.CTkButton(box, text="Masuk Aplikasi", width=330, height=44, corner_radius=12, font=ctk.CTkFont(weight="bold"), fg_color="#2563eb", command=self.proses_login)
        btn_login.pack(pady=10)
        
        btn_ke_reg = ctk.CTkButton(box, text="Belum punya akun? Daftar disini", fg_color="transparent", text_color="#2563eb", command=lambda: self.controller.show_frame("PageRegister"))
        btn_ke_reg.pack()

    def proses_login(self):
        u = self.entry_user.get()
        p = self.entry_pass.get()
        if u == "usyikkk" and p == "123":
            self.controller.show_frame("PageDashboardUtama")
        else:
            messagebox.showerror("Gagal", "Username atau Password salah! (Akun dev: usyikkk / 123)")


# ==============================================================================
# 3. FRAME HALAMAN: REGISTER
# ==============================================================================
class PageRegister(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color=("#f8fafc", "#0f172a"))
        
        box = ctk.CTkFrame(self, width=420, height=520, corner_radius=20, fg_color=("#ffffff", "#1e293b"), border_width=1, border_color=("#e2e8f0", "#334155"))
        box.place(relx=0.5, rely=0.5, anchor="center")
        box.pack_propagate(False)
        
        ctk.CTkLabel(box, text="📝 Registrasi Akun", font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold")).pack(pady=(40, 30))
        
        ctk.CTkLabel(box, text="Username Baru", font=ctk.CTkFont(size=11, weight="bold"), text_color="gray").pack(anchor="w", padx=45)
        self.entry_user_reg = ctk.CTkEntry(box, width=330, height=40, placeholder_text="Buat nama pengguna...")
        self.entry_user_reg.pack(pady=(2, 15))
        
        ctk.CTkLabel(box, text="Password Baru", font=ctk.CTkFont(size=11, weight="bold"), text_color="gray").pack(anchor="w", padx=45)
        self.entry_pass_reg = ctk.CTkEntry(box, width=330, height=40, placeholder_text="Buat sandi aman...", show="*")
        self.entry_pass_reg.pack(pady=(2, 25))
        
        btn_reg = ctk.CTkButton(box, text="Buat Akun Sekarang", width=330, height=44, corner_radius=12, fg_color="#10b981", font=ctk.CTkFont(weight="bold"), command=self.proses_register)
        btn_reg.pack(pady=10)
        
        btn_ke_log = ctk.CTkButton(box, text="Sudah punya akun? Login", fg_color="transparent", text_color="#10b981", command=lambda: self.controller.show_frame("PageLogin"))
        btn_ke_log.pack()

    def proses_register(self):
        if self.entry_user_reg.get().strip() == "" or self.entry_pass_reg.get().strip() == "":
            messagebox.showwarning("Peringatan", "Form tidak boleh ada yang kosong!")
        else:
            messagebox.showinfo("Sukses", "Akun Berhasil Dibuat! Silakan login kembali.")
            self.controller.show_frame("PageLogin")


# ==============================================================================
# 4. FRAME HALAMAN: DASHBOARD UTAMA (MURNI CTKFRAME - BEBAS ERROR AFTER)
# ==============================================================================
class PageDashboardUtama(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, fg_color=("#f1f5f9", "#0f172a"))
        self.controller = controller

        # Header Area
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=35, pady=(30, 15))
        ctk.CTkLabel(header_frame, text="Selamat datang kembali, usyikkk! 👋", font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(header_frame, text="Pantau ringkasan log pelacakan kuota serta statistik transaksi booking tiket.", font=ctk.CTkFont(size=13), text_color="#64748b").pack(anchor="w", pady=2)

        # Split Konten Utama
        main_layout = ctk.CTkFrame(self, fg_color="transparent")
        main_layout.pack(fill="both", expand=True, padx=35, pady=10)
        main_layout.grid_columnconfigure(0, weight=3)
        main_layout.grid_columnconfigure(1, weight=2)
        main_layout.grid_rowconfigure(0, weight=1)

        # Kiri: Wadah Grafik Matplotlib Real
        chart_card = ctk.CTkFrame(main_layout, fg_color=("#ffffff", "#1e293b"), corner_radius=16, border_width=1, border_color=("#e2e8f0", "#334155"))
        chart_card.grid(row=0, column=0, padx=(0, 12), sticky="nsew", ipady=15)
        ctk.CTkLabel(chart_card, text="📊 Tren Pengunjung Wisata Terkini", font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold")).pack(anchor="w", padx=20, pady=(15, 10))

        # Menggambar Grafik Tren Linier Matplotlib ke Tkinter Canvas
        fig = Figure(figsize=(5, 3.2), dpi=100, facecolor='#ffffff')
        ax = fig.add_subplot(111)
        ax.set_facecolor('#f8fafc')
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun']
        visitors = [45, 60, 55, 85, 120, 150]
        ax.plot(months, visitors, marker='o', color='#5a51e6', linewidth=2.5, markersize=6)
        ax.fill_between(months, visitors, color='#5a51e6', alpha=0.1)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#cbd5e1')
        ax.spines['bottom'].set_color('#cbd5e1')
        ax.tick_params(colors='#64748b', labelsize=9)
        ax.grid(axis='y', linestyle='--', alpha=0.5, color='#e2e8f0')

        canvas = FigureCanvasTkAgg(fig, master=chart_card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=(0,10))

        # Kanan: Daftar Destinasi Populer Favorit
        pop_card = ctk.CTkFrame(main_layout, fg_color=("#ffffff", "#1e293b"), corner_radius=16, border_width=1, border_color=("#e2e8f0", "#334155"))
        pop_card.grid(row=0, column=1, padx=(12, 0), sticky="nsew")
        ctk.CTkLabel(pop_card, text="🔥 Destinasi Terpopuler", font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold")).pack(anchor="w", padx=20, pady=(15, 10))

        pop_data = [
            {"nama": "Karimunjawa", "lokasi": "Jepara", "kunjungan": "1.2k visit", "icon": "🏝️"},
            {"nama": "Candi Borobudur", "lokasi": "Magelang", "kunjungan": "980 visit", "icon": "🗿"},
            {"nama": "Solo Safari", "lokasi": "Surakarta", "kunjungan": "850 visit", "icon": "🦁"}
        ]
        
        for i, data in enumerate(pop_data):
            row = ctk.CTkFrame(pop_card, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=8)
            ctk.CTkLabel(row, text=str(i+1), font=ctk.CTkFont(size=12, weight="bold"), fg_color=("#edf2ff", "#131b2e"), text_color="#5a51e6", width=26, height=26, corner_radius=13).pack(side="left", padx=(0, 10))
            
            fd = ctk.CTkFrame(row, fg_color="transparent")
            fd.pack(side="left", fill="both", expand=True)
            ctk.CTkLabel(fd, text=f"{data['icon']} {data['nama']}", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w")
            ctk.CTkLabel(fd, text=data["lokasi"], font=ctk.CTkFont(size=11), text_color="#64748b").pack(anchor="w")
            ctk.CTkLabel(row, text=data["kunjungan"], font=ctk.CTkFont(size=12, weight="bold"), text_color="#475569").pack(side="right", padx=10)


# ==============================================================================
# 5. FRAME HALAMAN: DESTINASI WISATA (MURNI CTKFRAME - AMAN RENDERING)
# ==============================================================================
class PageDestinasi(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, fg_color=("#f1f5f9", "#0f172a"))
        self.controller = controller

        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=35, pady=(30, 10))
        ctk.CTkLabel(header_frame, text="Destinasi Wisata & Live Kuota", font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(header_frame, text="Pantau kapasitas sisa kuota tempat pelacakan wisata secara real-time.", font=ctk.CTkFont(size=13), text_color="#64748b").pack(anchor="w", pady=2)

        self.DATA_DESTINASI = [
            {"nama": "Karimunjawa", "lokasi": "Jepara, Jawa Tengah", "kuota": 8, "max": 50, "warna": "#ef4444", "status": "Hampir Habis 🚨"},
            {"nama": "Agrowisata Tasikmadu", "lokasi": "Karanganyar, Jawa Tengah", "kuota": 200, "max": 200, "warna": "#10b981", "status": "Longgar ✅"},
            {"nama": "Solo Safari", "lokasi": "Surakarta, Jawa Tengah", "kuota": 120, "max": 150, "warna": "#10b981", "status": "Tersedia ✅"},
            {"nama": "Saloka Theme Park", "lokasi": "Semarang, Jawa Tengah", "kuota": 45, "max": 100, "warna": "#f59e0b", "status": "Ramai ⚠️"},
            {"nama": "Candi Borobudur", "lokasi": "Magelang, Jawa Tengah", "kuota": 15, "max": 80, "warna": "#f59e0b", "status": "Terbatas ⚠️"}
        ]

        grid_container = ctk.CTkFrame(self, fg_color="transparent")
        grid_container.pack(fill="both", expand=True, padx=35, pady=5)
        grid_container.grid_columnconfigure((0, 1), weight=1, uniform="card")

        for idx, item in enumerate(self.DATA_DESTINASI):
            r = idx // 2
            c = idx % 2
            
            card = ctk.CTkFrame(grid_container, fg_color=("#ffffff", "#1e293b"), corner_radius=14, border_width=1, border_color=("#e2e8f0", "#334155"))
            card.grid(row=r, column=c, padx=8, pady=8, sticky="nsew")
            
            ctk.CTkLabel(card, text=item["nama"], font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold")).pack(anchor="w", padx=18, pady=(12, 2))
            ctk.CTkLabel(card, text=f"📍 {item['lokasi']}", font=ctk.CTkFont(size=11), text_color="#64748b").pack(anchor="w", padx=18)
            
            prog = ctk.CTkProgressBar(card, progress_color=item["warna"], height=6, corner_radius=3)
            prog.pack(fill="x", padx=18, pady=12)
            prog.set(item["kuota"] / item["max"])
            
            bot_frame = ctk.CTkFrame(card, fg_color="transparent")
            bot_frame.pack(fill="x", padx=18, pady=(0, 12))
            ctk.CTkLabel(bot_frame, text=f"Sisa: {item['kuota']}/{item['max']} ({item['status']})", font=ctk.CTkFont(size=11, weight="bold"), text_color=item["warna"]).pack(side="left")
            ctk.CTkButton(bot_frame, text="Pesan Tiket", width=90, height=28, corner_radius=6, font=ctk.CTkFont(size=11, weight="bold"), fg_color="#5a51e6", command=lambda n=item["nama"]: self.aksi_pesan_cepat(n)).pack(side="right")

        fs = ctk.CTkFrame(self, fg_color=("#ffffff", "#1e293b"), corner_radius=12, border_width=1, border_color=("#e2e8f0", "#334155"))
        fs.pack(fill="x", padx=35, pady=(10, 20), ipady=8)
        ctk.CTkLabel(fs, text=f"📊   Total Destinasi Terdaftar: {len(self.DATA_DESTINASI)} Wisata   |   Total Live Kuota Aktif: {sum(d['kuota'] for d in self.DATA_DESTINASI)} Slot Tersedia", font=ctk.CTkFont(size=12), text_color="#475569").pack(side="left", padx=15)

    def aksi_pesan_cepat(self, nama_wisata):
        self.controller.show_frame("PagePesanTiket")


# ==============================================================================
# 6. FRAME HALAMAN: BOOKING TIKET ONLINE FORM
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
        messagebox.showinfo("Booking Berhasil 🎉", f"Terima kasih, usyikkk!\nPemesanan tiket {self.opt_destinasi.get()} sebanyak {self.jumlah_tiket} slot sukses dilakukan!")


# ==============================================================================
# 7. FRAME HALAMAN: RIWAYAT PESANAN
# ==============================================================================
class PageRiwayatTiket(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, fg_color=("#f1f5f9", "#0f172a"))
        self.controller = controller

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=35, pady=(30, 15))
        ctk.CTkLabel(header, text="📋 Riwayat Kunjungan & Tiket", font=ctk.CTkFont(size=26, weight="bold")).pack(anchor="w")

        tc = ctk.CTkFrame(self, fg_color=("#ffffff", "#1e293b"), corner_radius=20, border_width=1, border_color=("#e2e8f0", "#334155"))
        tc.pack(fill="both", expand=True, padx=35, pady=(15, 30))

        ht = ctk.CTkFrame(tc, fg_color=("#f8fafc", "#131b2e"), height=40, corner_radius=8)
        ht.pack(fill="x", padx=20, pady=(20, 10))
        
        cols = [("KODE TIKET", 0.02), ("TANGGAL", 0.20), ("DESTINASI WISATA", 0.40), ("JUMLAH", 0.68), ("TOTAL", 0.78), ("STATUS", 0.90)]
        for text, relx in cols:
            ctk.CTkLabel(ht, text=text, font=ctk.CTkFont(size=11, weight="bold"), text_color="#64748b").place(relx=relx, rely=0.5, anchor="w")

        data_riwayat = [
            {"kode": "TKT-09823", "tgl": "05 Juni 2026", "wisata": "Agrowisata Tasikmadu", "qty": "3 Tiket", "total": "Rp 60.000", "status": "LUNAS", "bg": "#e6f4ea", "fg": "#137333"},
            {"kode": "TKT-09822", "tgl": "02 Juni 2026", "wisata": "Karimunjawa", "qty": "2 Tiket", "total": "Rp 500.000", "status": "LUNAS", "bg": "#e6f4ea", "fg": "#137333"}
        ]

        for item in data_riwayat:
            row = ctk.CTkFrame(tc, fg_color="transparent", height=60)
            row.pack(fill="x", padx=20, pady=4)
            
            ctk.CTkLabel(row, text=item["kode"], font=ctk.CTkFont(size=13, weight="bold"), text_color="#5a51e6").place(relx=0.02, rely=0.5, anchor="w")
            ctk.CTkLabel(row, text=item["tgl"], font=ctk.CTkFont(size=12)).place(relx=0.20, rely=0.5, anchor="w")
            ctk.CTkLabel(row, text=item["wisata"], font=ctk.CTkFont(size=13, weight="bold")).place(relx=0.40, rely=0.5, anchor="w")
            ctk.CTkLabel(row, text=item["qty"], font=ctk.CTkFont(size=12)).place(relx=0.68, rely=0.5, anchor="w")
            ctk.CTkLabel(row, text=item["total"], font=ctk.CTkFont(size=13, weight="bold")).place(relx=0.78, rely=0.5, anchor="w")
            ctk.CTkLabel(row, text=item["status"], font=ctk.CTkFont(size=10, weight="bold"), fg_color=item["bg"], text_color=item["fg"], corner_radius=6, width=75, height=24).place(relx=0.90, rely=0.5, anchor="w")
            
            ctk.CTkFrame(tc, fg_color=("#f1f5f9", "#334155"), height=1).pack(fill="x", padx=20, pady=2)


# ==============================================================================
# 8. FRAME HALAMAN: PROFIL AKUN PENGGUNA
# ==============================================================================
class PageProfilAkun(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, fg_color=("#f8fafc", "#0f172a"))
        self.controller = controller
        
        card = ctk.CTkFrame(self, width=500, height=450, corner_radius=24, fg_color=("#ffffff", "#1e293b"), border_width=1, border_color=("#e2e8f0", "#334155"))
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)
        
        ctk.CTkLabel(card, text="👤 Profil Pengguna", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=30)
        
        self.ent_nama = ctk.CTkEntry(card, width=400, height=44, placeholder_text="Nama Lengkap")
        self.ent_nama.pack(pady=10)
        self.ent_nama.insert(0, "usyikkk")
        
        self.ent_email = ctk.CTkEntry(card, width=400, height=44, placeholder_text="Alamat Email")
        self.ent_email.pack(pady=10)
        self.ent_email.insert(0, "usyikkk@pbo_uas.com")
        
        ctk.CTkButton(card, text="Simpan Perubahan Profil", width=400, height=44, corner_radius=12, fg_color="#2563eb", font=ctk.CTkFont(weight="bold"), command=self.aksi_simpan).pack(pady=20)

    def aksi_simpan(self):
        messagebox.showinfo("Sukses", f"Profil atas nama {self.ent_nama.get()} berhasil diperbarui!")


# ==============================================================================
# 9. FRAME HALAMAN: LOGOUT
# ==============================================================================
class PageLogout(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, fg_color=("#f1f5f9", "#0f172a"))
        self.controller = controller
        
        card = ctk.CTkFrame(self, width=450, height=260, corner_radius=20, fg_color=("#ffffff", "#1e293b"))
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)
        
        ctk.CTkLabel(card, text="🚪 Konfirmasi Keluar", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(40, 15))
        ctk.CTkLabel(card, text="Apakah Anda yakin ingin keluar dan menutup sesi aplikasi?", text_color="#64748b").pack(pady=(0, 30))
        
        bc = ctk.CTkFrame(card, fg_color="transparent")
        bc.pack(fill="x", padx=40)
        
        ctk.CTkButton(bc, text="Batal", width=160, height=40, fg_color=("#e2e8f0", "#334155"), text_color=("#0f172a", "#f8fafc"), command=lambda: self.controller.show_frame("PageDashboardUtama")).pack(side="left")
        ctk.CTkButton(bc, text="Ya, Keluar", width=160, height=40, fg_color="#ef4444", hover_color="#dc2626", command=self.quit).pack(side="right")


# ==============================================================================
# TRIGGER RUN UTAMA PROGRAM
# ==============================================================================
if __name__ == "__main__":
    app = AplikasiUtama()
    app.mainloop()