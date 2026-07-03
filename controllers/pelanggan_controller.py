from utils.database import Database
from models.pelanggan import Pelanggan
from utils.helpers import hash_password, verify_password

class PelangganController:
    """Controller untuk Pelanggan"""

    def __init__(self):
        self.db = Database('data')

    def create_pelanggan(self, nama, email, nomor_hp, password):
        """Membuat pelanggan baru"""
        if self.db.get_pelanggan_by_email(email):
            return False, "Email sudah terdaftar"
        if self.db.get_pelanggan_by_nohp(nomor_hp):
            return False, "Nomor HP sudah terdaftar"

        pelanggan_id = self.db.generate_id("PLG", "pelanggan")
        hashed_password = hash_password(password)
        pelanggan = Pelanggan(pelanggan_id, nama, email, nomor_hp, hashed_password)
        pelanggan_data = pelanggan.get_info_dict()

        if self.db.save_pelanggan(pelanggan_data):
            return True, f"Pelanggan {nama} berhasil ditambahkan"
        return False, "Gagal menambahkan pelanggan"

    def login_pelanggan(self, email, password):
        """Login pelanggan menggunakan email dan password."""
        pelanggan = self.db.get_pelanggan_by_email(email)
        if pelanggan and verify_password(password, pelanggan.get('password', '')):
            return True, pelanggan, "Login pelanggan berhasil"
        return False, None, "Email atau password tidak cocok"
    
    def get_all_pelanggan(self):
        """Mendapatkan semua pelanggan"""
        return self.db.get_all_pelanggan()
    
    def get_pelanggan_by_id(self, pelanggan_id):
        """Mendapatkan pelanggan berdasarkan ID"""
        return self.db.get_pelanggan_by_id(pelanggan_id)
    
    def update_pelanggan(self, pelanggan_id, nama=None, email=None, nomor_hp=None):
        """Update data pelanggan"""
        pelanggan_data = {}
        if nama:
            pelanggan_data['nama'] = nama
        if email:
            pelanggan_data['email'] = email
        if nomor_hp:
            pelanggan_data['nomor_hp'] = nomor_hp
        
        if self.db.update_pelanggan(pelanggan_id, pelanggan_data):
            return True, "Pelanggan berhasil diupdate"
        return False, "Gagal mengupdate pelanggan"
    
    def delete_pelanggan(self, pelanggan_id):
        """Menghapus pelanggan"""
        if self.db.delete_pelanggan(pelanggan_id):
            return True, "Pelanggan berhasil dihapus"
        return False, "Gagal menghapus pelanggan"
    
    def get_riwayat_pelanggan(self, pelanggan_id):
        """Mendapatkan riwayat layanan pelanggan"""
        return self.db.get_riwayat_by_pelanggan(pelanggan_id)
    
    def get_reservasi_pelanggan(self, pelanggan_id):
        """Mendapatkan reservasi pelanggan"""
        return self.db.get_reservasi_by_pelanggan(pelanggan_id)
