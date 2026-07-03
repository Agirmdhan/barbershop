from utils.database import Database
from models.barber import Barber
from utils.helpers import hash_password, verify_password

class BarberController:
    """Controller untuk Barber"""

    def __init__(self):
        self.db = Database('data')

    def create_barber(self, nama, nohp, usia, username, password, spesialisasi):
        """Membuat barber baru"""
        if self.db.get_barber_by_username(username):
            return False, "Username barber sudah terdaftar"
        if self.db.get_barber_by_nohp(nohp):
            return False, "Barber dengan nomor HP ini sudah terdaftar"

        barber_id = self.db.generate_id("BAR", "barber")
        hashed_password = hash_password(password)
        barber = Barber(barber_id, nama, nohp, usia, username, hashed_password, spesialisasi)
        barber_data = barber.get_info_dict()

        if self.db.save_barber(barber_data):
            return True, f"Barber {nama} berhasil ditambahkan"
        return False, "Gagal menambahkan barber"

    def login_barber(self, username, password):
        """Login barber menggunakan username dan password."""
        barber = self.db.get_barber_by_username(username)
        if barber and verify_password(password, barber.get('password', '')):
            return True, barber, "Login barber berhasil"
        return False, None, "Username atau password barber tidak cocok"
    
    def get_all_barbers(self):
        """Mendapatkan semua barber"""
        return self.db.get_all_barbers()
    
    def get_barber_by_id(self, barber_id):
        """Mendapatkan barber berdasarkan ID"""
        return self.db.get_barber_by_id(barber_id)
    
    def get_available_barbers(self):
        """Mendapatkan barber yang tersedia"""
        barbers = self.db.get_all_barbers()
        return [b for b in barbers if b.get('status') == 'Tersedia']
    
    def update_barber(self, barber_id, nama=None, nohp=None, usia=None, spesialisasi=None, status=None):
        """Update data barber"""
        barber_data = {}
        if nama:
            barber_data['nama'] = nama
        if nohp:
            barber_data['nohp'] = nohp
        if usia:
            barber_data['usia'] = usia
        if spesialisasi:
            barber_data['spesialisasi'] = spesialisasi
        if status:
            barber_data['status'] = status
        
        if self.db.update_barber(barber_id, barber_data):
            return True, "Barber berhasil diupdate"
        return False, "Gagal mengupdate barber"
    
    def delete_barber(self, barber_id):
        """Menghapus barber"""
        if self.db.delete_barber(barber_id):
            return True, "Barber berhasil dihapus"
        return False, "Gagal menghapus barber"
    
    def update_status(self, barber_id, status):
        """Mengubah status barber"""
        valid_status = ["Tersedia", "Sibuk", "Libur"]
        if status not in valid_status:
            return False, f"Status harus salah satu dari: {', '.join(valid_status)}"
        
        if self.db.update_barber(barber_id, {'status': status}):
            return True, f"Status barber berhasil diubah menjadi {status}"
        return False, "Gagal mengubah status barber"
