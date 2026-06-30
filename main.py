import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import urllib.request
import io

# ==============================================================================
# MASTER CONTROLLER WINDOWS
# ==============================================================================
class AplikasiUtama(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Sistem Informasi Wisata & Tracking Kuota Pengunjung")
        self.geometry("1150x700")
        self.minsize(1000, 650)
        
        ctk.set_appearance_mode("System")  
        ctk.set_default_color_theme("blue") 
        
        self.session_user = {
            "nama": "Alfina Putri",
            "email": "alfina.putri@example.com",
            "telp": "081234567890"
        }
        
        self.container = ctk.CTkFrame(self, fg_color=("#f8fafc", "#0f172a"))
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        list_halaman = (PageLogin, PageRegister, PenampungDashboardUtama)
        for PageClass in list_halaman:
            page_name = PageClass.__name__
            frame = PageClass(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.tampilkan_halaman("PageLogin")

    def tampilkan_halaman(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


# ==============================================================================
# 1. HALAMAN LOGIN
# ==============================================================================
class PageLogin(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        box = ctk.CTkFrame(self, width=420, height=500, corner_radius=20,
                           fg_color=("#ffffff", "#1e293b"), border_width=1, border_color=("#e2e8f0", "#334155"))
        box.place(relx=0.5, rely=0.5, anchor="center")
        box.pack_propagate(False)
        
        ctk.CTkLabel(box, text="🏔️", font=ctk.CTkFont(size=40)).pack(pady=(35, 5))
        
        title = ctk.CTkLabel(box, text="WELCOME BACK", font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"), text_color=("#0f172a", "#f8fafc"))
        title.pack(pady=(0, 2))
        
        subtitle = ctk.CTkLabel(box, text="Silakan masuk ke akun Anda", font=ctk.CTkFont(family="Segoe UI", size=12), text_color=("#64748b", "#94a3b8"))
        subtitle.pack(pady=(0, 25))
        
        ctk.CTkLabel(box, text="Username", font=ctk.CTkFont(size=12, weight="bold"), text_color=("#475569", "#cbd5e1")).pack(anchor="w", padx=50, pady=(0, 4))
        self.username_input = ctk.CTkEntry(box, width=320, height=40, corner_radius=10, placeholder_text="Ketik username Anda...", fg_color=("#f8fafc", "#0f172a"))
        self.username_input.pack(pady=(0, 15))
        self.username_input.insert(0, "Alfina Putri") 
        
        ctk.CTkLabel(box, text="Password", font=ctk.CTkFont(size=12, weight="bold"), text_color=("#475569", "#cbd5e1")).pack(anchor="w", padx=50, pady=(0, 4))
        self.password_input = ctk.CTkEntry(box, width=320, height=40, corner_radius=10, placeholder_text="Masukkan password...", show="*", fg_color=("#f8fafc", "#0f172a"))
        self.password_input.pack(pady=(0, 25))
        self.password_input.insert(0, "password")
        
        btn_login = ctk.CTkButton(box, text="Sign In Account", width=320, height=42, corner_radius=10, font=ctk.CTkFont(weight="bold"), fg_color="#2563eb", hover_color="#1d4ed8", command=self.proses_login)
        btn_login.pack(pady=(5, 10))
        
        btn_ke_register = ctk.CTkButton(box, text="Belum punya akun? Daftar di sini", font=ctk.CTkFont(size=12), fg_color="transparent", hover_color=None, text_color="#2563eb",
                                         command=lambda: self.controller.tampilkan_halaman("PageRegister"))
        btn_ke_register.pack()
        
    def proses_login(self):
        user = self.username_input.get().strip()
        pwd = self.password_input.get().strip()
        if user == "" or pwd == "":
            messagebox.showwarning("Peringatan", "Username dan Password harus diisi!")
        else:
            messagebox.showinfo("Sukses", f"Selamat datang kembali, {user}!")
            self.controller.tampilkan_halaman("PenampungDashboardUtama")


# ==============================================================================
# 2. HALAMAN REGISTER
# ==============================================================================
class PageRegister(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        box = ctk.CTkFrame(self, width=420, height=540, corner_radius=20,
                           fg_color=("#ffffff", "#1e293b"), border_width=1, border_color=("#e2e8f0", "#334155"))
        box.place(relx=0.5, rely=0.5, anchor="center")
        box.pack_propagate(False)
        
        ctk.CTkLabel(box, text="✨", font=ctk.CTkFont(size=40)).pack(pady=(25, 5))
        
        title = ctk.CTkLabel(box, text="CREATE ACCOUNT", font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"), text_color=("#0f172a", "#f8fafc"))
        title.pack(pady=(0, 2))
        
        subtitle = ctk.CTkLabel(box, text="Daftarkan akun baru Anda untuk menjelajah", font=ctk.CTkFont(family="Segoe UI", size=12), text_color=("#64748b", "#94a3b8"))
        subtitle.pack(pady=(0, 20))
        
        ctk.CTkLabel(box, text="Nama Lengkap", font=ctk.CTkFont(size=12, weight="bold"), text_color=("#475569", "#cbd5e1")).pack(anchor="w", padx=50, pady=(0, 4))
        self.nama_input = ctk.CTkEntry(box, width=320, height=40, corner_radius=10, placeholder_text="Ketik nama lengkap Anda...", fg_color=("#f8fafc", "#0f172a"))
        self.nama_input.pack(pady=(0, 12))
        
        ctk.CTkLabel(box, text="Username Baru", font=ctk.CTkFont(size=12, weight="bold"), text_color=("#475569", "#cbd5e1")).pack(anchor="w", padx=50, pady=(0, 4))
        self.username_input = ctk.CTkEntry(box, width=320, height=40, corner_radius=10, placeholder_text="Pilih nama penunjuk akun...", fg_color=("#f8fafc", "#0f172a"))
        self.username_input.pack(pady=(0, 12))
        
        ctk.CTkLabel(box, text="Password Baru", font=ctk.CTkFont(size=12, weight="bold"), text_color=("#475569", "#cbd5e1")).pack(anchor="w", padx=50, pady=(0, 4))
        self.password_input = ctk.CTkEntry(box, width=320, height=40, corner_radius=10, placeholder_text="Buat sandi yang aman...", show="*", fg_color=("#f8fafc", "#0f172a"))
        self.password_input.pack(pady=(0, 20))
        
        btn_register = ctk.CTkButton(box, text="Daftar Akun Baru", width=320, height=42, corner_radius=10, font=ctk.CTkFont(weight="bold"), fg_color="#10b981", hover_color="#059669", command=self.proses_register)
        btn_register.pack(pady=(5, 10))
        
        btn_ke_login = ctk.CTkButton(box, text="Sudah punya akun? Masuk di sini", font=ctk.CTkFont(size=12), fg_color="transparent", hover_color=None, text_color="#2563eb",
                                     command=lambda: self.controller.tampilkan_halaman("PageLogin"))
        btn_ke_login.pack()
        
    def proses_register(self):
        nama = self.nama_input.get().strip()
        user = self.username_input.get().strip()
        pwd = self.password_input.get().strip()
        
        if nama == "" or user == "" or pwd == "":
            messagebox.showwarning("Peringatan", "Semua kolom registrasi wajib diisi!")
        else:
            messagebox.showinfo("Registrasi Berhasil", "Akun Anda berhasil terdaftar!\nSilakan login.")
            self.controller.tampilkan_halaman("PageLogin")


# ==============================================================================
# 3. PENAMPUNG WORKSPACE UTAMA (LAYOUT SIDEBAR & SUB-FRAMES NAVIGATION)
# ==============================================================================
class PenampungDashboardUtama(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        self.grid_columnconfigure(0, weight=0) 
        self.grid_columnconfigure(1, weight=1) 
        self.grid_rowconfigure(0, weight=1)
        
        # SIDEBAR PANEL MENU (KIRI)
        sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=("#ffffff", "#1e293b"), border_width=1, border_color=("#e2e8f0", "#334155"))
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.pack_propagate(False)
        
        lbl_logo = ctk.CTkLabel(sidebar, text="🗺️ TRACKING GO", font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"), text_color="#2563eb")
        lbl_logo.pack(pady=(30, 25))
        
        # Action Command diperbaiki agar memanggil string key nama Class dengan benar
        self.btn_m1 = ctk.CTkButton(sidebar, text="🗺️ Destinasi Wisata", anchor="w", height=38, fg_color="transparent", text_color=("#334155", "#cbd5e1"), hover_color=("#f1f5f9", "#334155"), command=lambda: self.ganti_sub_halaman("SubPageDestinasi"))
        self.btn_m1.pack(fill="x", padx=15, pady=4)
        
        self.btn_m2 = ctk.CTkButton(sidebar, text="🎟️ Pesan Tiket Masuk", anchor="w", height=38, fg_color="transparent", text_color=("#334155", "#cbd5e1"), hover_color=("#f1f5f9", "#334155"), command=lambda: self.ganti_sub_halaman("PagePesanTiket"))
        self.btn_m2.pack(fill="x", padx=15, pady=4)
        
        self.btn_m3 = ctk.CTkButton(sidebar, text="📜 Riwayat Pemesanan", anchor="w", height=38, fg_color="transparent", text_color=("#334155", "#cbd5e1"), hover_color=("#f1f5f9", "#334155"), command=lambda: self.ganti_sub_halaman("SubPageRiwayat"))
        self.btn_m3.pack(fill="x", padx=15, pady=4)
        
        self.btn_m4 = ctk.CTkButton(sidebar, text="👤 Profil Akun", anchor="w", height=38, fg_color="transparent", text_color=("#334155", "#cbd5e1"), hover_color=("#f1f5f9", "#334155"), command=lambda: self.ganti_sub_halaman("SubPageProfil"))
        self.btn_m4.pack(fill="x", padx=15, pady=4)
        
        spacer = ctk.CTkLabel(sidebar, text="")
        spacer.pack(fill="both", expand=True)
        
        self.btn_logout = ctk.CTkButton(sidebar, text="🚪 Keluar Aplikasi", anchor="w", height=38, fg_color="transparent", text_color="#ef4444", hover_color=("#fef2f2", "rgba(239, 68, 68, 0.1)"), command=lambda: self.ganti_sub_halaman("SubPageLogout"))
        self.btn_logout.pack(fill="x", padx=15, pady=(0, 20))

        # KONTEN SUB-FRAME KANAN
        self.konten_kanan = ctk.CTkFrame(self, fg_color="transparent")
        self.konten_kanan.grid(row=0, column=1, sticky="nsew")
        self.konten_kanan.grid_rowconfigure(0, weight=1)
        self.konten_kanan.grid_columnconfigure(0, weight=1)
        
        self.sub_frames = {}
        
        list_sub = (SubPageDestinasi, PagePesanTiket, SubPageRiwayat, SubPageProfil, SubPageLogout)
        for SubClass in list_sub:
            name = SubClass.__name__
            frame = SubClass(parent=self.konten_kanan, master_dashboard=self)
            self.sub_frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.ganti_sub_halaman("SubPageDestinasi")

    def ganti_sub_halaman(self, name):
        frame = self.sub_frames[name]
        frame.tkraise()


# ==============================================================================
# SUB-PAGE A: DASHBOARD UTAMA (FIXED GRID SCROLLABLE & BANNER ONLINE)
# ==============================================================================
class SubPageDestinasi(ctk.CTkScrollableFrame):
    def __init__(self, parent, master_dashboard):
        # Inisialisasi Frame Scrollable bawaan CustomTkinter
        super().__init__(parent, fg_color=("#f1f5f9", "#0f172a"))
        self.master_dashboard = master_dashboard
        
        # Header Area
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(25, 15))
        ctk.CTkLabel(header, text="🏖️ DASHBOARD UTAMA DESTINASI WISATA", font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(header, text="Manajemen kuota masuk gerbang pariwisata terintegrasi secara live.", font=ctk.CTkFont(size=12), text_color="gray").pack(anchor="w")
        
        # Main Grid Container Box
        self.grid_box = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_box.pack(fill="both", expand=True, padx=15)
        self.grid_box.grid_columnconfigure((0, 1), weight=1)
        
        # Array Data Destinasi dengan link Unsplash Gambar Landscape
        data_wisata = [
            {
                "nama": "Pantai Parangtritis", 
                "harga": "Rp 15.000", 
                "kuota": "120 Orang Tersisa", 
                "color": "#10b981",
                "url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=500&auto=format&fit=crop&q=60"
            },
            {
                "nama": "Lereng Gunung Merbabu", 
                "harga": "Rp 25.000", 
                "kuota": "45 Orang Tersisa", 
                "color": "#eab308",
                "url": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=500&auto=format&fit=crop&q=60"
            },
            {
                "nama": "Wisata Budaya Keraton", 
                "harga": "Rp 20.000", 
                "kuota": "15 Tempat Tersedia", 
                "color": "#ef4444",
                "url": "https://images.unsplash.com/photo-1596402184320-417e7178b2cd?w=500&auto=format&fit=crop&q=60"
            }
        ]
        
        for idx, item in enumerate(data_wisata):
            # Card Base Frame
            card = ctk.CTkFrame(self.grid_box, fg_color=("#ffffff", "#1e293b"), corner_radius=15, border_width=1, border_color=("#e2e8f0", "#334155"), height=260)
            card.grid(row=idx//2, column=idx%2, padx=15, pady=15, sticky="nsew")
            card.pack_propagate(False)
            
            # Label Placeholder Banner
            lbl_banner = ctk.CTkLabel(card, text="Memuat Gambar Spanduk...", font=ctk.CTkFont(size=11))
            lbl_banner.pack(fill="x", side="top")
            
            # Download dan pasang gambar otomatis ke Card Box
            self.download_spanduk_internet(lbl_banner, item["url"])
            
            # Info Deskripsi Bawah Gambar
            info_box = ctk.CTkFrame(card, fg_color="transparent")
            info_box.pack(fill="both", expand=True, padx=15, pady=12)
            
            ctk.CTkLabel(info_box, text=item["nama"], font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold")).pack(anchor="w")
            
            row_detil = ctk.CTkFrame(info_box, fg_color="transparent")
            row_detil.pack(fill="x", pady=4)
            
            ctk.CTkLabel(row_detil, text=f"HTM: {item['harga']}", text_color="#2563eb", font=ctk.CTkFont(weight="bold", size=13)).pack(side="left")
            ctk.CTkLabel(row_detil, text=item["kuota"], text_color=item["color"], font=ctk.CTkFont(weight="bold", size=13)).pack(side="right")

    def download_spanduk_internet(self, label_target, url_tujuan):
        try:
            req = urllib.request.Request(url_tujuan, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                img_bytes = response.read()
            
            img_pil = Image.open(io.BytesIO(img_bytes))
            # Konfigurasi dimensi gambar lanskap agar pas di dashboard
            ctk_img = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(410, 135))
            
            label_target.configure(image=ctk_img, text="")
            label_target.image = ctk_img
        except Exception:
            label_target.configure(text="⚠️ Foto Wisata Gagal Dimuat", text_color="#ef4444")


# ==============================================================================
# SUB-PAGE B: HALAMAN TIKET DENGAN GAMBAR DINAMIS INTERNET
# ==============================================================================
class PagePesanTiket(ctk.CTkFrame):
    def __init__(self, parent, master_dashboard):
        super().__init__(parent, fg_color=("#f1f5f9", "#0f172a"))
        self.master_dashboard = master_dashboard
        
        self.DATA_WISATA = {
            "🏖️ Pantai Parangtritis (Rp 15.000)": 15000,
            "🏔️ Lereng Gunung Merbabu (Rp 25.000)": 25000,
            "🏛️ Wisata Budaya Keraton (Rp 20.000)": 20000
        }
        
        self.URL_GAMBAR_WISATA = {
            "🏖️ Pantai Parangtritis (Rp 15.000)": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=400&auto=format&fit=crop&q=60",
            "🏔️ Lereng Gunung Merbabu (Rp 25.000)": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=400&auto=format&fit=crop&q=60",
            "🏛️ Wisata Budaya Keraton (Rp 20.000)": "https://images.unsplash.com/photo-1596402184320-417e7178b2cd?w=400&auto=format&fit=crop&q=60"
        }
        
        self.box = ctk.CTkFrame(self, width=820, height=540, corner_radius=20, fg_color=("#ffffff", "#1e293b"), border_width=1, border_color=("#e2e8f0", "#334155"))
        self.box.place(relx=0.5, rely=0.5, anchor="center")
        self.box.pack_propagate(False)
        
        self.box.grid_columnconfigure(0, weight=1) 
        self.box.grid_columnconfigure(1, weight=1) 
        self.box.grid_rowconfigure(0, weight=1)

        self.frame_kiri = ctk.CTkFrame(self.box, fg_color="transparent")
        self.frame_kiri.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        
        self.lbl_visual_gambar = ctk.CTkLabel(self.frame_kiri, text="Memuat Gambar...", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_visual_gambar.pack(fill="both", expand=True)

        self.frame_kanan = ctk.CTkFrame(self.box, fg_color="transparent")
        self.frame_kanan.grid(row=0, column=1, sticky="nsew", padx=20, pady=15)
        
        ctk.CTkLabel(self.frame_kanan, text="🎫", font=ctk.CTkFont(size=30)).pack(pady=(10, 5))
        
        title = ctk.CTkLabel(self.frame_kanan, text="BOOKING TIKET ONLINE", font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"))
        title.pack()
        
        subtitle = ctk.CTkLabel(self.frame_kanan, text="Isi formulir untuk pemesanan tiket wisata", font=ctk.CTkFont(family="Segoe UI", size=11), text_color="gray")
        subtitle.pack(pady=(0, 15))
        
        ctk.CTkLabel(self.frame_kanan, text="Pilih Destinasi Wisata", font=ctk.CTkFont(size=12, weight="bold"), text_color=("#475569", "#cbd5e1")).pack(anchor="w")
        self.pilihan_wisata = ctk.CTkOptionMenu(self.frame_kanan, width=340, height=38, values=list(self.DATA_WISATA.keys()), command=self.event_opsi_berubah)
        self.pilihan_wisata.pack(pady=(2, 10))
        
        ctk.CTkLabel(self.frame_kanan, text="Jumlah Tiket", font=ctk.CTkFont(size=12, weight="bold"), text_color=("#475569", "#cbd5e1")).pack(anchor="w")
        self.jumlah_input = ctk.CTkEntry(self.frame_kanan, width=340, height=38, placeholder_text="Contoh: 2", fg_color=("#f8fafc", "#0f172a"))
        self.jumlah_input.pack(pady=(2, 5))
        self.jumlah_input.bind("<KeyRelease>", self.update_total_harga)
        
        ctk.CTkLabel(self.frame_kanan, text="Metode Pembayaran", font=ctk.CTkFont(size=12, weight="bold"), text_color=("#475569", "#cbd5e1")).pack(anchor="w", pady=(5, 0))
        self.pilihan_bayar = ctk.CTkOptionMenu(self.frame_kanan, width=340, height=38, values=["QRIS (Otomatis Lunas)", "Transfer Bank Mandiri/BCA", "Bayar di Lokasi (Cash)"], fg_color=("#64748b", "#334155"))
        self.pilihan_bayar.pack(pady=(2, 10))
        
        self.box_total = ctk.CTkFrame(self.frame_kanan, width=340, height=45, fg_color=("#f8fafc", "#0f172a"), corner_radius=10)
        self.box_total.pack(pady=10)
        self.box_total.pack_propagate(False)
        
        self.lbl_total = ctk.CTkLabel(self.box_total, text="Total Bayar: Rp 0", font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), text_color="#2563eb")
        self.lbl_total.place(relx=0.5, rely=0.5, anchor="center")
        
        self.btn_pesan = ctk.CTkButton(self.frame_kanan, text="Konfirmasi & Pesan Tiket", width=340, height=42, corner_radius=10, font=ctk.CTkFont(weight="bold"), fg_color="#2563eb", command=self.proses_pemesanan)
        self.btn_pesan.pack()

        self.ganti_visual_gambar(self.pilihan_wisata.get())

    def event_opsi_berubah(self, pilihan):
        self.update_total_harga()
        self.ganti_visual_gambar(pilihan)

    def ganti_visual_gambar(self, nama_opsi):
        url_gambar = self.URL_GAMBAR_WISATA[nama_opsi]
        self.lbl_visual_gambar.configure(image=None, text="Memuat Gambar Baru...")
        self.update() 

        try:
            req = urllib.request.Request(url_gambar, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                img_data = response.read()
            
            img_pil = Image.open(io.BytesIO(img_data))
            ctk_img = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(360, 480))
            self.lbl_visual_gambar.configure(image=ctk_img, text="")
            self.lbl_visual_gambar.image = ctk_img
        except Exception:
            self.lbl_visual_gambar.configure(image=None, text="⚠️ Gagal Load Gambar", text_color="#ef4444")

    def update_total_harga(self, event=None):
        try:
            wisata_terpilih = self.pilihan_wisata.get()
            harga_satuan = self.DATA_WISATA[wisata_terpilih]
            jumlah_tiket_str = self.jumlah_input.get().strip()
            
            if jumlah_tiket_str == "":
                self.lbl_total.configure(text="Total Bayar: Rp 0")
                return
                
            jumlah_tiket = int(jumlah_tiket_str)
            if jumlah_tiket <= 0:
                self.lbl_total.configure(text="Jumlah harus lebih dari 0")
                return
                
            total_harga = harga_satuan * jumlah_tiket
            self.lbl_total.configure(text=f"Total Bayar: Rp {total_harga:,}".replace(",", "."))
        except ValueError:
            self.lbl_total.configure(text="⚠️ Input harus angka!")

    def proses_pemesanan(self):
        destinasi = self.pilihan_wisata.get()
        jumlah = self.jumlah_input.get().strip()
        metode = self.pilihan_bayar.get()
        
        if jumlah == "":
            messagebox.showwarning("Gagal", "Silakan masukkan jumlah tiket!")
            return
            
        try:
            int_jumlah = int(jumlah)
            if int_jumlah <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Eror", "Jumlah tiket harus angka positif!")
            return
            
        total_akhir = self.lbl_total.cget("text")
        struk_pesan = f"=== NOTA TIKET ONLINE ===\n\nDestinasi : {destinasi.split(' (')[0]}\nJumlah    : {int_jumlah} Tiket\nMetode    : {metode}\n-------------------------\n{total_akhir}\n\nStatus: Berhasil!"
        messagebox.showinfo("Transaksi Sukses", struk_pesan)
        self.jumlah_input.delete(0, 'end')
        self.lbl_total.configure(text="Total Bayar: Rp 0")


# ==============================================================================
# SUB-PAGE C: RIWAYAT PESANAN
# ==============================================================================
class SubPageRiwayat(ctk.CTkFrame):
    def __init__(self, parent, master_dashboard):
        super().__init__(parent, fg_color=("#f1f5f9", "#0f172a"))
        
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(25, 15))
        ctk.CTkLabel(header, text="📜 LOG MANIFES RIWAYAT KUNJUNGAN", font=ctk.CTkFont(size=22, weight="bold")).pack(anchor="w")
        
        tabel = ctk.CTkScrollableFrame(self, fg_color=("#ffffff", "#1e293b"), corner_radius=12, border_width=1, border_color=("#e2e8f0", "#334155"))
        tabel.pack(fill="both", expand=True, padx=30, pady=(0, 30))
        
        h_row = ctk.CTkFrame(tabel, fg_color=("#f8fafc", "#0f172a"), height=35)
        h_row.pack(fill="x", padx=5, pady=5)
        ctk.CTkLabel(h_row, text="KODE TIKET", font=ctk.CTkFont(size=11, weight="bold"), text_color="gray").pack(side="left", padx=20)
        ctk.CTkLabel(h_row, text="DESTINASI WISATA", font=ctk.CTkFont(size=11, weight="bold"), text_color="gray").pack(side="left", padx=60)
        ctk.CTkLabel(h_row, text="STATUS GAIN", font=ctk.CTkFont(size=11, weight="bold"), text_color="gray").pack(side="right", padx=20)
        
        row = ctk.CTkFrame(tabel, fg_color="transparent", height=40)
        row.pack(fill="x", padx=5, pady=2)
        ctk.CTkLabel(row, text="🎟️ TKT-09823", font=ctk.CTkFont(weight="bold"), text_color="#2563eb").pack(side="left", padx=20)
        ctk.CTkLabel(row, text="Wisata Budaya Keraton", font=ctk.CTkFont(weight="normal")).pack(side="left", padx=35)
        ctk.CTkLabel(row, text="LUNAS / ACTIVE", text_color="#10b981", font=ctk.CTkFont(weight="bold")).pack(side="right", padx=20)


# ==============================================================================
# SUB-PAGE D: PROFIL PENGGUNA
# ==============================================================================
class SubPageProfil(ctk.CTkFrame):
    def __init__(self, parent, master_dashboard):
        super().__init__(parent, fg_color=("#f1f5f9", "#0f172a"))
        self.master_dashboard = master_dashboard
        
        card = ctk.CTkFrame(self, width=460, height=460, corner_radius=16, fg_color=("#ffffff", "#1e293b"), border_width=1, border_color=("#e2e8f0", "#334155"))
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)
        
        nama_user = self.master_dashboard.controller.session_user["nama"]
        email_user = self.master_dashboard.controller.session_user["email"]
        telp_user = self.master_dashboard.controller.session_user["telp"]
        
        ctk.CTkLabel(card, text="👩‍💻", font=ctk.CTkFont(size=40)).pack(pady=(25, 5))
        self.lbl_header = ctk.CTkLabel(card, text=nama_user, font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_header.pack()
        ctk.CTkLabel(card, text="Sesi Akses: Terautentikasi (User)", text_color="#10b981", font=ctk.CTkFont(size=12)).pack(pady=(0, 15))
        
        ctk.CTkLabel(card, text="Nama Pengguna", font=ctk.CTkFont(size=11, weight="bold"), text_color="gray").pack(anchor="w", padx=45)
        self.ent_nama = ctk.CTkEntry(card, width=370, height=35)
        self.ent_nama.pack(pady=(2, 10))
        self.ent_nama.insert(0, nama_user)
        
        ctk.CTkLabel(card, text="Alamat Email Active", font=ctk.CTkFont(size=11, weight="bold"), text_color="gray").pack(anchor="w", padx=45)
        self.ent_mail = ctk.CTkEntry(card, width=370, height=35)
        self.ent_mail.pack(pady=(2, 10))
        self.ent_mail.insert(0, email_user)

        ctk.CTkLabel(card, text="Nomor Kontak WhatsApp", font=ctk.CTkFont(size=11, weight="bold"), text_color="gray").pack(anchor="w", padx=45)
        self.ent_telp = ctk.CTkEntry(card, width=370, height=35)
        self.ent_telp.pack(pady=(2, 15))
        self.ent_telp.insert(0, telp_user)
        
        btn = ctk.CTkButton(card, text="Simpan Data Profil Baru", width=370, height=38, font=ctk.CTkFont(weight="bold"), fg_color="#2563eb", command=self.simpan)
        btn.pack()
        
    def simpan(self):
        nama_baru = self.ent_nama.get().strip()
        if nama_baru == "":
            messagebox.showwarning("Gagal", "Nama tidak boleh kosong!")
        else:
            self.lbl_header.configure(text=nama_baru)
            messagebox.showinfo("Sukses", "Detail data profil berhasil diperbarui!")


# ==============================================================================
# SUB-PAGE E: KONFIRMASI LOGOUT
# ==============================================================================
class SubPageLogout(ctk.CTkFrame):
    def __init__(self, parent, master_dashboard):
        super().__init__(parent, fg_color=("#f1f5f9", "#0f172a"))
        self.master_dashboard = master_dashboard
        
        box = ctk.CTkFrame(self, width=420, height=260, corner_radius=16, fg_color=("#ffffff", "#1e293b"), border_width=1, border_color=("#e2e8f0", "#334155"))
        box.place(relx=0.5, rely=0.5, anchor="center")
        box.pack_propagate(False)
        
        ctk.CTkLabel(box, text="🚪", font=ctk.CTkFont(size=40)).pack(pady=(25, 5))
        ctk.CTkLabel(box, text="Ingin mengakhiri sesi?", font=ctk.CTkFont(size=18, weight="bold")).pack()
        ctk.CTkLabel(box, text="Anda harus memasukkan kredensial login kembali nanti.", font=ctk.CTkFont(size=12), text_color="gray").pack(pady=(2, 20))
        
        btn_area = ctk.CTkFrame(box, fg_color="transparent")
        btn_area.pack(fill="x", padx=40)
        
        ctk.CTkButton(btn_area, text="Batal", width=160, height=36, fg_color=("#e2e8f0", "#334155"), text_color=("#0f172a", "#f8fafc"), command=lambda: self.master_dashboard.ganti_sub_halaman("SubPageDestinasi")).pack(side="left", padx=(0, 10))
        ctk.CTkButton(btn_area, text="Ya, Keluar Sesi", width=160, height=36, fg_color="#ef4444", text_color="white", hover_color="#dc2626", command=self.keluar_proses).pack(side="right")
        
    def keluar_proses(self):
        messagebox.showinfo("Selesai Sesi", "Sesi login dibersihkan dengan aman.")
        self.master_dashboard.controller.tampilkan_halaman("PageLogin")


# ==============================================================================
# ENGINE RUNNER
# ==============================================================================
if __name__ == "__main__":
    app = AplikasiUtama()
    app.mainloop()