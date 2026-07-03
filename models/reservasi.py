from datetime import datetime

class Reservasi:
    """Class untuk Reservasi"""
    
    def __init__(self, id_reservasi, id_pelanggan, id_barber, id_layanan, tanggal, jam, status="Pending"):
        self.id_reservasi = id_reservasi
        self.id_pelanggan = id_pelanggan
        self.id_barber = id_barber
        self.id_layanan = id_layanan
        self.tanggal = tanggal  # format: YYYY-MM-DD
        self.jam = jam  # format: HH:MM
        self.status = status  # Pending, Dikonfirmasi, Selesai, Dibatalkan
        self.catatan = ""
        self.tanggal_dibuat = datetime.now()
    
    def tampilkan_info(self):
        """Menampilkan informasi reservasi"""
        return f"""
        === INFO RESERVASI ===
        ID: {self.id_reservasi}
        Pelanggan ID: {self.id_pelanggan}
        Barber ID: {self.id_barber}
        Layanan ID: {self.id_layanan}
        Tanggal: {self.tanggal}
        Jam: {self.jam}
        Status: {self.status}
        Catatan: {self.catatan}
        """
    
    def get_info_dict(self):
        """Mendapatkan info reservasi sebagai dictionary"""
        return {
            'id_reservasi': self.id_reservasi,
            'id_pelanggan': self.id_pelanggan,
            'id_barber': self.id_barber,
            'id_layanan': self.id_layanan,
            'tanggal': self.tanggal,
            'jam': self.jam,
            'status': self.status,
            'catatan': self.catatan,
            'tanggal_dibuat': self.tanggal_dibuat.isoformat()
        }
    
    def konfirmasi_reservasi(self):
        """Mengkonfirmasi reservasi"""
        if self.status == "Pending":
            self.status = "Dikonfirmasi"
            return True
        return False
    
    def selesaikan_reservasi(self):
        """Menyelesaikan reservasi"""
        if self.status == "Dikonfirmasi":
            self.status = "Selesai"
            return True
        return False
    
    def batalkan_reservasi(self, alasan=""):
        """Membatalkan reservasi."""
        if self.status in ["Pending", "Dikonfirmasi"]:
            self.status = "Dibatalkan"
            self.catatan = alasan
            return True
        return False

    def tolak_reservasi(self, alasan=""):
        """Menolak reservasi."""
        if self.status == "Pending":
            self.status = "Ditolak"
            self.catatan = alasan
            return True
        return False

    def update_status(self, status_baru):
        """Update status reservasi."""
        valid_status = ["Pending", "Dikonfirmasi", "Ditolak", "Selesai", "Dibatalkan"]
        if status_baru in valid_status:
            self.status = status_baru
            return True
        return False

    def ubah_tanggal(self, tanggal_baru, jam_baru):
        """Mengubah tanggal dan jam reservasi (hanya jika status Pending atau Dikonfirmasi)."""
        if self.status in ["Pending", "Dikonfirmasi"]:
            self.tanggal = tanggal_baru
            self.jam = jam_baru
            return True
        return False
