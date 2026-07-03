from utils.database import Database
from models.admin import Admin
from utils.helpers import hash_password, verify_password

class AdminController:
    """Controller untuk Admin"""
    
    def __init__(self):
        self.db = Database('data')
    
    def register_admin(self, nama, nohp, usia, username, password):
        """Register admin baru"""
        # Check if username already exists
        if self.db.get_admin_by_username(username):
            return False, "Username sudah terdaftar"
        
        admin_id = self.db.generate_id("ADM", "admin")
        hashed_password = hash_password(password)
        
        admin = Admin(admin_id, nama, nohp, usia, username, hashed_password)
        admin_data = admin.get_info_dict()
        
        if self.db.save_admin(admin_data):
            return True, f"Admin {nama} berhasil didaftarkan"
        return False, "Gagal mendaftarkan admin"
    
    def login_admin(self, username, password):
        """Login admin"""
        admin = self.db.get_admin_by_username(username)
        if not admin:
            return False, None, "Username tidak ditemukan"
        
        if verify_password(password, admin['password']):
            return True, admin, "Login berhasil"
        return False, None, "Password salah"
    
    def get_all_admins(self):
        """Mendapatkan semua admin"""
        return self.db.get_all_admins()
    
    def get_admin_by_username(self, username):
        """Mendapatkan admin berdasarkan username"""
        return self.db.get_admin_by_username(username)
    
    def update_admin(self, username, nama=None, nohp=None, usia=None):
        """Update data admin"""
        admin_data = {}
        if nama:
            admin_data['nama'] = nama
        if nohp:
            admin_data['nohp'] = nohp
        if usia:
            admin_data['usia'] = usia
        
        if self.db.update_admin(username, admin_data):
            return True, "Admin berhasil diupdate"
        return False, "Gagal mengupdate admin"
    
    def change_password(self, username, old_password, new_password):
        """Mengubah password admin"""
        admin = self.db.get_admin_by_username(username)
        if not admin:
            return False, "Admin tidak ditemukan"
        
        if not verify_password(old_password, admin['password']):
            return False, "Password lama salah"
        
        hashed_new_password = hash_password(new_password)
        if self.db.update_admin(username, {'password': hashed_new_password}):
            return True, "Password berhasil diubah"
        return False, "Gagal mengubah password"
