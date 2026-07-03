from utils.database import Database

class RiwayatController:
    """Controller untuk Riwayat Layanan"""
    
    def __init__(self):
        self.db = Database('data')
    
    def get_all_riwayat(self):
        """Mendapatkan semua riwayat layanan"""
        return self.db.get_all_riwayat()
    
    def get_riwayat_by_pelanggan(self, id_pelanggan):
        """Mendapatkan riwayat berdasarkan pelanggan"""
        return self.db.get_riwayat_by_pelanggan(id_pelanggan)
    
    def get_riwayat_by_id(self, id_riwayat):
        """Mendapatkan riwayat berdasarkan ID"""
        return self.db.get_riwayat_by_id(id_riwayat)
    
    def delete_riwayat(self, id_riwayat):
        """Menghapus riwayat"""
        if self.db.delete_riwayat(id_riwayat):
            return True, "Riwayat berhasil dihapus"
        return False, "Gagal menghapus riwayat"
