from .pegawai import Pegawai

class Admin(Pegawai):
    """Class Admin yang mewarisi dari Pegawai"""
    
    def __init__(self, id_pegawai, nama, nohp, usia, username, password):
        super().__init__(id_pegawai, nama, nohp, usia)
        self.username = username
        self.password = password
        self.role = "Admin"
    
    def tampilkan_info(self):
        """Menampilkan informasi admin"""
        return f"""
        === INFO ADMIN ===
        ID: {self.id_pegawai}
        Nama: {self.nama}
        No. HP: {self.nohp}
        Usia: {self.usia}
        Username: {self.username}
        Role: {self.role}
        """
    
    def get_info_dict(self):
        """Mendapatkan info admin sebagai dictionary"""
        return {
            'id_pegawai': self.id_pegawai,
            'nama': self.nama,
            'nohp': self.nohp,
            'usia': self.usia,
            'username': self.username,
            'password': self.password,
            'role': self.role,
            'tanggal_dibuat': self.tanggal_dibuat.isoformat()
        }
    
    def kelola_layanan(self):
        """Admin dapat mengelola layanan"""
        pass
    
    def kelola_reservasi(self):
        """Admin dapat mengelola reservasi"""
        pass
    
    def lihat_laporan(self):
        """Admin dapat melihat laporan"""
        pass
