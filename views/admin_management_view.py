import streamlit as st
import pandas as pd
import time  
from controllers.barber_controller import BarberController
from controllers.pelanggan_controller import PelangganController
from controllers.layanan_controller import LayananController

def show_barber_management():
    """Manajemen Barber"""
    st.subheader(" Manajemen Barber")
    
    barber_controller = BarberController()
    
    tab1, tab2, tab3 = st.tabs(["Daftar Barber", "Tambah Barber", "Update Status"])
    
    # Tab 1: Daftar Barber
    with tab1:
        st.write("#### Daftar Barber")
        barbers = barber_controller.get_all_barbers()
        
        if barbers:
            import pandas as pd
            df_barbers = pd.DataFrame(barbers)
            st.dataframe(df_barbers, use_container_width=True)
            
            # Delete option
            st.write("##### Hapus Barber")
            barber_id_delete = st.selectbox("Pilih Barber untuk dihapus:", [b['id_pegawai'] for b in barbers], key="delete_barber")
            if st.button("Hapus Barber", key="btn_delete_barber"):
                success, message = barber_controller.delete_barber(barber_id_delete)
                if success:
                    st.success(message)
                    time.sleep(2)  # <-- TAMBAHAN
                    st.rerun()
                else:
                    st.error(message)
        else:
            st.info("Belum ada barber terdaftar")
    
    # Tab 2: Tambah Barber
    with tab2:
        st.write("#### Tambah Barber Baru")
        
        col1, col2 = st.columns(2)
        with col1:
            barber_nama = st.text_input("Nama Barber")
            barber_spesialisasi = st.text_input("Spesialisasi")
        with col2:
            barber_username = st.text_input("Username Barber")
            barber_nohp = st.text_input("No. HP")
            barber_usia = st.number_input("Usia", min_value=17, max_value=80)
            barber_password = st.text_input("Password", type="password")
        
        if st.button("Tambah Barber"):
            if barber_nama and barber_username and barber_nohp and barber_spesialisasi and barber_password:
                success, message = barber_controller.create_barber(
                    barber_nama,
                    barber_nohp,
                    barber_usia,
                    barber_username,
                    barber_password,
                    barber_spesialisasi
                )
                if success:
                    st.success(message)
                    time.sleep(2)  
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.error("Semua field harus diisi!")
    
    # Tab 3: Update Status
    with tab3:
        st.write("#### Update Status Barber")
        barbers = barber_controller.get_all_barbers()
        
        if barbers:
            barber_id = st.selectbox("Pilih Barber:", [b['id_pegawai'] for b in barbers], key="status_barber")
            status = st.selectbox("Status", ["Tersedia", "Sibuk", "Libur"])
            
            if st.button("Update Status"):
                success, message = barber_controller.update_status(barber_id, status)
                if success:
                    st.success(message)
                    time.sleep(2)  # <-- TAMBAHAN
                    st.rerun()
                else:
                    st.error(message)
        else:
            st.info("Belum ada barber terdaftar")


def show_pelanggan_management():
    """Manajemen Pelanggan"""
    st.subheader(" Manajemen Pelanggan")
    
    pelanggan_controller = PelangganController()
    
    tab1, tab2, tab3 = st.tabs(["Daftar Pelanggan", "Tambah Pelanggan", "Update Pelanggan"])
    
    # Tab 1: Daftar Pelanggan
    with tab1:
        st.write("#### Daftar Pelanggan")
        pelanggan_list = pelanggan_controller.get_all_pelanggan()
        
        if pelanggan_list:
            import pandas as pd
            df_pelanggan = pd.DataFrame(pelanggan_list)
            st.dataframe(df_pelanggan, use_container_width=True)
            
            # Delete option
            st.write("##### Hapus Pelanggan")
            pelanggan_id_delete = st.selectbox("Pilih Pelanggan untuk dihapus:", [p['id_pelanggan'] for p in pelanggan_list], key="delete_pelanggan")
            if st.button("Hapus Pelanggan", key="btn_delete_pelanggan"):
                success, message = pelanggan_controller.delete_pelanggan(pelanggan_id_delete)
                if success:
                    st.success(message)
                    time.sleep(2)  # <-- TAMBAHAN
                    st.rerun()
                else:
                    st.error(message)
        else:
            st.info("Belum ada pelanggan terdaftar")
    
    # Tab 2: Tambah Pelanggan
    with tab2:
        st.write("#### Tambah Pelanggan Baru")
        
        col1, col2 = st.columns(2)
        with col1:
            bytes_nama = st.text_input("Nama Pelanggan")
            pelanggan_email = st.text_input("Email")
        with col2:
            pelanggan_nohp = st.text_input("No. HP")
            pelanggan_password = st.text_input("Password", type="password")
        
        if st.button("Tambah Pelanggan"):
            if bytes_nama and pelanggan_nohp and pelanggan_email and pelanggan_password:
                success, message = pelanggan_controller.create_pelanggan(
                    bytes_nama,
                    pelanggan_email,
                    pelanggan_nohp,
                    pelanggan_password
                )
                if success:
                    st.success(message)
                    time.sleep(2)  # <-- TAMBAHAN
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.error("Semua field harus diisi!")
    # Tab 3: Update Pelanggan
    with tab3:
        st.write("#### Update Data Pelanggan")
        pelanggan_list = pelanggan_controller.get_all_pelanggan()
        
        if pelanggan_list:
            pelanggan_id = st.selectbox("Pilih Pelanggan:", [p['id_pelanggan'] for p in pelanggan_list], key="update_pelanggan")
            
            pelanggan = pelanggan_controller.get_pelanggan_by_id(pelanggan_id)
            
            col1, col2 = st.columns(2)
            with col1:
                nama_baru = st.text_input("Nama", value=pelanggan['nama'])
            with col2:
                nohp_baru = st.text_input("No. HP", value=pelanggan['nomor_hp'])
            
            email_baru = st.text_input("Email", value=pelanggan['email'])
            
            if st.button("Update Pelanggan"):
                success, message = pelanggan_controller.update_pelanggan(
                    pelanggan_id, nama_baru, email_baru, nohp_baru
                )
                if success:
                    st.success(message)
                    time.sleep(2)  # <-- TAMBAHAN
                    st.rerun()
                else:
                    st.error(message)
        else:
            st.info("Belum ada pelanggan terdaftar")
def show_layanan_management():
    """Manajemen Layanan"""
    st.subheader(" Manajemen Layanan")
    
    layanan_controller = LayananController()
    
    tab1, tab2, tab3 = st.tabs(["Daftar Layanan", "Tambah Layanan", "Update Layanan"])
    
    # Tab 1: Daftar Layanan
    with tab1:
        st.write("#### Daftar Layanan")
        layanan_list = layanan_controller.get_all_layanan()
        
        if layanan_list:
            import pandas as pd
            df_layanan = pd.DataFrame(layanan_list)
            st.dataframe(df_layanan, use_container_width=True)
            
            # Delete option
            st.write("##### Hapus Layanan")
            layanan_id_delete = st.selectbox("Pilih Layanan untuk dihapus:", [l['id_layanan'] for l in layanan_list], key="delete_layanan")
            if st.button("Hapus Layanan", key="btn_delete_layanan"):
                success, message = layanan_controller.delete_layanan(layanan_id_delete)
                if success:
                    st.success(message)
                    time.sleep(2)  # <-- TAMBAHAN
                    st.rerun()
                else:
                    st.error(message)
        else:
            st.info("Belum ada layanan terdaftar")
    
    # Tab 2: Tambah Layanan
    with tab2:
        st.write("#### Tambah Layanan Baru")
        
        col1, col2 = st.columns(2)
        with col1:
            layanan_nama = st.text_input("Nama Layanan")
            layanan_durasi = st.number_input("Durasi (menit)", min_value=5, max_value=480, value=30)
        with col2:
            layanan_harga = st.number_input("Harga (Rp)", min_value=0, value=50000)
        
        layanan_deskripsi = st.text_area("Deskripsi", height=100)
        
        if st.button("Tambah Layanan"):
            if layanan_nama and layanan_harga > 0:
                success, message = layanan_controller.create_layanan(
                    layanan_nama, layanan_harga, layanan_durasi, layanan_deskripsi
                )
                if success:
                    st.success(message)
                    time.sleep(2)  # <-- TAMBAHAN
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.error("Nama dan harga harus diisi dengan benar!")
    
    # Tab 3: Update Layanan
    with tab3:
        st.write("#### Update Layanan")
        layanan_list = layanan_controller.get_all_layanan()
        
        if layanan_list:
            layanan_id = st.selectbox("Pilih Layanan:", [l['id_layanan'] for l in layanan_list], key="update_layanan")
            
            layanan = layanan_controller.get_layanan_by_id(layanan_id)
            
            col1, col2 = st.columns(2)
            with col1:
                nama_baru = st.text_input("Nama Layanan", value=layanan['nama_layanan'])
                durasi_baru = st.number_input("Durasi (menit)", min_value=5, value=layanan['durasi'])
            with col2:
                harga_baru = st.number_input(
                    "Harga (Rp)", 
                    min_value=0, 
                    value=int(layanan['harga']), 
                    key=f"harga_{layanan['id_layanan']}"
                )
            
            deskripsi_baru = st.text_area("Deskripsi", value=layanan['deskripsi'], height=100)
            
            if st.button("Update Layanan"):
                success, message = layanan_controller.update_layanan(
                    layanan_id, nama_baru, harga_baru, durasi_baru, deskripsi_baru
                )
                if success:
                    st.success(message)
                    time.sleep(2)  # <-- TAMBAHAN
                    st.rerun()
                else:
                    st.error(message)
        else:
            st.info("Belum ada layanan terdaftar")