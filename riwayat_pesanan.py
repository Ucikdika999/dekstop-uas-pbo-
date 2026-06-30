import customtkinter as ctk
from tkinter import messagebox

class PageRiwayatTiket(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, fg_color=("#f1f5f9", "#0f172a"))
        self.controller = controller

        # ==============================================================================
        # 1. HEADER HALAMAN
        # ==============================================================================
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=35, pady=(30, 15))
        
        # Sisi Kiri: Judul dan Subtitle Berwarna Biru Soft
        frame_title = ctk.CTkFrame(header_frame, fg_color="transparent")
        frame_title.pack(side="left", fill="both", expand=True)
        
        txt_title = ctk.CTkLabel(
            frame_title, 
            text="📋 Riwayat Kunjungan & Tiket", 
            font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
            text_color=("#0f172a", "#f8fafc")
        )
        txt_title.pack(anchor="w", pady=(0, 2))
        
        txt_sub = ctk.CTkLabel(
            frame_title, 
            text="Daftar log manifest pemesanan tiket masuk pariwisata terintegrasi Anda.", 
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=("#64748b", "#94a3b8")
        )
        txt_sub.pack(anchor="w")

        # ==============================================================================
        # 2. BARIS ATAS: INDIKATOR STATISTIK LOG (4 CARD SEJAJAR)
        # ==============================================================================
        stats_container = ctk.CTkFrame(self, fg_color="transparent")
        stats_container.pack(fill="x", padx=35, pady=10)
        stats_container.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="equal")

        self.buat_card_log(stats_container, 0, "Total Pemesanan", "24", "Semua waktu", "#5a51e6", "#edf2ff")
        self.buat_card_log(stats_container, 1, "Selesai", "18", "75% dari total", "#10b981", "#e6f4ea")
        self.buat_card_log(stats_container, 2, "Pending", "3", "12.5% dari total", "#f59e0b", "#fef3c7")
        self.buat_card_log(stats_container, 3, "Expired", "3", "12.5% dari total", "#ef4444", "#fee2e2")

        # ==============================================================================
        # 3. KARTU UTAMA TABLE CONTAINER (TABEL DATA RIWAYAT)
        # ==============================================================================
        table_card = ctk.CTkFrame(self, fg_color=("#ffffff", "#1e293b"), corner_radius=20, border_width=1, border_color=("#e2e8f0", "#334155"))
        table_card.pack(fill="both", expand=True, padx=35, pady=(15, 30))

        # --- HEADER INTERNAL TABEL ---
        header_table = ctk.CTkFrame(table_card, fg_color=("#f8fafc", "#131b2e"), height=40, corner_radius=8)
        header_table.pack(fill="x", padx=20, pady=(20, 10))
        
        # Distribusi Kolom Tabel Sesuai Gambar Mockup
        cols = [
            ("KODE TIKET", 0.02), 
            ("TANGGAL KUNJUNGAN", 0.20), 
            ("DESTINASI WISATA", 0.40), 
            ("JUMLAH", 0.68), 
            ("TOTAL BAYAR", 0.78), 
            ("STATUS", 0.90)
        ]
        for text, relx in cols:
            lbl = ctk.CTkLabel(header_table, text=text, font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), text_color="#64748b")
            lbl.place(relx=relx, rely=0.5, anchor="w")

        # ==============================================================================
        # DATA SINKRON: Menggunakan data tujuan barumu (Karimunjawa & Tasikmadu)
        # ==============================================================================
        data_riwayat = [
            {"kode": "TKT-09823", "inv": "INV/2026/0605/001", "tgl": "05 Juni 2026", "hari": "Jumat", "wisata": "Agrowisata Tasikmadu", "lokasi": "Karanganyar, Jawa Tengah", "qty": "3 Tiket", "total": "Rp 60.000", "status": "LUNAS", "bg_s": "#e6f4ea", "fg_s": "#137333"},
            {"kode": "TKT-09822", "inv": "INV/2026/0602/002", "tgl": "02 Juni 2026", "hari": "Selasa", "wisata": "Karimunjawa", "lokasi": "Jepara, Jawa Tengah", "qty": "2 Tiket", "total": "Rp 500.000", "status": "LUNAS", "bg_s": "#e6f4ea", "fg_s": "#137333"},
            {"kode": "TKT-09821", "inv": "INV/2026/0528/003", "tgl": "28 Mei 2026", "hari": "Kamis", "wisata": "Solo Safari", "lokasi": "Surakarta, Jawa Tengah", "qty": "1 Tiket", "total": "Rp 45.000", "status": "PENDING", "bg_s": "#fef3c7", "fg_s": "#b45309"},
            {"kode": "TKT-09815", "inv": "INV/2026/0515/004", "tgl": "15 Mei 2026", "hari": "Jumat", "wisata": "Candi Borobudur", "lokasi": "Magelang, Jawa Tengah", "qty": "5 Tiket", "total": "Rp 250.000", "status": "EXPIRED", "bg_s": "#fee2e2", "fg_s": "#b91c1c"}
        ]

        # Me-render baris data ke dalam tabel
        for item in data_riwayat:
            self.buat_baris_tabel(table_card, item)

    def buat_card_log(self, parent, col, title, value, sub, color, bg_color):
        """Membuat komponen kotak indikator status ringkasan di atas tabel"""
        card = ctk.CTkFrame(parent, fg_color=("#ffffff", "#1e293b"), corner_radius=16, border_width=1, border_color=("#e2e8f0", "#334155"))
        card.grid(row=0, column=col, padx=8, pady=5, sticky="nsew")
        
        # Indikator warna kecil di pojok kiri atas card
        badge_dot = ctk.CTkFrame(card, width=12, height=12, corner_radius=6, fg_color=color)
        badge_dot.place(x=15, y=15)

        lbl_val = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"), text_color=("#0f172a", "#f8fafc"))
        lbl_val.place(x=15, y=32)

        lbl_tit = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), text_color=("#334155", "#cbd5e1"))
        lbl_tit.place(x=60, y=10)

        lbl_sub = ctk.CTkLabel(card, text=sub, font=ctk.CTkFont(family="Segoe UI", size=11), text_color="#64748b")
        lbl_sub.place(x=60, y=32)

    def buat_baris_tabel(self, parent, data):
        """Membuat baris record data pesanan tiket secara rapi"""
        row = ctk.CTkFrame(parent, fg_color="transparent", height=60)
        row.pack(fill="x", padx=20, pady=4)

        # 1. Kode Tiket & Invoice
        frame_kode = ctk.CTkFrame(row, fg_color="transparent")
        frame_kode.place(relx=0.02, rely=0.5, anchor="w")
        ctk.CTkLabel(frame_kode, text=data["kode"], font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), text_color="#5a51e6").pack(anchor="w")
        ctk.CTkLabel(frame_kode, text=data["inv"], font=ctk.CTkFont(family="Segoe UI", size=10), text_color="#94a3b8").pack(anchor="w")

        # 2. Tanggal Kunjungan
        frame_tgl = ctk.CTkFrame(row, fg_color="transparent")
        frame_tgl.place(relx=0.20, rely=0.5, anchor="w")
        ctk.CTkLabel(frame_tgl, text=data["tgl"], font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), text_color=("#0f172a", "#f8fafc")).pack(anchor="w")
        ctk.CTkLabel(frame_tgl, text=data["hari"], font=ctk.CTkFont(family="Segoe UI", size=11), text_color="#64748b").pack(anchor="w")

        # 3. Nama Destinasi Wisata
        frame_wisata = ctk.CTkFrame(row, fg_color="transparent")
        frame_wisata.place(relx=0.40, rely=0.5, anchor="w")
        ctk.CTkLabel(frame_wisata, text=data["wisata"], font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), text_color=("#0f172a", "#f8fafc")).pack(anchor="w")
        ctk.CTkLabel(frame_wisata, text=f"📍 {data['lokasi']}", font=ctk.CTkFont(family="Segoe UI", size=11), text_color="#64748b").pack(anchor="w")

        # 4. Jumlah Tiket
        ctk.CTkLabel(row, text=data["qty"], font=ctk.CTkFont(family="Segoe UI", size=12), text_color=("#475569", "#cbd5e1")).place(relx=0.68, rely=0.5, anchor="w")

        # 5. Total Bayar
        frame_bayar = ctk.CTkFrame(row, fg_color="transparent")
        frame_bayar.place(relx=0.78, rely=0.5, anchor="w")
        ctk.CTkLabel(frame_bayar, text=data["total"], font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), text_color=("#0f172a", "#f8fafc")).pack(anchor="w")
        ctk.CTkLabel(frame_bayar, text="💳 QRIS", font=ctk.CTkFont(family="Segoe UI", size=10), text_color="#64748b").pack(anchor="w")

        # 6. Badge Status Cetak
        badge_status = ctk.CTkLabel(
            row, text=data["status"], 
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"), 
            fg_color=data["bg_s"], text_color=data["fg_s"], 
            corner_radius=6, width=75, height=24
        )
        badge_status.place(relx=0.90, rely=0.5, anchor="w")

        # Garis pembatas tipis antar baris biar elegan
        separator = ctk.CTkFrame(parent, fg_color=("#f1f5f9", "#334155"), height=1)
        separator.pack(fill="x", padx=20, pady=2)


# ==============================================================================
# --- BLOK TESTING MANDIRI HALAMAN RIWAYAT TIKET
# ==============================================================================
if __name__ == "__main__":
    ctk.set_appearance_mode("Light")
    
    root = ctk.CTk()
    root.title("Menu Riwayat Sistem Tiket & Tracking")
    root.geometry("1100x700")
    
    frame_riwayat = PageRiwayatTiket(parent=root)
    frame_riwayat.pack(fill="both", expand=True)
    
    root.mainloop()