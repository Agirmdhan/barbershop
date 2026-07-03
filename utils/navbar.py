import streamlit as st

def create_sidebar_navigation(menu_items, current_page, key_prefix="nav"):
    """
    Membuat sidebar navigation untuk navigasi
    
    Args:
        menu_items: List of tuple (nama_tampil, nama_internal) - icon sudah dihapus
        current_page: Halaman yang sedang aktif
        key_prefix: Prefix untuk unique key
    
    Returns:
        Nama halaman yang dipilih
    """
    with st.sidebar:
        st.markdown("### Menu Navigasi")
        st.markdown("---")
        
        selected_page = current_page
        
        for display_name, internal_name in menu_items:
            # Tentukan style berdasarkan apakah ini halaman aktif
            if internal_name == current_page:
                button_type = "primary"
            else:
                button_type = "secondary"
            
            if st.button(
                display_name,
                key=f"{key_prefix}_{internal_name}",
                type=button_type,
                use_container_width=True
            ):
                selected_page = internal_name
        
        st.markdown("---")
        
        # Tombol logout di sidebar
        if st.button("Logout", key=f"{key_prefix}_logout", use_container_width=True, type="secondary"):
            from utils.helpers import logout
            logout()
            st.rerun()
    
    return selected_page

def create_navbar(menu_items, current_page, key_prefix="nav"):
    """
    Membuat navbar horizontal untuk navigasi (legacy - gunakan create_sidebar_navigation untuk sidebar)
    
    Args:
        menu_items: List of tuple (nama_tampil, nama_internal)
        current_page: Halaman yang sedang aktif
        key_prefix: Prefix untuk unique key
    
    Returns:
        Nama halaman yang dipilih
    """
    # Buat kolom untuk setiap menu item
    cols = st.columns(len(menu_items) + 1)
    
    # Tombol logout di kolom terakhir
    with cols[-1]:
        if st.button("🚪 Logout", key=f"{key_prefix}_logout", use_container_width=True):
            from utils.helpers import logout
            logout()
            st.rerun()
    
    # Tombol menu di kolom-kolom sebelumnya
    selected_page = current_page
    for idx, (display_name, internal_name) in enumerate(menu_items):
        with cols[idx]:
            # Tentukan style berdasarkan apakah ini halaman aktif
            if internal_name == current_page:
                button_type = "primary"
            else:
                button_type = "secondary"
            
            if st.button(
                display_name,
                key=f"{key_prefix}_{internal_name}",
                type=button_type,
                use_container_width=True
            ):
                selected_page = internal_name
    
    return selected_page

def create_top_bar(title, user_info=None):
    """
    Membuat top bar dengan judul dan info user
    
    Args:
        title: Judul halaman
        user_info: Dict dengan info user (opsional)
    """
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.title(title)
    
    with col2:
        if user_info:
            st.write(f"👤 {user_info.get('nama', 'User')}")
            st.caption(f"Role: {user_info.get('role', '-')}")
