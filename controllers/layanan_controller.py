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
        """Update data layanan dengan validasi"""
        layanan_data = {}
        
        # Validasi harga jika diberikan
        if harga is not None:
            if not Layanan.validasi_nilai_positif(harga):
                return False, "Harga harus lebih besar dari 0"
            layanan_data['harga'] = harga
        
        # Validasi durasi jika diberikan
        if durasi is not None:
            if not Layanan.validasi_nilai_positif(durasi):
                return False, "Durasi harus lebih besar dari 0"
            layanan_data['durasi'] = durasi
        
        # Update field lain
        if nama_layanan:
            layanan_data['nama_layanan'] = nama_layanan
        if deskripsi is not None:
            layanan_data['deskripsi'] = deskripsi
        
        # Jika tidak ada data yang diupdate
        if not layanan_data:
            return False, "Tidak ada data yang diupdate"
        
        if self.db.update_layanan(layanan_id, layanan_data):
            return True, "Layanan berhasil diupdate"
        return False, "Gagal mengupdate layanan"
    
    def delete_layanan(self, layanan_id):
        """Menghapus layanan"""
        if self.db.delete_layanan(layanan_id):
            return True, "Layanan berhasil dihapus"
        return False, "Gagal menghapus layanan"
