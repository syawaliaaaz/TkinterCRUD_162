# Import library untuk database dan GUI
import sqlite3  # Untuk koneksi ke database SQLite
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk  # Untuk membuat GUI

# Fungsi untuk Membuat database dan tabel
def create_database():
    conn = sqlite3.connect('nilai_siswa.db')  # Membuat atau membuka file database SQLite
    cursor = conn.cursor()  # Membuat cursor untuk mengeksekusi perintah SQL
    cursor.execute('''  
        CREATE TABLE IF NOT EXISTS nilai_siswa(
            id INTEGER PRIMARY KEY AUTOINCREMENT,  
            nama_siswa TEXT,  
            biologi INTEGER,  
            fisika INTEGER,  
            inggris INTEGER,  
            prediksi_fakultas TEXT  
        )
    ''')
    conn.commit()  # Menyimpan perubahan ke database
    conn.close()  # Menutup koneksi database

# Fungsi untuk mengambil semua data dari database
def fetch_data():
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database
    cursor = conn.cursor()  # Membuat cursor
    cursor.execute("SELECT * FROM nilai_siswa")  # Mengambil semua data dari tabel
    rows = cursor.fetchall()  # Menyimpan hasil query ke dalam variabel rows
    conn.close()  # Menutup koneksi database
    return rows  # Mengembalikan data hasil query

# Fungsi untuk menyimpan data baru ke database
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database
    cursor = conn.cursor()  # Membuat cursor
    cursor.execute(''' 
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, prediksi))  # Data dimasukkan sebagai tuple
    conn.commit()  # Menyimpan perubahan ke database
    conn.close()  # Menutup koneksi database

# Fungsi untuk memperbarui data di database
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database
    cursor = conn.cursor()  # Membuat cursor
    cursor.execute('''  # Memperbarui data berdasarkan ID
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?
    ''', (nama, biologi, fisika, inggris, prediksi, record_id))  # Data yang diperbarui
    conn.commit()  # Menyimpan perubahan
    conn.close()  # Menutup koneksi database

# Fungsi untuk menghapus data dari database
def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database
    cursor = conn.cursor()  # Membuat cursor
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))  # Menghapus data berdasarkan ID
    conn.commit()  # Menyimpan perubahan
    conn.close()  # Menutup koneksi database

# Fungsi untuk menghitung prediksi fakultas berdasarkan nilai
def database_prediction(biologi, fisika, inggris):
    if biologi >= fisika and biologi >= inggris:  # Jika nilai Biologi tertinggi
        return "Kedokteran"  # Prediksi Kedokteran
    elif fisika >= biologi and fisika >= inggris:  # Jika nilai Fisika tertinggi
        return "Teknik"  # Prediksi Teknik
    elif inggris >= biologi and inggris >= fisika:  # Jika nilai Inggris tertinggi
        return "Bahasa"  # Prediksi Bahasa
    else:
        return "Tidak diketahui"  # Jika tidak ada nilai dominan

# Fungsi untuk menambahkan data baru ke database
def submit():
    try:
        nama = nama_var.get()  # Mengambil input nama siswa
        biologi = int(biologi_var.get())  # Mengambil dan mengubah nilai Biologi menjadi integer
        fisika = int(fisika_var.get())  # Mengambil dan mengubah nilai Fisika menjadi integer
        inggris = int(inggris_var.get())  # Mengambil dan mengubah nilai Inggris menjadi integer

        if not nama:  # Jika nama kosong, raise error
            raise ValueError("Nama siswa tidak boleh kosong!")

        prediksi = database_prediction(biologi, fisika, inggris)  # Hitung prediksi fakultas
        save_to_database(nama, biologi, fisika, inggris, prediksi)  # Simpan ke database

        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")  # Pesan sukses
        clear_inputs()  # Membersihkan input
        populate_table()  # Mengisi tabel dengan data terbaru
    except ValueError as e:
        messagebox.showerror("Error", f"Input tidak valid: {e}")  # Menampilkan pesan error jika input tidak valid

# Fungsi untuk memperbarui data di database
def update(): 
    try:
        if not selected_record_id.get():  # Mengecek apakah ada ID yang dipilih dari tabel
            raise ValueError("Pilih data dari tabel untuk diupdate!")  # Jika tidak ada, tampilkan error
        record_id = int(selected_record_id.get())  # Mengambil dan mengubah ID yang dipilih menjadi integer
        nama = nama_var.get()  # Mengambil input nama dari variabel
        biologi = int(biologi_var.get())  # Mengambil input nilai Biologi dan mengubahnya menjadi integer
        fisika = int(fisika_var.get())  # Mengambil input nilai Fisika dan mengubahnya menjadi integer
        inggris = int(inggris_var.get())  # Mengambil input nilai Inggris dan mengubahnya menjadi integer

        if not nama:  # Mengecek apakah nama kosong
            raise ValueError("Nama siswa tidak boleh kosong!")  # Jika kosong, tampilkan error

        prediksi = database_prediction(biologi, fisika, inggris)  # Menghitung prediksi fakultas berdasarkan nilai
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)  # Memperbarui data di database

        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")  # Menampilkan pesan sukses
        clear_inputs()  # Membersihkan input setelah data diperbarui
        populate_table()  # Memperbarui tabel dengan data terbaru
    except ValueError as e:  # Menangkap error jika ada masalah pada input atau data
        messagebox.showerror("Error", f"Kesalahan: {e}")  # Menampilkan pesan error

# Fungsi untuk menghapus data dari database
def delete():
    try:
        if not selected_record_id.get():  # Mengecek apakah ada ID yang dipilih dari tabel
            raise ValueError("Pilih data dari tabel untuk dihapus!")  # Jika tidak ada, tampilkan error
        record_id = int(selected_record_id.get())  # Mengambil dan mengubah ID yang dipilih menjadi integer
        delete_database(record_id)  # Menghapus data dari database berdasarkan ID
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")  # Menampilkan pesan sukses
        clear_inputs()  # Membersihkan input setelah data dihapus
        populate_table()  # Memperbarui tabel dengan data terbaru
    except ValueError as e:  # Menangkap error jika ada masalah pada input atau data
        messagebox.showerror("Error", f"Kesalahan: {e}")  # Menampilkan pesan error

# Fungsi untuk membersihkan input pada form
def clear_inputs():
    nama_var.set("")  # Mengosongkan input nama
    biologi_var.set("")  # Mengosongkan input nilai Biologi
    fisika_var.set("")  # Mengosongkan input nilai Fisika
    inggris_var.set("")  # Mengosongkan input nilai Inggris
    selected_record_id.set("")  # Mengosongkan ID yang dipilih

# Fungsi untuk mengisi tabel dengan data dari database
def populate_table():
    for row in tree.get_children():  # Menghapus semua data yang ada di tabel
        tree.delete(row)
    for row in fetch_data():  # Mengambil semua data dari database
        tree.insert('', 'end', values=row)  # Menambahkan data ke tabel

# Fungsi untuk mengisi input form berdasarkan data yang dipilih di tabel
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]  # Mengambil item yang dipilih dari tabel
        selected_row = tree.item(selected_item)['values']  # Mendapatkan nilai dari item yang dipilih

        selected_record_id.set(selected_row[0])  # Mengisi ID ke input
        nama_var.set(selected_row[1])  # Mengisi nama ke input
        biologi_var.set(selected_row[2])  # Mengisi nilai Biologi ke input
        fisika_var.set(selected_row[3])  # Mengisi nilai Fisika ke input
        inggris_var.set(selected_row[4])  # Mengisi nilai Inggris ke input
    except IndexError:  # Jika tidak ada data yang dipilih
        messagebox.showerror("Error", "Pilih data yang valid!")  # Menampilkan pesan error

# Membuat database jika belum ada
create_database()

# Membuat jendela utama aplikasi
root = Tk()  # Inisialisasi Tkinter
root.title("Prediksi Fakultas Siswa")  # Judul aplikasi
root.configure(bg="pink")  # Warna latar belakang jendela

# Membuat variabel untuk input form
nama_var = StringVar()  # Variabel untuk menyimpan input nama siswa
biologi_var = StringVar()  # Variabel untuk menyimpan input nilai Biologi
fisika_var = StringVar()  # Variabel untuk menyimpan input nilai Fisika
inggris_var = StringVar()  # Variabel untuk menyimpan input nilai Inggris
selected_record_id = StringVar()  # Variabel untuk menyimpan ID yang dipilih

# Font yang digunakan
font_style = ("Segoe UI Black", 10)

# Membuat label dan entry untuk input nama siswa
Label(root, text="Nama Siswa", bg="pink", fg="black", font=font_style).grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var, bg="lightpink", font=font_style).grid(row=0, column=1, padx=10, pady=5)

# Membuat label dan entry untuk input nilai Biologi
Label(root, text="Nilai Biologi", bg="pink", fg="black", font=font_style).grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=biologi_var, bg="lightpink", font=font_style).grid(row=1, column=1, padx=10, pady=5)

# Membuat label dan entry untuk input nilai Fisika
Label(root, text="Nilai Fisika", bg="pink", fg="black", font=font_style).grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=fisika_var, bg="lightpink", font=font_style).grid(row=2, column=1, padx=10, pady=5)

# Membuat label dan entry untuk input nilai Inggris
Label(root, text="Nilai Inggris", bg="pink", fg="black", font=font_style).grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=inggris_var, bg="lightpink", font=font_style).grid(row=3, column=1, padx=10, pady=5)

# Membuat tombol untuk menambah, memperbarui, dan menghapus data
Button(root, text="Add", command=submit, bg="pink", fg="black", font=font_style).grid(row=4, column=0, pady=10)
Button(root, text="Update", command=update, bg="pink", fg="black", font=font_style).grid(row=4, column=1, pady=10)
Button(root, text="Delete", command=delete, bg="pink", fg="black", font=font_style).grid(row=4, column=2, pady=10)

# Membuat tabel untuk menampilkan data
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")  # Kolom tabel
tree = ttk.Treeview(root, columns=columns, show='headings')  # Inisialisasi tabel

# Menambahkan gaya tabel
style = ttk.Style()
style.configure("Treeview", font=font_style, rowheight=25, background="lightpink", fieldbackground="lightpink")
style.configure("Treeview.Heading", font=("Segoe UI Black", 12), background="pink")

for col in columns:  # Menambahkan heading untuk setiap kolom
    tree.heading(col, text=col.capitalize())
    tree.column(col, anchor='center')

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)  # Menempatkan tabel di grid
tree.bind('<ButtonRelease-1>', fill_inputs_from_table)  # Menghubungkan event klik dengan fungsi

# Mengisi tabel dengan data dari database
populate_table()

# Menjalankan aplikasi
root.mainloop()
