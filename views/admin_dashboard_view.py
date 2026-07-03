import streamlit as st
from utils.helpers import logout, add_dashboard_theme
from utils.navbar import create_sidebar_navigation

def show_admin_dashboard():
    """Dashboard Admin"""
    add_dashboard_theme()
    user_data = st.session_state.get('user_data', {})
    
    # Header
    st.markdown(
        f"""
        <div class="dashboard-shell">
            <div class="dashboard-kicker">Home > Dashboard Admin</div>
            <div class="dashboard-title">Barbershop Management System</div>
            <p class="dashboard-subtitle">Selamat datang, {user_data.get('nama', 'Admin')}. Kelola barber, pelanggan, layanan, reservasi, pembayaran, dan laporan.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.write("")
    
    # Navigation menu - menggunakan sidebar
    menu_items = [
        ("Dashboard", "Dashboard Utama"),
        ("Barber", "Manajemen Barber"),
        ("Pelanggan", "Manajemen Pelanggan"),
        ("Layanan", "Manajemen Layanan"),
        ("Reservasi", "Manajemen Reservasi"),
        ("Pembayaran", "Manajemen Pembayaran"),
        ("Laporan", "Laporan")
    ]
    
    current_page = st.session_state.get('page', 'Dashboard Utama')
    selected_page = create_sidebar_navigation(menu_items, current_page, key_prefix="admin")
    
    st.session_state.page = selected_page
