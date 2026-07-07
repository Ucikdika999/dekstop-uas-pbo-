import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import hashlib, datetime, random, string

# ══════════════════════════════════════════════════════
#  IN-MEMORY DATA STORE  (tidak butuh database / file)
# ══════════════════════════════════════════════════════

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def gen_kode():
    return "TKT-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))

DB = {
    "users": [
        {"id":1,"username":"admin","password":hash_pw("admin123"),"email":"admin@tiket.com","phone":"081234567890","role":"admin","created_at":"2025-01-01"},
        {"id":2,"username":"budi","password":hash_pw("budi123"),"email":"budi@email.com","phone":"081111111111","role":"user","created_at":"2025-03-10"},
        {"id":3,"username":"sari","password":hash_pw("sari123"),"email":"sari@email.com","phone":"082222222222","role":"user","created_at":"2025-04-05"},
        {"id":4,"username":"rara","password":hash_pw("rara123"),"email":"rara@email.com","phone":"083333333333","role":"user","created_at":"2025-05-20"},
    ],
    "destinasi": [
        {"id":1,"nama":"Candi Borobudur","lokasi":"Magelang","deskripsi":"Candi Buddha terbesar di dunia","harga":50000,"kapasitas":500,"tersedia":480,"kategori":"Budaya"},
        {"id":2,"nama":"Pantai Parangtritis","lokasi":"Yogyakarta","deskripsi":"Pantai terkenal di DIY","harga":10000,"kapasitas":1000,"tersedia":950,"kategori":"Alam"},
        {"id":3,"nama":"Keraton Yogyakarta","lokasi":"Yogyakarta","deskripsi":"Istana Sultan Yogyakarta","harga":15000,"kapasitas":300,"tersedia":290,"kategori":"Sejarah"},
        {"id":4,"nama":"Gunung Merapi","lokasi":"Sleman","deskripsi":"Wisata gunung berapi aktif","harga":25000,"kapasitas":200,"tersedia":180,"kategori":"Alam"},
        {"id":5,"nama":"Malioboro","lokasi":"Yogyakarta","deskripsi":"Pusat belanja dan budaya","harga":0,"kapasitas":9999,"tersedia":9999,"kategori":"Belanja"},
        {"id":6,"nama":"Prambanan","lokasi":"Klaten","deskripsi":"Kompleks candi Hindu terbesar","harga":50000,"kapasitas":600,"tersedia":560,"kategori":"Budaya"},
        {"id":7,"nama":"Pantai Indrayanti","lokasi":"Gunungkidul","deskripsi":"Pantai pasir putih eksotis","harga":10000,"kapasitas":500,"tersedia":480,"kategori":"Alam"},
        {"id":8,"nama":"Goa Pindul","lokasi":"Gunungkidul","deskripsi":"Cave tubing populer","harga":45000,"kapasitas":150,"tersedia":130,"kategori":"Petualangan"},
        {"id":9,"nama":"Taman Sari","lokasi":"Yogyakarta","deskripsi":"Bekas taman kerajaan Mataram","harga":15000,"kapasitas":400,"tersedia":390,"kategori":"Sejarah"},
        {"id":10,"nama":"Kalibiru","lokasi":"Kulon Progo","deskripsi":"Spot foto alam di atas bukit","harga":20000,"kapasitas":200,"tersedia":190,"kategori":"Alam"},
    ],
    "tiket": [
        {"id":1,"kode":"TKT-CONTOH1","user_id":2,"destinasi_id":1,"tgl_kunjungan":"2025-07-10","jumlah":2,"total":100000,"status":"confirmed","created_at":"2025-06-01 10:00"},
        {"id":2,"kode":"TKT-CONTOH2","user_id":3,"destinasi_id":3,"tgl_kunjungan":"2025-07-15","jumlah":3,"total":45000,"status":"pending","created_at":"2025-06-02 14:30"},
        {"id":3,"kode":"TKT-CONTOH3","user_id":2,"destinasi_id":6,"tgl_kunjungan":"2025-08-01","jumlah":1,"total":50000,"status":"confirmed","created_at":"2025-06-03 09:15"},
    ],
    "pembayaran": [
        {"id":1,"tiket_id":1,"metode":"Transfer Bank","jumlah":100000,"status":"lunas","tanggal":"2025-06-01 11:00"},
        {"id":2,"tiket_id":2,"metode":"QRIS","jumlah":45000,"status":"pending","tanggal":"2025-06-02 15:00"},
        {"id":3,"tiket_id":3,"metode":"Dompet Digital","jumlah":50000,"status":"lunas","tanggal":"2025-06-03 10:00"},
    ],
    "pesan": [
        {"id":1,"user_id":2,"subjek":"Pertanyaan Tiket","isi":"Apakah tiket bisa di-refund?","balasan":"Tiket tidak bisa di-refund.","status":"dibalas","tanggal":"2025-06-01"},
        {"id":2,"user_id":3,"subjek":"Kendala Pembayaran","isi":"Pembayaran saya gagal terus.","balasan":"","status":"baru","tanggal":"2025-06-02"},
    ],
    "visitor_log": [
        {"id":1,"user_id":1,"action":"login","waktu":"2025-06-01 08:00"},
        {"id":2,"user_id":2,"action":"login","waktu":"2025-06-01 09:00"},
        {"id":3,"user_id":3,"action":"login","waktu":"2025-06-02 10:00"},
        {"id":4,"user_id":2,"action":"booking:TKT-CONTOH1","waktu":"2025-06-01 10:05"},
    ],
    "_ctr": {"users":5,"destinasi":11,"tiket":4,"pembayaran":4,"pesan":3,"visitor_log":5},
}

def nid(table):
    v = DB["_ctr"][table]; DB["_ctr"][table] += 1; return v

def log_visitor(uid, action):
    DB["visitor_log"].append({"id":nid("visitor_log"),"user_id":uid,"action":action,
                               "waktu":str(datetime.datetime.now())[:16]})

def find_user(username, password):
    return next((u for u in DB["users"] if u["username"]==username and u["password"]==password), None)

def get_dest(did):
    return next((d for d in DB["destinasi"] if d["id"]==did), None)

def get_user(uid):
    return next((u for u in DB["users"] if u["id"]==uid), None)

def tiket_rows(user_id=None):
    src = DB["tiket"] if user_id is None else [t for t in DB["tiket"] if t["user_id"]==user_id]
    out = []
    for t in reversed(src):
        d = get_dest(t["destinasi_id"])
        out.append((t["kode"], d["nama"] if d else "?", t["tgl_kunjungan"],
                    t["jumlah"], t["total"], t["status"], t["created_at"]))
    return out

def bayar_rows(user_id=None):
    out = []
    for pm in reversed(DB["pembayaran"]):
        t = next((x for x in DB["tiket"] if x["id"]==pm["tiket_id"]), None)
        if not t: continue
        if user_id and t["user_id"]!=user_id: continue
        d = get_dest(t["destinasi_id"])
        out.append((pm["id"], t["kode"], d["nama"] if d else "?",
                    pm["metode"], pm["jumlah"], pm["status"], pm["tanggal"]))
    return out

# ══════════════════════════════════════════════════════
#  WARNA
# ══════════════════════════════════════════════════════
C = {
    "bg":"#0D1117","sidebar":"#161B22","card":"#1C2128",
    "accent":"#2563EB","accent2":"#10B981","warn":"#F59E0B",
    "danger":"#EF4444","text":"#E6EDF3","muted":"#8B949E",
    "border":"#30363D","hover":"#21262D","white":"#FFFFFF","inp":"#0D1117",
}

# ══════════════════════════════════════════════════════
#  APLIKASI UTAMA
# ══════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PBO – Sistem Tiket Online")
        self.geometry("1280x780")
        self.minsize(1100,700)
        self.configure(bg=C["bg"])
        self.current_user = None
        self.current_page = None
        self.nav_btns = {}
        self._style()
        self._login()

    # ── TTK STYLE ─────────────────────────────────────
    def _style(self):
        s = ttk.Style(self); s.theme_use("clam")
        s.configure("TEntry", fieldbackground=C["inp"], background=C["inp"],
            foreground=C["text"], insertcolor=C["text"],
            bordercolor=C["border"], lightcolor=C["border"], darkcolor=C["border"],
            relief="flat", padding=8)
        s.configure("TCombobox", fieldbackground=C["inp"], background=C["card"],
            foreground=C["text"], arrowcolor=C["text"], bordercolor=C["border"], relief="flat")
        s.configure("Treeview", background=C["card"], fieldbackground=C["card"],
            foreground=C["text"], rowheight=34, bordercolor=C["border"])
        s.configure("Treeview.Heading", background=C["sidebar"], foreground=C["text"],
            font=("Consolas",10,"bold"), relief="flat")
        s.map("Treeview", background=[("selected",C["accent"])])

    # ── HELPER WIDGET ─────────────────────────────────
    def _clr(self):
        for w in self.winfo_children(): w.destroy()

    def _lig(self, h):
        try:
            r=min(255,int(h[1:3],16)+28); g=min(255,int(h[3:5],16)+28); b=min(255,int(h[5:7],16)+28)
            return f"#{r:02x}{g:02x}{b:02x}"
        except: return h

    def btn(self, parent, text, cmd, bg=None, fg=None, fs=11, pad=(14,8), w=None):
        bg = bg or C["accent"]; fg = fg or C["white"]
        kw = dict(text=text,command=cmd,bg=bg,fg=fg,relief="flat",cursor="hand2",
                  font=("Consolas",fs,"bold"),padx=pad[0],pady=pad[1],
                  activebackground=bg,activeforeground=fg,bd=0)
        if w: kw["width"]=w
        b = tk.Button(parent,**kw)
        b.bind("<Enter>", lambda e,_b=b,_bg=bg: _b.config(bg=self._lig(_bg)))
        b.bind("<Leave>", lambda e,_b=b,_bg=bg: _b.config(bg=_bg))
        return b

    def lbl(self, p, text, size=10, bold=False, color=None, **kw):
        return tk.Label(p,text=text,bg=p.cget("bg"),fg=color or C["text"],
                        font=("Consolas",size,"bold" if bold else "normal"),**kw)

    def entry(self, p, w=34, show=""):
        e = ttk.Entry(p, width=w, font=("Consolas",11), show=show); return e

    def tree(self, p, cols, h=15, widths=None):
        fr = tk.Frame(p,bg=C["bg"]); fr.pack(fill="both",expand=True)
        tv = ttk.Treeview(fr,columns=cols,show="headings",height=h)
        for i,c in enumerate(cols):
            ww = widths[i] if widths and i<len(widths) else 120
            tv.heading(c,text=c); tv.column(c,width=ww,anchor="center")
        sb = ttk.Scrollbar(fr,orient="vertical",command=tv.yview)
        tv.configure(yscrollcommand=sb.set)
        tv.pack(side="left",fill="both",expand=True); sb.pack(side="left",fill="y")
        return tv

    def hdr(self, p, text, color, btn_lbl=None, btn_cmd=None):
        f = tk.Frame(p,bg=color,height=68); f.pack(fill="x"); f.pack_propagate(False)
        tk.Label(f,text=f"  {text}",font=("Consolas",15,"bold"),bg=color,fg=C["white"]).pack(side="left",padx=14)
        if btn_lbl and btn_cmd:
            self.btn(f,btn_lbl,btn_cmd,bg=self._lig(color),fs=10).pack(side="right",padx=14,pady=12)
        return f

    # ══════════════════════════════════════════════════
    #  LOGIN
    # ══════════════════════════════════════════════════
    def _login(self):
        self._clr(); self.title("Login – PBO Tiket Online")
        outer = tk.Frame(self,bg=C["bg"]); outer.pack(fill="both",expand=True)

        # Panel kiri
        lp = tk.Frame(outer,bg=C["accent"],width=460); lp.pack(side="left",fill="y"); lp.pack_propagate(False)
        tk.Label(lp,text="🎫",font=("Segoe UI Emoji",60),bg=C["accent"],fg=C["white"]).pack(pady=(90,6))
        tk.Label(lp,text="TIKET ONLINE",font=("Consolas",30,"bold"),bg=C["accent"],fg=C["white"]).pack()
        tk.Label(lp,text="Sistem Manajemen Tiket Wisata\nTerintegrasi & Terpercaya",
                 font=("Consolas",11),bg=C["accent"],fg="#BFDBFE",justify="center").pack(pady=10)

        sf = tk.Frame(lp,bg="#1D4ED8"); sf.pack(fill="x",side="bottom")
        tv = len(DB["visitor_log"])
        tt = len([t for t in DB["tiket"] if t["status"]=="confirmed"])
        for lab,val in [("Total Login",tv),("Tiket Terjual",tt)]:
            ff = tk.Frame(sf,bg="#1D4ED8"); ff.pack(side="left",expand=True,pady=14)
            tk.Label(ff,text=str(val),font=("Consolas",22,"bold"),bg="#1D4ED8",fg=C["white"]).pack()
            tk.Label(ff,text=lab,font=("Consolas",9),bg="#1D4ED8",fg="#BFDBFE").pack()

        # Form kanan
        rp = tk.Frame(outer,bg=C["bg"]); rp.pack(side="left",fill="both",expand=True)
        fm = tk.Frame(rp,bg=C["bg"]); fm.place(relx=0.5,rely=0.5,anchor="center")

        tk.Label(fm,text="Selamat Datang",font=("Consolas",26,"bold"),bg=C["bg"],fg=C["text"]).pack(anchor="w")
        tk.Label(fm,text="Masuk ke akun Anda untuk melanjutkan",font=("Consolas",10),bg=C["bg"],fg=C["muted"]).pack(anchor="w",pady=(4,26))

        for lab in ["USERNAME","PASSWORD"]:
            tk.Label(fm,text=lab,font=("Consolas",9,"bold"),bg=C["bg"],fg=C["muted"]).pack(anchor="w")
            e = self.entry(fm, show="●" if lab=="PASSWORD" else "")
            e.pack(anchor="w",ipady=6,pady=(3,14))
            if lab=="USERNAME": self._eu=e; e.insert(0,"admin")
            else: self._ep=e; e.insert(0,"admin123")

        self.btn(fm,"  MASUK  →",self._do_login,fs=12,pad=(24,12)).pack(anchor="w")
        tk.Label(fm,text="Belum punya akun?",font=("Consolas",10),bg=C["bg"],fg=C["muted"]).pack(anchor="w",pady=(16,4))
        self.btn(fm,"Daftar Sekarang",self._register,bg=C["card"],fg=C["accent"],fs=10,pad=(14,8)).pack(anchor="w")

        hint = tk.Frame(fm,bg=C["hover"]); hint.pack(anchor="w",pady=(14,0))
        tk.Label(hint,text="  💡  Demo: admin/admin123 | budi/budi123 | sari/sari123  ",
                 font=("Consolas",9),bg=C["hover"],fg=C["muted"]).pack(padx=8,pady=6)

        self._eu.bind("<Return>",lambda e: self._ep.focus())
        self._ep.bind("<Return>",lambda e: self._do_login())
        self._eu.focus()

    def _do_login(self):
        u=self._eu.get().strip(); p=self._ep.get().strip()
        if not u or not p: messagebox.showwarning("Peringatan","Username & password harus diisi!"); return
        row = find_user(u,hash_pw(p))
        if row:
            self.current_user = dict(row); log_visitor(row["id"],"login"); self._main()
        else:
            messagebox.showerror("Gagal Login","Username atau password salah!")

    # ══════════════════════════════════════════════════
    #  REGISTER
    # ══════════════════════════════════════════════════
    def _register(self):
        self.register_user()

    def register_user(self):
        self._clr()
        outer = tk.Frame(self,bg=C["bg"]); outer.pack(fill="both",expand=True)
        lp = tk.Frame(outer,bg=C["accent2"],width=420); lp.pack(side="left",fill="y"); lp.pack_propagate(False)
        tk.Label(lp,text="📝",font=("Segoe UI Emoji",52),bg=C["accent2"],fg=C["white"]).pack(pady=(90,8))
        tk.Label(lp,text="DAFTAR AKUN",font=("Consolas",26,"bold"),bg=C["accent2"],fg=C["white"]).pack()
        tk.Label(lp,text="Buat akun baru untuk memesan\ntiket wisata impian Anda",
                 font=("Consolas",10),bg=C["accent2"],fg="#D1FAE5",justify="center").pack(pady=10)
        self.btn(lp,"← Kembali Login",self._login,bg="#059669",fs=10).pack(pady=36)

        rp = tk.Frame(outer,bg=C["bg"]); rp.pack(side="left",fill="both",expand=True)
        fm = tk.Frame(rp,bg=C["bg"]); fm.place(relx=0.5,rely=0.5,anchor="center")
        tk.Label(fm,text="Buat Akun Baru",font=("Consolas",22,"bold"),bg=C["bg"],fg=C["text"]).pack(anchor="w",pady=(0,18))

        self._re = {}
        for lab,hide in [("USERNAME *",False),("PASSWORD *",True),("KONFIRMASI PASSWORD *",True),("EMAIL",False),("NO. TELEPON",False)]:
            tk.Label(fm,text=lab,font=("Consolas",9,"bold"),bg=C["bg"],fg=C["muted"]).pack(anchor="w")
            e = self.entry(fm, show="●" if hide else "")
            e.pack(anchor="w",ipady=5,pady=(3,10)); self._re[lab]=e

        self.btn(fm,"  DAFTAR  →",self._do_register,bg=C["accent2"],fs=11,pad=(20,10)).pack(anchor="w",pady=(6,0))

    def _do_register(self):
        e=self._re; u=e["USERNAME *"].get().strip(); p=e["PASSWORD *"].get().strip()
        p2=e["KONFIRMASI PASSWORD *"].get().strip()
        em=e["EMAIL"].get().strip(); ph=e["NO. TELEPON"].get().strip()
        if not u or not p: messagebox.showwarning("Peringatan","Username & password wajib diisi!"); return
        if p!=p2: messagebox.showerror("Error","Password tidak cocok!"); return
        if any(x["username"]==u for x in DB["users"]): messagebox.showerror("Error","Username sudah digunakan!"); return
        DB["users"].append({"id":nid("users"),"username":u,"password":hash_pw(p),
                             "email":em,"phone":ph,"role":"user","created_at":str(datetime.date.today())})
        messagebox.showinfo("Berhasil",f"Akun '{u}' berhasil dibuat!\nSilakan login.")
        self._login()

    # ══════════════════════════════════════════════════
    #  MAIN SHELL (sidebar + konten)
    # ══════════════════════════════════════════════════
    def _main(self):
        self._clr(); self.title(f"PBO Tiket – {self.current_user['username'].upper()}")
        self.sidebar = tk.Frame(self,bg=C["sidebar"],width=220); self.sidebar.pack(side="left",fill="y"); self.sidebar.pack_propagate(False)

        # Logo
        logo = tk.Frame(self.sidebar,bg=C["accent"],height=68); logo.pack(fill="x"); logo.pack_propagate(False)
        tk.Label(logo,text="🎫 PBO TIKET",font=("Consolas",14,"bold"),bg=C["accent"],fg=C["white"]).pack(expand=True)

        # Info user
        uf = tk.Frame(self.sidebar,bg=C["hover"]); uf.pack(fill="x",padx=8,pady=8)
        tk.Label(uf,text="👤 "+self.current_user["username"].upper(),
                 font=("Consolas",10,"bold"),bg=C["hover"],fg=C["text"]).pack(pady=5,padx=8,anchor="w")
        rc = C["warn"] if self.current_user["role"]=="admin" else C["accent2"]
        tk.Label(uf,text=f"● {self.current_user['role'].upper()}",
                 font=("Consolas",8),bg=C["hover"],fg=rc).pack(padx=8,anchor="w",pady=(0,5))

        # Menu
        menus = [
            ("🏠","DASHBOARD",self._p_dashboard),
            ("🗺️","DESTINASI",self._p_destinasi),
            ("📨","PESAN",self._p_pesan),
            ("💳","PEMBAYARAN",self._p_pembayaran),
            ("📋","RIWAYAT",self._p_riwayat),
            ("👤","PROFILE",self._p_profile),
        ]
        if self.current_user["role"]=="admin":
            menus.insert(1,("📊","TRACKING",self._p_tracking))

        tk.Frame(self.sidebar,bg=C["border"],height=1).pack(fill="x",padx=12,pady=4)
        tk.Label(self.sidebar,text="MENU UTAMA",font=("Consolas",8),bg=C["sidebar"],fg=C["muted"]).pack(anchor="w",padx=16,pady=(4,2))

        self.nav_btns = {}
        for icon,name,cmd in menus:
            f = tk.Frame(self.sidebar,bg=C["sidebar"],cursor="hand2"); f.pack(fill="x",padx=8,pady=2)
            lb = tk.Label(f,text=f"  {icon}  {name}",font=("Consolas",11),bg=C["sidebar"],fg=C["muted"],anchor="w")
            lb.pack(fill="x",ipady=9,padx=4)
            for ww in (f,lb):
                ww.bind("<Enter>",lambda e,_f=f,_l=lb:(_f.config(bg=C["hover"]),_l.config(bg=C["hover"])))
                ww.bind("<Leave>",lambda e,_f=f,_l=lb,_n=name:(
                    _f.config(bg=C["accent"] if self.current_page==_n else C["sidebar"]),
                    _l.config(bg=C["accent"] if self.current_page==_n else C["sidebar"],
                              fg=C["white"] if self.current_page==_n else C["muted"])))
                ww.bind("<Button-1>",lambda e,_c=cmd,_n=name:self._nav(_c,_n))
            self.nav_btns[name]=(f,lb)

        tk.Frame(self.sidebar,bg=C["border"],height=1).pack(fill="x",padx=12,pady=8)
        self.btn(self.sidebar,"  🚪  LOGOUT",self._logout,bg=C["danger"],fs=10,pad=(16,10)).pack(fill="x",padx=8,pady=4)

        self.content = tk.Frame(self,bg=C["bg"]); self.content.pack(side="left",fill="both",expand=True)
        self._nav(self._p_dashboard,"DASHBOARD")

    def _nav(self,cmd,name):
        self.current_page=name
        for n,(f,lb) in self.nav_btns.items():
            if n==name: f.config(bg=C["accent"]); lb.config(bg=C["accent"],fg=C["white"])
            else:       f.config(bg=C["sidebar"]); lb.config(bg=C["sidebar"],fg=C["muted"])
        for w in self.content.winfo_children(): w.destroy()
        cmd()

    def _logout(self):
        if messagebox.askyesno("Logout","Yakin ingin keluar?"):
            log_visitor(self.current_user["id"],"logout"); self.current_user=None; self._login()

    # ══════════════════════════════════════════════════
    #  HALAMAN: DASHBOARD
    # ══════════════════════════════════════════════════
    def _p_dashboard(self):
        p=self.content; uid=self.current_user["id"]; is_adm=self.current_user["role"]=="admin"

        # Header
        hf=tk.Frame(p,bg=C["accent"],height=68); hf.pack(fill="x"); hf.pack_propagate(False)
        tk.Label(hf,text=f"  🏠  Dashboard – {self.current_user['username'].upper()}",
                 font=("Consolas",15,"bold"),bg=C["accent"],fg=C["white"]).pack(side="left",padx=14)
        tk.Label(hf,text=datetime.datetime.now().strftime("  %A, %d %B %Y  %H:%M"),
                 font=("Consolas",10),bg=C["accent"],fg="#BFDBFE").pack(side="right",padx=14)

        body=tk.Frame(p,bg=C["bg"]); body.pack(fill="both",expand=True,padx=18,pady=14)

        # Stat cards
        if is_adm:
            total_rp=sum(t["total"] for t in DB["tiket"] if t["status"]=="confirmed")
            stats=[("Total Pengguna",len(DB["users"]),"📊"),
                   ("Total Destinasi",len(DB["destinasi"]),"🗺️"),
                   ("Tiket Terjual",len([t for t in DB["tiket"] if t["status"]=="confirmed"]),"🎫"),
                   (f"Pendapatan (Rp)",int(total_rp),"💰")]
        else:
            my=[ t for t in DB["tiket"] if t["user_id"]==uid ]
            rp=sum(t["total"] for t in my if t["status"]=="confirmed")
            stats=[("Tiket Saya",len(my),"🎫"),
                   ("Tiket Aktif",len([t for t in my if t["status"]=="confirmed"]),"✅"),
                   ("Pesan Saya",len([m for m in DB["pesan"] if m["user_id"]==uid]),"📨"),
                   ("Total Bayar (Rp)",int(rp),"💰")]

        row1=tk.Frame(body,bg=C["bg"]); row1.pack(fill="x",pady=(0,18))
        clrs=[C["accent"],C["accent2"],C["warn"],"#8B5CF6"]
        for i,(lab,val,ico) in enumerate(stats):
            cc=clrs[i%len(clrs)]; cd=tk.Frame(row1,bg=C["card"]); cd.pack(side="left",expand=True,fill="both",padx=5)
            tk.Frame(cd,bg=cc,height=4).pack(fill="x")
            tk.Label(cd,text=ico,font=("Segoe UI Emoji",26),bg=C["card"]).pack(pady=(10,0))
            vs=f"Rp {val:,}" if "Rp" in lab else str(val)
            tk.Label(cd,text=vs,font=("Consolas",20,"bold"),bg=C["card"],fg=cc).pack()
            tk.Label(cd,text=lab,font=("Consolas",9),bg=C["card"],fg=C["muted"]).pack(pady=(0,12))

        # Tabel tiket terbaru
        tk.Label(body,text="TIKET TERBARU",font=("Consolas",11,"bold"),bg=C["bg"],fg=C["muted"]).pack(anchor="w",pady=(0,6))
        cols=("Kode Tiket","Destinasi","Tgl Kunjungan","Jumlah","Total","Status")
        tv=self.tree(body,cols,8,[140,200,120,70,120,100])
        for r in tiket_rows(None if is_adm else uid)[:10]:
            kode,nama,tgl,jml,total,status,_=r
            tv.insert("","end",values=(kode,nama,tgl,jml,f"Rp {int(total):,}",status))

    # ══════════════════════════════════════════════════
    #  HALAMAN: DESTINASI
    # ══════════════════════════════════════════════════
    def _p_destinasi(self):
        p=self.content; is_adm=self.current_user["role"]=="admin"
        self.hdr(p,"🗺️  DESTINASI WISATA","#7C3AED",
                 "+ Tambah Destinasi" if is_adm else None,
                 self._dlg_add_dest if is_adm else None)

        body=tk.Frame(p,bg=C["bg"]); body.pack(fill="both",expand=True,padx=14,pady=8)

        # Filter
        fb=tk.Frame(body,bg=C["bg"]); fb.pack(fill="x",pady=(0,8))
        tk.Label(fb,text="Filter Kategori:",font=("Consolas",10),bg=C["bg"],fg=C["muted"]).pack(side="left")
        self._df=ttk.Combobox(fb,values=["Semua","Budaya","Alam","Sejarah","Petualangan","Belanja"],width=16,state="readonly")
        self._df.set("Semua"); self._df.pack(side="left",padx=8)
        self.btn(fb,"Filter",self._load_dest,bg=C["card"],fg=C["text"],fs=10,pad=(12,5)).pack(side="left")

        cols=("ID","Nama","Lokasi","Harga","Tersedia","Kapasitas","Kategori")
        self._dtv=self.tree(body,cols,14,[40,210,130,110,80,80,110])
        self._load_dest()

        af=tk.Frame(p,bg=C["bg"]); af.pack(fill="x",padx=14,pady=8)
        self.btn(af,"🎫  Pesan Tiket",self._dlg_booking,bg=C["accent2"],fs=11,pad=(18,10)).pack(side="left")
        if is_adm:
            self.btn(af,"🗑  Hapus",self._hapus_dest,bg=C["danger"],fs=10,pad=(14,10)).pack(side="left",padx=8)

    def _load_dest(self):
        for i in self._dtv.get_children(): self._dtv.delete(i)
        kat=self._df.get()
        for d in DB["destinasi"]:
            if kat!="Semua" and d["kategori"]!=kat: continue
            self._dtv.insert("","end",values=(d["id"],d["nama"],d["lokasi"],
                f"Rp {int(d['harga']):,}",d["tersedia"],d["kapasitas"],d["kategori"]))

    def _dlg_add_dest(self):
        dlg=tk.Toplevel(self); dlg.title("Tambah Destinasi"); dlg.geometry("480x460")
        dlg.configure(bg=C["bg"]); dlg.grab_set()
        tk.Label(dlg,text="TAMBAH DESTINASI BARU",font=("Consolas",14,"bold"),bg=C["bg"],fg=C["text"]).pack(pady=14)
        flds=["Nama","Lokasi","Deskripsi","Harga","Kapasitas","Kategori"]; ent={}
        for f in flds:
            tk.Label(dlg,text=f.upper(),font=("Consolas",9),bg=C["bg"],fg=C["muted"]).pack(anchor="w",padx=30)
            e=ttk.Entry(dlg,width=44); e.pack(padx=30,pady=(2,8),ipady=5); ent[f]=e
        ent["Kategori"].insert(0,"Alam")
        def save():
            try:
                kap=int(ent["Kapasitas"].get() or 0)
                DB["destinasi"].append({"id":nid("destinasi"),"nama":ent["Nama"].get(),
                    "lokasi":ent["Lokasi"].get(),"deskripsi":ent["Deskripsi"].get(),
                    "harga":float(ent["Harga"].get() or 0),"kapasitas":kap,"tersedia":kap,
                    "kategori":ent["Kategori"].get()})
                messagebox.showinfo("Berhasil","Destinasi berhasil ditambahkan!"); dlg.destroy(); self._load_dest()
            except ValueError as ex: messagebox.showerror("Error",str(ex))
        self.btn(dlg,"SIMPAN",save,bg=C["accent2"],fs=11,pad=(22,10)).pack(pady=8)

    def _hapus_dest(self):
        sel=self._dtv.selection()
        if not sel: messagebox.showwarning("Peringatan","Pilih destinasi terlebih dahulu!"); return
        did=int(self._dtv.item(sel[0])["values"][0])
        if messagebox.askyesno("Hapus","Yakin hapus destinasi ini?"):
            DB["destinasi"]=[d for d in DB["destinasi"] if d["id"]!=did]; self._load_dest()

    def _dlg_booking(self):
        sel=self._dtv.selection()
        if not sel: messagebox.showwarning("Peringatan","Pilih destinasi terlebih dahulu!"); return
        item=self._dtv.item(sel[0])["values"]
        did=int(item[0]); dname=item[1]; tersedia=int(item[4])
        dest=get_dest(did); harga=dest["harga"] if dest else 0

        dlg=tk.Toplevel(self); dlg.title(f"Pesan – {dname}"); dlg.geometry("460,420".replace(",","x"))
        dlg.configure(bg=C["bg"]); dlg.grab_set()
        tk.Label(dlg,text="🎫 PESAN TIKET",font=("Consolas",16,"bold"),bg=C["bg"],fg=C["text"]).pack(pady=(16,4))
        tk.Label(dlg,text=dname,font=("Consolas",13,"bold"),bg=C["bg"],fg=C["accent2"]).pack()
        tk.Label(dlg,text=f"Tersedia: {tersedia}  |  Harga: Rp {int(harga):,}",
                 font=("Consolas",10),bg=C["bg"],fg=C["muted"]).pack(pady=6)
        tk.Frame(dlg,bg=C["border"],height=1).pack(fill="x",padx=30,pady=4)

        for lab in ["TANGGAL KUNJUNGAN (YYYY-MM-DD)","JUMLAH TIKET"]:
            tk.Label(dlg,text=lab,font=("Consolas",9),bg=C["bg"],fg=C["muted"]).pack(anchor="w",padx=34,pady=(10,0))
            e=ttk.Entry(dlg,width=36); e.pack(padx=34,ipady=5,pady=(2,0))
            if "TANGGAL" in lab: self._btgl=e; e.insert(0,str(datetime.date.today()))
            else: self._bjml=e; e.insert(0,"1")

        opts=["Transfer Bank","QRIS","Dompet Digital","Bayar di Tempat"]
        tk.Label(dlg,text="METODE PEMBAYARAN",font=("Consolas",9),bg=C["bg"],fg=C["muted"]).pack(anchor="w",padx=34,pady=(10,0))
        self._bmet=ttk.Combobox(dlg,values=opts,width=34,state="readonly"); self._bmet.set(opts[0]); self._bmet.pack(padx=34,pady=(2,14))

        def pesan():
            try:
                tgl=self._btgl.get().strip(); jml=int(self._bjml.get().strip()); met=self._bmet.get()
                if jml<=0: messagebox.showerror("Error","Jumlah harus > 0"); return
                if jml>tersedia: messagebox.showerror("Error",f"Hanya tersisa {tersedia} tiket!"); return
                total=jml*harga; kode=gen_kode(); tid=nid("tiket")
                DB["tiket"].append({"id":tid,"kode":kode,"user_id":self.current_user["id"],
                    "destinasi_id":did,"tgl_kunjungan":tgl,"jumlah":jml,"total":total,
                    "status":"pending","created_at":str(datetime.datetime.now())[:16]})
                DB["pembayaran"].append({"id":nid("pembayaran"),"tiket_id":tid,"metode":met,
                    "jumlah":total,"status":"pending","tanggal":str(datetime.datetime.now())[:16]})
                dest["tersedia"]-=jml
                log_visitor(self.current_user["id"],f"booking:{kode}")
                messagebox.showinfo("Berhasil! 🎉",
                    f"Tiket berhasil dipesan!\n\nKode   : {kode}\nTotal  : Rp {int(total):,}\nMetode : {met}\nStatus : Menunggu Konfirmasi")
                dlg.destroy(); self._load_dest()
            except ValueError: messagebox.showerror("Error","Jumlah tiket harus angka!")
        self.btn(dlg,"✅  KONFIRMASI PEMESANAN",pesan,bg=C["accent"],fs=11,pad=(20,10)).pack(pady=4)

    # ══════════════════════════════════════════════════
    #  HALAMAN: PESAN
    # ══════════════════════════════════════════════════
    def _p_pesan(self):
        p=self.content; is_adm=self.current_user["role"]=="admin"
        self.hdr(p,"📨  PESAN & BANTUAN",C["warn"])

        body=tk.Frame(p,bg=C["bg"]); body.pack(fill="both",expand=True,padx=14,pady=8)
        lp=tk.Frame(body,bg=C["bg"]); lp.pack(side="left",fill="both",expand=True)
        rp=tk.Frame(body,bg=C["card"],width=320); rp.pack(side="right",fill="y",padx=(10,0)); rp.pack_propagate(False)

        tk.Label(lp,text="DAFTAR PESAN",font=("Consolas",11,"bold"),bg=C["bg"],fg=C["muted"]).pack(anchor="w",pady=(0,6))
        cols=("ID","User","Subjek","Status","Tanggal")
        self._mtv=self.tree(lp,cols,14,[40,100,220,90,120])
        self._load_pesan()

        tk.Label(rp,text="KIRIM PESAN BARU",font=("Consolas",12,"bold"),bg=C["card"],fg=C["text"]).pack(pady=14)
        tk.Label(rp,text="SUBJEK",font=("Consolas",9),bg=C["card"],fg=C["muted"]).pack(anchor="w",padx=12)
        self._ms=ttk.Entry(rp,width=32); self._ms.pack(padx=12,pady=(3,10),ipady=5)
        tk.Label(rp,text="ISI PESAN",font=("Consolas",9),bg=C["card"],fg=C["muted"]).pack(anchor="w",padx=12)
        self._mi=tk.Text(rp,height=9,width=32,bg=C["inp"],fg=C["text"],insertbackground=C["text"],
                          relief="flat",padx=8,pady=8,font=("Consolas",10))
        self._mi.pack(padx=12,pady=(3,10))
        self.btn(rp,"📤  KIRIM",self._send_pesan,bg=C["warn"],fg="#1F2937",fs=11,pad=(16,10)).pack(padx=12,pady=4)
        if is_adm:
            tk.Frame(rp,bg=C["border"],height=1).pack(fill="x",padx=12,pady=8)
            self.btn(rp,"💬  Balas Terpilih",self._balas_pesan,bg=C["accent"],fs=10,pad=(12,8)).pack(padx=12)

    def _load_pesan(self):
        for i in self._mtv.get_children(): self._mtv.delete(i)
        uid=self.current_user["id"]; is_adm=self.current_user["role"]=="admin"
        for m in reversed(DB["pesan"]):
            if not is_adm and m["user_id"]!=uid: continue
            u=get_user(m["user_id"])
            self._mtv.insert("","end",values=(m["id"],u["username"] if u else "?",m["subjek"],m["status"],m["tanggal"]))

    def _send_pesan(self):
        s=self._ms.get().strip(); i=self._mi.get("1.0","end").strip()
        if not s or not i: messagebox.showwarning("Peringatan","Subjek & isi pesan harus diisi!"); return
        DB["pesan"].append({"id":nid("pesan"),"user_id":self.current_user["id"],
                             "subjek":s,"isi":i,"balasan":"","status":"baru",
                             "tanggal":str(datetime.date.today())})
        self._ms.delete(0,"end"); self._mi.delete("1.0","end")
        messagebox.showinfo("Terkirim","Pesan berhasil dikirim!"); self._load_pesan()

    def _balas_pesan(self):
        sel=self._mtv.selection()
        if not sel: messagebox.showwarning("Peringatan","Pilih pesan terlebih dahulu!"); return
        pid=int(self._mtv.item(sel[0])["values"][0])
        msg=next((m for m in DB["pesan"] if m["id"]==pid),None)
        if not msg: return
        dlg=tk.Toplevel(self); dlg.title("Balas Pesan"); dlg.geometry("450x320")
        dlg.configure(bg=C["bg"]); dlg.grab_set()
        tk.Label(dlg,text=f'Subjek: {msg["subjek"]}',font=("Consolas",11,"bold"),bg=C["bg"],fg=C["text"]).pack(pady=(14,4),padx=22,anchor="w")
        tk.Label(dlg,text=f'Isi: {msg["isi"][:80]}',font=("Consolas",9),bg=C["bg"],fg=C["muted"]).pack(padx=22,anchor="w")
        tk.Label(dlg,text="BALASAN",font=("Consolas",9),bg=C["bg"],fg=C["muted"]).pack(anchor="w",padx=22,pady=(10,0))
        txt=tk.Text(dlg,height=7,bg=C["inp"],fg=C["text"],insertbackground=C["text"],font=("Consolas",10),relief="flat",padx=8,pady=8)
        txt.pack(padx=22,pady=4,fill="both",expand=True)
        if msg["balasan"]: txt.insert("1.0",msg["balasan"])
        def kirim():
            bal=txt.get("1.0","end").strip()
            if not bal: return
            msg["balasan"]=bal; msg["status"]="dibalas"
            messagebox.showinfo("OK","Balasan terkirim!"); dlg.destroy(); self._load_pesan()
        self.btn(dlg,"KIRIM BALASAN",kirim,bg=C["accent2"],fs=11,pad=(16,8)).pack(pady=8)

    # ══════════════════════════════════════════════════
    #  HALAMAN: PEMBAYARAN
    # ══════════════════════════════════════════════════
    def _p_pembayaran(self):
        p=self.content; is_adm=self.current_user["role"]=="admin"
        self.hdr(p,"💳  PEMBAYARAN",C["accent2"])
        body=tk.Frame(p,bg=C["bg"]); body.pack(fill="both",expand=True,padx=14,pady=8)
        tk.Label(body,text="DAFTAR PEMBAYARAN",font=("Consolas",11,"bold"),bg=C["bg"],fg=C["muted"]).pack(anchor="w",pady=(0,6))

        cols=("ID","Kode Tiket","Destinasi","Metode","Jumlah","Status","Tanggal")
        self._ptv=self.tree(body,cols,16,[40,130,180,130,120,90,140])
        uid=self.current_user["id"]
        for r in bayar_rows(None if is_adm else uid):
            pid,kode,nama,met,jml,status,tgl=r
            self._ptv.insert("","end",values=(pid,kode,nama,met,f"Rp {int(jml):,}",status,tgl))

        if is_adm:
            af=tk.Frame(p,bg=C["bg"]); af.pack(fill="x",padx=14,pady=8)
            self.btn(af,"✅  Konfirmasi Lunas",self._konfirmasi_bayar,bg=C["accent2"],fs=11,pad=(18,10)).pack(side="left")
            self.btn(af,"❌  Tolak Pembayaran",self._tolak_bayar,bg=C["danger"],fs=11,pad=(18,10)).pack(side="left",padx=8)

    def _konfirmasi_bayar(self):
        sel=self._ptv.selection()
        if not sel: messagebox.showwarning("Peringatan","Pilih pembayaran terlebih dahulu!"); return
        pid=int(self._ptv.item(sel[0])["values"][0])
        pm=next((x for x in DB["pembayaran"] if x["id"]==pid),None)
        if pm:
            pm["status"]="lunas"
            t=next((x for x in DB["tiket"] if x["id"]==pm["tiket_id"]),None)
            if t: t["status"]="confirmed"
        messagebox.showinfo("Berhasil","Pembayaran dikonfirmasi & tiket aktif!"); self._p_pembayaran()

    def _tolak_bayar(self):
        sel=self._ptv.selection()
        if not sel: messagebox.showwarning("Peringatan","Pilih pembayaran terlebih dahulu!"); return
        pid=int(self._ptv.item(sel[0])["values"][0])
        pm=next((x for x in DB["pembayaran"] if x["id"]==pid),None)
        if pm:
            pm["status"]="ditolak"
            t=next((x for x in DB["tiket"] if x["id"]==pm["tiket_id"]),None)
            if t: t["status"]="cancelled"
        messagebox.showinfo("Info","Pembayaran ditolak."); self._p_pembayaran()

    # ══════════════════════════════════════════════════
    #  HALAMAN: RIWAYAT
    # ══════════════════════════════════════════════════
    def _p_riwayat(self):
        p=self.content; is_adm=self.current_user["role"]=="admin"
        self.hdr(p,"📋  RIWAYAT PEMESANAN","#7C3AED")
        body=tk.Frame(p,bg=C["bg"]); body.pack(fill="both",expand=True,padx=14,pady=8)
        cols=("Kode","Destinasi","Tgl Kunjungan","Jumlah","Total","Status","Dibuat")
        tv=self.tree(body,cols,18,[130,190,120,60,120,100,140])

        uid=self.current_user["id"]
        rows=tiket_rows(None if is_adm else uid)
        for r in rows:
            kode,nama,tgl,jml,total,status,created=r
            tv.insert("","end",values=(kode,nama,tgl,jml,f"Rp {int(total):,}",status,created))

        af=tk.Frame(p,bg=C["bg"]); af.pack(fill="x",padx=14,pady=8)
        self.btn(af,"📥  Export CSV",lambda:self._export(rows),bg=C["card"],fg=C["text"],fs=10,pad=(14,8)).pack(side="left")

    def _export(self,rows):
        path=filedialog.asksaveasfilename(defaultextension=".csv",filetypes=[("CSV","*.csv")],title="Simpan Riwayat")
        if not path: return
        with open(path,"w",encoding="utf-8") as f:
            f.write("Kode,Destinasi,Tgl Kunjungan,Jumlah,Total,Status,Dibuat\n")
            for r in rows: f.write(",".join(str(x) for x in r)+"\n")
        messagebox.showinfo("Berhasil",f"Data diekspor ke:\n{path}")

    # ══════════════════════════════════════════════════
    #  HALAMAN: PROFILE
    # ══════════════════════════════════════════════════
    def _p_profile(self):
        p=self.content; u=self.current_user
        self.hdr(p,"👤  PROFILE PENGGUNA","#374151")
        body=tk.Frame(p,bg=C["bg"]); body.pack(fill="both",expand=True)
        center=tk.Frame(body,bg=C["card"]); center.pack(expand=True,pady=36,padx=120,fill="both")

        row=get_user(u["id"])
        tk.Label(center,text="👤",font=("Segoe UI Emoji",52),bg=C["card"]).pack(pady=(28,4))
        tk.Label(center,text=u["username"].upper(),font=("Consolas",22,"bold"),bg=C["card"],fg=C["text"]).pack()
        rc=C["warn"] if u["role"]=="admin" else C["accent2"]
        tk.Label(center,text=f"● {u['role'].upper()}",font=("Consolas",10),bg=C["card"],fg=rc).pack(pady=4)
        tk.Frame(center,bg=C["border"],height=1).pack(fill="x",padx=60,pady=14)

        for lab,key in [("Email","email"),("Telepon","phone"),("Bergabung","created_at")]:
            rf=tk.Frame(center,bg=C["card"]); rf.pack(fill="x",padx=60,pady=4)
            tk.Label(rf,text=lab+":",font=("Consolas",10),bg=C["card"],fg=C["muted"],width=12,anchor="w").pack(side="left")
            tk.Label(rf,text=row.get(key) or "-",font=("Consolas",10,"bold"),bg=C["card"],fg=C["text"]).pack(side="left")

        tk.Frame(center,bg=C["border"],height=1).pack(fill="x",padx=60,pady=14)
        self.btn(center,"✏️  Edit Profile",self._dlg_edit_profile,bg=C["accent"],fs=11,pad=(20,10)).pack(pady=(0,28))

    def _dlg_edit_profile(self):
        row=get_user(self.current_user["id"])
        dlg=tk.Toplevel(self); dlg.title("Edit Profile"); dlg.geometry("420x340")
        dlg.configure(bg=C["bg"]); dlg.grab_set()
        tk.Label(dlg,text="EDIT PROFILE",font=("Consolas",14,"bold"),bg=C["bg"],fg=C["text"]).pack(pady=14)
        ent={}
        for lab,key,hide in [("Email","email",False),("Telepon","phone",False),("Password Baru",None,True)]:
            tk.Label(dlg,text=lab.upper(),font=("Consolas",9),bg=C["bg"],fg=C["muted"]).pack(anchor="w",padx=34)
            e=ttk.Entry(dlg,width=38,show="●" if hide else "")
            if key and row.get(key): e.insert(0,row[key])
            e.pack(padx=34,ipady=5,pady=(2,10)); ent[lab]=e
        def save():
            row["email"]=ent["Email"].get(); row["phone"]=ent["Telepon"].get()
            pw=ent["Password Baru"].get()
            if pw: row["password"]=hash_pw(pw)
            messagebox.showinfo("Berhasil","Profile berhasil diperbarui!"); dlg.destroy()
        self.btn(dlg,"SIMPAN PERUBAHAN",save,bg=C["accent2"],fs=11,pad=(20,10)).pack(pady=8)

    # ══════════════════════════════════════════════════
    #  HALAMAN: TRACKING (Admin)
    # ══════════════════════════════════════════════════
    def _p_tracking(self):
        p=self.content
        self.hdr(p,"📊  TRACKING PENGUNJUNG","#DC2626","🔄  Refresh",self._p_tracking)

        body=tk.Frame(p,bg=C["bg"]); body.pack(fill="both",expand=True,padx=14,pady=8)
        today=str(datetime.date.today()); logs=DB["visitor_log"]
        tv        = len(logs)
        tv_today  = len([l for l in logs if l["waktu"].startswith(today)])
        unik_today= len(set(l["user_id"] for l in logs if l["waktu"].startswith(today)))
        total_bk  = len([l for l in logs if "booking" in l["action"]])

        # Stat strip
        sf=tk.Frame(body,bg=C["bg"]); sf.pack(fill="x",pady=(0,12))
        for lab,val,col in [("Total Login",tv,"#DC2626"),("Login Hari Ini",tv_today,C["warn"]),
                             ("User Aktif Hari Ini",unik_today,C["accent"]),("Total Booking",total_bk,C["accent2"])]:
            cd=tk.Frame(sf,bg=C["card"]); cd.pack(side="left",expand=True,fill="both",padx=4)
            tk.Frame(cd,bg=col,height=4).pack(fill="x")
            tk.Label(cd,text=str(val),font=("Consolas",28,"bold"),bg=C["card"],fg=col).pack(pady=(10,0))
            tk.Label(cd,text=lab,font=("Consolas",9),bg=C["card"],fg=C["muted"]).pack(pady=(0,10))

        # Ringkasan per user
        tk.Label(body,text="RINGKASAN PER USER",font=("Consolas",11,"bold"),bg=C["bg"],fg=C["muted"]).pack(anchor="w",pady=(0,6))
        utv=self.tree(body,("Username","Role","Total Login","Total Booking","Bergabung"),5,[160,80,120,120,130])
        for u in DB["users"]:
            ul=[l for l in logs if l["user_id"]==u["id"]]
            utv.insert("","end",values=(u["username"],u["role"],
                len([l for l in ul if l["action"]=="login"]),
                len([l for l in ul if "booking" in l["action"]]),
                u["created_at"]))

        # Log aktivitas
        tk.Label(body,text="LOG AKTIVITAS TERBARU",font=("Consolas",11,"bold"),bg=C["bg"],fg=C["muted"]).pack(anchor="w",pady=(10,6))
        ltv=self.tree(body,("ID","User","Aksi","Waktu"),7,[50,130,250,160])
        for l in reversed(logs[-100:]):
            u=get_user(l["user_id"])
            ltv.insert("","end",values=(l["id"],u["username"] if u else "?",l["action"],l["waktu"]))


# ══════════════════════════════════════════════════════
if __name__ == "__main__":
    app = App()
    app.mainloop()