from utils.database import Database
from models.pembayaran import Pembayaran
from datetime import datetime

class PembayaranController:
    """Controller untuk Pembayaran"""
    
    def __init__(self):
        self.db = Database('data')
    
    def get_all_pembayaran(self):
        """Mendapatkan semua pembayaran"""
        return self.db.get_all_pembayaran()
    
    def get_pembayaran_by_id(self, pembayaran_id):
        """Mendapatkan pembayaran berdasarkan ID"""
        return self.db.get_pembayaran_by_id(pembayaran_id)
    
    def get_pembayaran_by_reservasi(self, reservasi_id):
        """Mendapatkan pembayaran berdasarkan reservasi"""
        return self.db.get_pembayaran_by_reservasi(reservasi_id)

    def get_pembayaran_by_pelanggan(self, id_pelanggan):
        """Mendapatkan pembayaran berdasarkan pelanggan."""
        pembayaran_list = self.get_all_pembayaran()
        reservasi_list = self.db.get_reservasi_by_pelanggan(id_pelanggan)
        reservasi_ids = {r['id_reservasi'] for r in reservasi_list}
        return [p for p in pembayaran_list if p.get('id_reservasi') in reservasi_ids]
    
    def proses_pembayaran(self, pembayaran_id, metode="Tunai"):
        """Memproses pembayaran"""
        pembayaran = self.db.get_pembayaran_by_id(pembayaran_id)
        if not pembayaran:
            return False, "Pembayaran tidak ditemukan"
        
        if pembayaran['status'] != 'Pending':
            return False, "Pembayaran sudah diproses"
        
        pembayaran_data = {
            'status': 'Lunas',
            'metode': metode,
            'tanggal_bayar': datetime.now().isoformat()
        }
        
        if self.db.update_pembayaran(pembayaran_id, pembayaran_data):
            return True, "Pembayaran berhasil diproses"
        return False, "Gagal memproses pembayaran"
    
    def get_laporan_pembayaran(self, tanggal_mulai=None, tanggal_akhir=None):
        """Mendapatkan laporan pembayaran"""
        pembayaran_list = self.db.get_all_pembayaran()
        
        if tanggal_mulai and tanggal_akhir:
            pembayaran_list = [
                p for p in pembayaran_list
                if tanggal_mulai <= p.get('tanggal_dibuat', '')[:10] <= tanggal_akhir
            ]
        
        return pembayaran_list
    
    def get_total_pembayaran(self, status='Lunas'):
        """Mendapatkan total pembayaran berdasarkan status"""
        pembayaran_list = self.db.get_all_pembayaran()
        total = sum(p['total'] for p in pembayaran_list if p.get('status') == status)
        return total
