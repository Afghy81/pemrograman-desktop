# Aplikasi Biodata Mahasiswa (OOP dengan Tkinter)

## Pendahuluan
Aplikasi desktop sederhana untuk mengelola biodata mahasiswa menggunakan Python dan Tkinter. Aplikasi ini mencakup fitur login, validasi form, logging, serta beberapa utilitas seperti Remember Me, Show/Hide Password, dan Reset Form.

## Fitur Utama
- Login dengan database pengguna sederhana (hardcoded)
- Remember Me (mengingkati username terakhir via file teks)
- Show/Hide Password (toggle visibility password)
- Form biodata dengan field: Nama, NIM, Jurusan, Alamat, Email, Telepon, Tanggal Lahir, Jenis Kelamin
- Validasi real-time untuk semua field menggunakan `StringVar.trace_add`
- Submit data dengan validasi lengkap (format email, telepon Indonesia, tanggal lahir DD/MM/YYYY)
- Tombol Submit hanya aktif ketika semua field valid dan checkbox persetujuan dicentang
- Tampilan hasil biodata di messagebox dan label di GUI
- Reset form dengan konfirmasi user (hanya aktif setelah submit berhasil)
- Simpan hasil biodata ke file teks dengan timestamp
- Logging aktivitas ke file `aplikasi_biodata.log`
- Menu bar dengan opsi: Simpan Hasil, Logout, Keluar
- Hover effect pada tombol Submit dan Reset
- Keyboard shortcut: Enter pada field untuk submit, dan Ctrl+R (jika ditambahkan) untuk reset

## Persyaratan Sistem
- Python 3.x
- Modul standar: tkinter, datetime, logging, os, re (tidak perlu instalasi eksternal)

## Cara Menggunakan

### 1. Menjalankan Aplikasi
Pastikan Anda berada dalam direktori yang berisi `aplikasi_biodata_oop.py`, lalu jalankan:
```bash
python aplikasi_biodata_oop.py
```

### 2. Login
- Masukkan username dan password.
- Username yang tersedia:
  - admin (password: 123)
  - user1 (password: password1)
  - mahasiswa (password: 123456)
- Centang "Remember Me" jika ingin mengingat username untuk sesi berikutnya.
- Klik tombol **Login** atau tekan Enter pada field password.

### 3. Remember Me
- Setelah login berhasil dengan checkbox Remember Me tercentang, username akan disimpan ke file `remember_me.txt`.
- Saat aplikasi dibuka lagi, username akan terisi otomatis jika file tersebut ada.
- Jika checkbox tidak dicentang, file `remember_me.txt` akan dihapus.

### 4. Show/Hide Password
- Klik ikon mata (👁) di sebelah field password untuk menampilkan/menyembunyikan password.
- Ikon akan berubah menjadi kunci (🔒) ketika password terlihat, dan kembali menjadi mata ketika disembunyikan.

### 5. Form Biodata
Setelah login, Anda akan diarahkan ke halaman biodata. Isi semua field:
- Nama Lengkap (hanya huruf, tidak boleh angka saja)
- NIM (angka minimal 8 digit)
- Jurusan (teks bebas)
- Alamat (teks bebas, bisa multi-baris)
- Email (format umum, contoh: user@domain.com)
- Telepon (format Indonesia: +62, 62, atau 0 diikuti 8 dan 8-11 digit angka)
- Tanggal Lahir (format DD/MM/YYYY, tanggal harus valid sesuai kalender)
- Jenis Kelamin (Pria/Wanita, pilih dengan radio button)
- Centang kotak "Saya menyetujui pengumpulan data ini."

### 6. Validasi Real-Time
Setiap perubahan pada field akan memicu validasi:
- Field yang kosong atau tidak valid akan ditandai dengan border merah (jika sebelumnya error dan kini valid, border akan hilang).
- Tombol Submit akan aktif (berwarna abu-abu terang saat hover) hanya ketika semua field valid dan checkbox dicentang.
- Jika ada field invalid, tooltip akan muncul saat fokus pada field tersebut (via fokus dan pesan warning saat submit).

### 7. Submit Data
- Klik tombol **Submit Biodata** atau tekan Enter pada salah satu field (nama, NIM, jurusan, atau alamat).
- Jika validasi lolos, messagebox akan menampilkan data yang berhasil disimpan.
- Label hasil di bawah akan berisi informasi lengkap termasuk user yang login.
- Tombol Reset Form akan aktif (berwarna merah) setelah submit berhasil.

### 8. Reset Form
- Tombol Reset Form hanya aktif setelah submit berhasil.
- Klik tombol Reset Form, kemudian konfirmasi dengan "Ya" pada dialog.
- Semua field akan dikosongkan, jenis kelamin dikembalikan ke "Pria", checkbox persetujuan tidak tercentang, dan border error dihapus.
- Tombol Reset akan kembali ke state nonaktif (DISABLED) setelah reset.

### 9. Simpan Hasil
- Pilih menu **File > Simpan Hasil** untuk menyimpan hasil biodata terakhir ke file teks.
- File akan diberi nama format: `biodata_{username}_{timestamp}.txt`.
- Isi file meliputi user yang menyimpan, timestamp, dan hasil biodata lengkap.
- Jika belum ada data yang disimpan (belum submit), akan muncul peringatan.

### 10. Logout
- Pilih menu **File > Logout** untuk keluar dari akun saat ini.
- Aplikasi akan kembali ke halaman login, field login dibersihkan, dan form biodata direset.

### 11. Keluar Aplikasi
- Pilih menu **File > Keluar** untuk menutup aplikasi sepenuhnya.
- Akan ada konfirmasi keluar.

## Penjelasan Teknis Singkat
- **Struktur OOP**: Kelas `AplikasiBiodata` mewarisi dari `tk.Tk`.
- **State Management**: Menggunakan `StringVar`, `IntVar` untuk mengikat nilai widget ke variabel.
- **Validasi**: Metode `_validasi_email`, `_validasi_telepon`, dan `_validasi_tanggal` menggunakan regex dan `datetime.strptime`.
- **Event Binding**: 
  - `trace_add("write", validate_form)` untuk validasi real-time.
  - Bind `<Enter>` dan `<Leave>` untuk hover effect pada tombol.
  - Bind `<Return>` untuk shortcut submit.
- **Logging**: Konfigurasi dasar logging ke file `aplikasi_biodata.log` dengan level INFO.
- **Frame Management**: Menggunakan metode `_pindah_ke` untuk beralih antara frame login dan biodata.
- **Menu Bar**: Dibuat dengan `tk.Menu` dan cascade.

## Kontribusi
Jika Anda ingin berkontribusi pada proyek ini:
1. Fork repositori ini.
2. Buat branch fitur baru (`git checkout -b fitur/AmazingFeature`).
3. Commit perubahan Anda (`git commit -m 'Tambahkan AmazingFeature'`).
4. Push ke branch (`git push origin fitur/AmazingFeature`).
5. Buka Pull Request.

## Lisensi
Proyek ini lisensi bajo MIT - lihat file `LICENSE` untuk detail lebih lanjut.

---
*Catatan: Aplikasi ini dibuat untuk keperluan pembelajaran Pemrograman Desktop.*