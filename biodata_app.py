# Mengimpor library tkinter
import tkinter as tk
from tkinter import messagebox

# def submit_data():
#     # Cek Checkbox
#     if var_setuju.get() == 0:
#         messagebox.showwarning("Peringatan", "Anda harus menyetujui pengumpulan data!")
#         return
    
#     # Ambil data dari form
#     nama = entry_nama.get()
#     nim = entry_nim.get()
#     jurusan = entry_jurusan.get()
#     jenis_kelamin = var_jk.get()
    
#     # Cek field kosong
#     if not nama or not nim or not jurusan:
#         messagebox.showwarning("Input Kosong", "Semua field harus diisi!")
#         return
    
#     # Tampilkan Hasil
#     hasil = f"Nama: {nama}\nNIM: {nim}\nJurusan: {jurusan}\nJenis Kelamin: {jenis_kelamin}"
#     messagebox.showinfo("Data Tersimpan", hasil)

def submit_data():
    if var_setuju.get() == 0:
        messagebox.showwarning("Peringatan", "Anda harus menyetujui pengumpulan data!")
        return

    nama = entry_nama.get()
    nim = entry_nim.get()
    jurusan = entry_jurusan.get()
    alamat = text_alamat.get("1.0", tk.END).strip()  # Baris baru ini
    jenis_kelamin = var_jk.get()

    if not nama or not nim or not jurusan or not alamat:  # Tambahkan alamat
        messagebox.showwarning("Input Kosong", "Semua field harus diisi!")
        return

    hasil = f"Nama: {nama}\nNIM: {nim}\nJurusan: {jurusan}\nAlamat: {alamat}\nJenis Kelamin: {jenis_kelamin}"
    messagebox.showinfo("Data Tersimpan", hasil)

# Membuat jendela utama
window = tk.Tk()

# Memberikan judul pada jendela
window.title("Form Biodata Mahasiswa")

# Mengatur ukuran jendela (lebar x tinggi)
window.geometry("500x600")

# Mencegah jendela dapat diubah ukurannya
window.resizable(True,True)
window.minsize(500, 600)

# Geometry Manager Grid : Membuat Frame Utama

main_frame = tk.Frame(master=window, padx=20, pady=20)
main_frame.pack(fill=tk.BOTH, expand=True)

# Variabel untuk radiobutton jenis kelamin
var_jk = tk.StringVar(value="Pria")


# Judul Menggunakan Grid
label_judul = tk.Label(master=main_frame, text="FORM BIODATA MAHASISWA", font=("Arial", 16, "bold"))
label_judul.grid(row=0, column=0, columnspan=2, pady=20)

# Frame khusus untuk input dengan border
frame_input = tk.Frame(master=main_frame, relief=tk.GROOVE, borderwidth=2, padx=10, pady=10)

# Input nama di dalam frame_input
label_nama = tk.Label(master=frame_input, text="Nama Lengkap:", font=("Arial", 12))
label_nama.grid(row=0, column=0, sticky="W", pady=2)
entry_nama = tk.Entry(master=frame_input, width=30, font=("Arial", 12))
entry_nama.grid(row=0, column=1, pady=2)

# Input NIM di dalam frame_input
label_nim = tk.Label(master=frame_input, text="NIM:", font=("Arial", 12))
label_nim.grid(row=1, column=0, sticky="W", pady=2)
entry_nim = tk.Entry(master=frame_input, width=30, font=("Arial", 12))
entry_nim.grid(row=1, column=1, pady=2)

# Input Jurusan di dalam frame_input
label_jurusan = tk.Label(master=frame_input, text="Jurusan:", font=("Arial", 12))
label_jurusan.grid(row=2, column=0, sticky="W", pady=2)
entry_jurusan = tk.Entry(master=frame_input, width=30, font=("Arial", 12))
entry_jurusan.grid(row=2, column=1, pady=2)

# Input alamat dengan Text widget
label_alamat = tk.Label(master=frame_input, text="Alamat:", font=("Arial", 12))
label_alamat.grid(row=3, column=0, sticky="NW", pady=2)

# Frame untuk Text dan Scrollbar
frame_alamat = tk.Frame(master=frame_input, relief=tk.SUNKEN, borderwidth=1)

# Scrollbar untuk alamat
scrollbar_alamat = tk.Scrollbar(master=frame_alamat)
scrollbar_alamat.pack(side=tk.RIGHT, fill=tk.Y)

# Text widget untuk alamat
text_alamat = tk.Text(master=frame_alamat, height=5, width=28, font=("Arial", 12))
text_alamat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Hubungkan scrollbar dengan text
scrollbar_alamat.config(command=text_alamat.yview)
text_alamat.config(yscrollcommand=scrollbar_alamat.set)

frame_alamat.grid(row=3, column=1, pady=2)

# Jenis kelamin di dalam frame_input
label_jk = tk.Label(master=frame_input, text="Jenis Kelamin:", font=("Arial", 12))
label_jk.grid(row=4, column=0, sticky="W", pady=2)

frame_jk = tk.Frame(master=frame_input)
frame_jk.grid(row=4, column=1, sticky="W")

radio_pria = tk.Radiobutton(master=frame_jk, text="Pria", variable=var_jk, value="Pria")
radio_pria.pack(side=tk.LEFT)
radio_wanita = tk.Radiobutton(master=frame_jk, text="Wanita", variable=var_jk, value="Wanita")
radio_wanita.pack(side=tk.LEFT)

# Variabel untuk checkbox
var_setuju = tk.IntVar()

# Checkbox di dalam frame_input
check_setuju = tk.Checkbutton(
    master=frame_input,
    text="Saya menyetujui pengumpulan data ini.",
    variable=var_setuju,
    font=("Arial", 10)
)
check_setuju.grid(row=5, column=0, columnspan=2, pady=10, sticky="W")

frame_input.grid(row=1, column=0, columnspan=2, sticky="EW")

#Input Nama dengan Grid
# label_nama = tk.Label(master=main_frame, text="Nama Lengkap:", font=("Arial", 12))
# label_nama.grid(row=1, column=0, sticky="W", pady=5)


# entry_nama = tk.Entry(master=main_frame, width=30, font=("Arial", 12))
# entry_nama.grid(row=1, column=1, pady=5)

# Input NIM
# label_nim = tk.Label(master=main_frame, text="NIM:", font=("Arial", 12))
# label_nim.grid(row=2, column=0, sticky="W", pady=5)
# entry_nim = tk.Entry(master=main_frame, width=30, font=("Arial", 12))
# entry_nim.grid(row=2, column=1, pady=5)

# Input Jurusan
# label_jurusan = tk.Label(master=main_frame, text="Jurusan:", font=("Arial", 12))
# label_jurusan.grid(row=3, column=0, sticky="W", pady=5)
# entry_jurusan = tk.Entry(master=main_frame, width=30, font=("Arial", 12))
# entry_jurusan.grid(row=3, column=1, pady=5)

# Label Jenis Kelamin
# label_jk = tk.Label(master=main_frame, text="Jenis Kelamin:", font=("Arial", 12))
# label_jk.grid(row=4, column=0, sticky="W", pady=5)

# Frame Untuk Radiobutton
# frame_jk = tk.Frame(master=main_frame)
# frame_jk.grid(row=4, column=1, sticky="W")

# # Radiobutton pria dan wanita
# radio_pria = tk.Radiobutton(master=frame_jk, text="Pria", variable=var_jk, value="Pria")
# radio_pria.pack(side=tk.LEFT)

# radio_wanita = tk.Radiobutton(master=frame_jk, text="Wanita", variable=var_jk, value="Wanita")
# radio_wanita.pack(side=tk.LEFT)

# Checkbox Persetujuan
# check_setuju = tk.Checkbutton(master=main_frame, text="Saya menyetujui pengumpulan data ini.", variable=var_setuju,font=("Arial", 10))
# check_setuju.grid(row=5, column=0, columnspan=2, pady=10, sticky="W")

# Tombol Submit
btn_submit = tk.Button(master=main_frame, text="Submit Biodata", font=("Arial", 12, "bold"), command=submit_data, bg="light gray")
# Button submit (posisi disesuaikan)
btn_submit.grid(row=2, column=0, columnspan=2, pady=20, sticky="EW")

# btn_submit.grid(row=6, column=0, columnspan=2, pady=20, sticky="EW")

main_frame.grid_columnconfigure(1, weight=1)

# Membuat label judul
# label_judul = tk.Label(
#     master=window,
#     text="FORM BIODATA MAHASISWA",
#     font=("Arial", 16, "bold"),
#     bg="AntiqueWhite1",
#     fg="blue"
# )

# # Menampilkan label dengan pack
# label_judul.pack(pady=20)

# #Input Nama

# #Label Untuk Input Nama
# label_nama = tk.Label(master=window, text="Nama Lengkap:", font=("Arial", 12))
# label_nama.pack(pady=5)

# #Entry Untuk Input Nama
# entry_nama = tk.Entry(master=window, width=50)
# entry_nama.pack(pady=5)


# # Input NIM

# label_nim = tk.Label(master=window, text="NIM:", font=("Arial", 12))
# label_nim.pack(pady=5)
# entry_nim = tk.Entry(master=window, width=50)
# entry_nim.pack(pady=5)

# # Input Jurusan

# label_jurusan = tk.Label(master=window, text="Jurusan:", font=("Arial", 12))
# label_jurusan.pack(pady=5)
# entry_jurusan = tk.Entry(master=window, width=50)
# entry_jurusan.pack(pady=5)

# Mengatur warna latar belakang jendela
window.configure(bg="AntiqueWhite1")

# Menjalankan event loop
window.mainloop()

