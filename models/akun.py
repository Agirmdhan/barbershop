from abc import ABC, abstractmethod
from datetime import datetime

class Akun(ABC):
    """Abstract class dasar untuk semua entitas pengguna dan pegawai."""

    def __init__(self, id_, nama, nohp):
        self._id = id_
        self._nama = nama
        self._nohp = nohp
        self._tanggal_dibuat = datetime.now()

    @property
    def id(self):
        return self._id

    @property
    def nama(self):
        return self._nama

    @property
    def nohp(self):
        return self._nohp

    @property
    def tanggal_dibuat(self):
        return self._tanggal_dibuat

    @nama.setter
    def nama(self, value):
        self._nama = value

    @nohp.setter
    def nohp(self, value):
        self._nohp = value

    def update_contact(self, nama=None, nohp=None):
        if nama:
            self.nama = nama
        if nohp:
            self.nohp = nohp
        return True

    @abstractmethod
    def tampilkan_info(self):
        pass

    @abstractmethod
    def get_info_dict(self):
        pass
