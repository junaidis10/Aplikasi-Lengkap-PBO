import datetime
# --- Kelas Induk: Orang ---
class Orang:
    def __init__(self, nama, tanggal_lahir):
        self.nama = nama
        self.tanggal_lahir = tanggal_lahir
    def hitung_umur(self):
        """Menghitung umur berdasarkan tanggal lahir."""
        hari_ini = datetime.date.today()
        tahun_lahir = self.tanggal_lahir.year
        bulan_lahir = self.tanggal_lahir.month
        tanggal_lahir_hari = self.tanggal_lahir.day
        umur = hari_ini.year - tahun_lahir
        if (hari_ini.month, hari_ini.day) < (bulan_lahir, tanggal_lahir_hari):
            umur -= 1
        return umur
    def tampilkan_info(self):
        """Metode dasar untuk menampilkan informasi umum orang."""
        print(f"Nama: {self.nama}")
        print(f"Tanggal Lahir: {self.tanggal_lahir.strftime('%d-%m-%Y')}")
        print(f"Umur: {self.hitung_umur()} tahun")
# --- Kelas Anak: Mahasiswa ---
class Mahasiswa(Orang):
    def __init__(self, nama, tanggal_lahir, nim, program_studi, ipk=0.0):
        super().__init__(nama, tanggal_lahir) # Panggil konstruktor kelas induk
        self.nim = nim
        self.program_studi = program_studi
        self.ipk = ipk # Asumsikan IPK diset langsung untuk demo ini
    def tampilkan_info(self):
        """  Override metode tampilkan_info dari kelas Orang.
        Menambahkan informasi spesifik mahasiswa.  """
        super().tampilkan_info() # Memanggil implementasi tampilkan_info dari kelas Orang
        print(f"NIM: {self.nim}")
        print(f"Program Studi: {self.program_studi}")
        print(f"IPK: {self.ipk:.2f}")
# --- Kelas Anak: Dosen ---
class Dosen(Orang):
    def __init__(self, nama, tanggal_lahir, nidn, bidang_keahlian):
        super().__init__(nama, tanggal_lahir) # Panggil konstruktor kelas induk
        self.nidn = nidn
        self.bidang_keahlian = bidang_keahlian

    def tampilkan_info(self):
        """  Override metode tampilkan_info dari kelas Orang.
        Menambahkan informasi spesifik dosen.  """
        super().tampilkan_info() # Memanggil implementasi tampilkan_info dari kelas Orang
        print(f"NIDN: {self.nidn}")
        print(f"Bidang Keahlian: {self.bidang_keahlian}")

# --- Demonstrasi Polymorphism ---
if __name__ == "__main__":
    print("--- Membuat Objek dari Berbagai Tipe ---")
    individu1 = Orang("Iman Santoso", datetime.date(1980, 5, 20))
    individu2 = Mahasiswa("Siti Aminah", datetime.date(2003, 11, 15), "20111007", "Sistem Informasi", 3.65)
    individu3 = Dosen("Junaidi Surya, M.Kom", datetime.date(1976, 10, 10), "1010107601", "Pemrograman Berorientasi Objek")

    print("\n" + "="*50 + "\n")
    print("--- Memanggil tampilkan_info() pada Masing-Masing Objek ---")
    print("Info Individu 1 (Orang):")
    individu1.tampilkan_info() # Memanggil Orang.tampilkan_info()

    print("\nInfo Individu 2 (Mahasiswa):")
    individu2.tampilkan_info() # Memanggil Mahasiswa.tampilkan_info()

    print("\nInfo Individu 3 (Dosen):")
    individu3.tampilkan_info() # Memanggil Dosen.tampilkan_info()

    print("\n" + "="*50 + "\n")
    print("--- Demonstrasi Polymorphism dalam Koleksi ---")
    daftar_civitas = [individu1, individu2, individu3]
    for civitas in daftar_civitas:
        print(f"\n--- Informasi untuk {civitas.nama} ---")
        civitas.tampilkan_info() # Python secara otomatis memanggil versi yang benar