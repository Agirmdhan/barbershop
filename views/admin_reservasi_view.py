import streamlit as st
import pandas as pd
import time
# --- MODIFIKASI: Import JadwalPenuhError ---
from controllers.reservasi_controller import ReservasiController, JadwalPenuhError
from controllers.barber_controller import BarberController
from controllers.pelanggan_controller import PelangganController
from controllers.layanan_controller import LayananController

def show_reservasi_management():
    """Manajemen Reservasi"""
    st.subheader(" Manajemen Reservasi")
    
    reservasi_controller = ReservasiController()
    barber_controller = BarberController()
    pelanggan_controller = PelangganController()
    layanan_controller = LayananController()
    
    tab1, tab2, tab3 = st.tabs(["Daftar Reservasi", "Buat Reservasi", "Update Status"])
    
    pelanggan_list = pelanggan_controller.get_all_pelanggan()
    barber_list = barber_controller.get_all_barbers()
    layanan_list = layanan_controller.get_all_layanan()
    
    # Tab 1: Daftar Reservasi
    with tab1:
        st.write("#### Daftar Reservasi")
        
        filter_status = st.multiselect(
            "Filter Status:",
            ["Pending", "Dikonfirmasi", "Selesai", "Dibatalkan"],
            default=["Pending", "Dikonfirmasi"]
        )
        
        reservasi_list = reservasi_controller.get_all_reservasi()
        
        if filter_status:
            reservasi_list = [r for r in reservasi_list if r.get('status') in filter_status]
        
        if reservasi_list:
            tampilan_list = []
            for res in reservasi_list:
                nama_pelanggan = next((p['nama'] for p in pelanggan_list if p['id_pelanggan'] == res.get('id_pelanggan')), res.get('id_pelanggan'))
                nama_barber = next((b['nama'] for b in barber_list if b['id_pegawai'] == res.get('id_barber')), res.get('id_barber'))
                nama_layanan = next((l['nama_layanan'] for l in layanan_list if l['id_layanan'] == res.get('id_layanan')), res.get('id_layanan'))
                
                tampilan_list.append({
                    "ID Reservasi": res.get('id_reservasi'),
                    "Nama Pelanggan": nama_pelanggan,
                    "Barber": nama_barber,
                    "Layanan": nama_layanan,
                    "Tanggal": res.get('tanggal'),
                    "Jam": res.get('jam'),
                    "Status": res.get('status'),
                    "Catatan": res.get('catatan'),
                    "Tanggal Dibuat": res.get('tanggal_dibuat')
                })
            
            df_reservasi = pd.DataFrame(tampilan_list)
            st.dataframe(df_reservasi, use_container_width=True)
        else:
            st.info("Belum ada reservasi")
    
    # Tab 2: Buat Reservasi
    with tab2:
        st.write("#### Buat Reservasi Baru")
        
        if pelanggan_list and barber_list and layanan_list:
            col1, col2 = st.columns(2)
            
            with col1:
                pelanggan_selected = st.selectbox(
                    "Pilih Pelanggan:",
                    [p['id_pelanggan'] for p in pelanggan_list],
                    format_func=lambda x: next((p['nama'] for p in pelanggan_list if p['id_pelanggan'] == x), x)
                )
                
                barber_selected = st.selectbox(
                    "Pilih Barber:",
                    [b['id_pegawai'] for b in barber_list],
                    format_func=lambda x: next((b['nama'] for b in barber_list if b['id_pegawai'] == x), x)
                )
            
            with col2:
                layanan_selected = st.selectbox(
                    "Pilih Layanan:",
                    [l['id_layanan'] for l in layanan_list],
                    format_func=lambda x: next((l['nama_layanan'] for l in layanan_list if l['id_layanan'] == x), x)
                )
                
                tanggal = st.date_input("Tanggal Reservasi")
            
            jam_operasional = []
            for hour in range(9, 22):
                for minute in [0, 15, 30, 45]:
                    if hour == 21 and minute > 0:
                        break
                    jam_operasional.append(f"{hour:02d}:{minute:02d}")
            
            jam = st.selectbox("Jam Reservasi", options=jam_operasional)
            
            if st.button("Buat Reservasi"):
                jam_str = jam
                tanggal_str = tanggal.strftime('%Y-%m-%d')
                
                # --- MODIFIKASI: Implementasi try-except untuk custom error ---
                try:
                    success, message = reservasi_controller.create_reservasi(
                        pelanggan_selected, barber_selected, layanan_selected, tanggal_str, jam_str
                    )
                    
                    if success:
                        st.success(message)
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error(message)
                except JadwalPenuhError as e:
                    st.warning(str(e))
                # ----------------------------------------------------------------
        else:
            st.warning("Pastikan ada pelanggan, barber, dan layanan yang terdaftar terlebih dahulu")
    
    # Tab 3: Update Status
    with tab3:
        st.write("#### Update Status Reservasi")
        
        reservasi_list = reservasi_controller.get_all_reservasi()
        
        if reservasi_list:
            reservasi_id = st.selectbox(
                "Pilih Reservasi:",
                [r['id_reservasi'] for r in reservasi_list],
                format_func=lambda x: f"{x} - {next((r['status'] for r in reservasi_list if r['id_reservasi'] == x), 'Unknown')}"
            )
            
            status_baru = st.selectbox("Status Baru:", ["Pending", "Dikonfirmasi", "Selesai", "Dibatalkan"])
            
            if status_baru == "Dibatalkan":
                alasan = st.text_area("Alasan pembatalan:")
            else:
                alasan = ""
            
            if st.button("Update Status"):
                if status_baru == "Dibatalkan":
                    # Memanggil fungsi pembatalan
                    success, message = reservasi_controller.batalkan_reservasi(reservasi_id, alasan)
                elif status_baru == "Selesai":
                    # MODIFIKASI: Pastikan memanggil selesaikan_reservasi agar Riwayat dibuat!
                    success, message = reservasi_controller.selesaikan_reservasi(reservasi_id)
                else:
                    # Untuk status Pending dan Dikonfirmasi
                    success, message = reservasi_controller.update_status(reservasi_id, status_baru)
                
                if success:
                    st.success(message)
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error(message)
        else:
            st.info("Belum ada reservasi")