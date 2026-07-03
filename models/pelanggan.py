from datetime import datetime
from .akun import Akun

class Pelanggan(Akun):
    """Class untuk Pelanggan yang merupakan turunan dari Akun."""

    def __init__(self, id_pelanggan, nama, email, nomor_hp, password):
        super().__init__(id_pelanggan, nama, nomor_hp)
        self.email = email
        self.nomor_hp = nomor_hp
        self.password = password
        self.role = "Pelanggan"
        self.tanggal_daftar = datetime.now()

    def tampilkan_info(self):
        """Menampilkan informasi pelanggan."""
        return f"""
        === INFO PELANGGAN ===
        ID: {self.id}
        Nama: {self.nama}
        Email: {self.email}
        Nomor HP: {self.nomor_hp}
        Tanggal Daftar: {self.tanggal_daftar.strftime('%Y-%m-%d %H:%M:%S')}
        """

    def get_info_dict(self):
        """Mendapatkan info pelanggan sebagai dictionary."""
        return {
            'id_pelanggan': self.id,
            'nama': self.nama,
            'email': self.email,
            'nomor_hp': self.nomor_hp,
            'password': self.password,
            'tanggal_daftar': self.tanggal_daftar.isoformat(),
            'role': self.role
        }

    def update_profile(self, nama=None, email=None, nomor_hp=None):
        """Update profil pelanggan."""
        if nama:
            self.nama = nama
        if email:
            self.email = email
        if nomor_hp:
            self.nomor_hp = nomor_hp
            self.nohp = nomor_hp
        return True
