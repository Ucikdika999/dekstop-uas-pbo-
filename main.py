import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import urllib.request
import io
import json
import os

# Nama file database konfigurasi JSON untuk menyimpan data user & password
DATABASE_JSON = "users.json"

# ==============================================================================
# DESIGN SYSTEM — palet warna & tipografi terpusat biar konsisten di semua halaman
# ==============================================================================
class Warna:
    BG_APP        = ("#eef1f8", "#0b0f1a")
    BG_CARD       = ("#ffffff", "#161b2e")
    BG_CARD_SOFT  = ("#f6f7fb", "#111527")
    BG_INPUT      = ("#f4f5fa", "#0d1120")
    BORDER        = ("#e5e7f2", "#242a44")
    SHADOW        = ("#d8dbec", "#05070d")

    TEXT_MAIN     = ("#181b2e", "#f5f6fb")
    TEXT_SUB      = ("#6b7089", "#8a8fb0")
    TEXT_MUTED    = ("#9a9db8", "#5b5f7e")

    PRIMARY       = "#5b5fef"
    PRIMARY_HOVER = "#4548d6"
    PRIMARY_SOFT  = ("#eeeeff", "#1c1d3d")

    ACCENT_GREEN  = "#12b886"
    ACCENT_GREEN_H= "#0ea471"
    ACCENT_AMBER  = "#f5a524"
    ACCENT_RED    = "#f0393f"
    ACCENT_RED_H  = "#d62e33"
    ACCENT_GRAY   = "#8b8fa8"
    ACCENT_GRAY_H = "#71758c"

FONT_FAMILY = "Segoe UI"

def f_title(size=24):
    return ctk.CTkFont(family=FONT_FAMILY, size=size, weight="bold")

def f_subtitle(size=13):
    return ctk.CTkFont(family=FONT_FAMILY, size=size)

def f_label(size=12):
    return ctk.CTkFont(family=FONT_FAMILY, size=size, weight="bold")

def f_body(size=13, bold=False):
    return ctk.CTkFont(family=FONT_FAMILY, size=size, weight="bold" if bold else "normal")


def buat_kartu_bayangan(parent, width, height, corner_radius=24):
    """Membuat efek 'shadow card': frame tipis di belakang sebagai bayangan,
    lalu kartu asli di atasnya sedikit bergeser supaya terasa mengambang."""
    stage = ctk.CTkFrame(parent, fg_color="transparent")
    stage.place(relx=0.5, rely=0.5, anchor="center", width=width + 14, height=height + 14)

    bayangan = ctk.CTkFrame(stage, width=width, height=height, corner_radius=corner_radius,
                             fg_color=Warna.SHADOW)
    bayangan.place(x=13, y=13)

    kartu = ctk.CTkFrame(stage, width=width, height=height, corner_radius=corner_radius,
                          fg_color=Warna.BG_CARD, border_width=1, border_color=Warna.BORDER)
    kartu.place(x=0, y=0)
    kartu.pack_propagate(False)
    return kartu


def inisialisasi_database():
    """Memastikan file JSON siap digunakan dan memiliki data awal jika kosong."""
    if not os.path.exists(DATABASE_JSON):
        data_awal = {
            "Alfina Putri": {
                "password": "password",
                "nama_lengkap": "Alfina Putri",
                "email": "alfina.putri@example.com",
                "telp": "081234567890"
            }
        }
        with open(DATABASE_JSON, "w") as f:
            json.dump(data_awal, f, indent=4)

def muat_semua_user():
    """Membaca seluruh data akun dari file JSON."""
    try:
        with open(DATABASE_JSON, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def simpan_semua_user(data):
    """Menyimpan kembali seluruh struktur data ke file JSON."""
    try:
        with open(DATABASE_JSON, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception:
        return False


# ==============================================================================
# MASTER CONTROLLER WINDOWS
# ==============================================================================
class AplikasiUtama(ctk.CTk):
    def __init__(self):
        super().__init__()

        inisialisasi_database()

        self.title("Sistem Informasi Wisata & Tracking Kuota Pengunjung")
        self.geometry("1180x720")
        self.minsize(1050, 680)

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.session_user = {
            "username": "",
            "nama": "",
            "email": "",
            "telp": ""
        }

        self.container = ctk.CTkFrame(self, fg_color=Warna.BG_APP)
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
        if page_name == "PenampungDashboardUtama":
            frame.refresh_profil_data()


# ==============================================================================
# 1. HALAMAN LOGIN
# ==============================================================================
class PageLogin(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=Warna.BG_APP)
        self.controller = controller

        box = buat_kartu_bayangan(self, width=440, height=540)

        badge = ctk.CTkFrame(box, width=64, height=64, corner_radius=18, fg_color=Warna.PRIMARY_SOFT)
        badge.pack(pady=(42, 14))
        badge.pack_propagate(False)
        ctk.CTkLabel(badge, text="⛰️", font=ctk.CTkFont(size=28)).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(box, text="Selamat Datang Kembali", font=f_title(23), text_color=Warna.TEXT_MAIN).pack(pady=(0, 4))
        ctk.CTkLabel(box, text="Masuk untuk melanjutkan perjalanan wisata Anda", font=f_subtitle(12.5), text_color=Warna.TEXT_SUB).pack(pady=(0, 30))

        ctk.CTkLabel(box, text="USERNAME", font=f_label(11), text_color=Warna.TEXT_SUB).pack(anchor="w", padx=52, pady=(0, 5))
        self.username_input = ctk.CTkEntry(box, width=336, height=44, corner_radius=12,
                                            placeholder_text="Ketik username Anda...",
                                            fg_color=Warna.BG_INPUT, border_color=Warna.BORDER,
                                            text_color=Warna.TEXT_MAIN, font=f_body(13))
        self.username_input.pack(pady=(0, 16))

        ctk.CTkLabel(box, text="PASSWORD", font=f_label(11), text_color=Warna.TEXT_SUB).pack(anchor="w", padx=52, pady=(0, 5))
        self.password_input = ctk.CTkEntry(box, width=336, height=44, corner_radius=12,
                                            placeholder_text="Masukkan password...", show="•",
                                            fg_color=Warna.BG_INPUT, border_color=Warna.BORDER,
                                            text_color=Warna.TEXT_MAIN, font=f_body(13))
        self.password_input.pack(pady=(0, 28))
        self.password_input.bind("<Return>", lambda e: self.proses_login())

        btn_login = ctk.CTkButton(box, text="Masuk ke Akun  →", width=336, height=46, corner_radius=12,
                                   font=f_body(14, bold=True), fg_color=Warna.PRIMARY,
                                   hover_color=Warna.PRIMARY_HOVER, command=self.proses_login)
        btn_login.pack(pady=(4, 14))

        garis = ctk.CTkFrame(box, height=1, width=336, fg_color=Warna.BORDER)
        garis.pack(pady=(2, 14))

        btn_ke_register = ctk.CTkButton(box, text="Belum punya akun?  Daftar Sekarang", font=f_body(12, bold=True),
                                         fg_color="transparent", hover_color=Warna.PRIMARY_SOFT[0],
                                         text_color=Warna.PRIMARY, height=32,
                                         command=lambda: self.controller.tampilkan_halaman("PageRegister"))
        btn_ke_register.pack()

    def proses_login(self):
        user = self.username_input.get().strip()
        pwd = self.password_input.get().strip()

        if user == "" or pwd == "":
            messagebox.showwarning("Peringatan", "Username dan Password wajib diisi!")
            return

        users_data = muat_semua_user()

        if user in users_data and users_data[user]["password"] == pwd:
            self.controller.session_user["username"] = user
            self.controller.session_user["nama"] = users_data[user]["nama_lengkap"]
            self.controller.session_user["email"] = users_data[user]["email"]
            self.controller.session_user["telp"] = users_data[user]["telp"]

            messagebox.showinfo("Sukses", f"Selamat datang kembali, {users_data[user]['nama_lengkap']}!")

            self.username_input.delete(0, 'end')
            self.password_input.delete(0, 'end')

            self.controller.tampilkan_halaman("PenampungDashboardUtama")
        else:
            messagebox.showerror("Gagal Masuk", "Username atau Password yang Anda masukkan salah!")


# ==============================================================================
# 2. HALAMAN REGISTER
# ==============================================================================
class PageRegister(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=Warna.BG_APP)
        self.controller = controller

        box = buat_kartu_bayangan(self, width=440, height=630)

        badge = ctk.CTkFrame(box, width=60, height=60, corner_radius=16, fg_color=("#e9fbf4", "#0e2a22"))
        badge.pack(pady=(30, 12))
        badge.pack_propagate(False)
        ctk.CTkLabel(badge, text="✨", font=ctk.CTkFont(size=26)).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(box, text="Buat Akun Baru", font=f_title(21), text_color=Warna.TEXT_MAIN).pack(pady=(0, 4))
        ctk.CTkLabel(box, text="Daftarkan akun untuk mulai menjelajah destinasi", font=f_subtitle(12), text_color=Warna.TEXT_SUB).pack(pady=(0, 22))

        ctk.CTkLabel(box, text="NAMA LENGKAP", font=f_label(11), text_color=Warna.TEXT_SUB).pack(anchor="w", padx=52, pady=(0, 5))
        self.nama_input = ctk.CTkEntry(box, width=336, height=42, corner_radius=11,
                                        placeholder_text="Ketik nama lengkap Anda...",
                                        fg_color=Warna.BG_INPUT, border_color=Warna.BORDER,
                                        text_color=Warna.TEXT_MAIN, font=f_body(13))
        self.nama_input.pack(pady=(0, 14))

        ctk.CTkLabel(box, text="USERNAME BARU", font=f_label(11), text_color=Warna.TEXT_SUB).pack(anchor="w", padx=52, pady=(0, 5))
        self.username_input = ctk.CTkEntry(box, width=336, height=42, corner_radius=11,
                                            placeholder_text="Pilih nama pengguna...",
                                            fg_color=Warna.BG_INPUT, border_color=Warna.BORDER,
                                            text_color=Warna.TEXT_MAIN, font=f_body(13))
        self.username_input.pack(pady=(0, 14))

        ctk.CTkLabel(box, text="PASSWORD BARU", font=f_label(11), text_color=Warna.TEXT_SUB).pack(anchor="w", padx=52, pady=(0, 5))
        self.password_input = ctk.CTkEntry(box, width=336, height=42, corner_radius=11,
                                            placeholder_text="Buat sandi keamanan...", show="•",
                                            fg_color=Warna.BG_INPUT, border_color=Warna.BORDER,
                                            text_color=Warna.TEXT_MAIN, font=f_body(13))
        self.password_input.pack(pady=(0, 26))
        self.password_input.bind("<Return>", lambda e: self.proses_register())

        btn_register = ctk.CTkButton(box, text="Daftar Akun Baru", width=336, height=46, corner_radius=12,
                                      font=f_body(14, bold=True), fg_color=Warna.ACCENT_GREEN,
                                      hover_color=Warna.ACCENT_GREEN_H, command=self.proses_register)
        btn_register.pack(pady=(5, 14))

        garis = ctk.CTkFrame(box, height=1, width=336, fg_color=Warna.BORDER)
        garis.pack(pady=(2, 14))

        btn_ke_login = ctk.CTkButton(box, text="Sudah punya akun?  Masuk di sini", font=f_body(12, bold=True),
                                      fg_color="transparent", hover_color=Warna.PRIMARY_SOFT[0],
                                      text_color=Warna.PRIMARY, height=32,
                                      command=lambda: self.controller.tampilkan_halaman("PageLogin"))
        btn_ke_login.pack()

    def proses_register(self):
        nama = self.nama_input.get().strip()
        user = self.username_input.get().strip()
        pwd = self.password_input.get().strip()

        if nama == "" or user == "" or pwd == "":
            messagebox.showwarning("Peringatan", "Semua kolom registrasi wajib diisi!")
            return

        users_data = muat_semua_user()

        if user in users_data:
            messagebox.showwarning("Gagal", "Username sudah terdaftar! Gunakan nama yang lain.")
            return

        users_data[user] = {
            "password": pwd,
            "nama_lengkap": nama,
            "email": f"{user.lower().replace(' ', '')}@example.com",
            "telp": "081234567890"
        }

        if simpan_semua_user(users_data):
            messagebox.showinfo("Registrasi Berhasil", f"Akun '{user}' berhasil didaftarkan secara aman!\nSilakan lakukan login.")

            self.nama_input.delete(0, 'end')
            self.username_input.delete(0, 'end')
            self.password_input.delete(0, 'end')

            self.controller.tampilkan_halaman("PageLogin")
        else:
            messagebox.showerror("Error", "Gagal menyimpan database internal baru.")


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
        sidebar = ctk.CTkFrame(self, width=248, corner_radius=0, fg_color=Warna.BG_CARD,
                                border_width=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.pack_propagate(False)

        garis_kanan = ctk.CTkFrame(self, width=1, fg_color=Warna.BORDER)
        garis_kanan.place(x=248, y=0, relheight=1)

        logo_box = ctk.CTkFrame(sidebar, fg_color="transparent")
        logo_box.pack(pady=(34, 26), padx=24, fill="x")
        ctk.CTkLabel(logo_box, text="🗺️  TRACKING GO", font=f_title(18), text_color=Warna.PRIMARY).pack(anchor="w")
        ctk.CTkLabel(logo_box, text="Wisata & Kuota Pengunjung", font=f_subtitle(11), text_color=Warna.TEXT_MUTED).pack(anchor="w", pady=(2, 0))

        ctk.CTkLabel(sidebar, text="MENU UTAMA", font=f_label(10), text_color=Warna.TEXT_MUTED).pack(anchor="w", padx=26, pady=(6, 6))

        self.menu_buttons = {}
        menu_items = [
            ("SubPageDestinasi", "🗺️", "Destinasi Wisata"),
            ("PagePesanTiket", "🎟️", "Pesan Tiket Masuk"),
            ("SubPageRiwayat", "📜", "Riwayat Pemesanan"),
            ("SubPageProfil", "👤", "Profil Akun"),
        ]
        for key, icon, label in menu_items:
            btn = ctk.CTkButton(sidebar, text=f"  {icon}   {label}", anchor="w", height=44, corner_radius=10,
                                 fg_color="transparent", text_color=Warna.TEXT_SUB, font=f_body(13, bold=True),
                                 hover_color=Warna.PRIMARY_SOFT[0], border_width=0,
                                 command=lambda k=key: self.ganti_sub_halaman(k))
            btn.pack(fill="x", padx=16, pady=4)
            self.menu_buttons[key] = btn

        spacer = ctk.CTkLabel(sidebar, text="")
        spacer.pack(fill="both", expand=True)

        garis_atas = ctk.CTkFrame(sidebar, height=1, fg_color=Warna.BORDER)
        garis_atas.pack(fill="x", padx=16, pady=(0, 14))

        self.btn_logout = ctk.CTkButton(sidebar, text="  🚪   Keluar Aplikasi", anchor="w", height=44, corner_radius=10,
                                         fg_color="transparent", font=f_body(13, bold=True),
                                         text_color=Warna.ACCENT_RED, hover_color=("#fdecec", "#2a1416"),
                                         command=lambda: self.ganti_sub_halaman("SubPageLogout"))
        self.btn_logout.pack(fill="x", padx=16, pady=(0, 24))

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

        # Sorot menu sidebar yang sedang aktif
        for key, btn in self.menu_buttons.items():
            if key == name:
                btn.configure(fg_color=Warna.PRIMARY_SOFT[0], text_color=Warna.PRIMARY)
            else:
                btn.configure(fg_color="transparent", text_color=Warna.TEXT_SUB)

    def refresh_profil_data(self):
        if "SubPageProfil" in self.sub_frames:
            self.sub_frames["SubPageProfil"].muat_ulang_sesi()


# ==============================================================================
# SUB-PAGE A: DASHBOARD UTAMA (FIXED GRID SCROLLABLE & BANNER ONLINE)
# ==============================================================================
class SubPageDestinasi(ctk.CTkScrollableFrame):
    def __init__(self, parent, master_dashboard):
        super().__init__(parent, fg_color=Warna.BG_APP)
        self.master_dashboard = master_dashboard

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=34, pady=(28, 18))
        ctk.CTkLabel(header, text="Destinasi Wisata Populer", font=f_title(23), text_color=Warna.TEXT_MAIN).pack(anchor="w")
        ctk.CTkLabel(header, text="Pantau kuota masuk gerbang pariwisata secara real-time.",
                     font=f_subtitle(12.5), text_color=Warna.TEXT_SUB).pack(anchor="w", pady=(3, 0))

        self.grid_box = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_box.pack(fill="both", expand=True, padx=20)
        self.grid_box.grid_columnconfigure((0, 1), weight=1)

        data_wisata = [
            {
                "nama": "Pantai Parangtritis",
                "harga": "Rp 15.000",
                "kuota": "120 Orang Tersisa",
                "color": Warna.ACCENT_GREEN,
                "url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=500&auto=format&fit=crop&q=60"
            },
            {
                "nama": "Lereng Gunung Merbabu",
                "harga": "Rp 25.000",
                "kuota": "45 Orang Tersisa",
                "color": Warna.ACCENT_AMBER,
                "url": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=500&auto=format&fit=crop&q=60"
            },
            {
                "nama": "Wisata Budaya Keraton",
                "harga": "Rp 20.000",
                "kuota": "15 Tempat Tersedia",
                "color": Warna.ACCENT_RED,
                "url": "https://images.unsplash.com/photo-1596402184320-417e7178b2cd?w=500&auto=format&fit=crop&q=60"
            }
        ]

        for idx, item in enumerate(data_wisata):
            card = ctk.CTkFrame(self.grid_box, fg_color=Warna.BG_CARD, corner_radius=18,
                                 border_width=1, border_color=Warna.BORDER, height=270)
            card.grid(row=idx // 2, column=idx % 2, padx=14, pady=14, sticky="nsew")
            card.pack_propagate(False)

            lbl_banner = ctk.CTkLabel(card, text="Memuat Gambar Spanduk...", font=f_subtitle(11),
                                       text_color=Warna.TEXT_MUTED, fg_color=Warna.BG_CARD_SOFT, height=140,
                                       corner_radius=0)
            lbl_banner.pack(fill="x", side="top")

            self.download_spanduk_internet(lbl_banner, item["url"])

            info_box = ctk.CTkFrame(card, fg_color="transparent")
            info_box.pack(fill="both", expand=True, padx=20, pady=14)

            ctk.CTkLabel(info_box, text=item["nama"], font=f_body(16, bold=True),
                         text_color=Warna.TEXT_MAIN).pack(anchor="w")

            row_detil = ctk.CTkFrame(info_box, fg_color="transparent")
            row_detil.pack(fill="x", pady=(8, 0))

            harga_pill = ctk.CTkFrame(row_detil, fg_color=Warna.PRIMARY_SOFT[0], corner_radius=8, height=26)
            harga_pill.pack(side="left")
            ctk.CTkLabel(harga_pill, text=f"  HTM {item['harga']}  ", text_color=Warna.PRIMARY,
                         font=f_body(12, bold=True)).pack(padx=2, pady=3)

            ctk.CTkLabel(row_detil, text=f"● {item['kuota']}", text_color=item["color"],
                         font=f_body(12, bold=True)).pack(side="right")

    def download_spanduk_internet(self, label_target, url_tujuan):
        try:
            req = urllib.request.Request(url_tujuan, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                img_bytes = response.read()

            img_pil = Image.open(io.BytesIO(img_bytes))
            ctk_img = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(430, 140))
            label_target.configure(image=ctk_img, text="")
            label_target.image = ctk_img
        except Exception:
            label_target.configure(text="⚠️ Foto Wisata Gagal Dimuat", text_color=Warna.ACCENT_RED)


# ==============================================================================
# SUB-PAGE B: HALAMAN TIKET DENGAN GAMBAR DINAMIS INTERNET
# ==============================================================================
class PagePesanTiket(ctk.CTkFrame):
    def __init__(self, parent, master_dashboard):
        super().__init__(parent, fg_color=Warna.BG_APP)
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

        self.box = buat_kartu_bayangan(self, width=880, height=580, corner_radius=22)

        self.box.grid_columnconfigure(0, weight=1)
        self.box.grid_columnconfigure(1, weight=1)
        self.box.grid_rowconfigure(0, weight=1)

        self.frame_kiri = ctk.CTkFrame(self.box, fg_color="transparent")
        self.frame_kiri.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)

        self.lbl_visual_gambar = ctk.CTkLabel(self.frame_kiri, text="Memuat Gambar...", font=f_body(12, bold=True),
                                               text_color=Warna.TEXT_MUTED, fg_color=Warna.BG_CARD_SOFT, corner_radius=16)
        self.lbl_visual_gambar.pack(fill="both", expand=True)

        self.frame_kanan = ctk.CTkFrame(self.box, fg_color="transparent")
        self.frame_kanan.grid(row=0, column=1, sticky="nsew", padx=24, pady=18)

        badge = ctk.CTkFrame(self.frame_kanan, width=52, height=52, corner_radius=14, fg_color=Warna.PRIMARY_SOFT)
        badge.pack(pady=(6, 10))
        badge.pack_propagate(False)
        ctk.CTkLabel(badge, text="🎫", font=ctk.CTkFont(size=22)).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(self.frame_kanan, text="Booking Tiket Online", font=f_title(18), text_color=Warna.TEXT_MAIN).pack()
        ctk.CTkLabel(self.frame_kanan, text="Isi formulir untuk pemesanan tiket wisata", font=f_subtitle(11),
                     text_color=Warna.TEXT_SUB).pack(pady=(2, 16))

        ctk.CTkLabel(self.frame_kanan, text="PILIH DESTINASI WISATA", font=f_label(11), text_color=Warna.TEXT_SUB).pack(anchor="w")
        self.pilihan_wisata = ctk.CTkOptionMenu(self.frame_kanan, width=340, height=42, corner_radius=10,
                                                 values=list(self.DATA_WISATA.keys()), command=self.event_opsi_berubah,
                                                 fg_color=Warna.PRIMARY, button_color=Warna.PRIMARY_HOVER,
                                                 button_hover_color=Warna.PRIMARY_HOVER, font=f_body(12))
        self.pilihan_wisata.pack(pady=(4, 14))

        ctk.CTkLabel(self.frame_kanan, text="JUMLAH TIKET", font=f_label(11), text_color=Warna.TEXT_SUB).pack(anchor="w")
        self.jumlah_input = ctk.CTkEntry(self.frame_kanan, width=340, height=42, corner_radius=10,
                                          placeholder_text="Contoh: 2", fg_color=Warna.BG_INPUT,
                                          border_color=Warna.BORDER, text_color=Warna.TEXT_MAIN, font=f_body(13))
        self.jumlah_input.pack(pady=(4, 14))
        self.jumlah_input.bind("<KeyRelease>", self.update_total_harga)

        ctk.CTkLabel(self.frame_kanan, text="METODE PEMBAYARAN", font=f_label(11), text_color=Warna.TEXT_SUB).pack(anchor="w")
        self.pilihan_bayar = ctk.CTkOptionMenu(self.frame_kanan, width=340, height=42, corner_radius=10,
                                                values=["QRIS (Otomatis Lunas)", "Transfer Bank Mandiri/BCA", "Bayar di Lokasi (Cash)"],
                                                fg_color=Warna.ACCENT_GRAY, button_color=Warna.ACCENT_GRAY_H,
                                                button_hover_color=Warna.ACCENT_GRAY_H, font=f_body(12))
        self.pilihan_bayar.pack(pady=(4, 16))

        self.box_total = ctk.CTkFrame(self.frame_kanan, width=340, height=52, fg_color=Warna.PRIMARY_SOFT[0],
                                       corner_radius=12, border_width=1, border_color=Warna.PRIMARY)
        self.box_total.pack(pady=10)
        self.box_total.pack_propagate(False)

        self.lbl_total = ctk.CTkLabel(self.box_total, text="Total Bayar: Rp 0", font=f_body(15, bold=True),
                                       text_color=Warna.PRIMARY)
        self.lbl_total.place(relx=0.5, rely=0.5, anchor="center")

        self.btn_pesan = ctk.CTkButton(self.frame_kanan, text="Konfirmasi & Pesan Tiket  →", width=340, height=46,
                                        corner_radius=12, font=f_body(14, bold=True), fg_color=Warna.PRIMARY,
                                        hover_color=Warna.PRIMARY_HOVER, command=self.proses_pemesanan)
        self.btn_pesan.pack(pady=6)

        self.ganti_visual_gambar(self.pilihan_wisata.get())

    def event_opsi_berubah(self, pilihan):
        self.update_total_harga()
        self.ganti_visual_gambar(pilihan)

    def ganti_visual_gambar(self, nama_opsi):
        url_gambar = self.URL_GAMBAR_WISATA[nama_opsi]
        self.lbl_visual_gambar.configure(image=None, text="Memuat Gambar Wisata Baru...")
        self.update()

        try:
            req = urllib.request.Request(url_gambar, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                img_data = response.read()

            img_pil = Image.open(io.BytesIO(img_data))
            ctk_img = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(380, 510))
            self.lbl_visual_gambar.configure(image=ctk_img, text="")
            self.lbl_visual_gambar.image = ctk_img
        except Exception:
            self.lbl_visual_gambar.configure(image=None, text="⚠️ Gagal Load Gambar", text_color=Warna.ACCENT_RED)

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
        super().__init__(parent, fg_color=Warna.BG_APP)

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=34, pady=(28, 16))
        ctk.CTkLabel(header, text="Riwayat Kunjungan", font=f_title(23), text_color=Warna.TEXT_MAIN).pack(anchor="w")
        ctk.CTkLabel(header, text="Manifes seluruh transaksi tiket yang pernah dilakukan.",
                     font=f_subtitle(12.5), text_color=Warna.TEXT_SUB).pack(anchor="w", pady=(3, 0))

        tabel_wrap = ctk.CTkFrame(self, fg_color="transparent")
        tabel_wrap.pack(fill="both", expand=True, padx=34, pady=(0, 30))

        tabel = ctk.CTkScrollableFrame(tabel_wrap, fg_color=Warna.BG_CARD, corner_radius=16,
                                        border_width=1, border_color=Warna.BORDER)
        tabel.pack(fill="both", expand=True)

        h_row = ctk.CTkFrame(tabel, fg_color=Warna.BG_CARD_SOFT, height=42, corner_radius=8)
        h_row.pack(fill="x", padx=6, pady=6)
        ctk.CTkLabel(h_row, text="KODE TIKET", font=f_label(11), text_color=Warna.TEXT_MUTED).pack(side="left", padx=20, pady=6)
        ctk.CTkLabel(h_row, text="DESTINASI WISATA", font=f_label(11), text_color=Warna.TEXT_MUTED).pack(side="left", padx=80, pady=6)
        ctk.CTkLabel(h_row, text="STATUS", font=f_label(11), text_color=Warna.TEXT_MUTED).pack(side="right", padx=20, pady=6)

        row = ctk.CTkFrame(tabel, fg_color="transparent", height=48)
        row.pack(fill="x", padx=6, pady=3)
        ctk.CTkLabel(row, text="🎟️ TKT-09823", font=f_body(13, bold=True), text_color=Warna.PRIMARY).pack(side="left", padx=20)
        ctk.CTkLabel(row, text="Wisata Budaya Keraton", font=f_body(13), text_color=Warna.TEXT_MAIN).pack(side="left", padx=55)

        status_pill = ctk.CTkFrame(row, fg_color=("#e8faf3", "#0e2a22"), corner_radius=8, height=26)
        status_pill.pack(side="right", padx=20)
        ctk.CTkLabel(status_pill, text="  ● LUNAS / ACTIVE  ", text_color=Warna.ACCENT_GREEN,
                     font=f_body(11, bold=True)).pack(padx=2, pady=3)


# ==============================================================================
# SUB-PAGE D: PROFIL PENGGUNA (TERKONEKSI KE DATABASE JSON)
# ==============================================================================
class SubPageProfil(ctk.CTkFrame):
    def __init__(self, parent, master_dashboard):
        super().__init__(parent, fg_color=Warna.BG_APP)
        self.master_dashboard = master_dashboard

        self.card = buat_kartu_bayangan(self, width=500, height=500, corner_radius=20)

        avatar = ctk.CTkFrame(self.card, width=76, height=76, corner_radius=38, fg_color=Warna.PRIMARY_SOFT)
        avatar.pack(pady=(28, 10))
        avatar.pack_propagate(False)
        ctk.CTkLabel(avatar, text="👩‍💻", font=ctk.CTkFont(size=32)).place(relx=0.5, rely=0.5, anchor="center")

        self.lbl_header = ctk.CTkLabel(self.card, text="Nama Pengguna", font=f_title(19), text_color=Warna.TEXT_MAIN)
        self.lbl_header.pack()

        status_pill = ctk.CTkFrame(self.card, fg_color=("#e8faf3", "#0e2a22"), corner_radius=8, height=24)
        status_pill.pack(pady=(6, 20))
        ctk.CTkLabel(status_pill, text="  ● Sesi Terautentikasi  ", text_color=Warna.ACCENT_GREEN,
                     font=f_body(11, bold=True)).pack(padx=2, pady=3)

        ctk.CTkLabel(self.card, text="NAMA PENGGUNA RESMI", font=f_label(11), text_color=Warna.TEXT_SUB).pack(anchor="w", padx=46)
        self.ent_nama = ctk.CTkEntry(self.card, width=408, height=40, corner_radius=10,
                                      fg_color=Warna.BG_INPUT, border_color=Warna.BORDER,
                                      text_color=Warna.TEXT_MAIN, font=f_body(13))
        self.ent_nama.pack(pady=(4, 14))

        ctk.CTkLabel(self.card, text="ALAMAT EMAIL AKTIF", font=f_label(11), text_color=Warna.TEXT_SUB).pack(anchor="w", padx=46)
        self.ent_mail = ctk.CTkEntry(self.card, width=408, height=40, corner_radius=10,
                                      fg_color=Warna.BG_INPUT, border_color=Warna.BORDER,
                                      text_color=Warna.TEXT_MAIN, font=f_body(13))
        self.ent_mail.pack(pady=(4, 14))

        ctk.CTkLabel(self.card, text="NOMOR KONTAK WHATSAPP", font=f_label(11), text_color=Warna.TEXT_SUB).pack(anchor="w", padx=46)
        self.ent_telp = ctk.CTkEntry(self.card, width=408, height=40, corner_radius=10,
                                      fg_color=Warna.BG_INPUT, border_color=Warna.BORDER,
                                      text_color=Warna.TEXT_MAIN, font=f_body(13))
        self.ent_telp.pack(pady=(4, 22))

        btn = ctk.CTkButton(self.card, text="Simpan Perubahan Profil", width=408, height=44, corner_radius=11,
                             font=f_body(14, bold=True), fg_color=Warna.PRIMARY, hover_color=Warna.PRIMARY_HOVER,
                             command=self.simpan)
        btn.pack()

    def muat_ulang_sesi(self):
        nama_user = self.master_dashboard.controller.session_user["nama"]
        email_user = self.master_dashboard.controller.session_user["email"]
        telp_user = self.master_dashboard.controller.session_user["telp"]

        self.lbl_header.configure(text=nama_user)

        self.ent_nama.delete(0, 'end')
        self.ent_nama.insert(0, nama_user)

        self.ent_mail.delete(0, 'end')
        self.ent_mail.insert(0, email_user)

        self.ent_telp.delete(0, 'end')
        self.ent_telp.insert(0, telp_user)

    def simpan(self):
        username_aktif = self.master_dashboard.controller.session_user["username"]
        nama_baru = self.ent_nama.get().strip()
        email_baru = self.ent_mail.get().strip()
        telp_baru = self.ent_telp.get().strip()

        if nama_baru == "" or email_baru == "" or telp_baru == "":
            messagebox.showwarning("Peringatan", "Semua kolom profil wajib diisi!")
            return

        users_data = muat_semua_user()
        if username_aktif in users_data:
            users_data[username_aktif]["nama_lengkap"] = nama_baru
            users_data[username_aktif]["email"] = email_baru
            users_data[username_aktif]["telp"] = telp_baru

            if simpan_semua_user(users_data):
                self.master_dashboard.controller.session_user["nama"] = nama_baru
                self.master_dashboard.controller.session_user["email"] = email_baru
                self.master_dashboard.controller.session_user["telp"] = telp_baru

                self.lbl_header.configure(text=nama_baru)
                messagebox.showinfo("Sukses", "Profil Anda berhasil diperbarui di dalam database.")
            else:
                messagebox.showerror("Error", "Gagal menyimpan perubahan ke database internal.")


# ==============================================================================
# SUB-PAGE E: KELUAR APLIKASI (LOGOUT)
# ==============================================================================
class SubPageLogout(ctk.CTkFrame):
    def __init__(self, parent, master_dashboard):
        super().__init__(parent, fg_color=Warna.BG_APP)
        self.master_dashboard = master_dashboard

        box = buat_kartu_bayangan(self, width=400, height=260, corner_radius=20)

        badge = ctk.CTkFrame(box, width=56, height=56, corner_radius=16, fg_color=("#fdecec", "#2a1416"))
        badge.pack(pady=(28, 10))
        badge.pack_propagate(False)
        ctk.CTkLabel(badge, text="🚪", font=ctk.CTkFont(size=24)).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(box, text="Konfirmasi Keluar", font=f_title(17), text_color=Warna.TEXT_MAIN).pack()
        ctk.CTkLabel(box, text="Apakah Anda yakin ingin keluar dari sistem?", text_color=Warna.TEXT_SUB,
                     font=f_subtitle(12)).pack(pady=(4, 22))

        btn_frame = ctk.CTkFrame(box, fg_color="transparent")
        btn_frame.pack()

        ctk.CTkButton(btn_frame, text="Batal", width=110, height=38, corner_radius=10,
                      fg_color=Warna.ACCENT_GRAY, hover_color=Warna.ACCENT_GRAY_H, font=f_body(13, bold=True),
                      command=lambda: self.master_dashboard.ganti_sub_halaman("SubPageDestinasi")).pack(side="left", padx=8)
        ctk.CTkButton(btn_frame, text="Keluar Sesi", width=110, height=38, corner_radius=10,
                      fg_color=Warna.ACCENT_RED, hover_color=Warna.ACCENT_RED_H, font=f_body(13, bold=True),
                      command=self.eksekusi_logout).pack(side="left", padx=8)

    def eksekusi_logout(self):
        self.master_dashboard.controller.session_user = {"username": "", "nama": "", "email": "", "telp": ""}
        self.master_dashboard.controller.tampilkan_halaman("PageLogin")
        self.master_dashboard.ganti_sub_halaman("SubPageDestinasi")


# ==============================================================================
# DRIVER CODE RUNNER
# ==============================================================================
if __name__ == "__main__":
    app = AplikasiUtama()
    app.mainloop()