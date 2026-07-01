import customtkinter as ctk
from tkinter import messagebox

# ==========================================
# 1. CLASS UTAMA (CONTROLLER / ROOT WINDOW)
# ==========================================
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Aplikasi UAS PBO")
        self.geometry("500x600")
        
        # Container untuk menampung semua halaman
        self.container = ctk.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Dictionary untuk menyimpan semua frame halaman
        self.frames = {}
        
        # Daftarkan semua halaman yang ada di sini
        for F in (PageLogin, PageRegister, PageDashboardUtama):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            # Letakkan semua halaman di posisi grid yang sama (bertumpuk)
            frame.grid(row=0, column=0, sticky="nsew")
            
        # Tampilkan halaman pertama kali (Login)
        self.show_frame("PageLogin")
        
    def show_frame(self, page_name):
        """Fungsi untuk mengangkat halaman ke paling depan"""
        frame = self.frames[page_name]
        frame.tkraise()

# ==========================================
# 2. HALAMAN LOGIN
# ==========================================
class PageLogin(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller 
        
        self.configure(fg_color=("#f8fafc", "#0f172a"))
        
        lbl_title = ctk.CTkLabel(self, text="Selamat Datang Kembali", font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"))
        lbl_title.pack(pady=(100, 20))
        
        self.entry_username = ctk.CTkEntry(self, placeholder_text="Masukkan Username", width=300, height=40)
        self.entry_username.pack(pady=10)
        
        self.entry_password = ctk.CTkEntry(self, placeholder_text="Masukkan Password", show="*", width=300, height=40)
        self.entry_password.pack(pady=10)
        
        self.btn_login = ctk.CTkButton(self, text="Login", width=300, height=42, font=ctk.CTkFont(weight="bold"), command=self.proses_login)
        self.btn_login.pack(pady=(20, 10))
        
        self.btn_ke_register = ctk.CTkButton(self, text="Belum punya akun? Daftar disini", fg_color="transparent", text_color="#2563eb", hover_color=("#e2e8f0", "#1e293b"), command=lambda: self.controller.show_frame("PageRegister"))
        self.btn_ke_register.pack()

    def proses_login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        if username == "usyikkk" and password == "123":
            # Update nama user di dashboard sebelum pindah halaman
            dashboard = self.controller.frames["PageDashboardUtama"]
            if hasattr(dashboard, "lbl_user"):
                dashboard.lbl_user.configure(text=f"Halo, {username}! Selamat Liburan.")
                
            self.controller.show_frame("PageDashboardUtama")
        else:
            messagebox.showerror("Login Gagal", "Username atau Password yang anda masukkan salah!")

# ==========================================
# 3. HALAMAN REGISTER
# ==========================================
class PageRegister(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color=("#f8fafc", "#0f172a"))
        
        lbl_title = ctk.CTkLabel(self, text="Buat Akun Baru", font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"))
        lbl_title.pack(pady=(100, 20))
        
        self.entry_user_reg = ctk.CTkEntry(self, placeholder_text="Buat Username", width=300, height=40)
        self.entry_user_reg.pack(pady=10)
        
        self.entry_pass_reg = ctk.CTkEntry(self, placeholder_text="Buat Password", show="*", width=300, height=40)
        self.entry_pass_reg.pack(pady=10)
        
        btn_register = ctk.CTkButton(self, text="Daftar Sekarang", width=300, height=42, command=self.proses_register)
        btn_register.pack(pady=(20, 10))
        
        btn_ke_login = ctk.CTkButton(self, text="Sudah punya akun? Login", fg_color="transparent", text_color="#2563eb", command=lambda: self.controller.show_frame("PageLogin"))
        btn_ke_login.pack()

    def proses_register(self):
        messagebox.showinfo("Registrasi", "Akun berhasil dibuat! Silakan login.")
        self.controller.show_frame("PageLogin") 

# ==========================================
# 4. HALAMAN DASHBOARD (DUMMY)
# ==========================================
class PageDashboardUtama(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color=("#f8fafc", "#0f172a"))
        
        # Label ini nanti teksnya akan diubah dinamis lewat proses_login
        self.lbl_user = ctk.CTkLabel(self, text="Halo, User!", font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"))
        self.lbl_user.pack(pady=(150, 20))
        
        btn_logout = ctk.CTkButton(self, text="Logout", fg_color="#ef4444", hover_color="#dc2626", command=lambda: self.controller.show_frame("PageLogin"))
        btn_logout.pack()

# ==========================================
# 5. MENJALANKAN APLIKASI
# ==========================================
if __name__ == "__main__":
    app = App()
    app.mainloop()