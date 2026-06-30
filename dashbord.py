import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PageDashboardUtama(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, fg_color=("#f1f5f9", "#0f172a"))
        self.controller = controller

        # ==============================================================================
        # 1. HEADER HALAMAN (SUDAH DIGANTI JADI USYIKKK)
        # ==============================================================================
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=35, pady=(30, 15))
        
        frame_welcome = ctk.CTkFrame(header_frame, fg_color="transparent")
        frame_welcome.pack(side="left", fill="both", expand=True)
        
        # TEXT UPDATE: Menggunakan nama usyikkk sesuai request
        txt_title = ctk.CTkLabel(
            frame_welcome, 
            text="Selamat datang kembali, usyikkk! 👋", 
            font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
            text_color=("#0f172a", "#f8fafc")
        )
        txt_title.pack(anchor="w", pady=(0, 2))
        
        txt_sub = ctk.CTkLabel(
            frame_welcome, 
            text="Berikut ringkasan statistik live tracking kuota dan transaksi tiket Anda hari ini.", 
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=("#64748b", "#94a3b8")
        )
        txt_sub.pack(anchor="w")

        # ==============================================================================
        # 2. BARIS ATAS: KARTU STATISTIK
        # ==============================================================================
        stats_container = ctk.CTkFrame(self, fg_color="transparent")
        stats_container.pack(fill="x", padx=35, pady=10)
        stats_container.grid_columnconfigure((0, 1, 2), weight=1, uniform="equal")

        self.buat_card_statistik(stats_container, 0, "Total Kunjungan", "1.240", "👥", "#2563eb", "↑ 12.5%", "#10b981")
        self.buat_card_statistik(stats_container, 1, "Sisa Kuota Live", "388", "🎟️", "#10b981", "↑ 5.3%", "#10b981")
        self.buat_card_statistik(stats_container, 2, "Total Transaksi", "Rp 850.000", "💳", "#f59e0b", "↑ 18.7%", "#10b981")

        # ==============================================================================
        # 3. BARIS TENGAH: RINGKASAN KATEGORI & DESTINASI TERPOPULER
        # ==============================================================================
        middle_container = ctk.CTkFrame(self, fg_color="transparent")
        middle_container.pack(fill="x", padx=35, pady=15)
        middle_container.grid_columnconfigure(0, weight=4, uniform="middle")
        middle_container.grid_columnconfigure(1, weight=5, uniform="middle")

        # --- SISI KIRI: Ringkasan Kategori ---
        chart_card = ctk.CTkFrame(middle_container, fg_color=("#ffffff", "#1e293b"), corner_radius=20, border_width=1, border_color=("#e2e8f0", "#334155"))
        chart_card.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        
        lbl_chart_title = ctk.CTkLabel(chart_card, text="Ringkasan Kategori", font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"), text_color=("#0f172a", "#f8fafc"))
        lbl_chart_title.pack(anchor="w", padx=20, pady=(15, 0))
        
        self.embed_donut_chart(chart_card)

        # --- SISI KANAN: Destinasi Terpopuler ---
        popular_card = ctk.CTkFrame(middle_container, fg_color=("#ffffff", "#1e293b"), corner_radius=20, border_width=1, border_color=("#e2e8f0", "#334155"))
        popular_card.grid(row=0, column=1, padx=(10, 0), sticky="nsew")
        
        lbl_pop_title = ctk.CTkLabel(popular_card, text="Destinasi Terpopuler", font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"), text_color=("#0f172a", "#f8fafc"))
        lbl_pop_title.pack(anchor="w", padx=20, pady=(15, 10))

        data_populer = [
            {"rank": "1", "nama": "Solo Safari", "lokasi": "Surakarta, DIY", "kunjungan": "420 Kunjungan", "icon": "🦁"},
            {"rank": "2", "nama": "Saloka Theme Park", "lokasi": "Semarang, Jawa Tengah", "kunjungan": "360 Kunjungan", "icon": "🎡"},
            {"rank": "3", "nama": "Candi Borobudur", "lokasi": "Magelang, Jawa Tengah", "kunjungan": "280 Kunjungan", "icon": "🛕"},
            {"rank": "4", "nama": "Karimunjawa", "lokasi": "Jepara, Jawa Tengah", "kunjungan": "180 Kunjungan", "icon": "🏖️"}
        ]
        
        for item in data_populer:
            self.buat_baris_populer(popular_card, item)

        # ==============================================================================
        # 4. BARIS BAWAH: TABEL TRANSAKSI TIKET TERBARU
        # ==============================================================================
        table_card = ctk.CTkFrame(self, fg_color=("#ffffff", "#1e293b"), corner_radius=20, border_width=1, border_color=("#e2e8f0", "#334155"))
        table_card.pack(fill="x", padx=35, pady=(10, 40))
        
        lbl_table_title = ctk.CTkLabel(table_card, text="📝 Transaksi Tiket Terbaru", font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"), text_color=("#0f172a", "#f8fafc"))
        lbl_table_title.pack(anchor="w", padx=20, pady=(15, 15))

        header_table = ctk.CTkFrame(table_card, fg_color=("#f8fafc", "#131b2e"), height=35, corner_radius=8)
        header_table.pack(fill="x", padx=20, pady=5)
        
        cols = [("ID Transaksi", 0.15), ("Destinasi", 0.35), ("Tiket", 0.15), ("Tanggal", 0.20), ("Status", 0.15)]
        for text, relx in cols:
            lbl = ctk.CTkLabel(header_table, text=text, font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), text_color="#64748b")
            lbl.place(relx=relx, rely=0.5, anchor="w")

        row_data = ctk.CTkFrame(table_card, fg_color="transparent", height=45)
        row_data.pack(fill="x", padx=20, pady=2)
        
        ctk.CTkLabel(row_data, text="TKT-00921", font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), text_color="#5a51e6").place(relx=0.0, rely=0.5, anchor="w")
        ctk.CTkLabel(row_data, text="🦁 Solo Safari (Surakarta)", font=ctk.CTkFont(family="Segoe UI", size=13), text_color=("#0f172a", "#f8fafc")).place(relx=0.15, rely=0.5, anchor="w")
        ctk.CTkLabel(row_data, text="2 Tiket Dewasa", font=ctk.CTkFont(family="Segoe UI", size=13), text_color="#475569").place(relx=0.5, rely=0.5, anchor="w")
        ctk.CTkLabel(row_data, text="22 Juni 2026", font=ctk.CTkFont(family="Segoe UI", size=13), text_color="#475569").place(relx=0.65, rely=0.5, anchor="w")
        
        badge_status = ctk.CTkLabel(row_data, text="Lunas", font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), fg_color="#e6f4ea", text_color="#137333", corner_radius=6, width=60, height=22)
        badge_status.place(relx=0.85, rely=0.5, anchor="w")

    def buat_card_statistik(self, parent, col, title, value, icon, icon_color, trend_text, trend_color):
        card = ctk.CTkFrame(parent, fg_color=("#ffffff", "#1e293b"), corner_radius=20, border_width=1, border_color=("#e2e8f0", "#334155"))
        card.grid(row=0, column=col, padx=10, pady=5, sticky="nsew")
        
        frame_text = ctk.CTkFrame(card, fg_color="transparent")
        frame_text.pack(side="left", padx=20, pady=20, fill="both", expand=True)
        
        lbl_title = ctk.CTkLabel(frame_text, text=title, font=ctk.CTkFont(family="Segoe UI", size=13), text_color="#64748b")
        lbl_title.pack(anchor="w")
        
        lbl_value = ctk.CTkLabel(frame_text, text=value, font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"), text_color=("#0f172a", "#f8fafc"))
        lbl_value.pack(anchor="w", pady=2)
        
        lbl_trend = ctk.CTkLabel(frame_text, text=trend_text, font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), text_color=trend_color)
        lbl_trend.pack(anchor="w")

        frame_icon_bg = ctk.CTkFrame(card, width=46, height=46, corner_radius=23, fg_color=(icon_color, icon_color))
        frame_icon_bg.pack(side="right", padx=20, anchor="center")
        frame_icon_bg.pack_propagate(False)
        
        lbl_icon = ctk.CTkLabel(frame_icon_bg, text=icon, font=ctk.CTkFont(size=20), text_color="white")
        lbl_icon.place(relx=0.5, rely=0.5, anchor="center")

    def embed_donut_chart(self, parent):
        labels = ['Solo Safari', 'Saloka', 'Borobudur', 'Lainnya']
        sizes = [38.7, 25.8, 19.4, 16.1]
        colors = ['#5a51e6', '#10b981', '#f59e0b', '#ef4444']
        
        fig, ax = plt.subplots(figsize=(3, 2.2), dpi=100)
        fig.patch.set_facecolor('none')
        ax.set_facecolor('none')
        
        wedges, texts = ax.pie(sizes, colors=colors, startangle=90, wedgeprops=dict(width=0.4, edgecolor='w', linewidth=2))
        ax.text(0, 0, 'Total\n1.240', ha='center', va='center', fontsize=11, weight='bold', color='#0f172a')
        ax.axis('equal')  
        
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(0, 10))
        canvas.draw()
        
        # Penutup proses background matplotlib agar bebas dari crash dpi_scaling
        plt.close(fig)

    def buat_baris_populer(self, parent, data):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=20, pady=6)
        
        lbl_rank = ctk.CTkLabel(row, text=data["rank"], font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), fg_color=("#edf2ff", "#131b2e"), text_color="#5a51e6", width=26, height=26, corner_radius=13)
        lbl_rank.pack(side="left", padx=(0, 10))
        
        frame_detail = ctk.CTkFrame(row, fg_color="transparent")
        frame_detail.pack(side="left", fill="both", expand=True)
        
        lbl_nama = ctk.CTkLabel(frame_detail, text=f"{data['icon']} {data['nama']}", font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), text_color=("#0f172a", "#f8fafc"))
        lbl_nama.pack(anchor="w")
        
        lbl_lok = ctk.CTkLabel(frame_detail, text=data["lokasi"], font=ctk.CTkFont(family="Segoe UI", size=11), text_color="#64748b")
        lbl_lok.pack(anchor="w")
        
        lbl_visit = ctk.CTkLabel(row, text=data["kunjungan"], font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), text_color=("#475569", "#cbd5e1"))
        lbl_visit.pack(side="right", padx=10)


# ==============================================================================
# --- BLOK TESTING MANDIRI DASHBOARD
# ==============================================================================
if __name__ == "__main__":
    ctk.set_appearance_mode("Light") 
    
    root = ctk.CTk()
    root.title("Sistem Tracking Wisata - Dashboard Cerah Elegan")
    root.geometry("1100x750") 
    
    dash_frame = PageDashboardUtama(parent=root)
    dash_frame.pack(fill="both", expand=True)
    
    root.mainloop()