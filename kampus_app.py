import streamlit as st
import mysql.connector
from mysql.connector import Error
from datetime import date

# --- Konfigurasi Database ---
DB_CONFIG = {
    'host': 'sql12.freesqldatabase.com',
    'database': 'sql12791028',
    'user': 'sql12791028',
    'password': 'D6uSBwHqxL',
    'port': 3306
}

# --- Class DatabaseManager untuk Interaksi DB ---
class DatabaseManager:
    def __init__(self, config):
        self.config = config
        self.connection = None
        self.cursor = None

    def connect(self):
        """Membuka koneksi ke database."""
        try:
            self.connection = mysql.connector.connect(**self.config)
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(buffered=True)
                st.success(f"Berhasil terhubung ke database '{self.config['database']}'")
                return True
        except Error as e:
            st.error(f"Error saat mencoba terhubung ke database: {e}")
        return False

    def disconnect(self):
        """Menutup koneksi ke database."""
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            st.info("Koneksi database ditutup.")

    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False):
        """Mengeksekusi query SQL (INSERT, UPDATE, DELETE, SELECT) dan mengembalikan hasilnya."""
        if not self.connection or not self.connection.is_connected():
            st.error("Error: Belum terhubung ke database. Harap panggil .connect() terlebih dahulu.")
            return None

        try:
            self.cursor.execute(query, params)
            if query.strip().upper().startswith(("INSERT", "UPDATE", "DELETE")):
                self.connection.commit()
                return self.cursor.rowcount
            elif fetch_one:
                return self.cursor.fetchone()
            elif fetch_all:
                return self.cursor.fetchall()
            return True
        except Error as e:
            st.error(f"Error saat mengeksekusi query: {e}")
            self.connection.rollback()
            return False

    def setup_tables(self):
        """Membuat semua tabel yang diperlukan jika belum ada."""
        # Table schemas are derived from the uploaded "Panduan Lengkap Membuat Database Online.pdf" [cite: 49, 50, 51, 52]
        queries = [
            """
            CREATE TABLE IF NOT EXISTS jurusan (
                id_jurusan INT AUTO_INCREMENT PRIMARY KEY,
                nama_jurusan VARCHAR(100) NOT NULL,
                kode_jurusan VARCHAR(10) UNIQUE NOT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS dosen (
                id_dosen INT AUTO_INCREMENT PRIMARY KEY,
                nidn VARCHAR(20) UNIQUE NOT NULL,
                nama_dosen VARCHAR(100) NOT NULL,
                jenis_kelamin ENUM('L', 'P'),
                tanggal_lahir DATE,
                alamat TEXT,
                email VARCHAR(100) UNIQUE,
                no_telepon VARCHAR(20),
                id_jurusan INT,
                FOREIGN KEY (id_jurusan) REFERENCES jurusan(id_jurusan)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS biodata (
                nim VARCHAR(15) PRIMARY KEY NOT NULL,
                nama_lengkap VARCHAR(100) NOT NULL,
                jenis_kelamin ENUM('L', 'P'),
                tanggal_lahir DATE,
                alamat TEXT,
                email VARCHAR(100) UNIQUE,
                no_telepon VARCHAR(20),
                angkatan YEAR,
                id_jurusan INT,
                FOREIGN KEY (id_jurusan) REFERENCES jurusan(id_jurusan)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS matakuliah (
                id_matakuliah INT AUTO_INCREMENT PRIMARY KEY,
                kode_matakuliah VARCHAR(10) UNIQUE NOT NULL,
                nama_matakuliah VARCHAR(100) NOT NULL,
                sks INT NOT NULL,
                semester INT,
                id_dosen INT,
                id_jurusan INT,
                FOREIGN KEY (id_dosen) REFERENCES dosen(id_dosen),
                FOREIGN KEY (id_jurusan) REFERENCES jurusan(id_jurusan)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS nilai (
                id_nilai INT AUTO_INCREMENT PRIMARY KEY,
                nim VARCHAR(15) NOT NULL,
                id_matakuliah INT NOT NULL,
                nilai_angka DECIMAL(4,2),
                nilai_huruf VARCHAR(2),
                tahun_akademik VARCHAR(9),
                semester_akademik ENUM('Ganjil', 'Genap', 'Pendek'),
                FOREIGN KEY (nim) REFERENCES biodata(nim),
                FOREIGN KEY (id_matakuliah) REFERENCES matakuliah(id_matakuliah)
            );
            """
        ]
        st.subheader("Menyiapkan Tabel Database")
        for query in queries:
            if self.execute_query(query):
               # st.success("Tabel berhasil dibuat atau sudah ada.")
            #else:
                st.warning("Gagal mengeksekusi query DDL.")
                return False
        st.success("Setup tabel selesai.")
        return True

# --- Class untuk Representasi Data (OOP) ---
class MataKuliah:
    def __init__(self, kode, nama, sks, id_matakuliah=None, semester=None, id_dosen=None, id_jurusan=None):
        self._id_matakuliah = id_matakuliah
        self._kode = kode
        self._nama = nama
        self._sks = sks
        self._semester = semester
        self._id_dosen = id_dosen
        self._id_jurusan = id_jurusan

    def get_id(self):
        return self._id_matakuliah

    def get_kode(self):
        return self._kode

    def get_nama(self):
        return self._nama

    def get_sks(self):
        return self._sks

    def get_semester(self):
        return self._semester

    def get_id_dosen(self):
        return self._id_dosen

    def get_id_jurusan(self):
        return self._id_jurusan

    def set_id(self, id_val):
        self._id_matakuliah = id_val

    def __str__(self):
        return f"[{self._kode}] {self._nama} ({self._sks} SKS)"

    def __eq__(self, other):
        if not isinstance(other, MataKuliah):
            return NotImplemented
        return self._kode == other._kode

    def __hash__(self):
        return hash(self._kode)

class Jurusan:
    def __init__(self, kode, nama, id_jurusan=None):
        self._id_jurusan = id_jurusan
        self._kode = kode
        self._nama = nama

    def get_id(self):
        return self._id_jurusan

    def get_kode(self):
        return self._kode

    def get_nama(self):
        return self._nama

    def set_id(self, id_val):
        self._id_jurusan = id_val

    def __str__(self):
        return f"Jurusan: {self._nama} ({self._kode})"

class Orang: # Parent class
    def __init__(self, nama, id_db=None, id_kampus=None, jenis_kelamin=None, tanggal_lahir=None, alamat=None, email=None, no_telepon=None, id_jurusan=None):
        self._id_db = id_db
        self._id_kampus = id_kampus # NIM/NIDN
        self._nama = nama
        self._jenis_kelamin = jenis_kelamin
        self._tanggal_lahir = tanggal_lahir
        self._alamat = alamat
        self._email = email
        self._no_telepon = no_telepon
        self._id_jurusan = id_jurusan

    def get_id_db(self):
        return self._id_db

    def get_id_kampus(self):
        return self._id_kampus

    def get_nama(self):
        return self._nama

    def get_jenis_kelamin(self):
        return self._jenis_kelamin

    def get_tanggal_lahir(self):
        return self._tanggal_lahir

    def get_alamat(self):
        return self._alamat

    def get_email(self):
        return self._email

    def get_no_telepon(self):
        return self._no_telepon

    def get_id_jurusan(self):
        return self._id_jurusan

    def set_id_db(self, id_val):
        self._id_db = id_val

    def __str__(self):
        return f"Orang: {self._nama} (ID: {self._id_kampus or self._id_db})"

class Mahasiswa(Orang):
    def __init__(self, nim, nama, jenis_kelamin=None, tanggal_lahir=None, alamat=None, email=None, no_telepon=None, angkatan=None, id_jurusan=None):
        super().__init__(nama, id_kampus=nim, jenis_kelamin=jenis_kelamin, tanggal_lahir=tanggal_lahir, alamat=alamat, email=email, no_telepon=no_telepon, id_jurusan=id_jurusan)
        self._nim = nim
        self._angkatan = angkatan
        self._krs = {}
        self._ipk = 0.0

    def get_nim(self):
        return self._nim

    def get_angkatan(self):
        return self._angkatan

    def get_krs_data(self):
        return self._krs

    def set_krs_data(self, krs_dict):
        self._krs = krs_dict
        self.__hitung_ipk()

    def get_ipk(self):
        return round(self._ipk, 2)

    def __hitung_ipk(self):
        total_sks_bernilai = 0
        total_bobot_nilai = 0
        for mk_id, data_nilai in self._krs.items():
            nilai_angka = data_nilai.get('nilai_angka')
            if nilai_angka is not None:
                # Placeholder for SKS, ideally fetch from MataKuliah object
                sks = 3 # Assuming average SKS for simplicity in IPK calculation here
                if nilai_angka >= 85:
                    bobot = 4.0
                elif nilai_angka >= 75: 
                    bobot = 3.0
                elif nilai_angka >= 65: 
                    bobot = 2.0
                elif nilai_angka >= 50: 
                    bobot = 1.0
                else: 
                    bobot = 0.0
                total_bobot_nilai += bobot * sks
                total_sks_bernilai += sks

        if total_sks_bernilai > 0:
            self._ipk = total_bobot_nilai / total_sks_bernilai
        else:
            self._ipk = 0.0

    def __str__(self):
        return f"Mahasiswa: {self.get_nama()} (NIM: {self._nim}), Angkatan: {self._angkatan}, IPK: {self.get_ipk()}"

class Dosen(Orang):
    def __init__(self, nidn, nama, jenis_kelamin=None, tanggal_lahir=None, alamat=None, email=None, no_telepon=None, id_jurusan=None):
        super().__init__(nama, id_kampus=nidn, jenis_kelamin=jenis_kelamin, tanggal_lahir=tanggal_lahir, alamat=alamat, email=email, no_telepon=no_telepon, id_jurusan=id_jurusan)
        self._nidn = nidn
        self._mata_kuliah_diampu = []

    def get_nidn(self):
        return self._nidn

    def set_mata_kuliah_diampu(self, mk_list):
        self._mata_kuliah_diampu = mk_list

    def lihat_jadwal_mengajar(self):
        if not self._mata_kuliah_diampu:
            return "Belum mengampu mata kuliah apapun."
        jadwal = [f"  - {mk.get_nama()} ({mk.get_kode()})" for mk in self._mata_kuliah_diampu]
        return "\n".join(jadwal)

    def __str__(self):
        return f"Dosen: {self.get_nama()} (NIDN: {self._nidn})"

# --- Class KampusManager (Mengelola Interaksi Logic dan DB) ---
class KampusManager:
    def __init__(self, db_manager):
        self.db = db_manager
        self.jurusan = {}
        self.mahasiswa = {}
        self.dosen = {}
        self.mata_kuliah = {}
        self.load_data_from_db() # Load data upon initialization

    def load_data_from_db(self):
        """Memuat semua data dari database ke objek di memori."""
        self.jurusan = {}
        self.mahasiswa = {}
        self.dosen = {}
        self.mata_kuliah = {}

        # Muat Jurusan
        jurusan_records = self.db.execute_query("SELECT id_jurusan, kode_jurusan, nama_jurusan FROM jurusan", fetch_all=True)
        if jurusan_records:
            for row in jurusan_records:
                jurusan_obj = Jurusan(id_jurusan=row[0], kode=row[1], nama=row[2])
                self.jurusan[jurusan_obj.get_id()] = jurusan_obj

        # Muat Dosen
        dosen_records = self.db.execute_query("SELECT id_dosen, nidn, nama_dosen, jenis_kelamin, tanggal_lahir, alamat, email, no_telepon, id_jurusan FROM dosen", fetch_all=True)
        if dosen_records:
            for row in dosen_records:
                dosen_obj = Dosen(nidn=row[1], nama=row[2], jenis_kelamin=row[3], tanggal_lahir=row[4], alamat=row[5], email=row[6], no_telepon=row[7], id_jurusan=row[8])
                dosen_obj.set_id_db(row[0])
                self.dosen[dosen_obj.get_nidn()] = dosen_obj

        # Muat Mata Kuliah
        mk_records = self.db.execute_query("SELECT id_matakuliah, kode_matakuliah, nama_matakuliah, sks, semester, id_dosen, id_jurusan FROM matakuliah", fetch_all=True)
        if mk_records:
            for row in mk_records:
                mk_obj = MataKuliah(id_matakuliah=row[0], kode=row[1], nama=row[2], sks=row[3], semester=row[4], id_dosen=row[5], id_jurusan=row[6])
                self.mata_kuliah[mk_obj.get_kode()] = mk_obj
                if mk_obj.get_id_dosen():
                    found_dosen = next((dsn for dsn in self.dosen.values() if dsn.get_id_db() == mk_obj.get_id_dosen()), None)
                    if found_dosen:
                        found_dosen._mata_kuliah_diampu.append(mk_obj)

        # Muat Mahasiswa (Biodata)
        mhs_records = self.db.execute_query("SELECT nim, nama_lengkap, jenis_kelamin, tanggal_lahir, alamat, email, no_telepon, angkatan, id_jurusan FROM biodata", fetch_all=True)
        if mhs_records:
            for row in mhs_records:
                mhs_obj = Mahasiswa(nim=row[0], nama=row[1], jenis_kelamin=row[2], tanggal_lahir=row[3], alamat=row[4], email=row[5], no_telepon=row[6], angkatan=row[7], id_jurusan=row[8])
                self.mahasiswa[mhs_obj.get_nim()] = mhs_obj

        # Muat Nilai (KRS) untuk setiap Mahasiswa
        nilai_records = self.db.execute_query("SELECT nim, id_matakuliah, nilai_angka, nilai_huruf, tahun_akademik, semester_akademik FROM nilai", fetch_all=True)
        if nilai_records:
            for row in nilai_records:
                nim, id_matakuliah, nilai_angka, nilai_huruf, tahun_akademik, semester_akademik = row
                if nim in self.mahasiswa:
                    mhs_obj = self.mahasiswa[nim]
                    krs_entry = {
                        'nilai_angka': float(nilai_angka) if nilai_angka is not None else None,
                        'nilai_huruf': nilai_huruf,
                        'tahun_akademik': tahun_akademik,
                        'semester_akademik': semester_akademik
                    }
                    mhs_obj._krs[id_matakuliah] = krs_entry
                    mhs_obj._Mahasiswa__hitung_ipk()

    # --- Metode Tambah Data ---
    def tambah_jurusan(self, kode, nama):
        if self._get_jurusan_id_by_kode(kode):
            st.warning(f"Jurusan dengan kode {kode} sudah ada.")
            return False
        if self.db.execute_query("INSERT INTO jurusan (kode_jurusan, nama_jurusan) VALUES (%s, %s)", (kode, nama)):
            new_id = self.db.cursor.lastrowid
            jurusan_obj = Jurusan(id_jurusan=new_id, kode=kode, nama=nama)
            self.jurusan[new_id] = jurusan_obj
            st.success(f"Jurusan {nama} berhasil ditambahkan.")
            self.load_data_from_db()
            return True
        return False

    def tambah_dosen(self, nidn, nama, jenis_kelamin, tanggal_lahir, alamat, email, no_telepon, kode_jurusan):
        if nidn in self.dosen:
            st.warning(f"Dosen dengan NIDN {nidn} sudah ada.")
            return False
        id_jurusan = self._get_jurusan_id_by_kode(kode_jurusan)
        if id_jurusan is None:
            st.error(f"Error: Jurusan dengan kode {kode_jurusan} tidak ditemukan.")
            return False

        query = "INSERT INTO dosen (nidn, nama_dosen, jenis_kelamin, tanggal_lahir, alamat, email, no_telepon, id_jurusan) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        params = (nidn, nama, jenis_kelamin, tanggal_lahir, alamat, email, no_telepon, id_jurusan)
        if self.db.execute_query(query, params):
            new_id = self.db.cursor.lastrowid
            dosen_obj = Dosen(nidn=nidn, nama=nama, jenis_kelamin=jenis_kelamin, tanggal_lahir=tanggal_lahir, alamat=alamat, email=email, no_telepon=no_telepon, id_jurusan=id_jurusan)
            dosen_obj.set_id_db(new_id)
            self.dosen[nidn] = dosen_obj
            st.success(f"Dosen {nama} berhasil ditambahkan.")
            self.load_data_from_db()
            return True
        return False

    def tambah_mahasiswa(self, nim, nama_lengkap, jenis_kelamin, tanggal_lahir, alamat, email, no_telepon, angkatan, kode_jurusan):
        if nim in self.mahasiswa:
            st.warning(f"Mahasiswa dengan NIM {nim} sudah ada.")
            return False
        id_jurusan = self._get_jurusan_id_by_kode(kode_jurusan)
        if id_jurusan is None:
            st.error(f"Error: Jurusan dengan kode {kode_jurusan} tidak ditemukan.")
            return False

        query = "INSERT INTO biodata (nim, nama_lengkap, jenis_kelamin, tanggal_lahir, alamat, email, no_telepon, angkatan, id_jurusan) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        params = (nim, nama_lengkap, jenis_kelamin, tanggal_lahir, alamat, email, no_telepon, angkatan, id_jurusan)
        if self.db.execute_query(query, params):
            mhs_obj = Mahasiswa(nim=nim, nama=nama_lengkap, jenis_kelamin=jenis_kelamin, tanggal_lahir=tanggal_lahir, alamat=alamat, email=email, no_telepon=no_telepon, angkatan=angkatan, id_jurusan=id_jurusan)
            self.mahasiswa[nim] = mhs_obj
            st.success(f"Mahasiswa {nama_lengkap} berhasil ditambahkan.")
            self.load_data_from_db()
            return True
        return False

    def tambah_mata_kuliah(self, kode_mk, nama_mk, sks, semester, nidn_dosen, kode_jurusan):
        if kode_mk in self.mata_kuliah:
            st.warning(f"Mata Kuliah dengan kode {kode_mk} sudah ada.")
            return False

        id_dosen_db = self.dosen[nidn_dosen].get_id_db() if nidn_dosen in self.dosen else None
        if id_dosen_db is None:
            st.error(f"Error: Dosen dengan NIDN {nidn_dosen} tidak ditemukan.")
            return False

        id_jurusan_db = self._get_jurusan_id_by_kode(kode_jurusan)
        if id_jurusan_db is None:
            st.error(f"Error: Jurusan dengan kode {kode_jurusan} tidak ditemukan.")
            return False

        query = "INSERT INTO matakuliah (kode_matakuliah, nama_matakuliah, sks, semester, id_dosen, id_jurusan) VALUES (%s, %s, %s, %s, %s, %s)"
        params = (kode_mk, nama_mk, sks, semester, id_dosen_db, id_jurusan_db)
        if self.db.execute_query(query, params):
            new_id = self.db.cursor.lastrowid
            mk_obj = MataKuliah(id_matakuliah=new_id, kode=kode_mk, nama=nama_mk, sks=sks, semester=semester, id_dosen=id_dosen_db, id_jurusan=id_jurusan_db)
            self.mata_kuliah[kode_mk] = mk_obj
            if nidn_dosen in self.dosen:
                self.dosen[nidn_dosen]._mata_kuliah_diampu.append(mk_obj)
            st.success(f"Mata kuliah {nama_mk} berhasil ditambahkan.")
            self.load_data_from_db()
            return True
        return False

    def bulk_tambah_mata_kuliah(self, mata_kuliah_list, id_dosen_default, id_jurusan_default):
        """Menambahkan daftar mata kuliah secara massal jika belum ada."""
        added_count = 0
        st.subheader("Melakukan Impor Mata Kuliah Kurikulum...")
        for mk_data in mata_kuliah_list:
            kode_mk = mk_data['kode_matakuliah']
            nama_mk = mk_data['nama_matakuliah']
            sks = mk_data['sks']
            semester = mk_data['semester']

            if kode_mk in self.mata_kuliah:
                # st.info(f"Mata Kuliah dengan kode {kode_mk} sudah ada. Melewati.")
                continue

            # Gunakan id_dosen_default dan id_jurusan_default
            id_dosen_db = id_dosen_default
            id_jurusan_db = id_jurusan_default

            query = "INSERT INTO matakuliah (kode_matakuliah, nama_matakuliah, sks, semester, id_dosen, id_jurusan) VALUES (%s, %s, %s, %s, %s, %s)"
            params = (kode_mk, nama_mk, sks, semester, id_dosen_db, id_jurusan_db)
            if self.db.execute_query(query, params):
                new_id = self.db.cursor.lastrowid
                mk_obj = MataKuliah(id_matakuliah=new_id, kode=kode_mk, nama=nama_mk, sks=sks, semester=semester, id_dosen=id_dosen_db, id_jurusan=id_jurusan_db)
                self.mata_kuliah[kode_mk] = mk_obj
                added_count += 1
            else:
                st.error(f"Gagal menambahkan mata kuliah: {nama_mk} ({kode_mk})")
        
        self.load_data_from_db() # Reload data to reflect changes
        st.success(f"Impor selesai. {added_count} mata kuliah baru ditambahkan (jika belum ada).")
        return added_count


    # --- Metode Operasi KRS ---
    def ambil_mata_kuliah_mhs(self, nim_mhs, kode_mk, tahun_akademik, semester_akademik):
        mhs_obj = self.mahasiswa.get(nim_mhs)
        mk_obj = self.mata_kuliah.get(kode_mk)

        if not mhs_obj:
            st.error(f"Error: Mahasiswa dengan NIM {nim_mhs} tidak ditemukan.")
            return False
        if not mk_obj:
            st.error(f"Error: Mata Kuliah dengan kode {kode_mk} tidak ditemukan.")
            return False

        # Check if already registered for this specific course in the same academic year and semester
        check_query = "SELECT id_nilai FROM nilai WHERE nim = %s AND id_matakuliah = %s AND tahun_akademik = %s AND semester_akademik = %s"
        check_params = (nim_mhs, mk_obj.get_id(), tahun_akademik, semester_akademik)
        existing_krs = self.db.execute_query(check_query, check_params, fetch_one=True)

        if existing_krs:
            st.warning(f"Mahasiswa {mhs_obj.get_nama()} sudah mengambil mata kuliah {mk_obj.get_nama()} di tahun akademik dan semester yang sama.")
            return False

        query = "INSERT INTO nilai (nim, id_matakuliah, tahun_akademik, semester_akademik) VALUES (%s, %s, %s, %s)"
        params = (nim_mhs, mk_obj.get_id(), tahun_akademik, semester_akademik)
        if self.db.execute_query(query, params):
            st.success(f"Mahasiswa {mhs_obj.get_nama()} berhasil mengambil mata kuliah {mk_obj.get_nama()}.")
            self.load_data_from_db()
            return True
        return False

    def input_nilai_mhs(self, nim_mhs, kode_mk, nilai_angka, nilai_huruf, tahun_akademik, semester_akademik):
        mhs_obj = self.mahasiswa.get(nim_mhs)
        mk_obj = self.mata_kuliah.get(kode_mk)

        if not mhs_obj:
            st.error(f"Error: Mahasiswa dengan NIM {nim_mhs} tidak ditemukan.")
            return False
        if not mk_obj:
            st.error(f"Error: Mata Kuliah dengan kode {kode_mk} tidak ditemukan.")
            return False

        # Validate nilai
        if not isinstance(nilai_angka, (int, float)) or not (0 <= nilai_angka <= 100):
            st.error("Error: Nilai angka harus berupa angka antara 0 dan 100.")
            return False
        if not isinstance(nilai_huruf, str) or len(nilai_huruf) > 2:
            st.error("Error: Nilai huruf harus berupa string dengan maks 2 karakter.")
            return False

        # Find existing grade entry for the student, course, year, and semester
        check_query = "SELECT id_nilai FROM nilai WHERE nim = %s AND id_matakuliah = %s AND tahun_akademik = %s AND semester_akademik = %s"
        check_params = (nim_mhs, mk_obj.get_id(), tahun_akademik, semester_akademik)
        existing_nilai_record = self.db.execute_query(check_query, check_params, fetch_one=True)

        if existing_nilai_record:
            # Update existing grade
            query = "UPDATE nilai SET nilai_angka = %s, nilai_huruf = %s WHERE id_nilai = %s"
            params = (nilai_angka, nilai_huruf, existing_nilai_record[0])
            if self.db.execute_query(query, params):
                st.success(f"Nilai {nilai_angka} ({nilai_huruf}) untuk {mk_obj.get_nama()} berhasil diupdate untuk {mhs_obj.get_nama()}.")
                self.load_data_from_db()
                return True
        else:
            # If no existing entry, insert new grade
            st.warning(f"Mahasiswa {mhs_obj.get_nama()} belum mengambil {mk_obj.get_nama()} untuk TA {tahun_akademik} {semester_akademik} atau entri nilai tidak ditemukan. Menambahkan entri baru.")
            query = "INSERT INTO nilai (nim, id_matakuliah, nilai_angka, nilai_huruf, tahun_akademik, semester_akademik) VALUES (%s, %s, %s, %s, %s, %s)"
            params = (nim_mhs, mk_obj.get_id(), nilai_angka, nilai_huruf, tahun_akademik, semester_akademik)
            if self.db.execute_query(query, params):
                st.success(f"Nilai {nilai_angka} ({nilai_huruf}) untuk {mk_obj.get_nama()} berhasil dimasukkan untuk {mhs_obj.get_nama()}.")
                self.load_data_from_db()
                return True
        return False

    def _get_jurusan_id_by_kode(self, kode_jurusan):
        for j_id, j_obj in self.jurusan.items():
            if j_obj.get_kode() == kode_jurusan:
                return j_id
        return None

# Data Mata Kuliah dari Kurikulum Sistem Informasi (dari dokumen docx yang diberikan) 
# id_jurusan_SI = 23114 (Berdasarkan data awal database Anda) 
# id_dosen_default = 760310014 (NIDN: 1010107601, Junaidi Surya,M.kom) (sebagai placeholder sementara) 
KURIKULUM_SI_MK = [
    {"kode_matakuliah": "SIKK1201", "nama_matakuliah": "Pengantar Manajemen", "sks": 2, "semester": 1},
    {"kode_matakuliah": "FKPN1201", "nama_matakuliah": "Aljabar Vektor dan Matriks", "sks": 2, "semester": 1},
    {"kode_matakuliah": "SIKK1302", "nama_matakuliah": "Sistem Dan Teknologi Informasi", "sks": 3, "semester": 1},
    {"kode_matakuliah": "SIKK1403", "nama_matakuliah": "Pemrogramman Dasar (P)", "sks": 4, "semester": 1},
    {"kode_matakuliah": "FKKK1402", "nama_matakuliah": "Algorithma dan Pemrograman (P)", "sks": 4, "semester": 1},
    {"kode_matakuliah": "FKKK1403", "nama_matakuliah": "Sistem Operasi dan Arsitektur Komputer (P)", "sks": 3, "semester": 1},
    {"kode_matakuliah": "SIPN2202", "nama_matakuliah": "Pengantar Akuntansi", "sks": 2, "semester": 2},
    {"kode_matakuliah": "PK2201", "nama_matakuliah": "Pendidikan Agama", "sks": 2, "semester": 2},
    {"kode_matakuliah": "NHPN2303", "nama_matakuliah": "Statistika dan Penerapan", "sks": 3, "semester": 2},
    {"kode_matakuliah": "SIPN2204", "nama_matakuliah": "Bahasa Inggris I", "sks": 3, "semester": 2},
    {"kode_matakuliah": "PK2204", "nama_matakuliah": "Bahasa Indonesia", "sks": 2, "semester": 2},
    {"kode_matakuliah": "SIPN2205", "nama_matakuliah": "Matematika Komputasi", "sks": 2, "semester": 2},
    {"kode_matakuliah": "SIKK2304", "nama_matakuliah": "Algoritma dan Pemrograman (P II)", "sks": 3, "semester": 2},
    {"kode_matakuliah": "NHKK2302", "nama_matakuliah": "Aplikasi Perkantoran (P)", "sks": 3, "semester": 2},
    {"kode_matakuliah": "SIKK3305", "nama_matakuliah": "Sistem Informasi Manajemen", "sks": 3, "semester": 3},
    {"kode_matakuliah": "SIKK3306", "nama_matakuliah": "Manajemen Investasi Teknologi Informasi", "sks": 3, "semester": 3},
    {"kode_matakuliah": "SIKK3207", "nama_matakuliah": "Manajemen Proses Bisnis", "sks": 2, "semester": 3},
    {"kode_matakuliah": "SIKK3308", "nama_matakuliah": "Konsep Sistem Informasi", "sks": 3, "semester": 3},
    {"kode_matakuliah": "PK3202", "nama_matakuliah": "Pendidikan Pancasila", "sks": 2, "semester": 3},
    {"kode_matakuliah": "FKKB3304", "nama_matakuliah": "Manajemen & Sistem Basis Data", "sks": 3, "semester": 3},
    {"kode_matakuliah": "SIKB3301", "nama_matakuliah": "Pemrograman Berbasis Platform (P)", "sks": 4, "semester": 3},
    {"kode_matakuliah": "SIPN3306", "nama_matakuliah": "Bahasa Inggris II", "sks": 2, "semester": 3},
    {"kode_matakuliah": "SIKB3302", "nama_matakuliah": "Teknologi Basis Data", "sks": 3, "semester": 4},
    {"kode_matakuliah": "SIKK4309", "nama_matakuliah": "Analisis dan Perancangan Sistem Informasi", "sks": 3, "semester": 4},
    {"kode_matakuliah": "FKKK4305", "nama_matakuliah": "Komunikasi Data dan Jaringan Komputer (P)", "sks": 3, "semester": 4},
    {"kode_matakuliah": "SIKK4311", "nama_matakuliah": "Tata Kelola Teknologi Informasi", "sks": 3, "semester": 4},
    {"kode_matakuliah": "SIKK4312", "nama_matakuliah": "Manajemen Sains", "sks": 3, "semester": 4},
    {"kode_matakuliah": "PK4203", "nama_matakuliah": "Pendidikan Kewarganegaraan", "sks": 2, "semester": 4},
    {"kode_matakuliah": "SIKK4213", "nama_matakuliah": "Arsitektur SI/IT Perusahaan", "sks": 2, "semester": 4},
    {"kode_matakuliah": "SIKB4303", "nama_matakuliah": "Matakuliah Pilihan 1", "sks": 3, "semester": 4},
    {"kode_matakuliah": "SIKM401", "nama_matakuliah": "Lintas Prodi / MBKM", "sks": 0, "semester": 4},
    {"kode_matakuliah": "SIKK5314", "nama_matakuliah": "Analisis dan Manajemen Jaringan (P)", "sks": 3, "semester": 5},
    {"kode_matakuliah": "SIKB5304", "nama_matakuliah": "Audit Sistem informasi", "sks": 3, "semester": 5},
    {"kode_matakuliah": "SIKK5315", "nama_matakuliah": "Manajemen Proyek SI", "sks": 3, "semester": 5},
    {"kode_matakuliah": "SIPN5307", "nama_matakuliah": "Testing dan Implementasi Sistem Informasi", "sks": 3, "semester": 5},
    {"kode_matakuliah": "NHKK5203", "nama_matakuliah": "Technopreneur", "sks": 2, "semester": 5},
    {"kode_matakuliah": "FKKK5406", "nama_matakuliah": "Pemrograman berbasis Web (P)", "sks": 4, "semester": 5},
    {"kode_matakuliah": "SIKB5304B", "nama_matakuliah": "Matakuliah Pilihan 2", "sks": 3, "semester": 5}, # Added B to avoid duplicate key in the list with SIKB5304
    {"kode_matakuliah": "SIKM502", "nama_matakuliah": "Lintas Prodi / MBKM", "sks": 0, "semester": 5},
    {"kode_matakuliah": "FKKK6307", "nama_matakuliah": "Metode Penelitian", "sks": 3, "semester": 6},
    {"kode_matakuliah": "SIKK6316", "nama_matakuliah": "Sistem Multimedia", "sks": 3, "semester": 6},
    {"kode_matakuliah": "FKKK6208", "nama_matakuliah": "Komputer dan Masyarakat", "sks": 2, "semester": 6},
    {"kode_matakuliah": "SIKB6306", "nama_matakuliah": "Sistem Pendukung Keputusan Berbasis Model", "sks": 3, "semester": 6},
    {"kode_matakuliah": "SIKB6407", "nama_matakuliah": "Rekayasa Web", "sks": 4, "semester": 6},
    {"kode_matakuliah": "SIKB6307", "nama_matakuliah": "Matakuliah Pilihan 3", "sks": 3, "semester": 6},
    {"kode_matakuliah": "SIKB6409", "nama_matakuliah": "Matakuliah Pilihan 4", "sks": 4, "semester": 6},
    {"kode_matakuliah": "SIKM603", "nama_matakuliah": "MBKM / Magang Industri Dll", "sks": 0, "semester": 6},
    {"kode_matakuliah": "FKPB7209", "nama_matakuliah": "Etika Profesi", "sks": 2, "semester": 7},
    {"kode_matakuliah": "NHPB7404", "nama_matakuliah": "Kerja Praktek", "sks": 4, "semester": 7},
    {"kode_matakuliah": "SIKK7217", "nama_matakuliah": "Interpersonal Skill", "sks": 2, "semester": 7},
    {"kode_matakuliah": "SIKB7210", "nama_matakuliah": "Interaksi Manusia dan Komputer", "sks": 2, "semester": 7},
    {"kode_matakuliah": "SIKB7311", "nama_matakuliah": "Matakuliah Pilihan 5", "sks": 3, "semester": 7},
    {"kode_matakuliah": "SIKB7314", "nama_matakuliah": "Matakuliah Pilihan 6", "sks": 3, "semester": 7},
    {"kode_matakuliah": "SIKM704", "nama_matakuliah": "MBKM / Magang Industri Dll", "sks": 0, "semester": 7},
    {"kode_matakuliah": "SIKB8613", "nama_matakuliah": "Skripsi", "sks": 6, "semester": 8},
]


# Streamlit UI
st.set_page_config(layout="wide", page_title="Sistem Informasi Kampus")

st.title("👨‍🎓 Sistem Informasi Kampus 🏫")

# Initialize db_manager and kampus_app in session state
if 'db_manager' not in st.session_state:
    st.session_state.db_manager = DatabaseManager(DB_CONFIG)
    if st.session_state.db_manager.connect():
        st.session_state.db_manager.setup_tables()
        st.session_state.kampus_app = KampusManager(st.session_state.db_manager)
    else:
        st.error("Tidak dapat terhubung ke database. Mohon cek konfigurasi.")
        st.stop()
elif not st.session_state.db_manager.connection or not st.session_state.db_manager.connection.is_connected():
    if st.session_state.db_manager.connect():
        st.session_state.db_manager.setup_tables()
        st.session_state.kampus_app = KampusManager(st.session_state.db_manager)
    else:
        st.error("Tidak dapat terhubung ke database. Mohon cek konfigurasi.")
        st.stop()

kampus_app = st.session_state.kampus_app


# Sidebar for navigation
st.sidebar.title("Navigasi")
menu_selection = st.sidebar.radio(
    "Pilih Menu:",
    ["Dashboard", "Jurusan", "Dosen", "Mahasiswa", "Mata Kuliah", "KRS & Nilai"]
)

# --- Dashboard ---
if menu_selection == "Dashboard":
    st.header("Dashboard")
    st.write("Selamat datang di Sistem Informasi Kampus!")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Jurusan", len(kampus_app.jurusan))
    col2.metric("Total Dosen", len(kampus_app.dosen))
    col3.metric("Total Mahasiswa", len(kampus_app.mahasiswa))

    st.subheader("Sekilas Data")
    # Display recent data
    st.write("**Daftar Jurusan:**")
    jurusan_data = [{"ID": j.get_id(), "Kode": j.get_kode(), "Nama": j.get_nama()} for j in kampus_app.jurusan.values()]
    st.dataframe(jurusan_data, use_container_width=True)

    st.write("**Daftar Dosen:**")
    dosen_data = []
    for d in kampus_app.dosen.values():
        jurusan_obj = kampus_app.jurusan.get(d.get_id_jurusan())
        jurusan_nama = jurusan_obj.get_nama() if jurusan_obj else "N/A"
        dosen_data.append({"NIDN": d.get_nidn(), "Nama": d.get_nama(), "Jurusan": jurusan_nama, "Email": d.get_email()})
    st.dataframe(dosen_data, use_container_width=True)

    st.write("**Daftar Mahasiswa:**")
    mahasiswa_data = []
    for m in kampus_app.mahasiswa.values():
        jurusan_obj = kampus_app.jurusan.get(m.get_id_jurusan())
        jurusan_nama = jurusan_obj.get_nama() if jurusan_obj else "N/A"
        mahasiswa_data.append({"NIM": m.get_nim(), "Nama": m.get_nama(), "Angkatan": m.get_angkatan(), "Jurusan": jurusan_nama, "IPK": m.get_ipk()})
    st.dataframe(mahasiswa_data, use_container_width=True)

# --- Jurusan ---
elif menu_selection == "Jurusan":
    st.header("Manajemen Jurusan")
    st.subheader("Tambah Jurusan Baru")
    with st.form("form_tambah_jurusan"):
        kode_jurusan_input = st.text_input("Kode Jurusan (e.g., TI, SI)", key="add_jurusan_kode")
        nama_jurusan_input = st.text_input("Nama Jurusan (e.g., Teknik Informatika)", key="add_jurusan_nama")
        submitted = st.form_submit_button("Tambah Jurusan")
        if submitted:
            if kode_jurusan_input and nama_jurusan_input:
                kampus_app.tambah_jurusan(kode_jurusan_input.upper(), nama_jurusan_input)
            else:
                st.error("Kode Jurusan dan Nama Jurusan tidak boleh kosong.")

    st.subheader("Daftar Jurusan")
    jurusan_display_data = []
    for j_id, jurusan_obj in kampus_app.jurusan.items():
        jurusan_display_data.append({
            "ID Jurusan": jurusan_obj.get_id(),
            "Kode Jurusan": jurusan_obj.get_kode(),
            "Nama Jurusan": jurusan_obj.get_nama()
        })
    if jurusan_display_data:
        st.dataframe(jurusan_display_data, use_container_width=True)
    else:
        st.info("Belum ada data jurusan.")

# --- Dosen ---
elif menu_selection == "Dosen":
    st.header("Manajemen Dosen")
    st.subheader("Tambah Dosen Baru")
    with st.form("form_tambah_dosen"):
        nidn_input = st.text_input("NIDN", key="add_dosen_nidn")
        nama_dosen_input = st.text_input("Nama Dosen", key="add_dosen_nama")
        jenis_kelamin_input = st.selectbox("Jenis Kelamin", ["L", "P"], key="add_dosen_jk")
        tanggal_lahir_input = st.date_input("Tanggal Lahir", value=date(1980, 1, 1), key="add_dosen_dob")
        alamat_input = st.text_area("Alamat", key="add_dosen_alamat")
        email_input = st.text_input("Email", key="add_dosen_email")
        no_telepon_input = st.text_input("No. Telepon", key="add_dosen_telp")

        jurusan_options = {j.get_kode(): j.get_id() for j in kampus_app.jurusan.values()}
        selected_jurusan_kode = st.selectbox(
            "Pilih Jurusan",
            options=list(jurusan_options.keys()) if jurusan_options else ["(Tidak ada jurusan)"],
            key="add_dosen_jurusan"
        )
        submitted = st.form_submit_button("Tambah Dosen")
        if submitted:
            if nidn_input and nama_dosen_input and selected_jurusan_kode != "(Tidak ada jurusan)":
                kampus_app.tambah_dosen(nidn_input, nama_dosen_input, jenis_kelamin_input,
                                        tanggal_lahir_input, alamat_input, email_input,
                                        no_telepon_input, selected_jurusan_kode)
            else:
                st.error("Semua field wajib diisi, terutama NIDN, Nama Dosen, dan Jurusan.")

    st.subheader("Daftar Dosen")
    dosen_display_data = []
    for nidn, dosen_obj in kampus_app.dosen.items():
        jurusan_obj = kampus_app.jurusan.get(dosen_obj.get_id_jurusan())
        jurusan_nama = jurusan_obj.get_nama() if jurusan_obj else "N/A"
        dosen_display_data.append({
            "NIDN": dosen_obj.get_nidn(),
            "Nama Dosen": dosen_obj.get_nama(),
            "Jenis Kelamin": dosen_obj.get_jenis_kelamin(),
            "Tanggal Lahir": dosen_obj.get_tanggal_lahir(),
            "Email": dosen_obj.get_email(),
            "No. Telepon": dosen_obj.get_no_telepon(),
            "Jurusan": jurusan_nama
        })
    if dosen_display_data:
        st.dataframe(dosen_display_data, use_container_width=True)
    else:
        st.info("Belum ada data dosen.")

# --- Mahasiswa ---
elif menu_selection == "Mahasiswa":
    st.header("Manajemen Mahasiswa")
    st.subheader("Tambah Mahasiswa Baru")
    with st.form("form_tambah_mahasiswa"):
        nim_input = st.text_input("NIM", key="add_mhs_nim")
        nama_mhs_input = st.text_input("Nama Lengkap", key="add_mhs_nama")
        jenis_kelamin_mhs_input = st.selectbox("Jenis Kelamin", ["L", "P"], key="add_mhs_jk")
        tanggal_lahir_mhs_input = st.date_input("Tanggal Lahir", value=date(2005, 1, 1), key="add_mhs_dob")
        alamat_mhs_input = st.text_area("Alamat", key="add_mhs_alamat")
        email_mhs_input = st.text_input("Email", key="add_mhs_email")
        no_telepon_mhs_input = st.text_input("No. Telepon", key="add_mhs_telp")
        angkatan_mhs_input = st.number_input("Angkatan (Tahun)", min_value=1900, max_value=2100, value=2023, step=1, key="add_mhs_angkatan")

        jurusan_options = {j.get_kode(): j.get_id() for j in kampus_app.jurusan.values()}
        selected_jurusan_kode = st.selectbox(
            "Pilih Jurusan",
            options=list(jurusan_options.keys()) if jurusan_options else ["(Tidak ada jurusan)"],
            key="add_mhs_jurusan"
        )
        submitted = st.form_submit_button("Tambah Mahasiswa")
        if submitted:
            if nim_input and nama_mhs_input and selected_jurusan_kode != "(Tidak ada jurusan)":
                kampus_app.tambah_mahasiswa(nim_input, nama_mhs_input, jenis_kelamin_mhs_input,
                                            tanggal_lahir_mhs_input, alamat_mhs_input, email_mhs_input,
                                            no_telepon_mhs_input, angkatan_mhs_input, selected_jurusan_kode)
            else:
                st.error("Semua field wajib diisi, terutama NIM, Nama Lengkap, dan Jurusan.")

    st.subheader("Daftar Mahasiswa")
    mahasiswa_display_data = []
    for nim, mhs_obj in kampus_app.mahasiswa.items():
        jurusan_obj = kampus_app.jurusan.get(mhs_obj.get_id_jurusan())
        jurusan_nama = jurusan_obj.get_nama() if jurusan_obj else "N/A"
        mahasiswa_display_data.append({
            "NIM": mhs_obj.get_nim(),
            "Nama Lengkap": mhs_obj.get_nama(),
            "Jenis Kelamin": mhs_obj.get_jenis_kelamin(),
            "Tanggal Lahir": mhs_obj.get_tanggal_lahir(),
            "Email": mhs_obj.get_email(),
            "No. Telepon": mhs_obj.get_no_telepon(),
            "Angkatan": mhs_obj.get_angkatan(),
            "Jurusan": jurusan_nama,
            "IPK": mhs_obj.get_ipk()
        })
    if mahasiswa_display_data:
        st.dataframe(mahasiswa_display_data, use_container_width=True)
    else:
        st.info("Belum ada data mahasiswa.")

# --- Mata Kuliah ---
elif menu_selection == "Mata Kuliah":
    st.header("Manajemen Mata Kuliah")

    st.subheader("Import Mata Kuliah dari Kurikulum Sistem Informasi")
    # Using a unique key for the import button to prevent issues on rerun
    if st.button("Import Mata Kuliah Kurikulum SI", key="import_mk_si"):
        id_jurusan_si = 23114 # ID Jurusan Sistem Informasi (sesuai data database Anda) 
        id_dosen_placeholder = 760310014 # ID Dosen Junaidi Surya,M.kom (sebagai placeholder) 
        kampus_app.bulk_tambah_mata_kuliah(KURIKULUM_SI_MK, id_dosen_placeholder, id_jurusan_si)


    st.subheader("Tambah Mata Kuliah Baru Secara Manual")
    with st.form("form_tambah_mk"):
        kode_mk_input = st.text_input("Kode Mata Kuliah", key="add_mk_kode")
        nama_mk_input = st.text_input("Nama Mata Kuliah", key="add_mk_nama")
        sks_input = st.number_input("SKS", min_value=1, max_value=6, value=3, step=1, key="add_mk_sks")
        semester_input = st.number_input("Semester", min_value=1, max_value=8, value=1, step=1, key="add_mk_semester")

        dosen_options = {d.get_nidn(): d.get_nama() for d in kampus_app.dosen.values()}
        dosen_display_options = ["(Pilih Dosen)"] + [f"{nidn} - {nama}" for nidn, nama in dosen_options.items()]
        selected_dosen_str = st.selectbox(
            "Pilih Dosen Pengampu",
            options=dosen_display_options,
            key="add_mk_dosen"
        )
        nidn_dosen_selected = selected_dosen_str.split(" - ")[0] if selected_dosen_str != "(Pilih Dosen)" else None

        jurusan_options = {j.get_kode(): j.get_id() for j in kampus_app.jurusan.values()}
        selected_jurusan_kode = st.selectbox(
            "Pilih Jurusan",
            options=list(jurusan_options.keys()) if jurusan_options else ["(Tidak ada jurusan)"],
            key="add_mk_jurusan"
        )

        submitted = st.form_submit_button("Tambah Mata Kuliah")
        if submitted:
            if kode_mk_input and nama_mk_input and sks_input and nidn_dosen_selected and selected_jurusan_kode != "(Tidak ada jurusan)":
                kampus_app.tambah_mata_kuliah(kode_mk_input.upper(), nama_mk_input, sks_input,
                                             semester_input, nidn_dosen_selected, selected_jurusan_kode)
            else:
                st.error("Semua field wajib diisi, terutama Kode MK, Nama MK, SKS, Dosen, dan Jurusan.")

    st.subheader("Daftar Mata Kuliah")
    mk_display_data = []
    for kode, mk_obj in kampus_app.mata_kuliah.items():
        dosen_pengampu = next((dsn.get_nama() for dsn in kampus_app.dosen.values() if dsn.get_id_db() == mk_obj.get_id_dosen()), "N/A")
        jurusan_mk = next((jrs.get_nama() for jrs in kampus_app.jurusan.values() if jrs.get_id() == mk_obj.get_id_jurusan()), "N/A")
        mk_display_data.append({
            "ID MK": mk_obj.get_id(),
            "Kode MK": mk_obj.get_kode(),
            "Nama MK": mk_obj.get_nama(),
            "SKS": mk_obj.get_sks(),
            "Semester": mk_obj.get_semester(),
            "Dosen Pengampu": dosen_pengampu,
            "Jurusan": jurusan_mk
        })
    if mk_display_data:
        st.dataframe(mk_display_data, use_container_width=True)
    else:
        st.info("Belum ada data mata kuliah.")

# --- KRS & Nilai ---
elif menu_selection == "KRS & Nilai":
    st.header("Manajemen KRS & Nilai Mahasiswa")

    st.subheader("Ambil Mata Kuliah (Isi KRS)")
    with st.form("form_ambil_mk"):
        mhs_options = {m.get_nim(): m.get_nama() for m in kampus_app.mahasiswa.values()}
        mhs_display_options = ["(Pilih Mahasiswa)"] + [f"{nim} - {nama}" for nim, nama in mhs_options.items()]
        selected_mhs_str_krs = st.selectbox(
            "Pilih Mahasiswa",
            options=mhs_display_options,
            key="krs_mhs"
        )
        nim_selected_krs = selected_mhs_str_krs.split(" - ")[0] if selected_mhs_str_krs != "(Pilih Mahasiswa)" else None

        mk_options = {mk.get_kode(): mk.get_nama() for mk in kampus_app.mata_kuliah.values()}
        mk_display_options = ["(Pilih Mata Kuliah)"] + [f"{kode} - {nama}" for kode, nama in mk_options.items()]
        selected_mk_str_krs = st.selectbox(
            "Pilih Mata Kuliah",
            options=mk_display_options,
            key="krs_mk"
        )
        kode_mk_selected_krs = selected_mk_str_krs.split(" - ")[0] if selected_mk_str_krs != "(Pilih Mata Kuliah)" else None

        tahun_akademik_krs = st.text_input("Tahun Akademik (e.g., 2024/2025)", key="krs_tahun")
        semester_akademik_krs = st.selectbox("Semester Akademik", ["Ganjil", "Genap", "Pendek"], key="krs_semester")

        submitted_krs = st.form_submit_button("Ambil Mata Kuliah")
        if submitted_krs:
            if nim_selected_krs and kode_mk_selected_krs and tahun_akademik_krs:
                kampus_app.ambil_mata_kuliah_mhs(nim_selected_krs, kode_mk_selected_krs, tahun_akademik_krs, semester_akademik_krs)
            else:
                st.error("Semua field KRS harus diisi.")

    st.subheader("Input / Update Nilai Mahasiswa")
    with st.form("form_input_nilai"):
        mhs_options_nilai = {m.get_nim(): m.get_nama() for m in kampus_app.mahasiswa.values()}
        mhs_display_options_nilai = ["(Pilih Mahasiswa)"] + [f"{nim} - {nama}" for nim, nama in mhs_options_nilai.items()]
        selected_mhs_str_nilai = st.selectbox(
            "Pilih Mahasiswa",
            options=mhs_display_options_nilai,
            key="nilai_mhs"
        )
        nim_selected_nilai = selected_mhs_str_nilai.split(" - ")[0] if selected_mhs_str_nilai != "(Pilih Mahasiswa)" else None

        mk_options_nilai = {mk.get_kode(): mk.get_nama() for mk in kampus_app.mata_kuliah.values()}
        mk_display_options_nilai = ["(Pilih Mata Kuliah)"] + [f"{kode} - {nama}" for kode, nama in mk_options_nilai.items()]
        selected_mk_str_nilai = st.selectbox(
            "Pilih Mata Kuliah",
            options=mk_display_options_nilai,
            key="nilai_mk"
        )
        kode_mk_selected_nilai = selected_mk_str_nilai.split(" - ")[0] if selected_mk_str_nilai != "(Pilih Mata Kuliah)" else None

        nilai_angka_input = st.number_input("Nilai Angka (0-100)", min_value=0.0, max_value=100.0, value=0.0, step=0.1, key="nilai_angka")
        nilai_huruf_input = st.text_input("Nilai Huruf (e.g., A, B+, C)", max_chars=2, key="nilai_huruf")
        tahun_akademik_nilai = st.text_input("Tahun Akademik (e.g., 2024/2025)", key="nilai_tahun")
        semester_akademik_nilai = st.selectbox("Semester Akademik", ["Ganjil", "Genap", "Pendek"], key="nilai_semester")

        submitted_nilai = st.form_submit_button("Input/Update Nilai")
        if submitted_nilai:
            if nim_selected_nilai and kode_mk_selected_nilai and tahun_akademik_nilai and nilai_huruf_input:
                kampus_app.input_nilai_mhs(nim_selected_nilai, kode_mk_selected_nilai,
                                           nilai_angka_input, nilai_huruf_input.upper(),
                                           tahun_akademik_nilai, semester_akademik_nilai)
            else:
                st.error("Semua field nilai harus diisi.")

    st.subheader("Daftar Nilai Mahasiswa")
    nilai_display_data = []
    for mhs_nim, mhs_obj in kampus_app.mahasiswa.items():
        if mhs_obj.get_krs_data():
            for mk_id, nilai_data in mhs_obj.get_krs_data().items():
                mk_obj_found = next((mk for mk in kampus_app.mata_kuliah.values() if mk.get_id() == mk_id), None)
                mk_nama = mk_obj_found.get_nama() if mk_obj_found else f"MK ID: {mk_id}"
                mk_kode = mk_obj_found.get_kode() if mk_obj_found else "N/A"
                nilai_display_data.append({
                    "NIM": mhs_obj.get_nim(),
                    "Nama Mahasiswa": mhs_obj.get_nama(),
                    "Kode MK": mk_kode,
                    "Nama Mata Kuliah": mk_nama,
                    "Nilai Angka": nilai_data['nilai_angka'],
                    "Nilai Huruf": nilai_data['nilai_huruf'],
                    "Tahun Akademik": nilai_data['tahun_akademik'],
                    "Semester": nilai_data['semester_akademik']
                })
    if nilai_display_data:
        st.dataframe(nilai_display_data, use_container_width=True)
    else:
        st.info("Belum ada data nilai.")