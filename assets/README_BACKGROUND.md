# Cara Menggunakan Background Image

## Instruksi

### 1. Siapkan Gambar Background
- Download gambar barbershop yang Anda inginkan
- Format yang didukung: JPG, PNG, JPEG
- Ukuran yang disarankan: 1920x1080px (Full HD) atau lebih besar
- File size: Kurang dari 2MB untuk performa optimal

### 2. Letakkan Gambar di Folder Assets
- Copy gambar Anda ke folder `assets/`
- Ganti nama menjadi: `barbershop_bg.jpg` atau `barbershop_bg.png`

### 3. Restart Aplikasi
- Stop aplikasi Streamlit (Ctrl+C di terminal)
- Jalankan kembali: `streamlit run app.py`

## Fitur Background

Sistem ini memiliki fitur background image dengan:
- **Overlay gelap** untuk memastikan konten tetap terbaca
- **Background transparan** untuk area konten utama
- **Fallback otomatis** ke gradient biru jika gambar tidak ditemukan

## Halaman yang Mendukung Background

Semua halaman sudah menggunakan background image:
- ✅ Halaman Login
- ✅ Dashboard Admin
- ✅ Dashboard Pelanggan
- ✅ Dashboard Barber

## Troubleshooting

**Gambar tidak muncul?**
1. Pastikan file ada di folder `assets/` dengan nama yang benar
2. Pastikan format file didukung (JPG/PNG)
3. Restart aplikasi setelah menambahkan gambar

**Konten sulit dibaca?**
- Sistem sudah menambahkan overlay gelap 75% untuk meningkatkan keterbacaan
- Area konten menggunakan background putih dengan transparansi 95%

## Contoh Gambar yang Cocok

- Interior barbershop dengan pencahayaan hangat
- Suasana barbershop vintage/retro
- Foto barbershop dengan chair dan perlengkapan cukur
- Gambar dengan tema gelap dan elegan