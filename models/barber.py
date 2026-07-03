from datetime import datetime  # <-- TAMBAHAN: Untuk mengantisipasi tanggal_dibuat
from .pegawai import Pegawai

class Barber(Pegawai):
    """Class Barber yang mewarisi dari Pegawai"""
    
    def __init__(self, id_pegawai, nama, nohp, usia, username, password, spesialisasi, status="Tersedia"):
        super().__init__(id_pegawai, nama, nohp, usia)
        
        self.id_pegawai = id_pegawai 
        
        self.username = username
        self.password = password
        self.spesialisasi = spesialisasi
        self.status = status  # Tersedia, Sibuk, Libur
        self.role = "Barber"
        
        if not hasattr(self, 'tanggal_dibuat'):
            self.tanggal_dibuat = datetime.now()
    
    def tampilkan_info(self):
        """Menampilkan informasi barber"""
        return f"""
        === INFO BARBER ===
        ID: {self.id_pegawai}
        Nama: {self.nama}
        No. HP: {self.nohp}
        Usia: {self.usia}
        Spesialisasi: {self.spesialisasi}
        Status: {self.status}
        Role: {self.role}
        """
    
    def get_info_dict(self):
        """Mendapatkan info barber sebagai dictionary"""
        # Proteksi aman untuk pemformatan tanggal_dibuat
        try:
            tgl_str = self.tanggal_dibuat.isoformat()
        except AttributeError:
            tgl_str = str(self.tanggal_dibuat)

        return {
            'id_pegawai': self.id_pegawai, 
            'nama': self.nama,
            'username': self.username,
            'password': self.password,
            'nohp': self.nohp,
            'usia': self.usia,
            'spesialisasi': self.spesialisasi,
            'status': self.status,
            'role': self.role,
            'tanggal_dibuat': tgl_str
        }
    
    def ubah_status(self, status_baru):
        """Mengubah status barber"""
        if status_baru in ["Tersedia", "Sibuk", "Libur"]:
            self.status = status_baru
            return True
        return False

    def selesaikan_layanan(self):
        """Barber menyelesaikan layanan"""
        self.status = "Tersedia"