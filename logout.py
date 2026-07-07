import customtkinter as ctk
from tkinter import messagebox

# ==============================================================================
# FRAME HALAMAN: LOGOUT
# Desain ini DISAMAKAN dengan class PageLogout di mainbaruuaspbo.py
# (Card 450x260, tombol Batal & Ya Keluar sejajar kiri-kanan)
# ==============================================================================
class PageLogout(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, fg_color=("#f1f5f9", "#0f172a"))
        self.controller = controller

        card = ctk.CTkFrame(self, width=450, height=260, corner_radius=20, fg_color=("#ffffff", "#1e293b"))
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)

        ctk.CTkLabel(card, text="🚪 Konfirmasi Keluar", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(40, 15))
        ctk.CTkLabel(card, text="Apakah Anda yakin ingin keluar dan menutup sesi aplikasi?", text_color="#64748b").pack(pady=(0, 30))

        bc = ctk.CTkFrame(card, fg_color="transparent")
        bc.pack(fill="x", padx=40)

        ctk.CTkButton(bc, text="Batal", width=160, height=40, fg_color=("#e2e8f0", "#334155"), text_color=("#0f172a", "#f8fafc"), command=lambda: self.controller.show_frame("PageDashboardUtama")).pack(side="left")
        ctk.CTkButton(bc, text="Ya, Keluar", width=160, height=40, fg_color="#ef4444", hover_color="#dc2626", command=self.aksi_logout).pack(side="right")

    def aksi_logout(self):
        # Reset sesi username aktif sebelum menutup ke halaman Login
        self.controller.username_aktif = None
        self.controller.show_frame("PageLogin")