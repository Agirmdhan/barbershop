from utils.database import Database
from models.reservasi import Reservasi
from models.pembayaran import Pembayaran
from models.riwayat_layanan import RiwayatLayanan
from datetime import datetime

class JadwalPenuhError(Exception):
    pass
    
class ReservasiController:
    """Controller untuk Reservasi"""

    OPERATING_START = 9
    OPERATING_END = 21

    def __init__(self):
        self.db = Database('data')

    def _is_within_operational_hours(self, jam):
        try:
            hour, minute = map(int, jam.split(':'))
            if hour < self.OPERATING_START or hour > self.OPERATING_END:
                return False
            if hour == self.OPERATING_END and minute > 0:
                return False
            return True
        except ValueError:
            return False

    
    def create_reservasi(self, id_pelanggan, id_barber, id_layanan, tanggal, jam):
        """Membuat reservasi baru"""
        pelanggan = self.db.get_pelanggan_by_id(id_pelanggan)
        if not pelanggan:
            return False, "Pelanggan tidak ditemukan"

        barber = self.db.get_barber_by_id(id_barber)
        if not barber:
            return False, "Barber tidak ditemukan"

        layanan = self.db.get_layanan_by_id(id_layanan)
        if not layanan:
            return False, "Layanan tidak ditemukan"

     
        if not self.check_ketersediaan_barber(id_barber, tanggal, jam):
            raise JadwalPenuhError(f"Maaf, Barber sedang tidak tersedia pada tanggal {tanggal} jam {jam}. Silakan pilih waktu lain.")

        reservasi_id = self.db.generate_id("RES", "reservasi")
        reservasi = Reservasi(reservasi_id, id_pelanggan, id_barber, id_layanan, tanggal, jam)
        reservasi_data = reservasi.get_info_dict()

        if self.db.save_reservasi(reservasi_data):
            self.create_pembayaran_untuk_reservasi(reservasi_id, id_layanan)
            return True, f"Reservasi berhasil dibuat (ID: {reservasi_id})"
        return False, "Gagal membuat reservasi"
    
    def create_pembayaran_untuk_reservasi(self, id_reservasi, id_layanan):
        """Membuat pembayaran untuk reservasi"""
        layanan = self.db.get_layanan_by_id(id_layanan)
        if not layanan:
            return False
        
        pembayaran_id = self.db.generate_id("PAY", "pembayaran")
        pembayaran = Pembayaran(pembayaran_id, id_reservasi, layanan['harga'])
        pembayaran_data = pembayaran.get_info_dict()
        
        return self.db.save_pembayaran(pembayaran_data)
    
    def get_all_reservasi(self):
        """Mendapatkan semua reservasi"""
        return self.db.get_all_reservasi()
    
    def get_reservasi_by_id(self, reservasi_id):
        """Mendapatkan reservasi berdasarkan ID"""
        return self.db.get_reservasi_by_id(reservasi_id)
    
    def get_reservasi_by_pelanggan(self, id_pelanggan):
        """Mendapatkan reservasi berdasarkan pelanggan"""
        return self.db.get_reservasi_by_pelanggan(id_pelanggan)
    
    def get_reservasi_by_barber(self, id_barber):
        """Mendapatkan reservasi berdasarkan barber"""
        return self.db.get_reservasi_by_barber(id_barber)
    
    def konfirmasi_reservasi(self, reservasi_id):
        """Mengkonfirmasi reservasi."""
        if self.db.update_reservasi(reservasi_id, {'status': 'Dikonfirmasi'}):
            return True, "Reservasi berhasil dikonfirmasi"
        return False, "Gagal mengkonfirmasi reservasi"

    def tolak_reservasi(self, reservasi_id, alasan=""):
        """Menolak reservasi."""
        if self.db.update_reservasi(reservasi_id, {'status': 'Ditolak', 'catatan': alasan}):
            return True, "Reservasi berhasil ditolak"
        return False, "Gagal menolak reservasi"
    
    def selesaikan_reservasi(self, reservasi_id):
        """Menyelesaikan reservasi"""
        reservasi = self.db.get_reservasi_by_id(reservasi_id)
        if not reservasi:
            return False, "Reservasi tidak ditemukan"
        
        # Update status reservasi
        if not self.db.update_reservasi(reservasi_id, {'status': 'Selesai'}):
            return False, "Gagal menyelesaikan reservasi"
        
        # Create riwayat layanan
        riwayat_id = self.db.generate_id("RIW", "riwayat")
        layanan = self.db.get_layanan_by_id(reservasi['id_layanan'])
        
        riwayat = RiwayatLayanan(
            riwayat_id,
            reservasi['id_pelanggan'],
            reservasi['id_layanan'],
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            layanan['harga'] if layanan else 0,
            "Layanan selesai"
        )
        riwayat_data = riwayat.get_info_dict()
        
        if self.db.save_riwayat(riwayat_data):
            return True, "Reservasi berhasil diselesaikan"
        return False, "Gagal menyelesaikan reservasi"
    
    def batalkan_reservasi(self, reservasi_id, alasan=""):
        """Membatalkan reservasi"""
        if self.db.update_reservasi(reservasi_id, {'status': 'Dibatalkan', 'catatan': alasan}):
            return True, "Reservasi berhasil dibatalkan"
        return False, "Gagal membatalkan reservasi"
    
    def update_status(self, reservasi_id, status):
        """Update status reservasi."""
        valid_status = ["Pending", "Dikonfirmasi", "Ditolak", "Selesai", "Dibatalkan"]
        if status not in valid_status:
            return False, f"Status harus salah satu dari: {', '.join(valid_status)}"

        if self.db.update_reservasi(reservasi_id, {'status': status}):
            return True, f"Status reservasi berhasil diubah menjadi {status}"
        return False, "Gagal mengubah status reservasi"
    
    def ubah_tanggal_reservasi(self, reservasi_id, tanggal_baru, jam_baru):
        """Mengubah tanggal dan jam reservasi (hanya untuk status Pending atau Dikonfirmasi)."""
        reservasi = self.db.get_reservasi_by_id(reservasi_id)
        if not reservasi:
            return False, "Reservasi tidak ditemukan"

        if reservasi['status'] not in ["Pending", "Dikonfirmasi"]:
            return False, f"Reservasi dengan status '{reservasi['status']}' tidak dapat diubah tanggalnya"

        # Validasi jam operasional
        if not self._is_within_operational_hours(jam_baru):
            return False, f"Jam {jam_baru} berada di luar jam operasional ({self.OPERATING_START}:00 - {self.OPERATING_END}:00)"

        # Validasi ketersediaan barber di tanggal dan jam baru
        if not self.check_ketersediaan_barber(reservasi['id_barber'], tanggal_baru, jam_baru):
            return False, f"Barber tidak tersedia pada tanggal {tanggal_baru} jam {jam_baru}. Silakan pilih waktu lain."

        # Update tanggal dan jam reservasi
        if self.db.update_reservasi(reservasi_id, {'tanggal': tanggal_baru, 'jam': jam_baru}):
            return True, f"Tanggal reservasi {reservasi_id} berhasil diubah menjadi {tanggal_baru} {jam_baru}"
        return False, "Gagal mengubah tanggal reservasi"

    def check_ketersediaan_barber(self, id_barber, tanggal, jam):
        """Check ketersediaan barber pada tanggal dan jam tertentu."""
        reservasi_list = self.db.get_reservasi_by_barber(id_barber)

        for res in reservasi_list:
            if res['tanggal'] == tanggal and res['jam'] == jam and res['status'] not in ['Dibatalkan', 'Ditolak']:
                return False
        return True
