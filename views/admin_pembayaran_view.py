import streamlit as st
import pandas as pd
from controllers.pembayaran_controller import PembayaranController
from controllers.reservasi_controller import ReservasiController
from utils.helpers import format_currency

def show_pembayaran_management():
    """Manajemen Pembayaran"""
    st.subheader(" Manajemen Pembayaran")
    
    pembayaran_controller = PembayaranController()
    reservasi_controller = ReservasiController()
    
    tab1, tab2, tab3 = st.tabs(["Daftar Pembayaran", "Proses Pembayaran", "Laporan"])
    
    # Tab 1: Daftar Pembayaran
    with tab1:
        st.write("#### Daftar Pembayaran")
        
        filter_status = st.multiselect(
            "Filter Status:",
            ["Pending", "Lunas"],
            default=["Pending", "Lunas"]
        )
        
        pembayaran_list = pembayaran_controller.get_all_pembayaran()
        
        if filter_status:
            pembayaran_list = [p for p in pembayaran_list if p.get('status') in filter_status]
        
        if pembayaran_list:
            df_pembayaran = pd.DataFrame(pembayaran_list)
            
            # Format currency
            if 'total' in df_pembayaran.columns:
                df_pembayaran['total'] = df_pembayaran['total'].apply(format_currency)
            
            st.dataframe(df_pembayaran, use_container_width=True)
        else:
            st.info("Belum ada pembayaran")
    
    # Tab 2: Proses Pembayaran
    with tab2:
        st.write("#### Proses Pembayaran")
        
        pembayaran_list = pembayaran_controller.get_all_pembayaran()
        pembayaran_pending = [p for p in pembayaran_list if p.get('status') == 'Pending']
        
        if pembayaran_pending:
            pembayaran_id = st.selectbox(
                "Pilih Pembayaran:",
                [p['id_pembayaran'] for p in pembayaran_pending],
                format_func=lambda x: f"{x} - {format_currency(next((p['total'] for p in pembayaran_pending if p['id_pembayaran'] == x), 0))}"
            )
            
            metode = st.selectbox("Metode Pembayaran:", ["Tunai", "Transfer", "Kartu Kredit"])
            
            if st.button("Proses Pembayaran"):
                success, message = pembayaran_controller.proses_pembayaran(pembayaran_id, metode)
                
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
        else:
            st.info("Tidak ada pembayaran yang menunggu")
    
    # Tab 3: Laporan
    with tab3:
        st.write("#### Laporan Pembayaran")
        
        col1, col2 = st.columns(2)
        with col1:
            tanggal_mulai = st.date_input("Tanggal Mulai")
        with col2:
            tanggal_akhir = st.date_input("Tanggal Akhir")
        
        if st.button("Tampilkan Laporan"):
            tanggal_mulai_str = tanggal_mulai.strftime('%Y-%m-%d')
            tanggal_akhir_str = tanggal_akhir.strftime('%Y-%m-%d')
            
            laporan = pembayaran_controller.get_laporan_pembayaran(tanggal_mulai_str, tanggal_akhir_str)
            
            if laporan:
                df_laporan = pd.DataFrame(laporan)
                
                # Format currency
                if 'total' in df_laporan.columns:
                    df_laporan['total'] = df_laporan['total'].apply(format_currency)
                
                st.dataframe(df_laporan, use_container_width=True)
                
                # Statistics
                st.write("#### Statistik")
                total_lunas = pembayaran_controller.get_total_pembayaran('Lunas')
                total_pending = pembayaran_controller.get_total_pembayaran('Pending')
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Lunas", format_currency(total_lunas))
                with col2:
                    st.metric("Total Pending", format_currency(total_pending))
                with col3:
                    st.metric("Total Semua", format_currency(total_lunas + total_pending))
            else:
                st.info("Tidak ada data pembayaran untuk periode tersebut")
