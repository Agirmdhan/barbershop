import streamlit as st
from controllers.admin_controller import AdminController
from controllers.pelanggan_controller import PelangganController
from controllers.barber_controller import BarberController
from utils.helpers import initialize_session_state, set_session_state

def show_login_page():
    """Halaman login terpusat untuk pelanggan dan pegawai."""
    initialize_session_state()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("💈 BARBERCHOP AMARIZ")
        st.markdown("---")

        tab1, tab2 = st.tabs(["Login", "Register Pelanggan"])

        with tab1:
            st.subheader("Login")
            identifier = st.text_input("Username atau Email", key="login_identifier")
            password = st.text_input("Password", type="password", key="login_password")

            if st.button("Login", key="login_button"):
                if identifier and password:
                    admin_controller = AdminController()
                    barber_controller = BarberController()
                    pelanggan_controller = PelangganController()

                    success, user_data, message = admin_controller.login_admin(identifier, password)
                    if success:
                        user_role = 'admin'
                    else:
                        success, user_data, message = barber_controller.login_barber(identifier, password)
                        if success:
                            user_role = 'barber'
                        else:
                            success, user_data, message = pelanggan_controller.login_pelanggan(identifier, password)
                            if success:
                                user_role = 'pelanggan'

                    if success:
                        st.success(message)
                        set_session_state('logged_in', True)
                        set_session_state('user_role', user_role)
                        set_session_state('user_data', user_data)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Identifier dan password harus diisi!")

        with tab2:
            st.subheader("Register Pelanggan Baru")
            col_form1, col_form2 = st.columns(2)

            with col_form1:
                reg_nama = st.text_input("Nama Lengkap", key="reg_nama")
                reg_email = st.text_input("Email", key="reg_email")
            with col_form2:
                reg_nohp = st.text_input("No. HP", key="reg_nohp")
                reg_password = st.text_input("Password", type="password", key="reg_password")

            reg_password_confirm = st.text_input("Konfirmasi Password", type="password", key="reg_password_confirm")

            if st.button("Register Pelanggan", key="register_button"):
                if not all([reg_nama, reg_email, reg_nohp, reg_password, reg_password_confirm]):
                    st.error("Semua field harus diisi!")
                elif reg_password != reg_password_confirm:
                    st.error("Password tidak cocok!")
                else:
                    pelanggan_controller = PelangganController()
                    success, message = pelanggan_controller.create_pelanggan(
                        reg_nama, reg_email, reg_nohp, reg_password
                    )
                    if success:
                        st.success(message)
                        st.info("Silahkan login dengan akun yang telah dibuat")
                    else:
                        st.error(message)
