class Mahasiswa:
    def __init__(self, nama, nim):
        self.nama = nama
        self.nim = nim
        self.matkul_diambil = []

    def tambah_matkul(self, mata_kuliah):
        self.matkul_diambil.append(mata_kuliah)

    def __len__(self):
        """
        Built-in Method: __len__
        Mengembalikan jumlah mata kuliah yang diambil mahasiswa.
        """
        return len(self.matkul_diambil)

    def __str__(self):
        """
        Built-in Method: __str__
        Mengembalikan representasi string yang mudah dibaca dari objek Mahasiswa.
        """
        return f"Mahasiswa: {self.nama} (NIM: {self.nim})"

class DaftarNilai:
    def __init__(self, nama_mk):
        self.nama_mk = nama_mk
        self.nilai_mahasiswa = {} # {'NIM': nilai}

    def tambah_nilai(self, nim, nilai):
        self.nilai_mahasiswa[nim] = nilai

    def __len__(self):
        """
        Built-in Method: __len__
        Mengembalikan jumlah mahasiswa yang memiliki nilai di daftar ini.
        """
        return len(self.nilai_mahasiswa)

    def __str__(self):
        """
        Built-in Method: __str__
        Mengembalikan representasi string yang mudah dibaca dari objek DaftarNilai.
        """
        return f"Daftar Nilai Mata Kuliah: {self.nama_mk} ({len(self.nilai_mahasiswa)} mahasiswa)"

# --- Demonstrasi Polymorphism dengan Built-in Methods ---

# Membuat objek Mahasiswa
mhs1 = Mahasiswa("Imaan Santoso", "12345")
mhs1.tambah_matkul("Pemrograman Python")
mhs1.tambah_matkul("Struktur Data")
mhs1.tambah_matkul("Basis Data")

mhs2 = Mahasiswa("Nabila Nur Assyifa", "67890")
mhs2.tambah_matkul("Algoritma")
mhs2.tambah_matkul("Jaringan Komputer")

# Membuat objek DaftarNilai
nilai_py = DaftarNilai("Pemrograman Python")
nilai_py.tambah_nilai("12345", 85)
nilai_py.tambah_nilai("67890", 90)

nilai_sd = DaftarNilai("Struktur Data")
nilai_sd.tambah_nilai("12345", 78)

# Menggunakan fungsi built-in len() secara polimorfik
print("--- Penggunaan len() secara Polymorphism ---")
print(f"Jumlah mata kuliah yang diambil {mhs1.nama}: {len(mhs1)}") # Memanggil Mahasiswa.__len__()
print(f"Jumlah mata kuliah yang diambil {mhs2.nama}: {len(mhs2)}") # Memanggil Mahasiswa.__len__()
print(f"Jumlah mahasiswa di daftar nilai '{nilai_py.nama_mk}': {len(nilai_py)}") # Memanggil DaftarNilai.__len__()
print(f"Jumlah mahasiswa di daftar nilai '{nilai_sd.nama_mk}': {len(nilai_sd)}") # Memanggil DaftarNilai.__len__()

print("\n--- Penggunaan str() secara Polymorphism (otomatis oleh print()) ---")
print(mhs1) # Memanggil Mahasiswa.__str__()
print(nilai_py) # Memanggil DaftarNilai.__str__()
print(f"Informasi: {mhs2}") # Juga memanggil Mahasiswa.__str__()