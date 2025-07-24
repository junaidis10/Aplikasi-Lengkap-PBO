import datetime

class Karyawan:
    """
    Class Karyawan yang mengenkapsulasi semua data dan logika terkait
    seorang karyawan. ID Karyawan dibuat otomatis dan tidak bisa diubah.
    """
    _id_counter = 1000  # Class variable untuk generate ID unik (protected)

    def __init__(self, nama, jabatan, gaji_pokok):
        # --- ATRIBUT PRIVATE & PROTECTED ---
        self.__id_karyawan = f"K-{Karyawan._id_counter}"
        self._nama = nama  # Protected: bisa diakses turunan
        self._jabatan = jabatan  # Protected
        self.__gaji_pokok = gaji_pokok  # Private: sangat rahasia
        self._tanggal_masuk = datetime.date.today()
        self._status_aktif = True

        Karyawan._id_counter += 1
        print(f" Karyawan '{self._nama}' (ID: {self.__id_karyawan}) telah ditambahkan.")

    # --- METODE PUBLIK (Public Interface) ---
    def tampilkan_profil(self):
        """Menampilkan data publik dan terproteksi dari karyawan."""
        status = "Aktif" if self._status_aktif else "Tidak Aktif"
        print(f"\n--- PROFIL: {self.get_id()} | {self._nama} ---")
        print(f"  Jabatan       : {self._jabatan}")
        print(f"  Tanggal Masuk : {self._tanggal_masuk.strftime('%d %B %Y')}")
        print(f"  Status        : {status}")
        print(f"  Lama Bekerja  : {self.hitung_lama_bekerja()}")

    def get_id(self):
        """Getter publik untuk mendapatkan ID Karyawan yang private."""
        return self.__id_karyawan

    def hitung_lama_bekerja(self):
        """
        Contoh enkapsulasi logika. Pengguna tidak perlu tahu cara menghitung,
        cukup panggil metodenya.
        """
        hari_ini = datetime.date.today()
        selisih = hari_ini - self._tanggal_masuk
        tahun = selisih.days // 365
        bulan = (selisih.days % 365) // 30
        return f"{tahun} tahun, {bulan} bulan"

    def promosi(self, jabatan_baru, kenaikan_gaji):
        """Metode terkontrol untuk mengubah jabatan dan gaji."""
        print(f"\n🎉 PROMOSI untuk {self._nama}!")
        self._jabatan = jabatan_baru
        self.__gaji_pokok += kenaikan_gaji
        print(f"  Jabatan baru: {self._jabatan}")
        self.__tampilkan_notifikasi_gaji() # Memanggil metode private lain

    def resign(self):
        """Mengubah status karyawan menjadi tidak aktif."""
        self._status_aktif = False
        print(f"\n Karyawan {self._nama} telah resign.")

    # --- METODE PRIVATE ---
    def __tampilkan_notifikasi_gaji(self):
        """Metode private yang hanya bisa dipanggil dari dalam class ini."""
        # Logika ini disembunyikan dari luar
        print(f"  Gaji pokok telah disesuaikan menjadi: Rp{self.__gaji_pokok:,.0f}")


class Departemen:
    """
    Class yang mengelola sekelompok objek Karyawan.
    Ini adalah contoh enkapsulasi tingkat lanjut dimana satu objek (Departemen)
    mengelola objek lain (Karyawan) melalui antarmuka publik mereka.
    """
    def __init__(self, nama_departemen):
        self.nama = nama_departemen
        self.__daftar_karyawan = [] # Daftar karyawan dienkapsulasi (private)

    def tambah_karyawan(self, karyawan: Karyawan):
        """Menambahkan objek Karyawan ke dalam daftar departemen."""
        if isinstance(karyawan, Karyawan):
            self.__daftar_karyawan.append(karyawan)
            print(f"-> '{karyawan._nama}' telah ditambahkan ke departemen {self.nama}.")
        else:
            print("Error: Hanya objek Karyawan yang bisa ditambahkan.")

    def tampilkan_semua_karyawan(self):
        """Menampilkan profil semua karyawan di departemen."""
        print(f"\n===== DAFTAR KARYAWAN DEPARTEMEN: {self.nama} =====")
        if not self.__daftar_karyawan:
            print("Tidak ada karyawan di departemen ini.")
            return
        for karyawan in self.__daftar_karyawan:
            karyawan.tampilkan_profil()
        print("=" * 55)

    def cari_karyawan_by_id(self, id_karyawan):
        """Mencari dan mengembalikan objek karyawan berdasarkan ID."""
        for karyawan in self.__daftar_karyawan:
            if karyawan.get_id() == id_karyawan:
                return karyawan
        return None # Return None jika tidak ditemukan


# --- MAIN APPLICATION (Contoh Skenario Penggunaan) ---
if __name__ == "__main__":
    # 1. Membuat Departemen
    dep_it = Departemen("Sistem Informasi")

    # 2. Merekrut Karyawan baru (membuat objek Karyawan)
    karyawan1 = Karyawan("Junaidi Surya", "DevOps Engineer", 1800000)
    karyawan2 = Karyawan("Andika Surya Saputra", "UI/UX Designer", 1500000)
    karyawan3 = Karyawan("Raihan Surya Saputra", "Junior Programmer", 1200000)

    # 3. Menambahkan Karyawan ke Departemen (interaksi antar objek)
    dep_it.tambah_karyawan(karyawan1)
    dep_it.tambah_karyawan(karyawan2)
    dep_it.tambah_karyawan(karyawan3)

    # 4. Menampilkan semua karyawan di departemen IT
    dep_it.tampilkan_semua_karyawan()

    # 5. Departemen melakukan proses promosi untuk Budi
    #    Departemen mencari karyawan, lalu memanggil metode publik 'promosi'
    karyawan_ditemukan = dep_it.cari_karyawan_by_id("K-1000")
    if karyawan_ditemukan:
        karyawan_ditemukan.promosi("Senior Programmer", 4000000)

    # 6. Salah satu karyawan resign
    karyawan_resign = dep_it.cari_karyawan_by_id("K-1001")
    if karyawan_resign:
        karyawan_resign.resign()

    # 7. Tampilkan daftar akhir karyawan untuk melihat perubahan
    dep_it.tampilkan_semua_karyawan()

    # 8. BUKTI ENKAPSULASI: Akses langsung GAGAL
    print("\n--- Mencoba Mengakses Data Private Secara Langsung ---")
    try:
        # Ini akan menyebabkan AttributeError karena __gaji_pokok di-mangle oleh Python
        print(f"Gaji Junaidi Surya: {karyawan1.__gaji_pokok}")
    except AttributeError as e:
        print(f"GAGAL! Tidak bisa mengakses '__gaji_pokok'. Error: {e}")
        print("Ini membuktikan data gaji benar-benar terlindungi.")