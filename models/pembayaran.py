from datetime import datetime

class Pembayaran:
    """Class untuk Pembayaran (Composition dengan Reservasi)"""
    
    def __init__(self, id_pembayaran, id_reservasi, total, metode="Tunai", status="Pending"):
        self.id_pembayaran = id_pembayaran
        self.id_reservasi = id_reservasi
        self.total = total
        self.metode = metode  # Tunai, Transfer, Kartu Kredit
        self.status = status  # Pending, Lunas, Cicilan
        self.tanggal_bayar = None
        self.tanggal_dibuat = datetime.now()
    
    def tampilkan_info(self):
        """Menampilkan informasi pembayaran"""
        tanggal_bayar_str = self.tanggal_bayar.strftime('%Y-%m-%d %H:%M:%S') if self.tanggal_bayar else "Belum dibayar"
        return f"""
        === INFO PEMBAYARAN ===
        ID: {self.id_pembayaran}
        ID Reservasi: {self.id_reservasi}
        Total: Rp {self.total:,.0f}
        Metode: {self.metode}
        Status: {self.status}
        Tanggal Bayar: {tanggal_bayar_str}
        """
    
    def get_info_dict(self):
        """Mendapatkan info pembayaran sebagai dictionary"""
        tanggal_bayar_str = self.tanggal_bayar.isoformat() if self.tanggal_bayar else None
        return {
            'id_pembayaran': self.id_pembayaran,
            'id_reservasi': self.id_reservasi,
            'total': self.total,
            'metode': self.metode,
            'status': self.status,
            'tanggal_bayar': tanggal_bayar_str,
            'tanggal_dibuat': self.tanggal_dibuat.isoformat()
        }
    
    def proses_pembayaran(self):
        """Memproses pembayaran"""
        if self.status == "Pending":
            self.status = "Lunas"
            self.tanggal_bayar = datetime.now()
            return True
        return False
    
    def cetak_struk(self):
        """Mencetak struk pembayaran"""
        tanggal_bayar_str = self.tanggal_bayar.strftime('%Y-%m-%d %H:%M:%S') if self.tanggal_bayar else "Belum dibayar"
        return f"""
        ==================
        STRUK PEMBAYARAN
        ==================
        ID Pembayaran: {self.id_pembayaran}
        ID Reservasi: {self.id_reservasi}
        Total: Rp {self.total:,.0f}
        Metode: {self.metode}
        Status: {self.status}
        Tanggal Bayar: {tanggal_bayar_str}
        ==================
        """
