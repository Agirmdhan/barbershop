import streamlit as st
from utils.helpers import logout

def show_admin_dashboard():
    """Dashboard Admin"""
    # Header
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.title("Barbershop Management System")
    with col2:
        st.write("")
    with col3:
        if st.button("🚪 Logout"):
            logout()
            st.rerun()
    
    st.markdown("---")
    
    # Display user info
    user_data = st.session_state.get('user_data', {})
    st.write(f"Welcome, **{user_data.get('nama', 'Admin')}**! ")
    
    # Navigation menu
    st.subheader("Menu Navigasi")
    
    menu = st.selectbox(
        "Pilih menu:",
        [
            "Dashboard Utama",
            "Manajemen Barber",
            "Manajemen Pelanggan",
            "Manajemen Layanan",
            "Manajemen Reservasi",
            "Manajemen Pembayaran",
            "Laporan"
        ]
    )
    
    st.session_state.page = menu
