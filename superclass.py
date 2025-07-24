class Orang:  # Superclass
    def __init__(self, nama, usia):
        self.nama = nama
        self.usia = usia

    def tampilkan_info(self):
        print(f"Nama: {self.nama}, Usia: {self.usia}")

class Mahasiswa(Orang):  # Subclass yang mewarisi dari Person
    def __init__(self, nama, usia, nim, jurusan):
        super().__init__(nama, usia)  # Memanggil konstruktor superclass
        self.nim = nim
        self.jurusan = jurusan

    def tampilkan_info(self):
        super().tampilkan_info()  # Memanggil metode superclass
        print(f"NIM: {self.nim}, Jurusan: {self.jurusan}")

# Membuat objek dari subclass Mahasiswa
mahasiswa1 = Mahasiswa("Nadira Khairunisa", 19, "22111001", "Sistem Informasi")
mahasiswa2 = Mahasiswa("Budi Haryanto", 20, "22112002", "Teknik Informatika")
mahasiswa3 = Mahasiswa("Dimas Susanto", 20, "22113003", "Teknologi Informasi")
# Memanggil metode dari objek
mahasiswa1.tampilkan_info()
print("" + "-" * 30)
mahasiswa2.tampilkan_info()
print("" + "-" * 30)
mahasiswa3.tampilkan_info()