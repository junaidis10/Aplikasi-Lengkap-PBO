from abc import ABC, abstractmethod

class Akun_Bank(ABC):
    def __init__(self, nomor_akun, nama_pemilik, saldo_awal):
        self._nomor_akun = nomor_akun
        self._nama_pemilik = nama_pemilik
        self._saldo = saldo_awal
        print(f"Akun baru dibuat: {self._nama_pemilik} ({self._nomor_akun}) dengan saldo awal Rp{self._saldo:,.2f}")

    @abstractmethod
    def deposit(self, jumlah):
        """Metode abstrak untuk menyetor uang ke akun."""
        pass

    @abstractmethod
    def tarik_tunai(self, jumlah):
        """Metode abstrak untuk menarik uang dari akun."""
        pass

    def lihat_saldo(self):
        """Metode konkret untuk melihat saldo akun."""
        return self._saldo

    def info_akun(self):
        """Metode konkret untuk menampilkan informasi dasar akun."""
        print("\n--- Detail Akun ---")
        print(f"Nomor Akun : {self._nomor_akun}")
        print(f"Nama Pemilik : {self._nama_pemilik}")
        print(f"Saldo Saat Ini: Rp{self._saldo:,.2f}")
class AkunTabungan(Akun_Bank):
    def __init__(self, nomor_akun, nama_pemilik, saldo_awal, batas_penarikan=10000000):
        super().__init__(nomor_akun, nama_pemilik, saldo_awal)
        self._batas_penarikan = batas_penarikan
        print(f"Jenis Akun : Tabungan (Batas Penarikan: Rp{self._batas_penarikan:,.2f})")

    def deposit(self, jumlah):
        if jumlah > 0:
            self._saldo += jumlah
            print(f"Deposit Rp{jumlah:,.2f} berhasil. Saldo saat ini: Rp{self._saldo:,.2f}")
        else:
            print("Jumlah deposit harus positif.")

    def tarik_tunai(self, jumlah):
        if jumlah <= 0:
            print("Jumlah penarikan harus positif.")
        elif jumlah > self._saldo:
            print("Saldo tidak mencukupi.")
        elif jumlah > self._batas_penarikan:
            print(f"Penarikan melebihi batas harian (Rp{self._batas_penarikan:,.2f}).")
        else:
            self._saldo -= jumlah
            print(f"Tarik tunai Rp{jumlah:,.2f} berhasil. Saldo saat ini: Rp{self._saldo:,.2f}")

class AkunGiro(Akun_Bank):
    def __init__(self, nomor_akun, nama_pemilik, saldo_awal, biaya_administrasi_bulanan=50000):
        super().__init__(nomor_akun, nama_pemilik, saldo_awal)
        self._biaya_administrasi_bulanan = biaya_administrasi_bulanan
        print(f"Jenis Akun : Giro (Biaya Administrasi Bulanan: Rp{self._biaya_administrasi_bulanan:,.2f})")

    def deposit(self, jumlah):
        if jumlah > 0:
            self._saldo += jumlah
            print(f"Deposit Rp{jumlah:,.2f} berhasil. Saldo saat ini: Rp{self._saldo:,.2f}")
        else:
            print("Jumlah deposit harus positif.")

    def tarik_tunai(self, jumlah):
        # Akun Giro mungkin punya fitur overdraft, tapi kita buat sederhana: tidak boleh minus
        if jumlah <= 0:
            print("Jumlah penarikan harus positif.")
        elif jumlah > self._saldo:
            print("Saldo tidak mencukupi untuk penarikan ini.")
        else:
            self._saldo -= jumlah
            print(f"Tarik tunai Rp{jumlah:,.2f} berhasil. Saldo saat ini: Rp{self._saldo:,.2f}")

    def terapkan_biaya_administrasi(self):
        """Metode spesifik AkunGiro untuk menerapkan biaya bulanan."""
        if self._saldo >= self._biaya_administrasi_bulanan:
            self._saldo -= self._biaya_administrasi_bulanan
            print(f"Biaya administrasi bulanan sebesar Rp{self._biaya_administrasi_bulanan:,.2f} diterapkan.")
        else:
            print(f"Saldo tidak cukup untuk biaya administrasi. Saldo saat ini: Rp{self._saldo:,.2f}")
        print(f"Saldo setelah biaya: Rp{self._saldo:,.2f}")

# --- Contoh Penggunaan Aplikasi Perbankan ---

print("=== Membuat Akun Tabungan ===")
akun_tabungan = AkunTabungan("1234567890", "Junaidi Surya", 5000000, 20000000) # Batas penarikan custom 20 juta

akun_tabungan.info_akun()
akun_tabungan.deposit(1500000)
akun_tabungan.tarik_tunai(500000)
akun_tabungan.tarik_tunai(18000000) # Penarikan yang diizinkan (kurang dari 20 juta)
akun_tabungan.tarik_tunai(50000000) # Penarikan melebihi batas

akun_tabungan.info_akun()

print("\n" + "="*30)

print("=== Membuat Akun Giro ===")
akun_giro = AkunGiro("0987654321", "Andika Surya", 10000000)

akun_giro.info_akun()
akun_giro.deposit(2500000)
akun_giro.tarik_tunai(7000000)
akun_giro.tarik_tunai(10000000) # Saldo tidak cukup

akun_giro.info_akun()
akun_giro.terapkan_biaya_administrasi() # Menerapkan biaya administrasi bulanan
akun_giro.info_akun()

print("="*30)

# --- Demonstrasi Abstraksi: Mencoba membuat objek dari kelas abstrak ---
print("=== Mencoba membuat objek dari kelas abstrak ===")
try:
    akun_dasar = Akun_Bank("A000", "Anonim", 0)
except TypeError as e:
    print(f"Error: {e}")
    print("Tidak bisa membuat objek dari kelas abstrak Akun_Bank secara langsung!")