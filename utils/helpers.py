import streamlit as st
import hashlib

def hash_password(password):
    """Hash password menggunakan SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed_password):
    """Verifikasi password"""
    return hash_password(password) == hashed_password

def set_session_state(key, value):
    """Set session state"""
    st.session_state[key] = value

def get_session_state(key, default=None):
    """Get session state"""
    return st.session_state.get(key, default)

def initialize_session_state():
    """Inisialisasi session state"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None
    if 'user_data' not in st.session_state:
        st.session_state.user_data = None
    if 'page' not in st.session_state:
        st.session_state.page = 'login'

def format_currency(amount):
    """Format currency ke format Rupiah"""
    return f"Rp {amount:,.0f}"

def format_date(date_str):
    """Format date string"""
    if isinstance(date_str, str):
        return date_str
    return str(date_str)

def is_logged_in():
    """Check jika user sudah login"""
    return st.session_state.get('logged_in', False)

def get_user_role():
    """Get user role"""
    return st.session_state.get('user_role', None)

def get_user_data():
    """Get user data"""
    return st.session_state.get('user_data', None)

def logout():
    """Logout user"""
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.user_data = None
    st.session_state.page = 'login'
