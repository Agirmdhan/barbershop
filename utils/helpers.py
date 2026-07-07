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

# =======================================================
# MATERI 5: IMPLEMENTASI DUCK TYPING
# =======================================================

def tampilkan_info_umum(obj):
    """
    Duck Typing: Menampilkan informasi dari ANY object yang punya method tampilkan_info()
    Fungsi ini bekerja dengan berbagai tipe object (Layanan, Reservasi, Pembayaran, dll)
    tanpa perlu check tipe object. Yang penting adalah object punya method tampilkan_info().
    
    Args:
        obj: Object apapun (Layanan, Reservasi, Pembayaran, dll)
        
    Returns:
        String informasi dari object
        
    Raises:
        TypeError: Jika object tidak punya method tampilkan_info()
    """
    # Duck typing: "If it walks like a duck and quacks like a duck, it's a duck"
    # Kita tidak peduli tipe objectnya, yang penting ada method tampilkan_info()
    if hasattr(obj, 'tampilkan_info'):
        return obj.tampilkan_info()
    raise TypeError(f"Object {type(obj).__name__} tidak memiliki method tampilkan_info()")


def hitung_statistik_umum(data_list):
    """
    Duck Typing: Menghitung statistik dari LIST apapun yang punya atribut 'total'
    
    Bisa dipakai untuk: pembayaran_list, riwayat_list, reservasi_list
    Yang penting adalah setiap item punya key 'total' (untuk dictionary) atau atribut 'total' (untuk object)
    
    Args:
        data_list: List of dictionaries atau list of objects
        
    Returns:
        Dictionary berisi statistik (total, count, rata_rata)
    """
    if not data_list:
        return {'total': 0, 'count': 0, 'rata_rata': 0, 'maks': 0, 'min': 0}
    
    # Ekstrak nilai total dari setiap item (bisa dictionary atau object)
    nilai_list = []
    for item in data_list:
        if isinstance(item, dict):
            # Jika dictionary, ambil dari key 'total'
            nilai = item.get('total', 0)
        elif hasattr(item, 'total'):
            # Jika object, ambil dari atribut 'total'
            nilai = item.total
        else:
            # Skip item yang tidak punya total
            continue
        nilai_list.append(nilai)
    
    if not nilai_list:
        return {'total': 0, 'count': 0, 'rata_rata': 0, 'maks': 0, 'min': 0}
    
    total = sum(nilai_list)
    count = len(nilai_list)
    
    return {
        'total': total,
        'count': count,
        'rata_rata': total / count if count > 0 else 0,
        'maks': max(nilai_list),
        'min': min(nilai_list)
    }


def filter_by_status(data_list, status_dicari):
    """
    Duck Typing: Filter list apapun berdasarkan status
    
    Bisa filter: reservasi, pembayaran, riwayat, dll
    Yang penting adalah item punya key 'status' (untuk dictionary) atau atribut 'status' (untuk object)
    
    Args:
        data_list: List of dictionaries atau list of objects
        status_dicari: Status yang ingin difilter (contoh: 'Pending', 'Lunas', 'Selesai')
        
    Returns:
        List yang sudah difilter
    """
    hasil_filter = []
    
    for item in data_list:
        # Duck typing: cek status tanpa peduli tipe data
        if isinstance(item, dict):
            status = item.get('status')
        elif hasattr(item, 'status'):
            status = item.status
        else:
            continue
        
        if status == status_dicari:
            hasil_filter.append(item)
    
    return hasil_filter


def format_harga_umum(obj):
    
    # Cek berbagai kemungkinan atribut harga
    if isinstance(obj, dict):
        nilai = obj.get('harga') or obj.get('total', 0)
    elif hasattr(obj, 'harga'):
        nilai = obj.harga
    elif hasattr(obj, 'total'):
        nilai = obj.total
    else:
        return format_currency(0)
    
    return format_currency(nilai)


def proses_aksi_umum(obj, nama_method, *args, **kwargs):
    if hasattr(obj, nama_method):
        method = getattr(obj, nama_method)
        return method(*args, **kwargs)
    raise AttributeError(f"Object {type(obj).__name__} tidak memiliki method '{nama_method}'")


def dapatkan_nilai_umum(obj, *nama_atribut):
   
    for atribut in nama_atribut:
        if isinstance(obj, dict):
            if atribut in obj:
                return obj[atribut]
        elif hasattr(obj, atribut):
            return getattr(obj, atribut)
    return None

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


def add_dashboard_theme():
    """Tema dashboard bergaya modern tanpa mengubah logika aplikasi."""
    st.markdown(
        """
        <style>
        :root {
            --barber-ink: #4b3f34;
            --barber-accent: #55708d;
            --barber-accent-dark: #405872;
            --barber-cream: #fbf7ef;
            --barber-card: #fffaf2;
            --barber-muted: #817468;
            --barber-line: #e8dccb;
            --barber-info: #c8ebe4;
        }

        .stApp {
            background:
                radial-gradient(circle at 20% 0%, rgba(244, 229, 203, 0.55), transparent 28rem),
                linear-gradient(180deg, #f3eadc 0%, var(--barber-cream) 8rem),
                var(--barber-cream) !important;
            color: var(--barber-ink) !important;
        }

        .main .block-container {
            max-width: 1180px;
            padding: 1.6rem 1.6rem 3rem !important;
            background: transparent !important;
            box-shadow: none !important;
            border-radius: 0 !important;
        }

        [data-testid="stSidebar"] {
            background: #f5ebe0 !important;
            border-right: none !important;
        }

        [data-testid="stSidebar"] * {
            color: var(--barber-ink) !important;
        }

        [data-testid="stSidebar"] .stButton > button {
            background: #faf3e8 !important;
            border: 1px solid #e8dccb !important;
            border-radius: 12px !important;
            color: var(--barber-ink) !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            box-shadow: 0 2px 8px rgba(90, 72, 52, 0.06) !important;
            transition: all 0.2s ease !important;
            padding: 0.6rem 1rem !important;
        }

        [data-testid="stSidebar"] .stButton > button:hover {
            background: #f0e4d4 !important;
            border-color: #d7c8b7 !important;
            box-shadow: 0 4px 12px rgba(90, 72, 52, 0.1) !important;
            transform: translateY(-1px) !important;
        }

        [data-testid="stSidebar"] .stButton > button[data-baseweb="button"][kind="primary"] {
            background: #3d3d3d !important;
            color: #ffffff !important;
            border-color: #3d3d3d !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
        }

        [data-testid="stSidebar"] .stButton > button[data-baseweb="button"][kind="primary"]:hover {
            background: #2d2d2d !important;
            border-color: #2d2d2d !important;
        }

        h1, h2, h3, h4 {
            color: var(--barber-ink) !important;
            letter-spacing: 0 !important;
            font-weight: 800 !important;
        }

        h1 {
            font-size: 2.1rem !important;
            text-transform: uppercase;
        }

        h2, h3 {
            font-size: 1.35rem !important;
        }

        hr {
            border-color: var(--barber-line) !important;
            margin: 1rem 0 1.2rem !important;
        }

        div[data-testid="stHorizontalBlock"] > div:has([data-testid="stMetric"]) {
            background: var(--barber-card) !important;
            border: 1px solid var(--barber-line) !important;
            border-radius: 7px !important;
            box-shadow: 0 14px 32px rgba(90, 72, 52, 0.09) !important;
            overflow: hidden;
            padding: 0 !important;
        }

        div[data-testid="stHorizontalBlock"] > div:has([data-testid="stMetric"])::before {
            content: "";
            display: block;
            height: 2.1rem;
            background: var(--barber-accent);
            border-radius: 7px 7px 0 0;
        }

        [data-testid="stMetric"] {
            padding: 0.85rem 1rem 1rem !important;
        }

        [data-testid="stMetricLabel"] {
            color: var(--barber-muted) !important;
            font-weight: 800 !important;
            text-transform: uppercase;
            letter-spacing: 0 !important;
        }

        [data-testid="stMetricValue"] {
            color: var(--barber-ink) !important;
            font-weight: 800 !important;
        }

        div[data-testid="stAlert"] {
            border: 0 !important;
            border-radius: 7px !important;
            background: var(--barber-info) !important;
            color: #24423e !important;
            box-shadow: 0 10px 24px rgba(90, 72, 52, 0.08) !important;
        }

        div[data-testid="stAlert"] * {
            color: #24423e !important;
        }

        div[data-testid="stDataFrame"],
        div[data-testid="stTable"],
        div[data-testid="stForm"],
        [data-testid="stExpander"] {
            background: var(--barber-card) !important;
            border: 1px solid var(--barber-line) !important;
            border-radius: 7px !important;
            box-shadow: 0 14px 32px rgba(90, 72, 52, 0.09) !important;
            padding: 0.7rem !important;
        }

        div[data-testid="stSelectbox"] label,
        div[data-testid="stTextInput"] label,
        div[data-testid="stTextArea"] label,
        div[data-testid="stDateInput"] label,
        div[data-testid="stMultiSelect"] label {
            color: var(--barber-ink) !important;
            font-weight: 700 !important;
        }

        div[data-baseweb="select"] > div,
        input,
        textarea {
            background: #f4ecdd !important;
            border-color: #d7c8b7 !important;
            border-radius: 7px !important;
        }

        div.stButton > button {
            border: 0 !important;
            border-radius: 7px !important;
            background: var(--barber-accent) !important;
            color: #ffffff !important;
            font-weight: 800 !important;
            box-shadow: 0 10px 22px rgba(64, 88, 114, 0.22) !important;
        }

        div.stButton > button:hover {
            background: var(--barber-accent-dark) !important;
            color: #ffffff !important;
        }

        div[data-testid="stTabs"] button[aria-selected="true"] {
            color: var(--barber-accent) !important;
            border-bottom-color: var(--barber-accent) !important;
        }

        .dashboard-shell {
            background: rgba(255, 250, 242, 0.82);
            border: 1px solid var(--barber-line);
            border-radius: 7px;
            box-shadow: 0 18px 45px rgba(90, 72, 52, 0.10);
            padding: 1.4rem 1.45rem;
            margin-bottom: 1.1rem;
        }

        .dashboard-kicker {
            color: var(--barber-muted);
            font-size: 0.78rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 0.35rem;
        }

        .dashboard-title {
            color: var(--barber-ink);
            font-size: 2rem;
            line-height: 1.15;
            font-weight: 900;
            margin: 0;
            text-transform: uppercase;
        }

        .dashboard-subtitle {
            color: var(--barber-ink);
            margin: 0.7rem 0 0;
        }

        .profile-strip {
            display: flex;
            flex-wrap: wrap;
            gap: 0.75rem;
            margin-top: 1rem;
        }

        .profile-pill {
            background: rgba(255, 250, 242, 0.92);
            border: 1px solid var(--barber-line);
            border-radius: 7px;
            color: var(--barber-ink);
            padding: 0.65rem 0.85rem;
            min-width: 150px;
            box-shadow: 0 8px 18px rgba(90, 72, 52, 0.06);
        }

        .profile-pill span {
            display: block;
            color: var(--barber-muted);
            font-size: 0.72rem;
            font-weight: 800;
            text-transform: uppercase;
        }

        .profile-pill strong {
            display: block;
            font-size: 0.95rem;
            margin-top: 0.15rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _use_fallback_background():
    """Fungsi helper untuk menggunakan fallback background"""
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%) !important;
        }

        .main .block-container {
            background: rgba(255, 255, 255, 0.95) !important;
            padding: 2rem !important;
            border-radius: 10px !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
