class Mahasiswa:
    # Konstruktor berparameter
    # 'self' adalah referensi ke instansi objek itu sendiri (wajib ada)
    # 'nama', 'nim', dan 'jurusan' adalah parameter yang akan kita berikan saat membuat objek
    def __init__(self, nama, nim, jurusan):
        print(f"Konstruktor dipanggil untuk Mahasiswa: {nama}")
        self.nama = nama        # Inisialisasi variabel instans 'nama'
        self.nim = nim          # Inisialisasi variabel instans 'nim'
        self.jurusan = jurusan  # Inisialisasi variabel instans 'jurusan'

    # Metode untuk menampilkan informasi mahasiswa
    def tampilkan_info(self):
        print(f"Nama: {self.nama}")
        print(f"NIM: {self.nim}")
        print(f"Jurusan: {self.jurusan}")
        print("-" * 30)
# --- Membuat Objek Mahasiswa dengan Constructor Berparameter ---
print("Membuat Objek Mahasiswa 1:")
# Saat objek dibuat, kita langsung memberikan nilai untuk nama, nim, dan jurusan
mahasiswa1 = Mahasiswa("Andika Surya Saputra", "20111001", "Sistem Informasi")
mahasiswa1.tampilkan_info()

print("\nMembuat Objek Mahasiswa 2:")
mahasiswa2 = Mahasiswa("Raihan Surya Saputra", "20112002", "Teknik Informatika")
mahasiswa2.tampilkan_info()

print("\nMembuat Objek Mahasiswa 3:")
mahasiswa3 = Mahasiswa("Nabila Suryani Saputri", "20113003", " Teknologi Informasi")
mahasiswa3.tampilkan_info()

# Kita tidak bisa membuat objek tanpa memberikan parameter yang dibutuhkan
# Jika Anda mencoba baris di bawah, akan terjadi error:
# mahasiswa_error = Mahasiswa() # TypeError: __init__() missing 3 required positional arguments: 'nama', 'nim', and 'jurusan'