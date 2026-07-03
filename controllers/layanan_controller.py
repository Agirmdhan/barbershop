from utils.database import Database
from models.layanan import Layanan

class LayananController:
    """Controller untuk Layanan"""
    
    def __init__(self):
        self.db = Database('data')
    
    def create_layanan(self, nama_layanan, harga, durasi, deskripsi=""):
        """Membuat layanan baru"""
        layanan_id = self.db.generate_id("LAY", "layanan")
        layanan = Layanan(layanan_id, nama_layanan, harga, durasi, deskripsi)
        layanan_data = layanan.get_info_dict()
        
        if self.db.save_layanan(layanan_data):
            return True, f"Layanan {nama_layanan} berhasil ditambahkan"
        return False, "Gagal menambahkan layanan"
    
    def get_all_layanan(self):
        """Mendapatkan semua layanan"""
        return self.db.get_all_layanan()
    
    def get_layanan_by_id(self, layanan_id):
        """Mendapatkan layanan berdasarkan ID"""
        return self.db.get_layanan_by_id(layanan_id)
    
    def update_layanan(self, layanan_id, nama_layanan=None, harga=None, durasi=None, deskripsi=None):
        """Update data layanan"""
        layanan_data = {}
        if nama_layanan:
            layanan_data['nama_layanan'] = nama_layanan
        if harga:
            layanan_data['harga'] = harga
        if durasi:
            layanan_data['durasi'] = durasi
        if deskripsi:
            layanan_data['deskripsi'] = deskripsi
        
        if self.db.update_layanan(layanan_id, layanan_data):
            return True, "Layanan berhasil diupdate"
        return False, "Gagal mengupdate layanan"
    
    def delete_layanan(self, layanan_id):
        """Menghapus layanan"""
        if self.db.delete_layanan(layanan_id):
            return True, "Layanan berhasil dihapus"
        return False, "Gagal menghapus layanan"
