import tkinter as tk
from tkinter import messagebox
import datetime
import logging
import os
import re

# Setup logging
logging.basicConfig(
    filename='aplikasi_biodata.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Membuat kelas utama aplikasi yang mewarisi dari tk.Tk
class AplikasiBiodata(tk.Tk):
    
    def __init__(self):
            # Memanggil constructor dari kelas induk (tk.Tk)
            super().__init__()
            
            # Mengkonfigurasi window utama
            self.title("Aplikasi Biodata Mahasiswa")
            self.geometry("600x700")
            self.resizable(True, True)
            
            # Database user sederhana (dalam aplikasi nyata ini akan di database)
            
            self.users_db = {
                "admin": "123",
                "user1": "password1",
                "mahasiswa": "123456"
            }
            
            
            # Status login
            self.current_user = None
            
             # Atribut untuk manajemen frame
            self.frame_aktif = None

            self.error_entries = set()
            # Buat tampilan
            self._buat_tampilan_login()
            self._muat_remember_me()   # Tambahkan baris ini
            self.password_visible = False  # State: password sedang tersembunyi
            self._buat_tampilan_biodata()
    
            # Tampilkan frame login di awal
            self._pindah_ke(self.frame_login)
            
            # Log aplikasi start
            logging.info("Application started")
            
    def _coba_login(self):
        """Method untuk memproses attempt login dengan logging"""
        username = self.entry_username.get().strip()
        password = self.entry_password.get()

        # Log attempt login
        logging.info(f"Login attempt for username: {username}")

        # Validasi input kosong
        if not username or not password:
            logging.warning(f"Empty credentials attempt for username: {username}")
            messagebox.showwarning("Login Gagal", "Username dan Password tidak boleh kosong.")
            self.entry_username.focus_set()
            return

        # Validasi panjang minimum
        if len(username) < 3:
            logging.warning(f"Username too short: {username}")
            messagebox.showwarning("Login Gagal", "Username minimal 3 karakter.")
            self.entry_username.focus_set()
            return

        # Cek kredensial di database
        if username in self.users_db and self.users_db[username] == password:
            self.current_user = username
            logging.info(f"Successful login for user: {username}")
            messagebox.showinfo("Login Berhasil", f"Selamat Datang, {username}!")
            
            self._simpan_remember_me(username)
            self._reset_form_biodata()
            self._update_title_with_user()
            self._pindah_ke(self.frame_biodata)
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
        else:
            logging.warning(f"Failed login attempt for username: {username}")
            messagebox.showerror("Login Gagal", "Username atau Password salah.")
            self.entry_password.delete(0, tk.END)
            self.entry_username.focus_set()
            
        self._update_color_with_user()
        self._pindah_ke(self.frame_biodata)
        # Membuat menu
        self._buat_menu()
            
    def _reset_form_biodata(self):
        """Reset semua field di form biodata"""
        self.var_nama.set("")
        self.var_nim.set("")
        self.var_jurusan.set("")
        self.text_alamat.delete("1.0", tk.END)
        self.var_jk.set("Pria")
        self.var_setuju.set(0)
        self.var_email.set("")
        self.var_telp.set("")
        self.var_tgllahir.set("")
        self.label_hasil.config(text="")
        if hasattr(self, "btn_reset"):
            self.btn_reset.config(state=tk.DISABLED)

    def _update_title_with_user(self):
        """Update judul window dengan nama user yang login"""
        if self.current_user:
            self.title(f"Aplikasi Biodata Mahasiswa - User: {self.current_user}")
        else:
            self.title("Aplikasi Biodata Mahasiswa")
            
    def _update_color_with_user(self):
        """Update background biodata sesuai user yang login."""
        warna_user = {'admin' : 'lightgreen', 
                      'user1' : 'lightblue',
                      'mahasiswa' : 'plum'}
        warna = warna_user.get(self.current_user, "plum")
        self.frame_biodata.config(bg=warna)
            
    def _logout(self):
        """Method untuk logout dengan logging"""
        if messagebox.askyesno("Logout", f"Apakah {self.current_user} yakin ingin logout?"):
            logging.info(f"User logout: {self.current_user}")
            # Reset status user
            self.current_user = None
            # Update title
            self._update_title_with_user()
            # Bersihkan field login
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            # Reset form biodata
            self._reset_form_biodata()
            # Kembali ke halaman login
            self._pindah_ke(self.frame_login)
            # Focus ke username field
            self.entry_username.focus_set()
            
    def keluar_aplikasi(self):
        """Keluar dari aplikasi dengan konfirmasi"""
        if messagebox.askokcancel("Keluar", "Apakah Anda yakin ingin keluar dari aplikasi?"):
            logging.info(f"Application closed by user: {self.current_user}")
            self.destroy()
            
            
    def _buat_tampilan_biodata(self):
            # --- Variabel Kontrol Tkinter ---
            self.var_nama = tk.StringVar()
            self.var_nim = tk.StringVar()
            self.var_jurusan = tk.StringVar()
            self.var_jk = tk.StringVar(value="Pria")
            self.var_setuju = tk.IntVar()
            
            # --- Variabel Kontrol Tambahan ---
            self.var_email = tk.StringVar()
            self.var_telp = tk.StringVar()
            self.var_tgllahir = tk.StringVar()

            for variable in (
                self.var_nama,
                self.var_nim,
                self.var_jurusan,
                self.var_email,
                self.var_telp,
                self.var_tgllahir,
            ):
                variable.trace_add("write", self.validate_form)
           
    
            # --- Frame Biodata ---
            self.frame_biodata = tk.Frame(master=self, padx=20, pady=20)
            self.frame_biodata.columnconfigure(1, weight=1)
    
            # Judul
            self.label_judul = tk.Label(
                master=self.frame_biodata, 
                text="FORM BIODATA MAHASISWA", 
                font=("Arial", 16, "bold")
            )
            self.label_judul.grid(row=0, column=0, columnspan=2, pady=20)
            
            # --- Membuat dan Menempatkan Widget ---
    
            # Frame khusus untuk input dengan border
            self.frame_input = tk.Frame(
                master=self.frame_biodata, 
                relief=tk.GROOVE, 
                borderwidth=2, 
                padx=10, 
                pady=10
            )
    
            # Input Nama
            self.label_nama = tk.Label(
                master=self.frame_input, 
                text="Nama Lengkap:", 
                font=("Arial", 12)
            )
            self.label_nama.grid(row=0, column=0, sticky="W", pady=2)
            self.entry_nama = tk.Entry(
                master=self.frame_input, 
                width=30, 
                font=("Arial", 12), 
                textvariable=self.var_nama
            )
            self.entry_nama.grid(row=0, column=1, pady=2)
    
            # Input NIM
            self.label_nim = tk.Label(
                master=self.frame_input, 
                text="NIM:", 
                font=("Arial", 12)
            )
            self.label_nim.grid(row=1, column=0, sticky="W", pady=2)
            self.entry_nim = tk.Entry(
                master=self.frame_input, 
                width=30, 
                font=("Arial", 12), 
                textvariable=self.var_nim
            )
            self.entry_nim.grid(row=1, column=1, pady=2)
            
            # Input Jurusan
            self.label_jurusan = tk.Label(
                master=self.frame_input, 
                text="Jurusan:", 
                font=("Arial", 12)
            )
            self.label_jurusan.grid(row=2, column=0, sticky="W", pady=2)
            self.entry_jurusan = tk.Entry(
                master=self.frame_input, 
                width=30, 
                font=("Arial", 12), 
                textvariable=self.var_jurusan
            )
            self.entry_jurusan.grid(row=2, column=1, pady=2)
    
            # Input alamat dengan Text widget
            self.label_alamat = tk.Label(
                master=self.frame_input, 
                text="Alamat:", 
                font=("Arial", 12)
            )
            self.label_alamat.grid(row=3, column=0, sticky="NW", pady=2)
    
            # Frame untuk Text dan Scrollbar
            self.frame_alamat = tk.Frame(
                master=self.frame_input, 
                relief=tk.SUNKEN, 
                borderwidth=1
            )
    
            # Scrollbar untuk alamat
            self.scrollbar_alamat = tk.Scrollbar(master=self.frame_alamat)
            self.scrollbar_alamat.pack(side=tk.RIGHT, fill=tk.Y)
    
            # Text widget untuk alamat
            self.text_alamat = tk.Text(
                master=self.frame_alamat, 
                height=5, 
                width=28, 
                font=("Arial", 12)
            )
            self.text_alamat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
            # Hubungkan scrollbar dengan text
            self.scrollbar_alamat.config(command=self.text_alamat.yview)
            self.text_alamat.config(yscrollcommand=self.scrollbar_alamat.set)
    
            self.frame_alamat.grid(row=3, column=1, pady=2)

            # --- Input Email ---
            tk.Label(
            master=self.frame_input,
            text="Email:",
            font=("Arial", 12)
            ).grid(row=4, column=0, sticky="W", pady=2)
            self.entry_email = tk.Entry(
                master=self.frame_input,
                width=30,
                font=("Arial", 12),
                textvariable=self.var_email
            )
            self.entry_email.grid(row=4, column=1, pady=2)

            # --- Input Telepon ---
            tk.Label(
            master=self.frame_input,
            text="Telepon:",
            font=("Arial", 12)
            ).grid(row=5, column=0, sticky="W", pady=2)
            self.entry_telp = tk.Entry(
                master=self.frame_input,
                width=30,
                font=("Arial", 12),
                textvariable=self.var_telp
            )
            self.entry_telp.grid(row=5, column=1, pady=2)

            # --- Input Tanggal Lahir ---
            tk.Label(
            master=self.frame_input,
            text="Tanggal Lahir (DD/MM/YYYY):",
            font=("Arial", 12)
            ).grid(row=6, column=0, sticky="W", pady=2)
            self.entry_tgllahir = tk.Entry(
                master=self.frame_input,
                width=30,
                font=("Arial", 12),
                textvariable=self.var_tgllahir
            )
            self.entry_tgllahir.grid(row=6, column=1, pady=2)

            # Jenis kelamin
            self.label_jk = tk.Label(
                master=self.frame_input, 
                text="Jenis Kelamin:", 
                font=("Arial", 12)
            )
            self.label_jk.grid(row=7, column=0, sticky="W", pady=2)
    
            self.frame_jk = tk.Frame(master=self.frame_input)
            self.frame_jk.grid(row=7, column=1, sticky="W")
    
            self.radio_pria = tk.Radiobutton(
                master=self.frame_jk, 
                text="Pria", 
                variable=self.var_jk, 
                value="Pria"
            )
            self.radio_pria.pack(side=tk.LEFT)
            self.radio_wanita = tk.Radiobutton(
                master=self.frame_jk, 
                text="Wanita", 
                variable=self.var_jk, 
                value="Wanita"
            )
            self.radio_wanita.pack(side=tk.LEFT)
    
            # Checkbox persetujuan
            self.check_setuju = tk.Checkbutton(
                master=self.frame_input,
                text="Saya menyetujui pengumpulan data ini.",
                variable=self.var_setuju,
                font=("Arial", 10),
                command=self.validate_form
            )
            self.check_setuju.grid(row=8, column=0, columnspan=2, pady=10, sticky="W")
    
            self.frame_input.grid(row=1, column=0, columnspan=2, sticky="EW")
            
            # Tombol submit
            self.btn_submit = tk.Button(
                master=self.frame_biodata, 
                text="Submit Biodata", 
                font=("Arial", 12, "bold"),
                command=self.submit_data,
                state=tk.DISABLED
            )
            self.btn_submit.grid(row=6, column=0, columnspan=2, pady=20, sticky="EW")
    
            # Event bindings untuk hover dan keyboard shortcuts
            self.btn_submit.bind("<Enter>", self.on_enter)
            self.btn_submit.bind("<Leave>", self.on_leave)
    
            # Keyboard shortcuts
            self.entry_nama.bind("<Return>", self.submit_shortcut)
            self.entry_nim.bind("<Return>", self.submit_shortcut)
            self.entry_jurusan.bind("<Return>", self.submit_shortcut)
            self.text_alamat.bind("<Return>", self.submit_shortcut)
            
            # Tombol Reset Form
            self.btn_reset = tk.Button(
                master=self.frame_biodata,
                text="Reset Form",
                font=("Arial", 12, "bold"),
                bg="#e74c3c",
                fg="black",
                command=self._on_reset_form,
                state=tk.DISABLED
            )
            self.btn_reset.grid(
                row=7, column=0, columnspan=2,
                pady=(0, 10), sticky="EW"
            )

            # Event bindings untuk hover reset button
            self.btn_reset.bind("<Enter>", self.on_enter_reset)
            self.btn_reset.bind("<Leave>", self.on_leave_reset)
    
            # Label hasil
            self.label_hasil = tk.Label(
                master=self.frame_biodata, 
                text="", 
                font=("Arial", 12, "italic"), 
                justify=tk.LEFT
            )
            self.label_hasil.grid(row=8, column=0, columnspan=2, sticky="W", padx=10)
            
    def _on_reset_form(self):
        """Reset form dengan konfirmasi user."""
        if self.btn_reset["state"] == tk.DISABLED:
            return
        if messagebox.askyesno(
            "Reset Form",
            "Apakah Anda yakin ingin mereset seluruh form?"
        ):
            self._reset_form_biodata()
            # Bersihkan juga error highlighting
            self.error_entries.clear()
            for entry in (
                self.entry_nama,
                self.entry_nim,
                self.entry_jurusan,
                self.entry_email,
                self.entry_telp,
                self.entry_tgllahir,
            ):
                self._atur_border_entry(entry)
            self.entry_nama.focus_set()
            logging.info(f"Form reset by user: {self.current_user}")
            
        # Metode __init__ adalah constructor yang akan dijalankan saat objek dibuat
        
    def _buat_menu(self):
        """Membuat menu bar untuk aplikasi"""
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)

        file_menu = tk.Menu(master=menu_bar, tearoff=0)
        file_menu.add_command(label="Simpan Hasil", command=self.simpan_hasil)
        file_menu.add_separator()
        file_menu.add_command(label="Logout", command=self._logout)
        file_menu.add_separator()
        file_menu.add_command(label="Keluar", command=self.keluar_aplikasi)

        menu_bar.add_cascade(label="File", menu=file_menu)
        
    def _hapus_menu(self):
        """Menghapus menu bar dari window."""
        empty_menu = tk.Menu(self)
        self.config(menu=empty_menu)
    
    def _buat_tampilan_login(self):
            self.frame_login = tk.Frame(master=self, padx=20, pady=100)
    
            # Konfigurasi grid untuk frame login agar terpusat
            self.frame_login.grid_columnconfigure(0, weight=1)
            self.frame_login.grid_columnconfigure(1, weight=1)
    
            # Judul Login
            tk.Label(
                self.frame_login, 
                text="HALAMAN LOGIN", 
                font=("Arial", 16, "bold")
            ).grid(row=0, column=0, columnspan=2, pady=20)
    
            # Input Username
            tk.Label(
                self.frame_login, 
                text="Username:", 
                font=("Arial", 12)
            ).grid(row=1, column=0, sticky="W", pady=5)
    
            self.entry_username = tk.Entry(self.frame_login, font=("Arial", 12))
            self.entry_username.grid(row=1, column=1, pady=5, sticky="EW")
            
            # Input Password
            tk.Label(
                self.frame_login, 
                text="Password:", 
                font=("Arial", 12)
            ).grid(row=2, column=0, sticky="W", pady=5)
    
            self.entry_password = tk.Entry(
                self.frame_login, 
                font=("Arial", 12), 
                show="*"
            )
            self.entry_password.grid(row=2, column=1, pady=5, sticky="EW")
            
            # Tombol Show/Hide Password
            self.btn_toggle_pw = tk.Button(
                self.frame_login,
                text="👁",
                font=("Arial", 10),
                width=3,
                command=self._toggle_password
            )
            self.btn_toggle_pw.grid(
                row=2, column=2, pady=5, padx=(5, 0)
            )
    
            # Tombol Login
            self.btn_login = tk.Button(
                self.frame_login, 
                text="Login", 
                font=("Arial", 12, "bold"),
                command=self._coba_login
            )
            self.btn_login.grid(row=3, column=0, columnspan=2, pady=20, sticky="EW")
    
            # Keyboard shortcuts untuk login
            self.entry_username.bind("<Return>", lambda e: self.entry_password.focus_set())
            self.entry_password.bind("<Return>", lambda e: self._coba_login())
            
            # --- Remember Me ---
            self.var_remember = tk.IntVar()
            self.check_remember = tk.Checkbutton(
                self.frame_login,
                text="Remember Me",
                variable=self.var_remember,
                font=("Arial", 10)
            )
            self.check_remember.grid(
                row=4, column=0, columnspan=2,
                pady=5, sticky="W"
            )
    
            # Info untuk user
            info_label = tk.Label(
                self.frame_login,
                text="Info: Username yang tersedia:\nadmin (password: 123)\nuser1 (password: password1)\nmahasiswa (password: 123456)",
                font=("Arial", 9),
                fg="gray",
                justify=tk.LEFT
            )
            info_label.grid(row=5, column=0, columnspan=2, pady=10)
            
    def _simpan_remember_me(self, username):
        """Simpan username ke file jika Remember Me dicentang."""
        if self.var_remember.get() == 1:
            with open("remember_me.txt", "w") as f:
                f.write(username)
            logging.info(f"Remember Me: username '{username}' disimpan")
        else:
            # Hapus file jika ada
            if os.path.exists("remember_me.txt"):
                os.remove("remember_me.txt")
            logging.info("Remember Me: file dihapus")

    def _muat_remember_me(self):
        """Muat username dari file jika ada."""
        if os.path.exists("remember_me.txt"):
            with open("remember_me.txt", "r") as f:
                username = f.read().strip()
            if username:
                self.entry_username.insert(0, username)
                self.var_remember.set(1)
                self.entry_password.focus_set()
                logging.info(f"Remember Me: username '{username}' dimuat")
                
    def _toggle_password(self):
        """Toggle tampilan password antara tersembunyi dan terlihat."""
        if self.password_visible:
            # Sembunyikan password
            self.entry_password.config(show="*")
            self.btn_toggle_pw.config(text="👁")
            self.password_visible = False
        else:
            # Tampilkan password
            self.entry_password.config(show="")
            self.btn_toggle_pw.config(text="🔒")
            self.password_visible = True
    
    def submit_data(self):
        """Submit data biodata dengan validasi lengkap"""
        try:
            # Cek checkbox
            if self.var_setuju.get() == 0:
                messagebox.showwarning("Peringatan", "Anda harus menyetujui pengumpulan data!")
                return

            # Ambil data dari form
            nama = self.entry_nama.get().strip()
            nim = self.entry_nim.get().strip()
            jurusan = self.entry_jurusan.get().strip()
            alamat = self.text_alamat.get("1.0", tk.END).strip()
            jenis_kelamin = self.var_jk.get()

            # Validasi field kosong
            if not nama or not nim or not jurusan:
                # self.entry_nama.config(bg="misty rose")
                messagebox.showwarning("Input Kosong", "Nama, NIM, dan Jurusan harus diisi!")
                if not nama:
                    self._tandai_error_entry("nama", self.entry_nama)
                if not nim:
                    self._tandai_error_entry("nim", self.entry_nim)
                if not jurusan:
                    self._tandai_error_entry("jurusan", self.entry_jurusan)
                return
            # Validasi format NIM (harus angka dan minimal 8 digit)
            if not nim.isdigit() or len(nim) < 8:
                messagebox.showwarning("Format NIM Salah", "NIM harus berupa angka minimal 8 digit!")
                self._tandai_error_entry("nim", self.entry_nim)
                self.entry_nim.focus_set()
                return

            # Validasi nama (tidak boleh hanya angka)
            if nama.isdigit():
                messagebox.showwarning("Format Nama Salah", "Nama tidak boleh hanya berupa angka!")
                self._tandai_error_entry("nama", self.entry_nama)
                self.entry_nama.focus_set()
                return

            # Validasi email
            if not self._validasi_email(self.var_email.get().strip()):
                messagebox.showwarning("Format Email Salah", "Masukkan format email yang valid (contoh: user@domain.com)!")
                self._tandai_error_entry("email", self.entry_email)
                self.entry_email.focus_set()
                return

            # Validasi telepon
            if not self._validasi_telepon(self.var_telp.get().strip()):
                messagebox.showwarning("Format Telepon Salah", "Masukkan format telepon Indonesia yang valid (+62/08xx, minimal 10 digit)!")
                self._tandai_error_entry("telp", self.entry_telp)
                self.entry_telp.focus_set()
                return

            # Validasi tanggal lahir
            if not self._validasi_tanggal(self.var_tgllahir.get().strip()):
                messagebox.showwarning("Format Tanggal Salah", "Masukkan tanggal lahir dengan format DD/MM/YYYY yang valid!")
                self._tandai_error_entry("tgllahir", self.entry_tgllahir)
                self.entry_tgllahir.focus_set()
                return

            # Tampilkan hasil
            email = self.var_email.get().strip()
            telp = self.var_telp.get().strip()
            tgllahir = self.var_tgllahir.get().strip()
            hasil = (f"Nama: {nama}\nNIM: {nim}\nJurusan: {jurusan}\n"
                     f"Alamat: {alamat}\nJenis Kelamin: {jenis_kelamin}\n"
                     f"Email: {email}\nTelepon: {telp}\nTanggal Lahir: {tgllahir}")
            messagebox.showinfo("Data Tersimpan", hasil)

            # Tampilkan hasil di label dengan info user
            hasil_lengkap = f"BIODATA TERSIMPAN:\nDiinput oleh: {self.current_user}\n\n{hasil}"
            self.label_hasil.config(text=hasil_lengkap)
            self.btn_reset.config(state=tk.NORMAL)

            # Log successful data submission
            logging.info(f"Data submitted by user: {self.current_user} - NIM: {nim}")

        except Exception as e:
            logging.error(f"Error in submit_data by {self.current_user}: {str(e)}")
            messagebox.showerror("Error", f"Terjadi kesalahan saat memproses data:\n{str(e)}")
            
    def simpan_hasil(self):
        """Simpan hasil biodata ke file dengan error handling"""
        try:
            hasil_tersimpan = self.label_hasil.cget("text")

            if not hasil_tersimpan or "BIODATA TERSIMPAN" not in hasil_tersimpan:
                messagebox.showwarning("Peringatan", "Tidak ada data untuk disimpan. Mohon submit terlebih dahulu.")
                return

            # Buat nama file dengan timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"biodata_{self.current_user}_{timestamp}.txt"

            with open(filename, "w", encoding="utf-8") as file:
                file.write(f"Data disimpan oleh: {self.current_user}\n")
                file.write(f"Waktu penyimpanan: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write("-" * 50 + "\n")
                file.write(hasil_tersimpan)

            messagebox.showinfo("Info", f"Data berhasil disimpan ke file '{filename}'.")

        except PermissionError:
            messagebox.showerror("Error", "Tidak memiliki izin untuk menyimpan file di lokasi ini.")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat menyimpan file:\n{str(e)}")
            
    def _atur_border_entry(self, entry, error=False):
        if error:
            entry.config(
                bg="misty rose",
                highlightthickness=2,
                highlightbackground="#d32f2f",
                highlightcolor="#d32f2f"
            )
        else:
            entry.config(
                bg="SystemButtonFace",
                highlightthickness=0
            )
        
    def _tandai_error_entry(self, nama_field, entry):
        self.error_entries.add(nama_field)
        self._atur_border_entry(entry, error=True)

    def _validasi_email(self, email):
        """Validasi format email sederhana."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{3,}$'
        return re.match(pattern, email) is not None

    def _validasi_telepon(self, telp):
        """Validasi format telepon Indonesia."""
        # Format: +62xxxxxxxxxx, 08xxxxxxxxxx, atau 62xxxxxxxxxx
        pattern = r'^(\+62|62|0)8[0-9]{8,11}$'
        return re.match(pattern, telp) is not None

    def _validasi_tanggal(self, tanggal):
        """Validasi format DD/MM/YYYY dan tanggal benar."""
        try:
            datetime.datetime.strptime(tanggal, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    def validate_form(self, *args):
        nama = self.var_nama.get().strip()
        nim = self.var_nim.get().strip()
        jurusan = self.var_jurusan.get().strip()

        nama_valid = bool(nama) and not nama.isdigit()
        nim_valid = nim.isdigit() and len(nim) >= 8
        jurusan_valid = bool(jurusan)
        setuju_valid = self.var_setuju.get() == 1
        email_valid = self._validasi_email(self.var_email.get().strip())
        telp_valid = self._validasi_telepon(self.var_telp.get().strip())
        tgl_valid = self._validasi_tanggal(self.var_tgllahir.get().strip())

        field_states = {
            "nama": (self.entry_nama, nama_valid),
            "nim": (self.entry_nim, nim_valid),
            "jurusan": (self.entry_jurusan, jurusan_valid),
            "email": (self.entry_email, email_valid),
            "telp": (self.entry_telp, telp_valid),
            "tgllahir": (self.entry_tgllahir, tgl_valid),
        }

        for nama_field, (entry, valid) in field_states.items():
            if nama_field in self.error_entries and valid:
                self._atur_border_entry(entry)
                self.error_entries.remove(nama_field)

        all_valid = (nama_valid and nim_valid and jurusan_valid and
                     setuju_valid and email_valid and telp_valid and tgl_valid)
        self.btn_submit.config(
            state=tk.NORMAL if setuju_valid else tk.DISABLED
        )

    # def validate_form(self, *args):
    #     nama_valid = self.var_nama.get().strip() != ""
    #     nim_valid = self.var_nim.get().strip() != ""
    #     jurusan_valid = self.var_jurusan.get().strip() != ""
    #     setuju_valid = self.var_setuju.get() == 1

    #     if nama_valid and nim_valid and jurusan_valid and setuju_valid:
    #         self.btn_submit.config(state=tk.NORMAL)
    #     else:
    #         self.btn_submit.config(state=tk.DISABLED)
            
    def on_enter(self, event):
        if self.btn_submit['state'] == tk.NORMAL:
            self.btn_submit.config(bg="lightgray")

    def on_leave(self, event):
        self.btn_submit.config(bg="SystemButtonFace")

    def on_enter_reset(self, event):
        if self.btn_reset['state'] == tk.NORMAL:
            self.btn_reset.config(bg="#c0392b")

    def on_leave_reset(self, event):
        self.btn_reset.config(bg="#e74c3c")

    def submit_shortcut(self, event=None):
        if self.btn_submit['state'] == tk.NORMAL:
            self.submit_data()
    
    def _pindah_ke(self, frame_tujuan):
        """Method untuk berpindah antar tampilan"""
        if self.frame_aktif is not None:
            self.frame_aktif.pack_forget()

        self.frame_aktif = frame_tujuan
        self.frame_aktif.pack(fill=tk.BOTH, expand=True)

        # Auto-focus berdasarkan frame yang ditampilkan
        if frame_tujuan == self.frame_login:
            self.after(100, lambda: self.entry_username.focus_set())
        elif frame_tujuan == self.frame_biodata:
            self.after(100, lambda: self.entry_nama.focus_set())
          
            
        # (Di sini kita akan meletakkan semua kode GUI nantinya)
        
# Blok berikut hanya akan dieksekusi jika file ini dijalankan secara langsung

if __name__ == "__main__":
    # Membuat instance dari kelas aplikasi kita
    app = AplikasiBiodata()
    # Menjalankan mainloop dari instance tersebut
    app.mainloop()
    
    