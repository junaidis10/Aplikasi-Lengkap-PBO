class Mahasiswa:
    def __init__(self, nama, nim):
        self.nama = nama
        self.nim = nim

    def tampilkan_info(self):
        """Metode dasar untuk menampilkan informasi mahasiswa."""
        return f"Nama: {self.nama}, NIM: {self.nim}"

class MahasiswaReguler(Mahasiswa):
    def __init__(self, nama, nim, jurusan):
        super().__init__(nama, nim)
        self.jurusan = jurusan
    def tampilkan_info(self):
        """Override metode tampilkan_info untuk MahasiswaReguler."""
        return f"{super().tampilkan_info()}, Jurusan: {self.jurusan}"

class MahasiswaBeasiswa(Mahasiswa):
    def __init__(self, nama, nim, jenis_beasiswa):
        super().__init__(nama, nim)
        self.jenis_beasiswa = jenis_beasiswa

    def tampilkan_info(self):
        """Override metode tampilkan_info untuk MahasiswaBeasiswa."""
        return f"{super().tampilkan_info()}, Beasiswa: {self.jenis_beasiswa}"

def tampilkan_daftar_mahasiswa(daftar_mahasiswa):
    """
    Fungsi ini mendemonstrasikan polymorphism.
    Menerima daftar objek mahasiswa dari berbagai tipe
    dan memanggil metode tampilkan_info() pada masing-masing objek.
    """
    print("--- Daftar Informasi Mahasiswa ---")
    for mahasiswa in daftar_mahasiswa:
        print(mahasiswa.tampilkan_info())
    print("---------------------------------")

# Membuat objek-objek mahasiswa
mhs_reguler1 = MahasiswaReguler("Iman Santoso", "123456789", "Teknik Informatika")
mhs_reguler2 = MahasiswaReguler("Nabila Nur Assyifa", "987654321", "Sistem Informasi")
mhs_beasiswa1 = MahasiswaBeasiswa("Dwi Prasetyo", "112233445", "Bidikmisi")
mhs_beasiswa2 = MahasiswaBeasiswa("Citra Dewi", "554433221", "Prestasi Akademik")

# Menyatukan objek-objek dalam satu daftar
daftar_mahasiswa = [mhs_reguler1, mhs_reguler2, mhs_beasiswa1, mhs_beasiswa2]

# Memanggil fungsi yang mendemonstrasikan polymorphism
tampilkan_daftar_mahasiswa(daftar_mahasiswa)

# Contoh penggunaan individual (opsional)
print("\n--- Informasi Mahasiswa Individu ---")
print(mhs_reguler1.tampilkan_info())
print(mhs_beasiswa1.tampilkan_info())