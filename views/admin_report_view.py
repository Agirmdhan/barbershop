import streamlit as st
import pandas as pd
from controllers.barber_controller import BarberController
from controllers.pelanggan_controller import PelangganController
from controllers.layanan_controller import LayananController
from controllers.reservasi_controller import ReservasiController
from controllers.pembayaran_controller import PembayaranController
from controllers.riwayat_controller import RiwayatController
from utils.helpers import format_currency, hitung_statistik_umum, filter_by_status

def show_main_dashboard():
    """Dashboard Utama dengan Statistik"""
    st.write("#### Dashboard Utama")
    
    barber_controller = BarberController()
    pelanggan_controller = PelangganController()
    layanan_controller = LayananController()
    reservasi_controller = ReservasiController()
    pembayaran_controller = PembayaranController()
    riwayat_controller = RiwayatController()
    
    # Statistics Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_barber = len(barber_controller.get_all_barbers())
        st.metric("Total Barber", total_barber)
    
    with col2:
        total_pelanggan = len(pelanggan_controller.get_all_pelanggan())
        st.metric("Total Pelanggan", total_pelanggan)
    
    with col3:
        total_layanan = len(layanan_controller.get_all_layanan())
        st.metric("Total Layanan", total_layanan)
    
    with col4:
        total_reservasi = len(reservasi_controller.get_all_reservasi())
        st.metric("Total Reservasi", total_reservasi)
    
    st.write("")
    
    # More statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        reservasi_pending = len([r for r in reservasi_controller.get_all_reservasi() if r.get('status') == 'Pending'])
        st.metric("Reservasi Pending", reservasi_pending)
    
    with col2:
        reservasi_dikonfirmasi = len([r for r in reservasi_controller.get_all_reservasi() if r.get('status') == 'Dikonfirmasi'])
        st.metric("Reservasi Dikonfirmasi", reservasi_dikonfirmasi)
    
    with col3:
        total_lunas = pembayaran_controller.get_total_pembayaran('Lunas')
        st.metric("Total Pembayaran Lunas", format_currency(total_lunas))
    
    st.write("")
    
    # Recent Reservations
    st.write("#### Reservasi Terbaru")
    reservasi_list = reservasi_controller.get_all_reservasi()
    barber_controller_res = BarberController()
    pelanggan_controller_res = PelangganController()
    layanan_controller_res = LayananController()
    all_barbers = {b['id_pegawai']: b['nama'] for b in barber_controller_res.get_all_barbers()}
    all_pelanggan = {p['id_pelanggan']: p['nama'] for p in pelanggan_controller_res.get_all_pelanggan()}
    all_layanan = {l['id_layanan']: l['nama_layanan'] for l in layanan_controller_res.get_all_layanan()}
    
    # --- MODIFIKASI: Implementasi IndexError ---
    try:
        reservasi_terakhir = reservasi_list[-1]
        
        st.success(f"📌 Highlight Reservasi Paling Baru: ID {reservasi_terakhir.get('id_reservasi')} untuk tanggal {reservasi_terakhir.get('tanggal')} (Status: {reservasi_terakhir.get('status')})")
        
        # Transform ID ke Nama untuk ditampilkan
        display_reservasi = []
        for r in reservasi_list[-5:]:
            display_reservasi.append({
                'ID Reservasi': r.get('id_reservasi'),
                'Pelanggan': all_pelanggan.get(r.get('id_pelanggan'), r.get('id_pelanggan')),
                'Barber': all_barbers.get(r.get('id_barber'), r.get('id_barber')),
                'Layanan': all_layanan.get(r.get('id_layanan'), r.get('id_layanan')),
                'Tanggal': r.get('tanggal'),
                'Jam': r.get('jam'),
                'Status': r.get('status'),
                'Catatan': r.get('catatan', '')
            })
        df_reservasi = pd.DataFrame(display_reservasi)
        st.dataframe(df_reservasi, use_container_width=True)
        
    except IndexError:
        # Menangkap error jika tidak ada index [-1] karena list kosong
        st.info("Belum ada reservasi sama sekali. Data tabel kosong.")
    # -------------------------------------------
    
    st.write("")
    
    # Available Barbers
    st.write("#### Barber Tersedia")
    available_barbers = barber_controller.get_available_barbers()
    
    if available_barbers:
        df_available = pd.DataFrame(available_barbers)
        st.dataframe(df_available, use_container_width=True)
    else:
        st.info("Tidak ada barber yang tersedia saat ini")


def show_laporan_page():
    """Halaman Laporan"""
    st.write("#### Laporan Transaksi")
    
    reservasi_controller = ReservasiController()
    pembayaran_controller = PembayaranController()
    riwayat_controller = RiwayatController()
    
    tab1, tab2, tab3 = st.tabs(["Laporan Reservasi", "Laporan Pembayaran", "Laporan Riwayat Layanan"])
    
    # Tab 1: Laporan Reservasi
    with tab1:
        st.write("##### Laporan Reservasi")
        
        col1, col2 = st.columns(2)
        with col1:
            status_filter = st.multiselect("Filter Status:", ["Pending", "Dikonfirmasi", "Selesai", "Dibatalkan"], default=["Dikonfirmasi", "Selesai"])
        
        reservasi_list = reservasi_controller.get_all_reservasi()
        if status_filter:
            reservasi_list = [r for r in reservasi_list if r.get('status') in status_filter]
        
        if reservasi_list:
            # Transform ID ke Nama
            barber_controller_lap = BarberController()
            pelanggan_controller_lap = PelangganController()
            layanan_controller_lap = LayananController()
            all_barbers_lap = {b['id_pegawai']: b['nama'] for b in barber_controller_lap.get_all_barbers()}
            all_pelanggan_lap = {p['id_pelanggan']: p['nama'] for p in pelanggan_controller_lap.get_all_pelanggan()}
            all_layanan_lap = {l['id_layanan']: l['nama_layanan'] for l in layanan_controller_lap.get_all_layanan()}
            
            display_reservasi = []
            for r in reservasi_list:
                display_reservasi.append({
                    'ID Reservasi': r.get('id_reservasi'),
                    'Pelanggan': all_pelanggan_lap.get(r.get('id_pelanggan'), r.get('id_pelanggan')),
                    'Barber': all_barbers_lap.get(r.get('id_barber'), r.get('id_barber')),
                    'Layanan': all_layanan_lap.get(r.get('id_layanan'), r.get('id_layanan')),
                    'Tanggal': r.get('tanggal'),
                    'Jam': r.get('jam'),
                    'Status': r.get('status'),
                    'Catatan': r.get('catatan', '')
                })
            df = pd.DataFrame(display_reservasi)
            st.dataframe(df, use_container_width=True)
            
            # Summary
            st.write("##### Ringkasan")
            total_status = hitung_statistik_umum([{'total': 1} for _ in reservasi_list])
            st.write(f"Total Reservasi: {total_status['count']}")
        else:
            st.info("Tidak ada data")
    
    # Tab 2: Laporan Pembayaran
    with tab2:
        st.write("##### Laporan Pembayaran")
        
        pembayaran_list = pembayaran_controller.get_all_pembayaran()
        
        if pembayaran_list:
            df = pd.DataFrame(pembayaran_list)
            
            if 'total' in df.columns:
                df['total'] = df['total'].apply(format_currency)
            
            st.dataframe(df, use_container_width=True)
            
            # Summary
            total_lunas = pembayaran_controller.get_total_pembayaran('Lunas')
            total_pending = pembayaran_controller.get_total_pembayaran('Pending')
            
            st.write("##### Ringkasan")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"Total Pembayaran Lunas: {format_currency(total_lunas)}")
            with col2:
                st.write(f"Total Pembayaran Pending: {format_currency(total_pending)}")
            with col3:
                st.write(f"Total: {format_currency(total_lunas + total_pending)}")
        else:
            st.info("Tidak ada data")
    
    # Tab 3: Laporan Riwayat
    with tab3:
        st.write("##### Laporan Riwayat Layanan")
        
        riwayat_list = riwayat_controller.get_all_riwayat()
        
        if riwayat_list:
            df = pd.DataFrame(riwayat_list)
            
            if 'total' in df.columns:
                df['total'] = df['total'].apply(format_currency)
            
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Tidak ada data riwayat layanan untuk ditampilkan pada tabel.")
            
        total_services = len(riwayat_list)
        total_revenue = sum(r.get('total', 0) for r in riwayat_list)
        
        st.write("##### Ringkasan")
        
        # --- IMPLEMENTASI ZeroDivisionError dan Try-Except-Else ---
        try:
            rata_rata = total_revenue / total_services
            
        except ZeroDivisionError:
            rata_rata = 0
            status_kalkulasi = "Belum ada transaksi untuk dihitung (pembagian dengan nol dicegah)."
            
        else:
            status_kalkulasi = "Perhitungan rata-rata berhasil ditarik."
        # ----------------------------------------------------------
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"Total Layanan: {total_services}")
        with col2:
            st.write(f"Total Pendapatan: {format_currency(total_revenue)}")
        with col3:
            st.write(f"Rata-rata /Layanan: {format_currency(rata_rata)}")
            
        st.caption(f"Status: {status_kalkulasi}")