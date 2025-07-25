from abc import ABC, abstractmethod

# --- 1. Kelas Abstrak: Kendaraan ---
class Kendaraan(ABC):
    """
    Kelas dasar abstrak untuk semua jenis kendaraan.
    Mendefinisikan perilaku dasar yang harus dimiliki setiap kendaraan.
    """
    def __init__(self, merek, tahun):
        self.merek = merek
        self.tahun = tahun
        self.mesin_hidup = False # Atribut status mesin

    @abstractmethod
    def hidupkan_mesin(self):
        """Metode abstrak untuk menghidupkan mesin kendaraan."""
        pass

    @abstractmethod
    def matikan_mesin(self):
        """Metode abstrak untuk mematikan mesin kendaraan."""
        pass

    @abstractmethod
    def info_spesifik(self):
        """Metode abstrak untuk menampilkan informasi spesifik kendaraan."""
        pass

    def tampilkan_info_umum(self):
        """Metode konkret: Menampilkan informasi umum tentang kendaraan."""
        status = "hidup" if self.mesin_hidup else "mati"
        print(f"Kendaraan: {self.merek}, Tahun: {self.tahun}, Mesin: {status}")

# --- 2. Subkelas Konkret: Mobil ---
class Mobil(Kendaraan):
    """
    Implementasi konkret dari Kendaraan untuk jenis Mobil.
    """
    def __init__(self, merek, tahun, jumlah_pintu):
        super().__init__(merek, tahun)
        self.jumlah_pintu = jumlah_pintu

    def hidupkan_mesin(self):
        if not self.mesin_hidup:
            print(f"Mobil {self.merek} distarter... VRROOM!")
            self.mesin_hidup = True
        else:
            print(f"Mobil {self.merek} sudah hidup.")

    def matikan_mesin(self):
        if self.mesin_hidup:
            print(f"Mobil {self.merek} dimatikan... KLIK!")
            self.mesin_hidup = False
        else:
            print(f"Mobil {self.merek} sudah mati.")

    def info_spesifik(self):
        print("  Tipe: Mobil")
        print(f"  Jumlah Pintu: {self.jumlah_pintu}")

# --- 3. Subkelas Konkret: SepedaMotor ---
class SepedaMotor(Kendaraan):
    """
    Implementasi konkret dari Kendaraan untuk jenis Sepeda Motor.
    """
    def __init__(self, merek, tahun, jenis_kopling):
        super().__init__(merek, tahun)
        self.jenis_kopling = jenis_kopling

    def hidupkan_mesin(self):
        if not self.mesin_hidup:
            print(f"Sepeda Motor {self.merek} diengkol... CENG CENG CENG!")
            self.mesin_hidup = True
        else:
            print(f"Sepeda Motor {self.merek} sudah hidup.")

    def matikan_mesin(self):
        if self.mesin_hidup:
            print(f"Sepeda Motor {self.merek} dimatikan... glek!")
            self.mesin_hidup = False
        else:
            print(f"Sepeda Motor {self.merek} sudah mati.")

    def info_spesifik(self):
        print("  Tipe: Sepeda Motor")
        print("  Jenis Kopling: {self.jenis_kopling}")

# --- 4. Subkelas Konkret: Sepeda (Studi Kasus Menarik) ---
# Bagaimana jika ada kendaraan tanpa mesin, seperti sepeda?
# Kita tetap harus mengimplementasikan metode abstrak,
# meskipun implementasinya mungkin "kosong" atau memberikan pesan relevan.
class Sepeda(Kendaraan):
    """
    Implementasi konkret dari Kendaraan untuk jenis Sepeda.
    Perhatikan penanganan metode mesin untuk kendaraan tanpa mesin.
    """
    def __init__(self, merek, tahun, jenis_frame):
        # Sepeda tidak punya mesin, jadi kita bisa abaikan parameter ini di super()
        # atau biarkan mesin_hidup selalu False.
        # Untuk tujuan abstraksi, kita tetap memanggil super().__init__
        super().__init__(merek, tahun)
        self.jenis_frame = jenis_frame
        self.mesin_hidup = False # Pastikan selalu False untuk sepeda

    def hidupkan_mesin(self):
        # Sepeda tidak punya mesin, jadi kita berikan pesan yang sesuai
        print(f"Sepeda {self.merek} tidak memiliki mesin untuk dihidupkan. Siap Gowes!")

    def matikan_mesin(self):
        # Sepeda tidak punya mesin, jadi kita berikan pesan yang sesuai
        print(f"Sepeda {self.merek} tidak memiliki mesin untuk dimatikan. Istirahat sejenak.")

    def info_spesifik(self):
        print("  Tipe: Sepeda")
        print("  Jenis Frame: {self.jenis_frame}")

# --- Bagian Utama Aplikasi: Pengujian ---
if __name__ == "__main__":
    print("--- Sistem Manajemen Kendaraan ---")

    # Membuat objek dari kelas konkret
    mobil_saya = Mobil("Toyota", 2020, 4)
    motor_saya = SepedaMotor("Honda", 2022, "Manual")
    sepeda_saya = Sepeda("Polygon", 2023, "Road Bike")

    kendaraan_list = [mobil_saya, motor_saya, sepeda_saya]

    for k in kendaraan_list:
        print("\n------------------------------")
        k.tampilkan_info_umum() # Memanggil metode konkret dari kelas abstrak
        k.info_spesifik()      # Memanggil metode abstrak yang diimplementasikan subkelas
        k.hidupkan_mesin()     # Memanggil metode abstrak yang diimplementasikan subkelas
        k.tampilkan_info_umum()
        k.matikan_mesin()      # Memanggil metode abstrak yang diimplementasikan subkelas
        k.tampilkan_info_umum()

    print("\n------------------------------")
    print("Mencoba membuat objek dari kelas abstrak Kendaraan:")
    try:
        # Ini akan menghasilkan TypeError karena Kendaraan adalah kelas abstrak
        kendaraan_abstrak = Kendaraan("Generic", 0)
        print("Berhasil membuat objek dari kelas abstrak (INI SEHARUSNYA TIDAK TERJADI)")
    except TypeError as e:
        print(f"Error: {e}")
        print("Tidak bisa membuat objek dari kelas abstrak Kendaraan!")

    print("\n------------------------------")
    print("Mencoba membuat subkelas yang tidak mengimplementasikan metode abstrak:")
    class Bus(Kendaraan):
        def __init__(self, merek, tahun, kapasitas):
            super().__init__(merek, tahun)
            self.kapasitas = kapasitas
        # Lupa mengimplementasikan hidupkan_mesin, matikan_mesin, info_spesifik

    try:
        # Ini juga akan menghasilkan TypeError karena Bus tidak mengimplementasikan semua metode abstrak
        bus_baru = Bus("Mercedes", 2018, 50)
        print("Berhasil membuat objek bus (INI SEHARUSNYA TIDAK TERJADI)")
    except TypeError as e:
        print(f"Error: {e}")
        print("Tidak bisa membuat objek Bus karena tidak mengimplementasikan semua metode abstrak!")