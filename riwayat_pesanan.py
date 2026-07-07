import customtkinter as ctk
from tkinter import messagebox

# ==============================================================================
# FRAME HALAMAN: RIWAYAT PESANAN
# Desain ini DISAMAKAN dengan class PageRiwayatTiket di mainbaruuaspbo.py
# (Tabel sederhana 6 kolom, tanpa kartu statistik 4-kolom di atasnya)
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