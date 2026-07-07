import customtkinter as ctk
from tkinter import messagebox

# ==============================================================================
# FRAME HALAMAN: DESTINASI WISATA
# Desain ini DISAMAKAN dengan class PageDestinasi di mainbaruuaspbo.py
# (Kartu grid 2 kolom + progress bar kuota, bukan lagi layout icon lingkaran)
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