import streamlit as st
import pandas as pd
from controllers.barber_controller import BarberController
from controllers.reservasi_controller import ReservasiController
from utils.helpers import format_currency
from utils.navbar import create_sidebar_navigation


def show_barber_dashboard():
    """Dashboard dan portal untuk barber."""
    from utils.helpers import logout, add_dashboard_theme
    
    add_dashboard_theme()
    barber = st.session_state.get('user_data', {})
    
    # Header
    st.markdown(
        f"""
        <div class="dashboard-shell">
            <div class="dashboard-kicker">Home > Portal Barber</div>
            <div class="dashboard-title">Portal Barber</div>
            <p class="dashboard-subtitle">Terima reservasi, konfirmasi atau tolak, dan pantau status layanan Anda.</p>
            <div class="profile-strip">
                <div class="profile-pill"><span>Nama</span><strong>{barber.get('nama', '-')}</strong></div>
                <div class="profile-pill"><span>Spesialisasi</span><strong>{barber.get('spesialisasi', '-')}</strong></div>
                <div class="profile-pill"><span>Status</span><strong>{barber.get('status', '-')}</strong></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.write("")
    
    # Navigation menu - menggunakan sidebar
    menu_items = [
        ("Dashboard", "Dashboard"),
        ("Reservasi", "Reservasi Saya"),
        ("Status", "Status Barber")
    ]
    
    current_page = st.session_state.get('page', 'Dashboard')
    selected_page = create_sidebar_navigation(menu_items, current_page, key_prefix="barber")
    
    st.session_state.page = selected_page

    reservasi_controller = ReservasiController()
    barber_controller = BarberController()

    # Gunakan selected_page dari navbar sebagai menu
    menu = selected_page

    if menu == "Dashboard":
        st.write("#### Ringkasan")
        st.info("Gunakan menu untuk melihat reservasi yang ditugaskan kepada Anda dan lakukan tindakan konfirmasi atau penolakan.")

    elif menu == "Reservasi Saya":
        st.write("#### Reservasi yang Ditugaskan")
        reservasi_list = reservasi_controller.get_reservasi_by_barber(barber.get('id_pegawai'))

        if reservasi_list:
            # Transform data to display names instead of IDs
            display_data = []
            for reservasi in reservasi_list:
                # Get pelanggan name
                pelanggan = reservasi_controller.db.get_pelanggan_by_id(reservasi.get('id_pelanggan'))
                nama_pelanggan = pelanggan.get('nama', '-') if pelanggan else '-'
                
                # Get layanan name
                layanan = reservasi_controller.db.get_layanan_by_id(reservasi.get('id_layanan'))
                nama_layanan = layanan.get('nama_layanan', '-') if layanan else '-'
                
                # Get barber name
                barber_data = reservasi_controller.db.get_barber_by_id(reservasi.get('id_barber'))
                nama_barber = barber_data.get('nama', '-') if barber_data else '-'
                
                display_data.append({
                    'ID Reservasi': reservasi.get('id_reservasi'),
                    'Pelanggan': nama_pelanggan,
                    'Barber': nama_barber,
                    'Layanan': nama_layanan,
                    'Tanggal': reservasi.get('tanggal'),
                    'Jam': reservasi.get('jam'),
                    'Status': reservasi.get('status'),
                    'Catatan': reservasi.get('catatan', ''),
                    'Tanggal Dibuat': reservasi.get('tanggal_dibuat', '')
                })
            
            df_reservasi = pd.DataFrame(display_data)
            st.dataframe(df_reservasi, use_container_width=True)

            pending_reservasi = [r for r in reservasi_list if r.get('status') == 'Pending']
            if pending_reservasi:
                reservasi_id = st.selectbox(
                    "Pilih Reservasi untuk Ditindaklanjuti:",
                    [r['id_reservasi'] for r in pending_reservasi],
                    format_func=lambda x: next((f"{r['id_reservasi']} - {r['tanggal']} {r['jam']}" for r in pending_reservasi if r['id_reservasi'] == x), x)
                )
                keputusan = st.selectbox("Tindakan:", ["Konfirmasi", "Tolak", "Selesai"])
                alasan = ""
                if keputusan == "Tolak":
                    alasan = st.text_area("Alasan penolakan:")

                if st.button("Terapkan"):
                    if keputusan == "Konfirmasi":
                        success, message = reservasi_controller.konfirmasi_reservasi(reservasi_id)
                    elif keputusan == "Tolak":
                        success, message = reservasi_controller.tolak_reservasi(reservasi_id, alasan)
                    else:
                        success, message = reservasi_controller.selesaikan_reservasi(reservasi_id)

                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
            else:
                st.info("Tidak ada reservasi pending untuk ditindaklanjuti.")
        else:
            st.info("Belum ada reservasi untuk barber ini.")

    elif menu == "Status Barber":
        st.write("#### Pengaturan Status")
        status = st.selectbox("Ubah status barber:", ["Tersedia", "Sibuk", "Libur"], index=["Tersedia", "Sibuk", "Libur"].index(barber.get('status', 'Tersedia')) if barber.get('status') in ["Tersedia", "Sibuk", "Libur"] else 0)
        if st.button("Simpan Status"):
            success, message = barber_controller.update_status(barber.get('id_pegawai'), status)
            if success:
                # Update session state dengan data terbaru dari database
                updated_barber = barber_controller.get_barber_by_id(barber.get('id_pegawai'))
                if updated_barber:
                    st.session_state.user_data = updated_barber
                st.success(message)
                st.rerun()
            else:
                st.error(message)
