# 1. Kelas-kelas Dasar (Produk dan Diskon) fundamental untuk sistem belanja
class Produk:
    """Merepresentasikan satu jenis barang."""
    def __init__(self, nama, harga):
        self.nama = nama
        self.harga = harga

    def __str__(self):
        # Representasi string untuk produk agar mudah dibaca
        return f"{self.nama} (Rp {self.harga:,})"

# --- KELAS-KELAS DISKON ---

class Diskon:
    """Kelas induk untuk semua jenis diskon."""
    def __init__(self, nama_promo):
        self.nama_promo = nama_promo

    def hitung_potongan(self, subtotal):
        """Menghitung BESARNYA potongan. Wajib di-override."""
        raise NotImplementedError("Metode ini harus diimplementasikan oleh subclass")

class Persentase_Diskon(Diskon):
    """Diskon berdasarkan persentase dari subtotal."""
    def __init__(self, nama_promo, persentase):
        super().__init__(nama_promo)
        self.persentase = persentase

    def hitung_potongan(self, subtotal):
        return subtotal * (self.persentase / 100)

class DiskonPotonganTetap(Diskon):
    """Diskon berdasarkan potongan harga tetap."""
    def __init__(self, nama_promo, jumlah_potongan):
        super().__init__(nama_promo)
        self.jumlah_potongan = jumlah_potongan

    def hitung_potongan(self, subtotal):
        return self.jumlah_potongan

class DiskonMinimalBelanja(Diskon):
    """Diskon yang hanya aktif jika total belanja mencapai nilai minimum."""
    def __init__(self, nama_promo, jumlah_potongan, min_belanja):
        super().__init__(nama_promo)
        self.jumlah_potongan = jumlah_potongan
        self.min_belanja = min_belanja

    def hitung_potongan(self, subtotal):
        if subtotal >= self.min_belanja:
            return self.jumlah_potongan
        else:
            return 0 # Tidak ada potongan jika tidak memenuhi syarat
        
# 2. Kelas Utama (Keranjang Belanja) sebagai inti dari sistem 
class Keranjang_Belanja:
    """Mengelola daftar produk, diskon, dan total harga."""
    def __init__(self):
        self.daftar_item = []
        self.diskon_terapan = None

    def tambah_produk(self, produk, kuantitas=1):
        self.daftar_item.append({"produk": produk, "kuantitas": kuantitas})
        print(f"-> Menambahkan {kuantitas}x '{produk.nama}' ke keranjang.")

    def hitung_subtotal(self):
        """Menghitung total harga sebelum diskon."""
        total = 0
        for item in self.daftar_item:
            total += item["produk"].harga * item["kuantitas"]
        return total

    def terapkan_diskon(self, diskon: Diskon):
        """
        Menerapkan objek diskon. INI ADALAH INTI POLIMORFISME.
        Metode ini menerima objek apa pun selama itu turunan dari 'Diskon'.
        """
        self.diskon_terapan = diskon
        print(f"-> Menerapkan diskon '{diskon.nama_promo}'.")

    def cetak_struk(self):
        """Menampilkan rincian belanja dan total akhir."""
        subtotal = self.hitung_subtotal()
        potongan = 0
        
        print("\n" + "="*40)
        print("          STRUK BELANJA DIGITAL")
        print("="*40)
        print("Rincian Produk:")
        for item in self.daftar_item:
            harga_item_total = item['produk'].harga * item['kuantitas']
            print(f"- {item['produk'].nama} ({item['kuantitas']}x)  : Rp {harga_item_total:,}")
        
        print("-" * 40)
        print(f"Subtotal                 : Rp {subtotal:,}")

        # Polimorfisme terjadi di sini saat memanggil .hitung_potongan()
        if self.diskon_terapan:
            potongan = self.diskon_terapan.hitung_potongan(subtotal)
            print(f"Diskon ({self.diskon_terapan.nama_promo})   : -Rp {int(potongan):,}")
        
        harga_akhir = subtotal - potongan
        harga_akhir = max(0, harga_akhir) # Pastikan harga tidak negatif

        print("-" * 40)
        print(f"TOTAL AKHIR              : Rp {int(harga_akhir):,}")
        print("="*40 + "\n")

# 1. Siapkan produk yang tersedia di toko
produk_laptop = Produk("Macbook Air M4", 25000000)
produk_mouse = Produk("Mouse Logitech MX Master", 1500000)
produk_keyboard = Produk("Keyboard Mekanikal Keychron", 2100000)

# 2. Siapkan berbagai jenis promo yang aktif
promo_orange = Persentase_Diskon("Promo 7,7-an", 10) # Diskon 10%
promo_flash_sale = DiskonPotonganTetap("Flash Sale Tengah Malam", 500000) # Potongan 500rb
promo_gratis_ongkir = DiskonMinimalBelanja("Gratis Ongkir", 50000, 2000000) # Potongan 50rb jika belanja min 2jt

# 3. Skenario Belanja Pertama: Menggunakan promo persentase
print("--- SKENARIO 1: Belanja Notebook dan Mouse ---")
keranjang1 = Keranjang_Belanja()
keranjang1.tambah_produk(produk_laptop)
keranjang1.tambah_produk(produk_mouse, kuantitas=2)

# Terapkan diskon persentase
keranjang1.terapkan_diskon(promo_orange)

# Cetak struknya
keranjang1.cetak_struk()


# 4. Skenario Belanja Kedua: Keranjang yang sama, tapi ganti promo
print("--- SKENARIO 2: Belanja yang sama, ganti diskon ---")
keranjang2 = Keranjang_Belanja()
keranjang2.tambah_produk(produk_laptop)
keranjang2.tambah_produk(produk_mouse, kuantitas=2)

# Terapkan diskon potongan tetap
keranjang2.terapkan_diskon(promo_flash_sale)

# Cetak struknya
keranjang2.cetak_struk()


# 5. Skenario Belanja Ketiga: Menguji diskon minimal belanja

print("--- SKENARIO 3: Belanja Keyboard (tidak memenuhi syarat) ---")
keranjang3 = Keranjang_Belanja()
keranjang3.tambah_produk(produk_keyboard) # Total belanja Rp 2.100.000

# Terapkan diskon minimal belanja
keranjang3.terapkan_diskon(promo_gratis_ongkir)
keranjang3.cetak_struk() # Harusnya potongan tidak berlaku