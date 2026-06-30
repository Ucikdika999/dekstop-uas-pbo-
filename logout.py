import customtkinter as ctk
from tkinter import messagebox

class PageLogout(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        # Background dasar mengikuti tema aplikasi (Light/Dark mode)
        super().__init__(parent, fg_color=("#f1f5f9", "#0f172a"))
        self.controller = controller
        
        # Desain Card Konfirmasi di Tengah Layar
        self.card = ctk.CTkFrame(
            self, 
            width=450, 
            height=320, 
            corner_radius=20,
            fg_color=("#ffffff", "#1e293b"),
            border_width=1,
            border_color=("#e2e8f0", "#334155")
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.pack_propagate(False)
        
        # ==============================================================================
        # 1. ICON & TEKS PERINGATAN
        # ==============================================================================
        lbl_icon = ctk.CTkLabel(self.card, text="🚪", font=ctk.CTkFont(size=50))
        lbl_icon.pack(pady=(35, 10))
        
        lbl_title = ctk.CTkLabel(
            self.card, 
            text="Konfirmasi Keluar", 
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color=("#0f172a", "#f8fafc")
        )
        lbl_title.pack()
        
        lbl_desc = ctk.CTkLabel(
            self.card, 
            text="Apakah Anda yakin ingin keluar dari sesi aplikasi desktop ini?", 
            font=ctk.CTkFont(size=12),
            text_color=("#64748b", "#94a3b8")
        )
        lbl_desc.pack(pady=(5, 30))
        
        # ==============================================================================
        # 2. TOMBOL AKSI (Batal vs Keluar)
        # ==============================================================================
        btn_container = ctk.CTkFrame(self.card, fg_color="transparent")
        btn_container.pack(fill="x", padx=40)
        
        # Tombol Batal (Tetap di aplikasi)
        self.btn_batal = ctk.CTkButton(
            btn_container, 
            text="Batal", 
            width=170, 
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            fg_color=("#e2e8f0", "#334155"),       
            text_color=("#0f172a", "#f8fafc"),
            hover_color=("#cbd5e1", "#475569"),
            command=self.aksi_batal
        )
        self.btn_batal.pack(side="left", padx=(0, 10))
        
        # Tombol Keluar (Proses Logout)
        self.btn_keluar = ctk.CTkButton(
            btn_container, 
            text="Ya, Keluar", 
            width=170, 
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            fg_color="#ef4444", # Warna merah tegas untuk aksi destruktif       
            text_color="white",
            hover_color="#dc2626",
            command=self.aksi_logout
        )
        self.btn_keluar.pack(side="right")

    def aksi_batal(self):
        """Kembali ke dashboard utama jika user membatalkan logout"""
        if self.controller:
            # Ganti 'PageDashboard' sesuai dengan nama class dashboard utama kamu
            self.controller.show_frame("PageDashboard")
        else:
            messagebox.showinfo("Info", "Kembali ke Dashboard Utama.")

    def aksi_logout(self):
        """Eksekusi pembersihan sesi dan penutupan aplikasi"""
        messagebox.showinfo("Logout Berhasil", "Sesi Anda telah dihapus secara aman. Sampai jumpa!")
        
        # Menutup aplikasi secara bersih
        self.quit()


# --- BLOK TESTING MANDIRI ---
if __name__ == "__main__":
    ctk.set_appearance_mode("System")  
    ctk.set_default_color_theme("blue") 
    
    root = ctk.CTk()
    root.title("Sistem Otentikasi & Logout")
    root.geometry("850x650")
    
    logout_frame = PageLogout(parent=root)
    logout_frame.pack(fill="both", expand=True)
    
    root.mainloop()