class DompetDigital:
    """
    Sebuah class sederhana untuk merepresentasikan dompet digital.
    Class ini menerapkan enkapsulasi untuk melindungi data saldo.
    """

    def __init__(self, pemilik, saldo_awal=0):
        """
        Constructor untuk membuat objek DompetDigital.
        - pemilik: Nama pemilik dompet (atribut publik).
        - __saldo: Saldo awal dompet (atribut 'private').
        """
        self.pemilik = pemilik  # Atribut ini bersifat publik, bisa diakses dari luar
        self.__saldo = saldo_awal # Atribut dengan '__' dianggap 'private'

        print(f"✅ Dompet digital untuk '{self.pemilik}' berhasil dibuat dengan saldo awal Rp{self.__saldo}.")

    # --- Ini adalah PUBLIC METHODS ---
    # Metode ini adalah 'pintu gerbang' untuk berinteraksi dengan data private.

    def cek_saldo(self):
        """Metode publik untuk menampilkan saldo saat ini."""
        print(f" Saldo Anda saat ini: Rp{self.__saldo}")

    def simpan_uang(self, jumlah):
        """Metode publik untuk menambah saldo."""
        if jumlah > 0:
            self.__saldo += jumlah
            print(f"Berhasil menyimpan Rp{jumlah}.")
            self.cek_saldo()
        else:
            print("Jumlah yang disimpan harus lebih dari nol.")

    def ambil_uang(self, jumlah):
        """Metode publik untuk mengurangi saldo dengan validasi."""
        if jumlah <= 0:
            print("Jumlah yang diambil harus lebih dari nol.")
            return # Hentikan fungsi

        if jumlah > self.__saldo:
            print(f"Maaf, saldo Anda (Rp{self.__saldo}) tidak mencukupi untuk penarikan Rp{jumlah}.")
        else:
            self.__saldo -= jumlah
            print(f"Berhasil mengambil Rp{jumlah}.")
            self.cek_saldo()

# --- Contoh Penggunaan Aplikasi ---

print("===== Membuat Dompet Digital Baru =====")
dompet_Andika = DompetDigital("Andika", 50000)
print("-" * 20)

print("\n===== Melakukan Transaksi =====")
# Menggunakan public method untuk berinteraksi
dompet_Andika.cek_saldo()
dompet_Andika.simpan_uang(25000)
dompet_Andika.ambil_uang(10000)
print("-" * 20)

print("\n===== Skenario Gagal =====")
# Mencoba mengambil uang lebih banyak dari saldo
dompet_Andika.ambil_uang(100000)
print("-" * 20)

print("\n===== Bukti Enkapsulasi =====")
# 1. Mencoba mengakses atribut 'private' secara langsung (akan gagal)
print("Mencoba mengakses 'dompet_Andika.__saldo' secara langsung...")
try:
    print(dompet_Andika.__saldo)
except AttributeError as e:
    print(f"GAGAL! Terjadi error: {e}")
    print("Ini membuktikan '__saldo' tidak bisa diakses dari luar class.")

# 2. Mencoba mengubah saldo secara langsung (tidak akan mengubah saldo asli)
print("\nMencoba mengubah saldo menjadi 1,000,000 secara paksa...")
dompet_Andika.__saldo = 1000000
print("Saldo setelah diubah paksa (menurut atribut baru):", dompet_Andika.__saldo)

print("\nCek saldo asli menggunakan metode publik:")
dompet_Andika.cek_saldo()
print("Terlihat bahwa saldo asli di dalam objek tetap aman dan tidak berubah!")