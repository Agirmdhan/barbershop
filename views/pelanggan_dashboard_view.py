import streamlit as st
import pandas as pd
import time
from controllers.pelanggan_controller import PelangganController
from controllers.barber_controller import BarberController
from controllers.layanan_controller import LayananController
from controllers.reservasi_controller import ReservasiController, JadwalPenuhError
from controllers.pembayaran_controller import PembayaranController
from utils.helpers import format_currency
from utils.navbar import create_sidebar_navigation


def show_pelanggan_dashboard():
    """Dashboard dan portal untuk pelanggan."""
    from utils.helpers import logout, add_dashboard_theme
    
    add_dashboard_theme()
    pengguna = st.session_state.get('user_data', {})
    
    # Header
    st.markdown(
        f"""
        <div class="dashboard-shell">
            <div class="dashboard-kicker">Home > Portal Pelanggan</div>
            <div class="dashboard-title">Portal Pelanggan</div>
            <p class="dashboard-subtitle">Buat reservasi, lihat riwayat, dan cek pembayaran Anda.</p>
            <div class="profile-strip">
                <div class="profile-pill"><span>Nama</span><strong>{pengguna.get('nama', '-')}</strong></div>
                <div class="profile-pill"><span>Email</span><strong>{pengguna.get('email', '-')}</strong></div>
                <div class="profile-pill"><span>Nomor HP</span><strong>{pengguna.get('nomor_hp', '-')}</strong></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.write("")
    
    # Navigation menu - menggunakan sidebar
    menu_items = [
        ("Dashboard", "Dashboard"),
        ("Buat Reservasi", "Buat Reservasi"),
        ("Riwayat", "Riwayat Reservasi"),
        ("Pembayaran", "Pembayaran")
    ]
    
    current_page = st.session_state.get('page', 'Dashboard')
    selected_page = create_sidebar_navigation(menu_items, current_page, key_prefix="pelanggan")
    
    st.session_state.page = selected_page

    pelanggan_controller = PelangganController()
    barber_controller = BarberController()
    layanan_controller = LayananController()
    reservasi_controller = ReservasiController()
    pembayaran_controller = PembayaranController()

    # Gunakan selected_page dari navbar sebagai menu
    menu = selected_page

    if menu == "Dashboard":
        st.write("#### Informasi Akun")
        st.info("Gunakan menu di atas untuk membuat reservasi, melihat riwayat reservasi, dan status pembayaran Anda.")

    elif menu == "Buat Reservasi":
        st.write("#### Buat Reservasi Baru")

        barber_list = barber_controller.get_available_barbers()
        layanan_list = layanan_controller.get_all_layanan()

        if not barber_list:
            st.warning("Belum ada barber tersedia. Silakan coba lagi nanti.")
            return
        if not layanan_list:
            st.warning("Belum ada layanan terdaftar. Silakan hubungi admin.")
            return

        col1, col2 = st.columns(2)
        with col1:
            barber_selected = st.selectbox(
                "Pilih Barber:",
                [b['id_pegawai'] for b in barber_list],
                format_func=lambda x: next((b['nama'] for b in barber_list if b['id_pegawai'] == x), x)
            )
            tanggal = st.date_input("Tanggal Reservasi")
        with col2:
            layanan_selected = st.selectbox(
                "Pilih Layanan:",
                [l['id_layanan'] for l in layanan_list],
                format_func=lambda x: next((l['nama_layanan'] for l in layanan_list if l['id_layanan'] == x), x)
            )
            jam_operasional = []
            for hour in range(9, 22):
                for minute in [0, 15, 30, 45]:
                    if hour == 21 and minute > 0:
                        break
                    jam_operasional.append(f"{hour:02d}:{minute:02d}")
            jam = st.selectbox("Jam Reservasi", options=jam_operasional)

        if st.button("Pesan Reservasi"):
            tanggal_str = tanggal.strftime('%Y-%m-%d')
            jam_str = jam
            
            try:
                success, message = reservasi_controller.create_reservasi(
                    pengguna.get('id_pelanggan'), barber_selected, layanan_selected, tanggal_str, jam_str
                )
                if success:
                    st.success(message)
                    time.sleep(2)  
                    st.rerun()
                else:
                    st.error(message)
            except JadwalPenuhError as e:
                # Menampilkan pesan error khusus ke pelanggan
                st.warning(str(e))
              

    elif menu == "Riwayat Reservasi":
        st.write("#### Riwayat Reservasi")
        reservasi_list = reservasi_controller.get_reservasi_by_pelanggan(pengguna.get('id_pelanggan'))

        if reservasi_list:
            barber_list = barber_controller.get_all_barbers()
            layanan_list = layanan_controller.get_all_layanan() 
            
            tampilan_list = []
            for res in reservasi_list:
                nama_barber = next((b['nama'] for b in barber_list if b['id_pegawai'] == res['id_barber']), res['id_barber'])
                nama_layanan = next((l['nama_layanan'] for l in layanan_list if l['id_layanan'] == res['id_layanan']), res['id_layanan'])
                
                tampilan_list.append({
                    "ID Reservasi": res['id_reservasi'],
                    "Nama Pelanggan": pengguna.get('nama'), 
                    "Barber": nama_barber,
                    "Layanan": nama_layanan,
                    "Tanggal": res['tanggal'],
                    "Jam": res['jam'],
                    "Status": res['status'],
                    "Catatan": res['catatan'],
                    "Tanggal Dibuat": res['tanggal_dibuat']
                })
            
            df_reservasi = pd.DataFrame(tampilan_list)
            st.dataframe(df_reservasi, use_container_width=True)

            # --- Form Ubah Tanggal Reservasi ---
            reservasi_bisa_diubah = [r for r in reservasi_list if r['status'] in ["Pending", "Dikonfirmasi"]]

            if reservasi_bisa_diubah:
                st.write("---")
                st.subheader("📅 Ubah Tanggal Reservasi")
                st.caption("Pilih reservasi dengan status **Pending** atau **Dikonfirmasi** untuk mengubah jadwal.")

                pilihan_reservasi = [r['id_reservasi'] for r in reservasi_bisa_diubah]
                id_reservasi_selected = st.selectbox(
                    "Pilih ID Reservasi:",
                    options=pilihan_reservasi,
                    format_func=lambda x: f"{x} - {next((r['tanggal'] for r in reservasi_bisa_diubah if r['id_reservasi'] == x), '')} {next((r['jam'] for r in reservasi_bisa_diubah if r['id_reservasi'] == x), '')}"
                )

                detail_reservasi = next(r for r in reservasi_bisa_diubah if r['id_reservasi'] == id_reservasi_selected)
                st.info(f"**Reservasi:** {id_reservasi_selected} | **Tanggal Saat Ini:** {detail_reservasi['tanggal']} | **Jam:** {detail_reservasi['jam']} | **Barber:** {next((b['nama'] for b in barber_list if b['id_pegawai'] == detail_reservasi['id_barber']), detail_reservasi['id_barber'])}")

                col1, col2 = st.columns(2)
                with col1:
                    tanggal_baru = st.date_input("Tanggal Baru", key="ubah_tanggal")
                with col2:
                    jam_operasional = []
                    for hour in range(9, 22):
                        for minute in [0, 15, 30, 45]:
                            if hour == 21 and minute > 0:
                                break
                            jam_operasional.append(f"{hour:02d}:{minute:02d}")
                    jam_baru = st.selectbox("Jam Baru", options=jam_operasional, key="ubah_jam")

                if st.button("Simpan Perubahan Tanggal", type="primary"):
                    tanggal_baru_str = tanggal_baru.strftime('%Y-%m-%d')
                    success, message = reservasi_controller.ubah_tanggal_reservasi(
                        id_reservasi_selected, tanggal_baru_str, jam_baru
                    )
                    if success:
                        st.success(message)
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error(message)
            else:
                st.write("---")
                st.info("Tidak ada reservasi dengan status **Pending** atau **Dikonfirmasi** yang dapat diubah tanggalnya.")
        else:
            st.info("Belum ada riwayat reservasi.")

    elif menu == "Pembayaran":
        st.write("#### Daftar Pembayaran")
        pembayaran_list = pembayaran_controller.get_pembayaran_by_pelanggan(pengguna.get('id_pelanggan'))

        if pembayaran_list:
            df_pembayaran = pd.DataFrame(pembayaran_list)
            df_tampilan = df_pembayaran.copy()
            if 'total' in df_tampilan.columns:
                df_tampilan['total'] = df_tampilan['total'].apply(format_currency)
            st.dataframe(df_tampilan, use_container_width=True)
            
            pembayaran_pending = [p for p in pembayaran_list if p.get('status', '').lower() == 'pending']
            
            if pembayaran_pending:
                st.write("---")
                st.subheader("💳 Form Konfirmasi Pembayaran")
                st.caption("Silakan pilih ID Pembayaran Anda yang berstatus Pending untuk diselesaikan.")
                
                pilihan_id_bayar = [p['id_pembayaran'] for p in pembayaran_pending]
                id_bayar_selected = st.selectbox("Pilih ID Pembayaran:", options=pilihan_id_bayar)
                
                detail_pembayaran = next(p for p in pembayaran_pending if p['id_pembayaran'] == id_bayar_selected)
                total_tagihan = detail_pembayaran.get('total', 0)
                
                st.info(f"**Total yang Harus Dibayar:** {format_currency(total_tagihan)}")
                metode_bayar = st.selectbox("Pilih Metode Pembayaran:", ["Transfer Bank", "E-Wallet"])
                
                if st.button("Konfirmasi Bayar Sekarang", type="primary"):
                    success, message = pembayaran_controller.proses_pembayaran(id_bayar_selected, metode_bayar)
                    
                    if success:
                        st.success(f"Pembayaran {id_bayar_selected} Berhasil! Status diperbarui.")
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error(message)
            else:
                st.write("---")
                st.success("🎉 Luar biasa! Semua tagihan pembayaran Anda telah Lunas.")
        else:
            st.info("Belum ada pembayaran untuk akun ini.")
