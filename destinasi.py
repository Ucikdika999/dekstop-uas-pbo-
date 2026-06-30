import customtkinter as ctk
from tkinter import messagebox

class PageDestinasi(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller=None):
        # Menggunakan latar belakang abu-biru super cerah/bersih mirip gambar referensi
        super().__init__(parent, fg_color=("#f1f5f9", "#0f172a")) 
        self.controller = controller
        
        # ==============================================================================
        # 1. HEADER HALAMAN
        # ==============================================================================
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=35, pady=(30, 15))
        
        txt_title = ctk.CTkLabel(
            header_frame, 
            text="Destinasi Wisata & Live Kuota", 
            font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
            text_color=("#0f172a", "#f8fafc")
        )
        txt_title.pack(anchor="w", pady=(0, 2))
        
        txt_sub = ctk.CTkLabel(
            header_frame, 
            text="Pantau kapasitas sisa kuota tempat pelacakan wisata secara real-time.", 
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=("#64748b", "#94a3b8")
        )
        txt_sub.pack(anchor="w")

        # ==============================================================================
        # 2. DATA UTAMA DESTINASI
        # ==============================================================================
        self.DATA_DESTINASI = [
            {"nama": "Candi Borobudur", "harga": 50000, "kuota": 15, "icon": "🛕", "lokasi": "Magelang, Jawa Tengah", "badge": "Sisa Sedikit!"},
            {"nama": "Solo Safari", "harga": 45000, "kuota": 120, "icon": "🦁", "lokasi": "Surakarta, Jawa Tengah", "badge": "Populer"},
            {"nama": "Agrowisata Tasikmadu", "harga": 20000, "kuota": 200, "icon": "🚂", "lokasi": "Karanganyar, Jawa Tengah", "badge": "Edukasi"},
            {"nama": "Saloka Theme Park", "harga": 120000, "kuota": 45, "icon": "🎡", "lokasi": "Semarang, Jawa Tengah", "badge": "Favorit"},
            {"nama": "Karimunjawa", "harga": 250000, "kuota": 8, "icon": "🏖️", "lokasi": "Jepara, Jawa Tengah", "badge": "Sisa Sedikit!"}
        ]

        # Container Grid kartu-kartu
        self.grid_container = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_container.pack(fill="x", expand=True, padx=35, pady=10)
        
        self.grid_container.grid_columnconfigure(0, weight=1)
        self.grid_container.grid_columnconfigure(1, weight=1)

        for index, destinasi in enumerate(self.DATA_DESTINASI):
            row_idx = index // 2
            col_idx = index % 2
            self.buat_kartu_destinasi(self.grid_container, destinasi, row_idx, col_idx)

        # ==============================================================================
        # 3. SUMMARY FOOTER (STATISTIK DENGAN WARNA WARNI MATCHING)
        # ==============================================================================
        self.buat_summary_footer()

    def buat_kartu_destinasi(self, parent, data, row, col):
        """Membuat kartu destinasi horizontal dengan warna akurat sesuai gambar"""
        # Card Base (Putih bersih)
        card = ctk.CTkFrame(
            parent,
            fg_color=("#ffffff", "#1e293b"),
            corner_radius=20,
            border_width=1,
            border_color=("#e2e8f0", "#334155")
        )
        card.grid(row=row, column=col, padx=12, pady=12, sticky="nsew")

        card.grid_columnconfigure(0, weight=0)
        card.grid_columnconfigure(1, weight=1)
        card.grid_rowconfigure(0, weight=1)

        # ----------------------------------------------------------------------
        # AREA KIRI: Lingkaran/Kotak Icon Lembut + Badge (Persis Gambar)
        # ----------------------------------------------------------------------
        # Menggunakan warna soft blue-purple (#edf2ff) untuk background icon
        frame_visual = ctk.CTkFrame(card, width=130, fg_color=("#edf2ff", "#131b2e"), corner_radius=16)
        frame_visual.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        frame_visual.pack_propagate(False)

        # Logika Warna Badge Kiri Atas Kartu
        if data["kuota"] <= 15:
            warna_badge = "#ef4444" # Merah cerah
        elif data["badge"] == "Populer":
            warna_badge = "#4f46e5" # Indigo tua
        else:
            warna_badge = "#f59e0b" # Oranye/Amber ("Favorit")
            
        lbl_badge = ctk.CTkLabel(
            frame_visual, 
            text=data["badge"].upper(),
            font=ctk.CTkFont(family="Segoe UI", size=9, weight="bold"),
            fg_color=warna_badge,
            text_color="white",
            corner_radius=6
        )
        lbl_badge.pack(pady=(12, 0), padx=8, fill="x")

        # Lingkaran putih kecil pelapis icon tengah (efek bayangan lingkaran di gambar)
        bg_lingkaran = ctk.CTkFrame(frame_visual, width=54, height=54, corner_radius=27, fg_color=("#ffffff", "#1e293b"))
        bg_lingkaran.place(relx=0.5, rely=0.6, anchor="center")
        
        lbl_icon = ctk.CTkLabel(bg_lingkaran, text=data["icon"], font=ctk.CTkFont(size=26))
        lbl_icon.place(relx=0.5, rely=0.5, anchor="center")

        # ----------------------------------------------------------------------
        # AREA KANAN: Informasi Detail & Tombol Transaksi
        # ----------------------------------------------------------------------
        frame_info = ctk.CTkFrame(card, fg_color="transparent")
        frame_info.grid(row=0, column=1, padx=(5, 20), pady=20, sticky="nsew")

        # Nama Tempat Wisata (Warna gelap bold)
        lbl_nama = ctk.CTkLabel(
            frame_info, 
            text=data["nama"], 
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            text_color=("#0f172a", "#f8fafc")
        )
        lbl_nama.pack(anchor="w")

        # Lokasi Muted Gray
        lbl_lokasi = ctk.CTkLabel(
            frame_info, 
            text=f"📍 {data['lokasi']}", 
            font=ctk.CTkFont(family="Segoe UI", size=11), 
            text_color="#64748b"
        )
        lbl_lokasi.pack(anchor="w", pady=(1, 6))

        # Komponen Harga Tiket (Warna Biru Indigo #4f46e5 sesuai mockup)
        lbl_harga = ctk.CTkLabel(
            frame_info, 
            text=f"Harga: Rp {data['harga']:,}".replace(",", "."), 
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color="#4f46e5"
        )
        lbl_harga.pack(anchor="w", pady=(0, 4))

        # Logika Live Indikator Kuota (Teks disesuaikan warna indikator status)
        if data["kuota"] > 100:
            warna_kuota = "#10b981" # Hijau emerald
            status_kuota = f"🟢 Kuota Melimpah\n    {data['kuota']} Tersedia"
        elif data["kuota"] > 30:
            warna_kuota = "#d97706" # Oranye gelap
            status_kuota = f"🟡 Kuota Terbatas\n    {data['kuota']} Tersisa"
        else:
            warna_kuota = "#ef4444" # Merah
            status_kuota = f"🔴 Sisa Sedikit!\n    {data['kuota']} Slot Tersisa"
        
        lbl_kuota = ctk.CTkLabel(
            frame_info, 
            text=status_kuota, 
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), 
            text_color=warna_kuota,
            justify="left"
        )
        lbl_kuota.pack(anchor="w", pady=(0, 10))

        # Tombol Pemesanan Tiket (Menggunakan warna Ungu/Indigo Unggul #5a51e6 & Hover #4338ca)
        btn_booking = ctk.CTkButton(
            frame_info,
            text="Pesan",
            width=95,
            height=34,
            corner_radius=10,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color="#5a51e6", 
            text_color="white",
            hover_color="#4338ca",
            command=lambda nama_wst=data["nama"]: self.aksi_pesan_cepat(nama_wst)
        )
        btn_booking.pack(anchor="e", pady=(2, 0))

    def buat_summary_footer(self):
        """Membuat bagian baris summary bawah agar match gradasi warnanya"""
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.pack(fill="x", padx=35, pady=(15, 35))
        
        total_destinasi = len(self.DATA_DESTINASI)
        total_kuota = sum(d["kuota"] for d in self.DATA_DESTINASI)

        # Card ringkasan bawah warna putih bersih bergaris tipis
        summary_card = ctk.CTkFrame(footer_frame, fg_color=("#ffffff", "#1e293b"), corner_radius=16, border_width=1, border_color=("#e2e8f0", "#334155"))
        summary_card.pack(fill="x", ipady=12)

        lbl_summary_text = ctk.CTkLabel(
            summary_card,
            text=f"📊   Total Destinasi Terdaftar: {total_destinasi} Wisata   |   Total Live Kuota Aktif: {total_kuota} Slot Tersedia",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="normal"),
            text_color=("#475569", "#cbd5e1")
        )
        lbl_summary_text.pack(side="left", padx=20)

    def aksi_pesan_cepat(self, nama_wisata):
        if self.controller:
            self.controller.show_frame("PagePesanTiket")
        else:
            messagebox.showinfo("Navigasi Pemesanan", f"Membuka modul pemesanan tiket untuk destinasi: {nama_wisata}")


# ==============================================================================
# --- BLOK TESTING MANDIRI
# ==============================================================================
if __name__ == "__main__":
    ctk.set_appearance_mode("Light") 
    
    root = ctk.CTk()
    root.title("Manajemen Modul Destinasi")
    root.geometry("1020x720")
    
    destinasi_frame = PageDestinasi(parent=root)
    destinasi_frame.pack(fill="both", expand=True)
    
    root.mainloop()