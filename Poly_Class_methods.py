import datetime
# --- Kelas Induk: Orang ---
class Orang:
    def __init__(self, nama, tanggal_lahir):
        self.nama = nama
        self.tanggal_lahir = tanggal_lahir
    def hitung_umur(self):
        hari_ini = datetime.date.today()
        tahun_lahir = self.tanggal_lahir.year
        bulan_lahir = self.tanggal_lahir.month
        tanggal_lahir_hari = self.tanggal_lahir.day
        umur = hari_ini.year - tahun_lahir
        if (hari_ini.month, hari_ini.day) < (bulan_lahir, tanggal_lahir_hari):
            umur -= 1
        return umur
    def tampilkan_info(self):
        """Metode instance untuk menampilkan info objek."""
        print(f"Nama: {self.nama}")
        print(f"Tanggal Lahir: {self.tanggal_lahir.strftime('%d-%m-%Y')}")
        print(f"Umur: {self.hitung_umur()} tahun")

    @classmethod
    def info_tipe_individu(cls):
        """Class method untuk memberikan informasi umum tentang tipe 'Orang'."""
        print(f"Ini adalah kelas dasar: {cls.__name__}.")
        print("Mewakili entitas manusia secara umum.")
# --- Kelas Anak: Mahasiswa ---
class Mahasiswa(Orang):
    def __init__(self, nama, tanggal_lahir, nim, program_studi, ipk=0.0):
        super().__init__(nama, tanggal_lahir)
        self.nim = nim
        self.program_studi = program_studi
        self.ipk = ipk
    def tampilkan_info(self):
        """Metode instance yang di-override untuk Mahasiswa."""
        super().tampilkan_info()
        print(f"NIM: {self.nim}")
        print(f"Program Studi: {self.program_studi}")
        print(f"IPK: {self.ipk:.2f}")
    @classmethod
    def info_tipe_individu(cls):
        """Class method yang di-override untuk Mahasiswa."""
        print(f"Ini adalah kelas turunan: {cls.__name__}.")
        print("Mewakili individu yang terdaftar di institusi pendidikan.")
        print("Memiliki NIM, Program Studi, dan IPK.")
# --- Kelas Anak: Dosen ---
class Dosen(Orang):
    def __init__(self, nama, tanggal_lahir, nidn, bidang_keahlian):
        super().__init__(nama, tanggal_lahir)
        self.nidn = nidn
        self.bidang_keahlian = bidang_keahlian
    def tampilkan_info(self):
        """Metode instance yang di-override untuk Dosen."""
        super().tampilkan_info()
        print(f"NIDN: {self.nidn}")
        print(f"Bidang Keahlian: {self.bidang_keahlian}")
    @classmethod
    def info_tipe_individu(cls):
        """Class method yang di-override untuk Dosen."""
        print(f"Ini adalah kelas turunan: {cls.__name__}.")
        print("Mewakili staf pengajar di institusi pendidikan.")
        print("Memiliki NIDN dan Bidang Keahlian.")

# --- Demonstrasi Polymorphism pada Class Methods ---
if __name__ == "__main__":
    print("--- Memanggil Class Method Secara Langsung pada Kelas ---")
    print("\nInfo dari Kelas Orang:")
    Orang.info_tipe_individu() # Memanggil class method dari kelas Orang
    print("\nInfo dari Kelas Mahasiswa:")
    Mahasiswa.info_tipe_individu() # Memanggil class method dari kelas Mahasiswa
    print("\nInfo dari Kelas Dosen:")
    Dosen.info_tipe_individu() # Memanggil class method dari kelas Dosen
    print("\n" + "="*50 + "\n")
    print("--- Demonstrasi Polymorphism Menggunakan List Kelas ---")
    # Kita bisa menyimpan referensi ke kelas itu sendiri dalam sebuah list
    daftar_tipe_civitas = [Orang, Mahasiswa, Dosen]
    for tipe_kelas in daftar_tipe_civitas:
        print(f"\n--- Informasi Tipe: {tipe_kelas.__name__} ---")
        tipe_kelas.info_tipe_individu() # Memanggil class method yang sama pada setiap kelas