import customtkinter as ctk
from tkinter import messagebox
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ==============================================================================
# FRAME HALAMAN: DASHBOARD UTAMA
# Desain ini DISAMAKAN dengan class PageDashboardUtama di mainbaruuaspbo.py
# (Sidebar biru/putih elegan, kartu grafik tren, kartu destinasi terpopuler)
# ==============================================================================
class PageDashboardUtama(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, fg_color=("#f1f5f9", "#0f172a"))
        self.controller = controller

        # Header Area
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=35, pady=(30, 15))
        self.lbl_sambutan = ctk.CTkLabel(header_frame, text="Selamat datang kembali! 👋", font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"))
        self.lbl_sambutan.pack(anchor="w")
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
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=(0, 10))

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
            ctk.CTkLabel(row, text=str(i + 1), font=ctk.CTkFont(size=12, weight="bold"), fg_color=("#edf2ff", "#131b2e"), text_color="#5a51e6", width=26, height=26, corner_radius=13).pack(side="left", padx=(0, 10))

            fd = ctk.CTkFrame(row, fg_color="transparent")
            fd.pack(side="left", fill="both", expand=True)
            ctk.CTkLabel(fd, text=f"{data['icon']} {data['nama']}", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w")
            ctk.CTkLabel(fd, text=data["lokasi"], font=ctk.CTkFont(size=11), text_color="#64748b").pack(anchor="w")
            ctk.CTkLabel(row, text=data["kunjungan"], font=ctk.CTkFont(size=12, weight="bold"), text_color="#475569").pack(side="right", padx=10)

    def refresh_data(self):
        """Dipanggil setiap kali halaman ini ditampilkan agar sapaan sesuai
        dengan username yang sedang login (bukan nama yang di-hardcode)."""
        username = getattr(self.controller, "username_aktif", None) or "Pengguna"
        self.lbl_sambutan.configure(text=f"Selamat datang kembali, {username}! 👋")