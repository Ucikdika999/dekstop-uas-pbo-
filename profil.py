import customtkinter as ctk
from tkinter import messagebox

class PageProfilAkun(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        # Latar belakang menggunakan warna cerah yang bersih (Light mode) dan slate modern (Dark mode)
        super().__init__(parent, fg_color=("#f8fafc", "#0f172a"))
        self.controller = controller
        
        # Desain Card Box Tengah untuk wadah Data Profil Pengguna (Lebih Elegan)
        self.card = ctk.CTkFrame(
            self, 
            width=500, 
            height=540, 
            corner_radius=24,
            fg_color=("#ffffff", "#1e293b"),
            border_width=1,
            border_color=("#e2e8f0", "#334155")
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.pack_propagate(False)
        
        # ==============================================================================
        # 1. AVATAR & IDENTITAS ATAS
        # ==============================================================================
        avatar_bg = ctk.CTkFrame(self.card, width=100, height=100, corner_radius=50, fg_color=("#e0f2fe", "#0369a1"))
        avatar_bg.pack(pady=(35, 12))
        avatar_bg.pack_propagate(False)
        
        lbl_avatar = ctk.CTkLabel(avatar_bg, text="👩‍💻", font=ctk.CTkFont(size=50))
        lbl_avatar.place(relx=0.5, rely=0.5, anchor="center")
        
        self.lbl_nama_header = ctk.CTkLabel(
            self.card, 
            text="Alfina Putri", 
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color=("#0f172a", "#f8fafc")
        )
        self.lbl_nama_header.pack()
        
        lbl_role = ctk.CTkLabel(
            self.card, 
            text="Premium Member • Terverifikasi", 
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="normal"), 
            text_color="#10b981"
        )
        lbl_role.pack(pady=(2, 25))
        
        # Container Form agar simetris di tengah card
        form_container = ctk.CTkFrame(self.card, fg_color="transparent")
        form_container.pack(fill="x", padx=50)
        
        # ==============================================================================
        # 2. INPUT DATA FORM
        # ==============================================================================
        ctk.CTkLabel(form_container, text="Nama Lengkap", font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), text_color=("#475569", "#cbd5e1")).pack(anchor="w")
        self.ent_nama = ctk.CTkEntry(form_container, height=40, corner_radius=12, fg_color=("#f8fafc", "#0f172a"), border_color=("#e2e8f0", "#475569"))
        self.ent_nama.pack(fill="x", pady=(2, 14))
        self.ent_nama.insert(0, "Alfina Putri")
        
        ctk.CTkLabel(form_container, text="Alamat Email", font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), text_color=("#475569", "#cbd5e1")).pack(anchor="w")
        self.ent_email = ctk.CTkEntry(form_container, height=40, corner_radius=12, fg_color=("#f8fafc", "#0f172a"), border_color=("#e2e8f0", "#475569"))
        self.ent_email.pack(fill="x", pady=(2, 25))
        self.ent_email.insert(0, "alfina.putri@university.ac.id")
        
        # ==============================================================================
        # 3. TOMBOL AKSI
        # ==============================================================================
        self.btn_simpan = ctk.CTkButton(
            self.card, 
            text="💾  Simpan Perubahan Profil", 
            width=400, 
            height=44,
            corner_radius=12,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            fg_color="#2563eb",       
            text_color="white",
            hover_color="#1d4ed8",
            command=self.aksi_simpan_profil
        )
        self.btn_simpan.pack(pady=(10, 0))

    def aksi_simpan_profil(self):
        """Fungsi PBO untuk membaca inputan baru dan menyimpannya"""
        nama_baru = self.ent_nama.get().strip()
        email_baru = self.ent_email.get().strip()
        
        if nama_baru == "" or email_baru == "":
            messagebox.showwarning("Peringatan", "Nama dan Email tidak boleh dikosongkan!")
            return
            
        self.lbl_nama_header.configure(text=nama_baru)
        messagebox.showinfo("Sukses", f"Profil atas nama {nama_baru} berhasil diperbarui!")


# PERBAIKAN UTAMA: Blok di bawah ini dipastikan menempel ke pinggir paling kiri (tanpa spasi/tab)
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Testing Halaman Profil")
    root.geometry("800x650")
    
    ctk.set_appearance_mode("Light")  
    ctk.set_default_color_theme("blue") 
    
    tampilan_profil = PageProfilAkun(parent=root)
    tampilan_profil.pack(fill="both", expand=True)
    
    root.mainloop()