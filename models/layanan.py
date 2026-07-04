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
        """Update harga layanan dengan memanfaatkan @staticmethod untuk validasi"""
        if self.validasi_nilai_positif(harga_baru):
            self.harga = harga_baru
            return True
        return False
    
    def update_durasi(self, durasi_baru):
        """Update durasi layanan dengan memanfaatkan @staticmethod untuk validasi"""
        if self.validasi_nilai_positif(durasi_baru):
            self.durasi = durasi_baru
            return True
        return False

    # =======================================================
    # MATERI 6: IMPLEMENTASI CLASS METHOD & STATIC METHOD
    # =======================================================

    @staticmethod
    def validasi_nilai_positif(angka):
        return isinstance(angka, (int, float)) and angka > 0
    
    @classmethod
    def from_dict(cls, data):
        
        layanan = cls(
            id_layanan=data['id_layanan'],
            nama_layanan=data['nama_layanan'],
            harga=data['harga'],
            durasi=data['durasi'],
            deskripsi=data.get('deskripsi', '')
        )
        
        # Set tanggal_dibuat jika ada di data
        if 'tanggal_dibuat' in data:
            from datetime import datetime
            layanan.tanggal_dibuat = datetime.fromisoformat(data['tanggal_dibuat'])
        
        return layanan
    
    @classmethod
    def buat_layanan_baru(cls, nama_layanan, harga, durasi, deskripsi=""):
        """
        Class method factory untuk membuat layanan baru dengan ID otomatis.
        
        Args:
            nama_layanan: Nama layanan
            harga: Harga layanan
            durasi: Durasi dalam menit
            deskripsi: Deskripsi opsional
            
        Returns:
            Instance Layanan dengan ID yang di-generate
        """
        # Generate ID unik berdasarkan timestamp
        id_layanan = f"L{int(datetime.now().timestamp())}"
        
        # Validasi input menggunakan static method
        if not cls.validasi_nilai_positif(harga):
            raise ValueError("Harga harus lebih besar dari 0")
        if not cls.validasi_nilai_positif(durasi):
            raise ValueError("Durasi harus lebih besar dari 0")
        
        return cls(id_layanan, nama_layanan, harga, durasi, deskripsi)
