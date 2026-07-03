from datetime import datetime

class RiwayatLayanan:
    """Class untuk Riwayat Layanan Pelanggan"""
    
    def __init__(self, id_riwayat, id_pelanggan, id_layanan, tanggal, total, catatan=""):
        self.id_riwayat = id_riwayat
        self.id_pelanggan = id_pelanggan
        self.id_layanan = id_layanan
        self.tanggal = tanggal  # tanggal layanan dilakukan
        self.total = total  # harga layanan
        self.catatan = catatan
        self.tanggal_dibuat = datetime.now()
    
    def tampilkan_info(self):
        """Menampilkan informasi riwayat layanan"""
        return f"""
        === RIWAYAT LAYANAN ===
        ID: {self.id_riwayat}
        ID Pelanggan: {self.id_pelanggan}
        ID Layanan: {self.id_layanan}
        Tanggal: {self.tanggal}
        Total: Rp {self.total:,.0f}
        Catatan: {self.catatan}
        """
    
    def get_info_dict(self):
        """Mendapatkan info riwayat layanan sebagai dictionary"""
        return {
            'id_riwayat': self.id_riwayat,
            'id_pelanggan': self.id_pelanggan,
            'id_layanan': self.id_layanan,
            'tanggal': self.tanggal,
            'total': self.total,
            'catatan': self.catatan,
            'tanggal_dibuat': self.tanggal_dibuat.isoformat()
        }
    
    def lihat_detail(self):
        """Melihat detail riwayat layanan"""
        return self.tampilkan_info()
