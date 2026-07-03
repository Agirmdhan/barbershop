import streamlit as st
from views.login_view import show_login_page
from views.admin_dashboard_view import show_admin_dashboard
from views.admin_management_view import show_barber_management, show_pelanggan_management, show_layanan_management
from views.admin_reservasi_view import show_reservasi_management
from views.admin_pembayaran_view import show_pembayaran_management
from views.admin_report_view import show_main_dashboard, show_laporan_page
from views.pelanggan_dashboard_view import show_pelanggan_dashboard
from views.barber_dashboard_view import show_barber_dashboard
from utils.helpers import initialize_session_state, is_logged_in, get_user_role

def main():
    """Main application"""

    st.set_page_config(
        page_title="Barbershop Management System",
        page_icon="💈",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    initialize_session_state()

    if not is_logged_in():
        show_login_page()
        return

    role = get_user_role()

    if role == 'admin':
        show_admin_dashboard()

        st.markdown("---")
        current_page = st.session_state.get('page', 'Dashboard Utama')

        if current_page == 'Dashboard Utama':
            show_main_dashboard()
        elif current_page == 'Manajemen Barber':
            show_barber_management()
        elif current_page == 'Manajemen Pelanggan':
            show_pelanggan_management()
        elif current_page == 'Manajemen Layanan':
            show_layanan_management()
        elif current_page == 'Manajemen Reservasi':
            show_reservasi_management()
        elif current_page == 'Manajemen Pembayaran':
            show_pembayaran_management()
        elif current_page == 'Laporan':
            show_laporan_page()

    elif role == 'barber':
        show_barber_dashboard()

    elif role == 'pelanggan':
        show_pelanggan_dashboard()

    else:
        st.error('Role tidak dikenal. Silakan login ulang.')
        show_login_page()

if __name__ == "__main__":
    main()
