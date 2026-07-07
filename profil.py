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


# ==============================================================================
# FRAME HALAMAN: PROFIL AKUN PENGGUNA
# Desain ini DISAMAKAN dengan class PageProfilAkun di mainbaruuaspbo.py
# (Card sederhana 500x450, tanpa avatar bulat/role badge seperti versi lama)
# ==============================================================================
class PageProfilAkun(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, fg_color=("#f8fafc", "#0f172a"))
        self.controller = controller

        card = ctk.CTkFrame(self, width=500, height=450, corner_radius=24, fg_color=("#ffffff", "#1e293b"), border_width=1, border_color=("#e2e8f0", "#334155"))
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)

        ctk.CTkLabel(card, text="👤 Profil Pengguna", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=30)

        self.ent_nama = ctk.CTkEntry(card, width=400, height=44, placeholder_text="Nama Lengkap (Username)")
        self.ent_nama.pack(pady=10)

        self.ent_email = ctk.CTkEntry(card, width=400, height=44, placeholder_text="Alamat Email")
        self.ent_email.pack(pady=10)

        ctk.CTkButton(card, text="Simpan Perubahan Profil", width=400, height=44, corner_radius=12, fg_color="#2563eb", font=ctk.CTkFont(weight="bold"), command=self.aksi_simpan).pack(pady=20)

    def refresh_data(self):
        """Mengisi ulang form dengan data akun yang sedang login dari JSON."""
        username = getattr(self.controller, "username_aktif", None)
        users = load_users()

        self.ent_nama.configure(state="normal")
        self.ent_nama.delete(0, "end")
        self.ent_email.delete(0, "end")

        if username and username in users:
            self.ent_nama.insert(0, username)
            self.ent_email.insert(0, users[username].get("email", ""))

        # Username sebagai identitas kunci JSON tidak diubah lewat form ini
        self.ent_nama.configure(state="disabled")

    def aksi_simpan(self):
        username = getattr(self.controller, "username_aktif", None)
        if not username:
            messagebox.showerror("Gagal", "Tidak ada sesi login aktif!")
            return

        users = load_users()
        if username in users:
            users[username]["email"] = self.ent_email.get().strip()
            save_users(users)
            messagebox.showinfo("Sukses", f"Profil atas nama {username} berhasil diperbarui!")