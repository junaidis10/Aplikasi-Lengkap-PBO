from abc import ABC, abstractmethod

# ==============================================================================
# KELAS DASAR (BASE CLASS) - Menunjukkan Inheritance & Encapsulation
# ==============================================================================
class Pegawai(ABC):
    """
    Kelas dasar abstrak untuk semua jenis pegawai.
    - Inheritance: Menjadi induk bagi kelas PegawaiTetap, PegawaiKontrak, dll.
    - Encapsulation: Menyembunyikan atribut __nama dan __nip.
    """
    def __init__(self, nip, nama, alamat):
        self.__nip = nip  # Atribut private (enkapsulasi)
        self.__nama = nama  # Atribut private (enkapsulasi)
        self.alamat = alamat

    # Getter untuk mengakses atribut private (enkapsulasi)
    def get_nip(self):
        return self.__nip

    def get_nama(self):
        return self.__nama

    @abstractmethod
    def hitung_gaji(self):
        """
        Metode abstrak untuk polimorfisme.
        Setiap subclass WAJIB mengimplementasikan metode ini.
        """
        pass

    def tampilkan_profil(self):
        """Metode umum untuk menampilkan profil pegawai."""
        return f"NIP: {self.get_nip()}, Nama: {self.get_nama()}, Alamat: {self.alamat}"


# ==============================================================================
# KELAS TURUNAN (DERIVED CLASSES) - Menunjukkan Inheritance & Polymorphism
# ==============================================================================
class PegawaiTetap(Pegawai):
    """
    Kelas untuk pegawai tetap.
    - Inheritance: Mewarisi dari kelas Pegawai.
    """
    def __init__(self, nip, nama, alamat, gaji_pokok, tunjangan_jabatan):
        super().__init__(nip, nama, alamat)
        self.gaji_pokok = gaji_pokok
        self.tunjangan_jabatan = tunjangan_jabatan

    def hitung_gaji(self):
        """
        Implementasi spesifik untuk gaji pegawai tetap (Polimorfisme).
        Gaji = Gaji Pokok + Tunjangan Jabatan.
        """
        return self.gaji_pokok + self.tunjangan_jabatan

class PegawaiKontrak(Pegawai):
    """
    Kelas untuk pegawai kontrak.
    - Inheritance: Mewarisi dari kelas Pegawai.
    """
    def __init__(self, nip, nama, alamat, upah_harian, jumlah_hari_masuk):
        super().__init__(nip, nama, alamat)
        self.upah_harian = upah_harian
        self.jumlah_hari_masuk = jumlah_hari_masuk

    def hitung_gaji(self):
        """
        Implementasi spesifik untuk gaji pegawai kontrak (Polimorfisme).
        Gaji = Upah Harian * Jumlah Hari Masuk.
        """
        return self.upah_harian * self.jumlah_hari_masuk

class Magang(Pegawai):
    """
    Kelas untuk pegawai magang.
    - Inheritance: Mewarisi dari kelas Pegawai.
    """
    def __init__(self, nip, nama, alamat, uang_saku_bulanan):
        super().__init__(nip, nama, alamat)
        self.uang_saku_bulanan = uang_saku_bulanan

    def hitung_gaji(self):
        """
        Implementasi spesifik untuk uang saku magang (Polimorfisme).
        Gaji = Uang Saku Bulanan.
        """
        return self.uang_saku_bulanan


# ==============================================================================
# KELAS PENGELOLA - Menunjukkan penggunaan objek-objek
# ==============================================================================
class Sistem_Penggajian:
    def __init__(self):
        self.daftar_pegawai = []

    def tambah_pegawai(self, pegawai):
        if isinstance(pegawai, Pegawai):
            self.daftar_pegawai.append(pegawai)
            print(f"Pegawai '{pegawai.get_nama()}' berhasil ditambahkan.")
        else:
            print("Error: Objek yang ditambahkan bukan turunan dari kelas Pegawai.")

    def proses_gaji_semua(self):
        """
        Fungsi ini menunjukkan Polimorfisme dalam aksi.
        Metode 'hitung_gaji()' yang sama dipanggil pada objek yang berbeda,
        dan Python secara otomatis memilih implementasi yang benar.
        """
        print("\n===== Proses Penggajian Bulan Ini =====")
        if not self.daftar_pegawai:
            print("Tidak ada pegawai dalam sistem.")
            return

        for pegawai in self.daftar_pegawai:
            gaji = pegawai.hitung_gaji()
            print(f"-> Slip Gaji untuk {pegawai.get_nama()} ({pegawai.__class__.__name__}):")
            print(f"   Profil: {pegawai.tampilkan_profil()}")
            print(f"   Gaji Bulan Ini: Rp {gaji:,.2f}")
            print("-" * 20)


# ==============================================================================
# FUNGSI UTAMA (MAIN EXECUTION)
# ==============================================================================
if __name__ == "__main__":
    # 1. Membuat objek dari berbagai jenis pegawai
    pegawai_tetap_1 = PegawaiTetap("PT001", "Junaidi Surya", "Jl. Merdeka No. 10", 7000000, 1500000)
    pegawai_kontrak_1 = PegawaiKontrak("PK001", "Nabila Nur Assyifa", "Jl. Sudirman No. 5", 250000, 22)
    mahasiswa_magang_1 = Magang("MG001", "Raihan Surya Saputra", "Jl. Pelajar No. 1", 1500000)
    
    # 2. Membuat sistem penggajian dan menambahkan pegawai
    sistem_gaji = Sistem_Penggajian()
    sistem_gaji.tambah_pegawai(pegawai_tetap_1)
    sistem_gaji.tambah_pegawai(pegawai_kontrak_1)
    sistem_gaji.tambah_pegawai(mahasiswa_magang_1)

    # 3. Menjalankan proses penggajian untuk semua pegawai
    sistem_gaji.proses_gaji_semua()