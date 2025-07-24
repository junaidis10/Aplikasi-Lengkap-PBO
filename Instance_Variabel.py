class Kucing:
    # 1. Class Variable (Variabel Kelas)
    # Ini terikat ke Class (Kucing itu sendiri).
    # Dideklarasikan di dalam kelas, tetapi di luar metode.
    # Dibagikan oleh semua objek dari kelas 'Kucing'.
    jumlah_kaki = 4
    habitat = "rumah" # Contoh lain dari Class Variable

    def __init__(self, nama, warna):
        # 2. Instance Variables (Variabel Instans)
        # Ini terikat ke setiap Objek (instans dari Kucing).
        # Dideklarasikan di dalam metode __init__ (konstruktor).
        # Tidak dibagikan oleh objek; setiap objek memiliki salinannya sendiri.
        self.nama = nama
        self.warna = warna

    def info(self):
        print(f"Nama: {self.nama}")
        print(f"Warna: {self.warna}")
        print(f"Jumlah Kaki: {self.jumlah_kaki}") # Mengakses Class Variable
        print(f"Habitat: {Kucing.habitat}") # Cara lain mengakses Class Variable melalui nama kelas
        print("-" * 20)

# --- Membuat Objek (Instans dari Class Kucing) ---

# Objek pertama
kucing1 = Kucing("Molly", "Putih-Oranye")
print("Info Kucing 1:")
kucing1.info()

# Objek kedua
kucing2 = Kucing("Puti", "Putih-Hitam")
print("Info Kucing 2:")
kucing2.info()

# --- Menunjukkan Perbedaan ---

# Mengubah Instance Variable untuk kucing1 saja
kucing1.warna = "Coklat"
print("\nSetelah mengubah warna Kucing 1:")
kucing1.info()
kucing2.info() # Kucing 2 tidak terpengaruh

# Mengakses Class Variable melalui Class itu sendiri
print(f"Jumlah kaki default untuk semua kucing: {Kucing.jumlah_kaki}")

# Mengubah Class Variable melalui Class itu sendiri
# Perubahan ini akan memengaruhi SEMUA objek Kucing
Kucing.jumlah_kaki = 3 # Misalkan ada kucing yang kakinya diamputasi
print("\nSetelah mengubah jumlah_kaki (Class Variable):")
kucing1.info()
kucing2.info() # Kedua kucing sekarang menunjukkan 3 kaki!

# Anda juga bisa 'menimpa' class variable di tingkat instance,
# tapi itu akan membuat instance variable baru dengan nama yang sama.
# Ini sedikit rumit dan biasanya dihindari jika tujuannya adalah memodifikasi class variable.
kucing1.jumlah_kaki = 5 # Ini membuat instance variable 'jumlah_kaki' baru untuk kucing1 saja
print("\nSetelah 'menimpa' jumlah_kaki untuk Kucing 1:")
kucing1.info() # Kucing 1 sekarang punya 5 kaki (instance variable baru)
kucing2.info() # Kucing 2 masih 3 kaki (class variable yang diubah sebelumnya)
print(f"Jumlah kaki Class Kucing (asli): {Kucing.jumlah_kaki}") # Class variable tetap 3