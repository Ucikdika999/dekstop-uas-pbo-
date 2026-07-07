import customtkinter as ctk
from tkinter import messagebox
import json
import os

# ==============================================================================
# SISTEM PENYIMPANAN AKUN BERBASIS JSON
# Disalin sama persis dengan bagian atas mainbaruuaspbo.py supaya file ini
# tetap bisa dites berdiri sendiri tanpa perlu mengimpor main.py.
# ==============================================================================
FILE_USERS = "users.json"

def load_users():
    if not os.path.exists(FILE_USERS):
        default_data = {"usyikkk": {"password": "123", "email": "usyikkk@pbo_uas.com"}}
        save_users(default_data)
        return default_data
    try:
        with open(FILE_USERS, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_users(data):
    with open(FILE_USERS, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def tambah_user(username, password, email=""):
    users = load_users()
    if username in users:
        return False
    users[username] = {"password": password, "email": email}
    save_users(users)
    return True

def cek_login(username, password):
    users = load_users()
    if username in users and users[username]["password"] == password:
        return True
    return False


# ==============================================================================
# FRAME HALAMAN: LOGIN
# Desain ini DISAMAKAN dengan class PageLogin di mainbaruuaspbo.py
# (Card 420x520 di tengah layar, cek akun ke users.json bukan hardcode)
# ==============================================================================
class PageLogin(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color=("#f8fafc", "#0f172a"))

        box = ctk.CTkFrame(self, width=420, height=520, corner_radius=20, fg_color=("#ffffff", "#1e293b"), border_width=1, border_color=("#e2e8f0", "#334155"))
        box.place(relx=0.5, rely=0.5, anchor="center")
        box.pack_propagate(False)

        ctk.CTkLabel(box, text="🔒 Login Akun", font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold")).pack(pady=(40, 30))

        ctk.CTkLabel(box, text="Username", font=ctk.CTkFont(size=11, weight="bold"), text_color="gray").pack(anchor="w", padx=45)
        self.entry_user = ctk.CTkEntry(box, width=330, height=40, placeholder_text="Masukkan nama pengguna...")
        self.entry_user.pack(pady=(2, 15))

        ctk.CTkLabel(box, text="Password", font=ctk.CTkFont(size=11, weight="bold"), text_color="gray").pack(anchor="w", padx=45)
        self.entry_pass = ctk.CTkEntry(box, width=330, height=40, placeholder_text="Masukkan kata sandi...", show="*")
        self.entry_pass.pack(pady=(2, 25))

        btn_login = ctk.CTkButton(box, text="Masuk Aplikasi", width=330, height=44, corner_radius=12, font=ctk.CTkFont(weight="bold"), fg_color="#2563eb", command=self.proses_login)
        btn_login.pack(pady=10)

        btn_ke_reg = ctk.CTkButton(box, text="Belum punya akun? Daftar disini", fg_color="transparent", text_color="#2563eb", command=lambda: self.controller.show_frame("PageRegister"))
        btn_ke_reg.pack()

        # Bind Enter key supaya bisa langsung login tanpa klik tombol
        self.entry_pass.bind("<Return>", lambda event: self.proses_login())

    def proses_login(self):
        u = self.entry_user.get().strip()
        p = self.entry_pass.get()

        if u == "" or p == "":
            messagebox.showwarning("Peringatan", "Username dan Password wajib diisi!")
            return

        if cek_login(u, p):
            self.controller.username_aktif = u
            self.entry_user.delete(0, "end")
            self.entry_pass.delete(0, "end")
            self.controller.show_frame("PageDashboardUtama")
        else:
            messagebox.showerror("Gagal", "Username atau Password salah, atau akun belum terdaftar!")


# ==============================================================================
# FRAME HALAMAN: REGISTER
# Desain ini DISAMAKAN dengan class PageRegister di mainbaruuaspbo.py
# (Card 420x560, ada field Email, simpan ke users.json lewat tambah_user)
# ==============================================================================
class PageRegister(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color=("#f8fafc", "#0f172a"))

        box = ctk.CTkFrame(self, width=420, height=560, corner_radius=20, fg_color=("#ffffff", "#1e293b"), border_width=1, border_color=("#e2e8f0", "#334155"))
        box.place(relx=0.5, rely=0.5, anchor="center")
        box.pack_propagate(False)

        ctk.CTkLabel(box, text="📝 Registrasi Akun", font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold")).pack(pady=(40, 25))

        ctk.CTkLabel(box, text="Username Baru", font=ctk.CTkFont(size=11, weight="bold"), text_color="gray").pack(anchor="w", padx=45)
        self.entry_user_reg = ctk.CTkEntry(box, width=330, height=40, placeholder_text="Buat nama pengguna...")
        self.entry_user_reg.pack(pady=(2, 15))

        ctk.CTkLabel(box, text="Email", font=ctk.CTkFont(size=11, weight="bold"), text_color="gray").pack(anchor="w", padx=45)
        self.entry_email_reg = ctk.CTkEntry(box, width=330, height=40, placeholder_text="Masukkan alamat email...")
        self.entry_email_reg.pack(pady=(2, 15))

        ctk.CTkLabel(box, text="Password Baru", font=ctk.CTkFont(size=11, weight="bold"), text_color="gray").pack(anchor="w", padx=45)
        self.entry_pass_reg = ctk.CTkEntry(box, width=330, height=40, placeholder_text="Buat sandi aman...", show="*")
        self.entry_pass_reg.pack(pady=(2, 25))

        btn_reg = ctk.CTkButton(box, text="Buat Akun Sekarang", width=330, height=44, corner_radius=12, fg_color="#10b981", font=ctk.CTkFont(weight="bold"), command=self.proses_register)
        btn_reg.pack(pady=10)

        btn_ke_log = ctk.CTkButton(box, text="Sudah punya akun? Login", fg_color="transparent", text_color="#10b981", command=lambda: self.controller.show_frame("PageLogin"))
        btn_ke_log.pack()

    def proses_register(self):
        username = self.entry_user_reg.get().strip()
        email = self.entry_email_reg.get().strip()
        password = self.entry_pass_reg.get()

        if username == "" or password == "":
            messagebox.showwarning("Peringatan", "Username dan Password tidak boleh kosong!")
            return

        if len(password) < 3:
            messagebox.showwarning("Peringatan", "Password minimal 3 karakter!")
            return

        sukses = tambah_user(username, password, email)

        if sukses:
            messagebox.showinfo("Sukses", f"Akun '{username}' berhasil dibuat! Silakan login kembali.")
            self.entry_user_reg.delete(0, "end")
            self.entry_email_reg.delete(0, "end")
            self.entry_pass_reg.delete(0, "end")
            self.controller.show_frame("PageLogin")
        else:
            messagebox.showerror("Gagal", f"Username '{username}' sudah digunakan, silakan pilih username lain!")