from abc import abstractmethod
from datetime import datetime
from .akun import Akun

class Pegawai(Akun):
    """Abstract class untuk Pegawai."""

    def __init__(self, id_pegawai, nama, nohp, usia):
        super().__init__(id_pegawai, nama, nohp)
        self.usia = usia
        self.role = None

    @abstractmethod
    def tampilkan_info(self):
        """Method abstract untuk menampilkan informasi pegawai."""
        pass

    @abstractmethod
    def get_info_dict(self):
        """Method abstract untuk mendapatkan info sebagai dictionary."""
        pass
