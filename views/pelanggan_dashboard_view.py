import streamlit as st
import pandas as pd
import time
from controllers.pelanggan_controller import PelangganController
from controllers.barber_controller import BarberController
from controllers.layanan_controller import LayananController
from controllers.reservasi_controller import ReservasiController, JadwalPenuhError
from controllers.pembayaran_controller import PembayaranController
from utils.helpers import format_currency


def show_pelanggan_dashboard():
    """Dashboard dan portal untuk pelanggan."""
    st.subheader(" Portal Pelanggan")
    st.write("Selamat datang di portal pelanggan. Silakan buat reservasi, lihat riwayat, dan cek pembayaran Anda.")

    pengguna = st.session_state.get('user_data', {})
    st.write(f"**Nama:** {pengguna.get('nama', '-')}")
    st.write(f"**Email:** {pengguna.get('email', '-')}")
    st.write(f"**Nomor HP:** {pengguna.get('nomor_hp', '-')}")

    menu = st.selectbox(
        "Pilih menu pelanggan:",
        ["Dashboard", "Buat Reservasi", "Riwayat Reservasi", "Pembayaran"]
    )

    pelanggan_controller = PelangganController()
    barber_controller = BarberController()
    layanan_controller = LayananController()
    reservasi_controller = ReservasiController()
    pembayaran_controller = PembayaranController()

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
            barber_list = barber_controller.get_available_barbers()
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