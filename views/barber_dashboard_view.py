import streamlit as st
import pandas as pd
from controllers.barber_controller import BarberController
from controllers.reservasi_controller import ReservasiController
from utils.helpers import format_currency


def show_barber_dashboard():
    """Dashboard dan portal untuk barber."""
    st.subheader("💈 Portal Barber")
    st.write("Selamat datang di portal barber. Terima reservasi, konfirmasi atau tolak, dan pantau status layanan Anda.")

    barber = st.session_state.get('user_data', {})
    st.write(f"**Nama:** {barber.get('nama', '-')}")
    st.write(f"**Spesialisasi:** {barber.get('spesialisasi', '-')}")
    st.write(f"**Status:** {barber.get('status', '-')}")

    menu = st.selectbox(
        "Pilih menu barber:",
        ["Dashboard", "Reservasi Saya", "Status Barber"]
    )

    reservasi_controller = ReservasiController()
    barber_controller = BarberController()

    if menu == "Dashboard":
        st.write("#### Ringkasan")
        st.info("Gunakan menu untuk melihat reservasi yang ditugaskan kepada Anda dan lakukan tindakan konfirmasi atau penolakan.")

    elif menu == "Reservasi Saya":
        st.write("#### Reservasi yang Ditugaskan")
        reservasi_list = reservasi_controller.get_reservasi_by_barber(barber.get('id_pegawai'))

        if reservasi_list:
            df_reservasi = pd.DataFrame(reservasi_list)
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
                        st.experimental_rerun()
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
                st.success(message)
                st.experimental_rerun()
            else:
                st.error(message)
