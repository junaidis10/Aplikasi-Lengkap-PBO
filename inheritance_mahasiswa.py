import datetime

# --- Kelas Induk: Orang ---
class Orang:
    """
    Kelas dasar untuk merepresentasikan seseorang dengan nama dan tanggal lahir.
    """
    def __init__(self, nama, tanggal_lahir):
        self.nama = nama
        self.tanggal_lahir = tanggal_lahir

    def hitung_umur(self):
        """Menghitung umur berdasarkan tanggal lahir."""
        hari_ini = datetime.date.today()
        tahun_lahir = self.tanggal_lahir.year
        bulan_lahir = self.tanggal_lahir.month
        tanggal_lahir = self.tanggal_lahir.day

        umur = hari_ini.year - tahun_lahir
        if (hari_ini.month, hari_ini.day) < (bulan_lahir, tanggal_lahir):
            umur -= 1
        return umur

    def tampilkan_info(self):
        """Menampilkan informasi dasar orang."""
        print(f"Nama: {self.nama}")
        print(f"Tanggal Lahir: {self.tanggal_lahir.strftime('%d-%m-%Y')}")
        print(f"Umur: {self.hitung_umur()} tahun")

# --- Kelas Anak: Mahasiswa ---
class Mahasiswa(Orang):
    """
    Kelas turunan dari Orang, merepresentasikan seorang mahasiswa.
    """
    def __init__(self, nama, tanggal_lahir, nim, program_studi):
        super().__init__(nama, tanggal_lahir)
        self.nim = nim
        self.program_studi = program_studi
        self.__ipk = 0.0  # IPK diset privat untuk enkapsulasi
        self.mata_kuliah_diambil = [] # Daftar mata kuliah yang diambil mahasiswa

    def get_ipk(self):
        """Mengambil nilai IPK."""
        return self.__ipk

    def set_ipk(self, nilai_ipk):
        """
        Mengatur nilai IPK dengan validasi.
        IPK harus antara 0.0 dan 4.0.
        """
        if 0.0 <= nilai_ipk <= 4.0:
            self.__ipk = nilai_ipk
            print(f"IPK {self.nama} ({self.nim}) berhasil diperbarui menjadi {self.__ipk:.2f}")
        else:
            print(f"Gagal memperbarui IPK {self.nama}: Nilai IPK {nilai_ipk} tidak valid. Harus antara 0.0 dan 4.0.")

    def daftar_mata_kuliah(self, mata_kuliah):
        """
        Mendaftarkan mahasiswa ke mata kuliah.
        Args:
            mata_kuliah (MataKuliah): Objek MataKuliah yang akan didaftarkan.
        """
        if isinstance(mata_kuliah, MataKuliah):
            if mata_kuliah not in self.mata_kuliah_diambil:
                self.mata_kuliah_diambil.append(mata_kuliah)
                print(f"{self.nama} ({self.nim}) berhasil mendaftar mata kuliah: {mata_kuliah.nama}")
            else:
                print(f"{self.nama} ({self.nim}) sudah terdaftar di mata kuliah: {mata_kuliah.nama}")
        else:
            print("Objek yang diberikan bukan MataKuliah yang valid.")

    def tampilkan_daftar_mata_kuliah(self):
        """Menampilkan daftar mata kuliah yang diambil mahasiswa."""
        print(f"\n--- Mata Kuliah yang Diambil {self.nama} ({self.nim}) ---")
        if not self.mata_kuliah_diambil:
            print("Belum ada mata kuliah yang diambil.")
        else:
            for mk in self.mata_kuliah_diambil:
                print(f"- {mk.nama} ({mk.kode}) - {mk.sks} SKS")

    def tampilkan_info(self):
        """
        Override metode tampilkan_info dari kelas Orang
        untuk menambahkan informasi spesifik mahasiswa.
        """
        super().tampilkan_info()
        print(f"NIM: {self.nim}")
        print(f"Program Studi: {self.program_studi}")
        print(f"IPK: {self.__ipk:.2f}")

# --- Kelas Anak: Dosen ---
class Dosen(Orang):
    """
    Kelas turunan dari Orang, merepresentasikan seorang dosen.
    """
    def __init__(self, nama, tanggal_lahir, nidn, bidang_keahlian):
        super().__init__(nama, tanggal_lahir)
        self.nidn = nidn
        self.bidang_keahlian = bidang_keahlian
        self.mata_kuliah_diampu = [] # Daftar mata kuliah yang diampu dosen

    def mengajar_mata_kuliah(self, mata_kuliah):
        """
        Menambahkan mata kuliah yang diampu dosen.
        Args:
            mata_kuliah (MataKuliah): Objek MataKuliah yang diampu.
        """
        if isinstance(mata_kuliah, MataKuliah):
            if mata_kuliah not in self.mata_kuliah_diampu:
                self.mata_kuliah_diampu.append(mata_kuliah)
                print(f"Dosen {self.nama} ({self.nidn}) kini mengampu mata kuliah: {mata_kuliah.nama}")
            else:
                print(f"Dosen {self.nama} ({self.nidn}) sudah mengampu mata kuliah: {mata_kuliah.nama}")
        else:
            print("Objek yang diberikan bukan MataKuliah yang valid.")

    def tampilkan_info(self):
        """
        Override metode tampilkan_info dari kelas Orang
        untuk menambahkan informasi spesifik dosen.
        """
        super().tampilkan_info()
        print(f"NIDN: {self.nidn}")
        print(f"Bidang Keahlian: {self.bidang_keahlian}")
        print("\n--- Mata Kuliah yang Diampu ---")
        if not self.mata_kuliah_diampu:
            print("Belum ada mata kuliah yang diampu.")
        else:
            for mk in self.mata_kuliah_diampu:
                print(f"- {mk.nama} ({mk.kode})")

# --- Kelas Independen: MataKuliah ---
class MataKuliah:
    """
    Kelas untuk merepresentasikan sebuah mata kuliah.
    """
    def __init__(self, kode, nama, sks):
        self.kode = kode
        self.nama = nama
        self.sks = sks

    def tampilkan_info(self):
        """Menampilkan informasi mata kuliah."""
        print(f"Kode: {self.kode}")
        print(f"Nama: {self.nama}")
        print(f"SKS: {self.sks}")

# --- Kelas Independen: Jurusan ---
class Jurusan:
    """
    Kelas untuk mengelola daftar mahasiswa, dosen, dan mata kuliah
    dalam sebuah jurusan.
    """
    def __init__(self, nama_jurusan):
        self.nama_jurusan = nama_jurusan
        self.daftar_mahasiswa = []
        self.daftar_dosen = []
        self.daftar_mata_kuliah = []

    def tambah_mahasiswa(self, mahasiswa):
        """
        Menambahkan objek Mahasiswa ke jurusan.
        Args:
            mahasiswa (Mahasiswa): Objek Mahasiswa yang akan ditambahkan.
        """
        if isinstance(mahasiswa, Mahasiswa):
            if mahasiswa not in self.daftar_mahasiswa:
                self.daftar_mahasiswa.append(mahasiswa)
                print(f"{mahasiswa.nama} ({mahasiswa.nim}) telah ditambahkan ke Jurusan {self.nama_jurusan}.")
            else:
                print(f"{mahasiswa.nama} sudah ada di Jurusan {self.nama_jurusan}.")
        else:
            print("Objek yang diberikan bukan Mahasiswa yang valid.")

    def tambah_dosen(self, dosen):
        """
        Menambahkan objek Dosen ke jurusan.
        Args:
            dosen (Dosen): Objek Dosen yang akan ditambahkan.
        """
        if isinstance(dosen, Dosen):
            if dosen not in self.daftar_dosen:
                self.daftar_dosen.append(dosen)
                print(f"Dosen {dosen.nama} ({dosen.nidn}) telah ditambahkan ke Jurusan {self.nama_jurusan}.")
            else:
                print(f"Dosen {dosen.nama} sudah ada di Jurusan {self.nama_jurusan}.")
        else:
            print("Objek yang diberikan bukan Dosen yang valid.")

    def tambah_mata_kuliah(self, mata_kuliah):
        """
        Menambahkan objek MataKuliah ke jurusan.
        Args:
            mata_kuliah (MataKuliah): Objek MataKuliah yang akan ditambahkan.
        """
        if isinstance(mata_kuliah, MataKuliah):
            if mata_kuliah not in self.daftar_mata_kuliah:
                self.daftar_mata_kuliah.append(mata_kuliah)
                print(f"Mata Kuliah '{mata_kuliah.nama}' ({mata_kuliah.kode}) telah ditambahkan ke Jurusan {self.nama_jurusan}.")
            else:
                print(f"Mata Kuliah '{mata_kuliah.nama}' sudah ada di Jurusan {self.nama_jurusan}.")
        else:
            print("Objek yang diberikan bukan MataKuliah yang valid.")

    def tampilkan_daftar_mahasiswa(self):
        """Menampilkan daftar mahasiswa di jurusan ini."""
        print(f"\n--- Daftar Mahasiswa Jurusan {self.nama_jurusan} ---")
        if not self.daftar_mahasiswa:
            print("Belum ada mahasiswa terdaftar.")
        else:
            for i, mhs in enumerate(self.daftar_mahasiswa, 1):
                print(f"{i}. {mhs.nama} (NIM: {mhs.nim})")

    def tampilkan_daftar_dosen(self):
        """Menampilkan daftar dosen di jurusan ini."""
        print(f"\n--- Daftar Dosen Jurusan {self.nama_jurusan} ---")
        if not self.daftar_dosen:
            print("Belum ada dosen terdaftar.")
        else:
            for i, dsn in enumerate(self.daftar_dosen, 1):
                print(f"{i}. {dsn.nama} (NIDN: {dsn.nidn}) - Bidang: {dsn.bidang_keahlian}")

    def tampilkan_daftar_mata_kuliah_jurusan(self):
        """Menampilkan daftar mata kuliah yang ditawarkan di jurusan ini."""
        print(f"\n--- Daftar Mata Kuliah Ditawarkan di Jurusan {self.nama_jurusan} ---")
        if not self.daftar_mata_kuliah:
            print("Belum ada mata kuliah yang ditawarkan.")
        else:
            for i, mk in enumerate(self.daftar_mata_kuliah, 1):
                print(f"{i}. {mk.nama} ({mk.kode}) - {mk.sks} SKS")

# --- Bagian Utama Aplikasi (Main Program) ---
if __name__ == "__main__":
    print("--- Inisialisasi Data ---")

    # Membuat objek Jurusan
    jurusan_ti = Jurusan("Teknik Informatika")
    jurusan_si = Jurusan("Sistem Informasi")

    # Membuat objek Mata Kuliah
    mk_pbo = MataKuliah("IT101", "Pemrograman Berorientasi Objek", 3)
    mk_struktur_data = MataKuliah("IT102", "Struktur Data", 3)
    mk_basis_data = MataKuliah("IT103", "Sistem Basis Data", 4)
    mk_jaringan = MataKuliah("IT201", "Jaringan Komputer", 3)

    # Menambahkan mata kuliah ke jurusan
    jurusan_si.tambah_mata_kuliah(mk_pbo)
    jurusan_ti.tambah_mata_kuliah(mk_struktur_data)
    jurusan_ti.tambah_mata_kuliah(mk_basis_data)
    jurusan_si.tambah_mata_kuliah(mk_basis_data) # Mata kuliah bisa lintas jurusan
    jurusan_si.tambah_mata_kuliah(mk_jaringan)

    # Membuat objek Dosen
    dosen1 = Dosen("Dr. Darex Susanto,M.Kom", datetime.date(1982, 10, 22), "1022108201", "Kecerdasan Buatan")
    dosen2 = Dosen("Junaidi Surya, M.Kom", datetime.date(1976, 10, 22), "1010107601", "Pemrograman Berorientasi Objek")
    dosen3 = Dosen("Ahmad Louis, M.Kom", datetime.date(1977, 4, 30), "10130477021", "Jaringan Komputer")

    # Menambahkan dosen ke jurusan
    jurusan_ti.tambah_dosen(dosen1)
    jurusan_si.tambah_dosen(dosen2)
    jurusan_si.tambah_dosen(dosen3)

    # Dosen mengampu mata kuliah
    dosen1.mengajar_mata_kuliah(mk_struktur_data)
    dosen2.mengajar_mata_kuliah(mk_pbo)
    dosen3.mengajar_mata_kuliah(mk_jaringan)

    # Membuat objek Mahasiswa
    mahasiswa1 = Mahasiswa("Putri Suryani", datetime.date(2003, 10, 20), "2023001", "Teknik Informatika")
    mahasiswa2 = Mahasiswa("Nabila Nur Assyifa", datetime.date(2004, 1, 5), "2023002", "Sistem Informasi")
    mahasiswa3 = Mahasiswa("Andika Surya Sputra", datetime.date(2003, 7, 12), "2023003", "Teknik Informatika")

    # Menambahkan mahasiswa ke jurusan
    jurusan_ti.tambah_mahasiswa(mahasiswa1)
    jurusan_si.tambah_mahasiswa(mahasiswa2)
    jurusan_ti.tambah_mahasiswa(mahasiswa3)

    print("\n" + "="*50 + "\n")

    print("--- Operasi Mahasiswa ---")
    mahasiswa1.tampilkan_info()
    mahasiswa1.set_ipk(3.85)
    mahasiswa1.daftar_mata_kuliah(mk_struktur_data)
    mahasiswa1.daftar_mata_kuliah(mk_basis_data)
    mahasiswa1.tampilkan_daftar_mata_kuliah()

    print("\n" + "="*50 + "\n")

    mahasiswa2.tampilkan_info()
    mahasiswa2.set_ipk(3.70)
    mahasiswa2.daftar_mata_kuliah(mk_pbo)
    mahasiswa2.daftar_mata_kuliah(mk_basis_data)
    mahasiswa2.daftar_mata_kuliah(mk_jaringan)
    mahasiswa2.set_ipk(4.5) # Contoh IPK tidak valid
    mahasiswa2.tampilkan_daftar_mata_kuliah()

    print("\n" + "="*50 + "\n")

    print("--- Operasi Dosen ---")
    dosen1.tampilkan_info()
    print("\n" + "="*50 + "\n")
    dosen2.tampilkan_info()

    print("\n" + "="*50 + "\n")

    print("--- Operasi Jurusan ---")
    jurusan_ti.tampilkan_daftar_mahasiswa()
    jurusan_ti.tampilkan_daftar_dosen()
    jurusan_ti.tampilkan_daftar_mata_kuliah_jurusan()

    print("\n" + "="*50 + "\n")

    jurusan_si.tampilkan_daftar_mahasiswa()
    jurusan_si.tampilkan_daftar_dosen()
    jurusan_si.tampilkan_daftar_mata_kuliah_jurusan()