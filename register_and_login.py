import customtkinter as ctk
from tkinter import messagebox

class PageLogin(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller # Menyimpan referensi pengendali utama
        
        # Pengaturan Tampilan Form Login
        self.configure(fg_color=("#f8fafc", "#0f172a"))
        
        # Judul
        lbl_title = ctk.CTkLabel(self, text="Selamat Datang Kembali", font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"))
        lbl_title.pack(pady=(100, 20))
        
        # Entry Username
        self.entry_username = ctk.CTkEntry(self, placeholder_text="Masukkan Username", width=300, height=40)
        self.entry_username.pack(pady=10)
        
        # Entry Password
        self.entry_password = ctk.CTkEntry(self, placeholder_text="Masukkan Password", show="*", width=300, height=40)
        self.entry_password.pack(pady=10)
        
        # Tombol Login (Sudah dihubungkan ke fungsi self.proses_login)
        self.btn_login = ctk.CTkButton(self, text="Login", width=300, height=42, font=ctk.CTkFont(weight="bold"), command=self.proses_login)
        self.btn_login.pack(pady=(20, 10))
        
        # Link ke Register jika belum punya akun
        self.btn_ke_register = ctk.CTkButton(self, text="Belum punya akun? Daftar disini", fg_color="transparent", text_color="#2563eb", hover_color=("#e2e8f0", "#1e293b"), command=lambda: self.controller.show_frame("PageRegister"))
        self.btn_ke_register.pack()

    def proses_login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        # Validasi Login (Untuk uji coba silakan ketik username: usyikkk dan password: 123)
        if username == "usyikkk" and password == "123":
            # Berhasil Login -> Alihkan ke Halaman Dashboard Utama
            self.controller.show_frame("PageDashboardUtama")
            
            # Opsional: Mengubah teks nama user di dashboard secara dinamis
            dashboard = self.controller.frames["PageDashboardUtama"]
            if hasattr(dashboard, "lbl_user"):
                dashboard.lbl_user.configure(text=f"Halo, {username}! Selamat Liburan.")
        else:
            messagebox.showerror("Login Gagal", "Username atau Password yang anda masukkan salah!")


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