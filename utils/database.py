import json
import os
from datetime import datetime
from pathlib import Path

class Database:
    """Class untuk mengelola database menggunakan JSON"""
    
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.ensure_data_dir()
        
        self.admins_file = os.path.join(data_dir, "admins.json")
        self.barbers_file = os.path.join(data_dir, "barbers.json")
        self.pelanggan_file = os.path.join(data_dir, "pelanggan.json")
        self.layanan_file = os.path.join(data_dir, "layanan.json")
        self.reservasi_file = os.path.join(data_dir, "reservasi.json")
        self.pembayaran_file = os.path.join(data_dir, "pembayaran.json")
        self.riwayat_file = os.path.join(data_dir, "riwayat_layanan.json")
        
        self.initialize_files()
    
    def ensure_data_dir(self):
        """Memastikan direktori data ada"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def initialize_files(self):
        """Inisialisasi file JSON jika belum ada"""
        files = [
            self.admins_file,
            self.barbers_file,
            self.pelanggan_file,
            self.layanan_file,
            self.reservasi_file,
            self.pembayaran_file,
            self.riwayat_file
        ]
        
        for file in files:
            if not os.path.exists(file):
                with open(file, 'w') as f:
                    json.dump([], f)

        self._create_default_admin_if_needed()
    
    def _create_default_admin_if_needed(self):
        """Buat akun admin default jika belum ada admin."""
        from utils.helpers import hash_password

        admins = self.get_all_admins()
        if not admins:
            default_admin = {
                'id_pegawai': 'ADM001',
                'nama': 'Admin Master',
                'nohp': '081234567890',
                'usia': 30,
                'username': 'admin',
                'password': hash_password('admin123'),
                'role': 'admin',
                'tanggal_dibuat': datetime.now().isoformat()
            }
            self.save_admin(default_admin)

    def read_json(self, filename):
        """Membaca file JSON"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def write_json(self, filename, data):
        """Menulis ke file JSON"""
        # --- IMPLEMENTASI Try-Except-Finally ---
        try:
            # Blok TRY: Mencoba membuka dan menulis data ke file
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            # Blok EXCEPT: Menangkap error jika gagal menulis (misal: memori penuh atau folder read-only)
            print(f"[ERROR] Terjadi kesalahan saat mencoba menulis ke {filename}: {e}")
            
        finally:
            print(f"[LOG FINALLY] Proses I/O pada file '{filename}' telah selesai dieksekusi.")
        # ---------------------------------------
    
    # ========== ADMIN OPERATIONS ==========
    
    def save_admin(self, admin_data):
        """Menyimpan data admin"""
        admins = self.read_json(self.admins_file)
        admin_data['tanggal_dibuat'] = datetime.now().isoformat()
        admins.append(admin_data)
        self.write_json(self.admins_file, admins)
        return True
    
    def get_all_admins(self):
        """Mendapatkan semua admin"""
        return self.read_json(self.admins_file)
    
    def get_admin_by_username(self, username):
        """Mendapatkan admin berdasarkan username"""
        admins = self.read_json(self.admins_file)
        for admin in admins:
            if admin.get('username') == username:
                return admin
        return None
    
    def update_admin(self, username, admin_data):
        """Update data admin"""
        admins = self.read_json(self.admins_file)
        for i, admin in enumerate(admins):
            if admin.get('username') == username:
                admin.update(admin_data)
                self.write_json(self.admins_file, admins)
                return True
        return False
    
    # ========== BARBER OPERATIONS ==========
    
    def save_barber(self, barber_data):
        """Menyimpan data barber"""
        barbers = self.read_json(self.barbers_file)
        barber_data['tanggal_dibuat'] = datetime.now().isoformat()
        barbers.append(barber_data)
        self.write_json(self.barbers_file, barbers)
        return True
    
    def get_all_barbers(self):
        """Mendapatkan semua barber"""
        return self.read_json(self.barbers_file)
    
    def get_barber_by_id(self, id_pegawai):
        """Mendapatkan barber berdasarkan ID"""
        barbers = self.read_json(self.barbers_file)
        for barber in barbers:
            if barber.get('id_pegawai') == id_pegawai:
                return barber
        return None

    def get_barber_by_username(self, username):
        """Mendapatkan barber berdasarkan username"""
        barbers = self.read_json(self.barbers_file)
        for barber in barbers:
            if barber.get('username') == username:
                return barber
        return None

    def get_barber_by_nohp(self, nohp):
        """Mendapatkan barber berdasarkan nomor HP"""
        barbers = self.read_json(self.barbers_file)
        for barber in barbers:
            if barber.get('nohp') == nohp:
                return barber
        return None
    
    def update_barber(self, id_pegawai, barber_data):
        """Update data barber"""
        barbers = self.read_json(self.barbers_file)
        for i, barber in enumerate(barbers):
            if barber.get('id_pegawai') == id_pegawai:
                barber.update(barber_data)
                self.write_json(self.barbers_file, barbers)
                return True
        return False
    
    def delete_barber(self, id_pegawai):
        """Menghapus barber"""
        barbers = self.read_json(self.barbers_file)
        barbers = [b for b in barbers if b.get('id_pegawai') != id_pegawai]
        self.write_json(self.barbers_file, barbers)
        return True
    
    # ========== PELANGGAN OPERATIONS ==========
    
    def save_pelanggan(self, pelanggan_data):
        """Menyimpan data pelanggan"""
        pelanggan = self.read_json(self.pelanggan_file)
        pelanggan_data['tanggal_daftar'] = datetime.now().isoformat()
        pelanggan.append(pelanggan_data)
        self.write_json(self.pelanggan_file, pelanggan)
        return True
    
    def get_all_pelanggan(self):
        """Mendapatkan semua pelanggan"""
        return self.read_json(self.pelanggan_file)
    
    def get_pelanggan_by_id(self, id_pelanggan):
        """Mendapatkan pelanggan berdasarkan ID"""
        pelanggan_list = self.read_json(self.pelanggan_file)
        for p in pelanggan_list:
            if p.get('id_pelanggan') == id_pelanggan:
                return p
        return None

    def get_pelanggan_by_email(self, email):
        """Mendapatkan pelanggan berdasarkan email"""
        pelanggan_list = self.read_json(self.pelanggan_file)
        for p in pelanggan_list:
            if p.get('email') == email:
                return p
        return None

    def get_pelanggan_by_nohp(self, nomor_hp):
        """Mendapatkan pelanggan berdasarkan nomor HP"""
        pelanggan_list = self.read_json(self.pelanggan_file)
        for p in pelanggan_list:
            if p.get('nomor_hp') == nomor_hp:
                return p
        return None
    
    def update_pelanggan(self, id_pelanggan, pelanggan_data):
        """Update data pelanggan"""
        pelanggan_list = self.read_json(self.pelanggan_file)
        for i, p in enumerate(pelanggan_list):
            if p.get('id_pelanggan') == id_pelanggan:
                p.update(pelanggan_data)
                self.write_json(self.pelanggan_file, pelanggan_list)
                return True
        return False
    
    def delete_pelanggan(self, id_pelanggan):
        """Menghapus pelanggan"""
        pelanggan_list = self.read_json(self.pelanggan_file)
        pelanggan_list = [p for p in pelanggan_list if p.get('id_pelanggan') != id_pelanggan]
        self.write_json(self.pelanggan_file, pelanggan_list)
        return True
    
    # ========== LAYANAN OPERATIONS ==========
    
    def save_layanan(self, layanan_data):
        """Menyimpan data layanan"""
        layanan = self.read_json(self.layanan_file)
        layanan_data['tanggal_dibuat'] = datetime.now().isoformat()
        layanan.append(layanan_data)
        self.write_json(self.layanan_file, layanan)
        return True
    
    def get_all_layanan(self):
        """Mendapatkan semua layanan"""
        return self.read_json(self.layanan_file)
    
    def get_layanan_by_id(self, id_layanan):
        """Mendapatkan layanan berdasarkan ID"""
        layanan_list = self.read_json(self.layanan_file)
        for l in layanan_list:
            if l.get('id_layanan') == id_layanan:
                return l
        return None
    
    def update_layanan(self, id_layanan, layanan_data):
        """Update data layanan"""
        layanan_list = self.read_json(self.layanan_file)
        for i, l in enumerate(layanan_list):
            if l.get('id_layanan') == id_layanan:
                l.update(layanan_data)
                self.write_json(self.layanan_file, layanan_list)
                return True
        return False
    
    def delete_layanan(self, id_layanan):
        """Menghapus layanan"""
        layanan_list = self.read_json(self.layanan_file)
        layanan_list = [l for l in layanan_list if l.get('id_layanan') != id_layanan]
        self.write_json(self.layanan_file, layanan_list)
        return True
    
    # ========== RESERVASI OPERATIONS ==========
    
    def save_reservasi(self, reservasi_data):
        """Menyimpan data reservasi"""
        reservasi = self.read_json(self.reservasi_file)
        reservasi_data['tanggal_dibuat'] = datetime.now().isoformat()
        reservasi.append(reservasi_data)
        self.write_json(self.reservasi_file, reservasi)
        return True
    
    def get_all_reservasi(self):
        """Mendapatkan semua reservasi"""
        return self.read_json(self.reservasi_file)
    
    def get_reservasi_by_id(self, id_reservasi):
        """Mendapatkan reservasi berdasarkan ID"""
        reservasi_list = self.read_json(self.reservasi_file)
        for r in reservasi_list:
            if r.get('id_reservasi') == id_reservasi:
                return r
        return None
    
    def get_reservasi_by_pelanggan(self, id_pelanggan):
        """Mendapatkan reservasi berdasarkan pelanggan"""
        reservasi_list = self.read_json(self.reservasi_file)
        return [r for r in reservasi_list if r.get('id_pelanggan') == id_pelanggan]
    
    def get_reservasi_by_barber(self, id_barber):
        """Mendapatkan reservasi berdasarkan barber"""
        reservasi_list = self.read_json(self.reservasi_file)
        return [r for r in reservasi_list if r.get('id_barber') == id_barber]
    
    def update_reservasi(self, id_reservasi, reservasi_data):
        """Update data reservasi"""
        reservasi_list = self.read_json(self.reservasi_file)
        for i, r in enumerate(reservasi_list):
            if r.get('id_reservasi') == id_reservasi:
                r.update(reservasi_data)
                self.write_json(self.reservasi_file, reservasi_list)
                return True
        return False
    
    def delete_reservasi(self, id_reservasi):
        """Menghapus reservasi"""
        reservasi_list = self.read_json(self.reservasi_file)
        reservasi_list = [r for r in reservasi_list if r.get('id_reservasi') != id_reservasi]
        self.write_json(self.reservasi_file, reservasi_list)
        return True
    
    # ========== PEMBAYARAN OPERATIONS ==========
    
    def save_pembayaran(self, pembayaran_data):
        """Menyimpan data pembayaran"""
        pembayaran = self.read_json(self.pembayaran_file)
        pembayaran_data['tanggal_dibuat'] = datetime.now().isoformat()
        pembayaran.append(pembayaran_data)
        self.write_json(self.pembayaran_file, pembayaran)
        return True
    
    def get_all_pembayaran(self):
        """Mendapatkan semua pembayaran"""
        return self.read_json(self.pembayaran_file)
    
    def get_pembayaran_by_id(self, id_pembayaran):
        """Mendapatkan pembayaran berdasarkan ID"""
        pembayaran_list = self.read_json(self.pembayaran_file)
        for p in pembayaran_list:
            if p.get('id_pembayaran') == id_pembayaran:
                return p
        return None
    
    def get_pembayaran_by_reservasi(self, id_reservasi):
        """Mendapatkan pembayaran berdasarkan reservasi"""
        pembayaran_list = self.read_json(self.pembayaran_file)
        for p in pembayaran_list:
            if p.get('id_reservasi') == id_reservasi:
                return p
        return None
    
    def update_pembayaran(self, id_pembayaran, pembayaran_data):
        """Update data pembayaran"""
        pembayaran_list = self.read_json(self.pembayaran_file)
        for i, p in enumerate(pembayaran_list):
            if p.get('id_pembayaran') == id_pembayaran:
                p.update(pembayaran_data)
                self.write_json(self.pembayaran_file, pembayaran_list)
                return True
        return False
    
    # ========== RIWAYAT LAYANAN OPERATIONS ==========
    
    def save_riwayat(self, riwayat_data):
        """Menyimpan riwayat layanan"""
        riwayat = self.read_json(self.riwayat_file)
        riwayat_data['tanggal_dibuat'] = datetime.now().isoformat()
        riwayat.append(riwayat_data)
        self.write_json(self.riwayat_file, riwayat)
        return True
    
    def get_all_riwayat(self):
        """Mendapatkan semua riwayat layanan"""
        return self.read_json(self.riwayat_file)
    
    def get_riwayat_by_pelanggan(self, id_pelanggan):
        """Mendapatkan riwayat layanan berdasarkan pelanggan"""
        riwayat_list = self.read_json(self.riwayat_file)
        return [r for r in riwayat_list if r.get('id_pelanggan') == id_pelanggan]
    
    def get_riwayat_by_id(self, id_riwayat):
        """Mendapatkan riwayat berdasarkan ID"""
        riwayat_list = self.read_json(self.riwayat_file)
        for r in riwayat_list:
            if r.get('id_riwayat') == id_riwayat:
                return r
        return None
    
    def delete_riwayat(self, id_riwayat):
        """Menghapus riwayat layanan"""
        riwayat_list = self.read_json(self.riwayat_file)
        riwayat_list = [r for r in riwayat_list if r.get('id_riwayat') != id_riwayat]
        self.write_json(self.riwayat_file, riwayat_list)
        return True
    
    # ========== HELPER METHODS ==========
    
    def generate_id(self, prefix, collection_name):
        """Generate ID unik"""
        if collection_name == "admin":
            data = self.get_all_admins()
        elif collection_name == "barber":
            data = self.get_all_barbers()
        elif collection_name == "pelanggan":
            data = self.get_all_pelanggan()
        elif collection_name == "layanan":
            data = self.get_all_layanan()
        elif collection_name == "reservasi":
            data = self.get_all_reservasi()
        elif collection_name == "pembayaran":
            data = self.get_all_pembayaran()
        elif collection_name == "riwayat":
            data = self.get_all_riwayat()
        else:
            return f"{prefix}001"
        
        if not data:
            return f"{prefix}001"
        
        # Extract numbers from IDs and get the max
        numbers = []
        for item in data:
            if collection_name == "admin":
                id_str = item.get('id_pegawai', '')
            elif collection_name in ["barber", "riwayat"]:
                id_str = item.get('id_pegawai', '') if collection_name == "barber" else item.get('id_riwayat', '')
            else:
                id_str = item.get(f'id_{collection_name}', '')
            
            try:
                num = int(id_str.replace(prefix, ''))
                numbers.append(num)
            except:
                pass
        
        next_num = max(numbers) + 1 if numbers else 1
        return f"{prefix}{str(next_num).zfill(3)}"