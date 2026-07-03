from datetime import datetime

class Layanan:
    """Class untuk Layanan Barbershop"""
    
    def __init__(self, id_layanan, nama_layanan, harga, durasi, deskripsi=""):
        self.id_layanan = id_layanan
        self.nama_layanan = nama_layanan
        self.harga = harga
        self.durasi = durasi  # dalam menit
        self.deskripsi = deskripsi
        self.tanggal_dibuat = datetime.now()
    
    def tampilkan_info(self):
        """Menampilkan informasi layanan"""
        return f"""
        === INFO LAYANAN ===
        ID: {self.id_layanan}
        Nama: {self.nama_layanan}
        Harga: Rp {self.harga:,.0f}
        Durasi: {self.durasi} menit
        Deskripsi: {self.deskripsi}
        """
    
    def get_info_dict(self):
        """Mendapatkan info layanan sebagai dictionary"""
        return {
            'id_layanan': self.id_layanan,
            'nama_layanan': self.nama_layanan,
            'harga': self.harga,
            'durasi': self.durasi,
            'deskripsi': self.deskripsi,
            'tanggal_dibuat': self.tanggal_dibuat.isoformat()
        }
    
    def update_harga(self, harga_baru):
        """Update harga layanan"""
        if harga_baru > 0:
            self.harga = harga_baru
            return True
        return False
    
    def update_durasi(self, durasi_baru):
        """Update durasi layanan"""
        if durasi_baru > 0:
            self.durasi = durasi_baru
            return True
        return False
