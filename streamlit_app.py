import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Tools Olah Data Google Maps", layout="wide")

st.title("🗺️ Tools Olah Data Profil Bisnis Google Maps")
st.markdown("Upload file CSV hasil scraping Google Maps untuk memfilter data")

# Inisialisasi session state
if 'results' not in st.session_state:
    st.session_state.results = {}
if 'df' not in st.session_state:
    st.session_state.df = None

# Upload file
uploaded_file = st.file_uploader("📂 Upload file CSV", type=['csv'])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.session_state.df = df
        st.success(f"✅ Berhasil! Total data: {len(df)} baris")
        
        # Preview data
        with st.expander("📋 Preview Data (10 baris pertama)"):
            st.dataframe(df.head(10))
        
        with st.expander("📊 Informasi Kolom"):
            st.write("**Nama-nama kolom dalam file Anda:**")
            st.code(', '.join(df.columns))
            
            # Deteksi kolom otomatis
            st.write("**Deteksi otomatis kolom:**")
            website_detected = None
            wa_detected = None
            review_detected = None
            
            for col in df.columns:
                col_lower = col.lower()
                if 'website' in col_lower or 'web' in col_lower:
                    website_detected = col
                    st.write(f"✅ Kolom Website terdeteksi: `{col}`")
                if 'whatsapp' in col_lower or 'wa' in col_lower or 'phone' in col_lower or 'telp' in col_lower:
                    wa_detected = col
                    st.write(f"✅ Kolom WhatsApp/Phone terdeteksi: `{col}`")
                if 'review' in col_lower or 'ulasan' in col_lower or 'rating_count' in col_lower or 'total_rating' in col_lower:
                    review_detected = col
                    st.write(f"✅ Kolom Ulasan terdeteksi: `{col}`")
            
            if not website_detected:
                st.warning("⚠️ Kolom Website tidak terdeteksi otomatis, silakan pilih manual di bawah")
            if not wa_detected:
                st.warning("⚠️ Kolom WhatsApp tidak terdeteksi otomatis, silakan pilih manual di bawah")
            if not review_detected:
                st.warning("⚠️ Kolom Ulasan tidak terdeteksi otomatis, silakan pilih manual di bawah")
        
        # Pilih kolom secara manual
        st.subheader("🔧 Konfigurasi Kolom (pilih kolom yang sesuai)")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            website_col = st.selectbox(
                "Kolom Website", 
                options=[''] + list(df.columns),
                index=0 if not website_detected else list(df.columns).index(website_detected) + 1
            )
            if website_col == '':
                website_col = None
        
        with col2:
            whatsapp_col = st.selectbox(
                "Kolom WhatsApp/Phone", 
                options=[''] + list(df.columns),
                index=0 if not wa_detected else list(df.columns).index(wa_detected) + 1
            )
            if whatsapp_col == '':
                whatsapp_col = None
        
        with col3:
            reviews_col = st.selectbox(
                "Kolom Jumlah Ulasan", 
                options=[''] + list(df.columns),
                index=0 if not review_detected else list(df.columns).index(review_detected) + 1
            )
            if reviews_col == '':
                reviews_col = None
        
        # Tombol filter
        st.markdown("---")
        st.subheader("🎯 Filter Data")
        
        # Baris tombol 1
        btn_col1, btn_col2, btn_col3 = st.columns(3)
        
        with btn_col1:
            if st.button("🌐 1. Profil dengan Website", use_container_width=True):
                if website_col:
                    filtered = df[df[website_col].notna() & (df[website_col].astype(str).str.strip() != '')]
                    st.session_state.results['🌐 Profil dengan Website'] = filtered
                    st.success(f"Ditemukan {len(filtered)} data")
                else:
                    st.error("Silakan pilih kolom Website terlebih dahulu!")
        
        with btn_col2:
            if st.button("📱 2. Profil dengan WhatsApp", use_container_width=True):
                if whatsapp_col:
                    filtered = df[df[whatsapp_col].notna() & (df[whatsapp_col].astype(str).str.strip() != '')]
                    st.session_state.results['📱 Profil dengan WhatsApp'] = filtered
                    st.success(f"Ditemukan {len(filtered)} data")
                else:
                    st.error("Silakan pilih kolom WhatsApp terlebih dahulu!")
        
        with btn_col3:
            if st.button("⭐ 3. Ulasan > 100", use_container_width=True):
                if reviews_col:
                    numeric_reviews = pd.to_numeric(df[reviews_col], errors='coerce')
                    filtered = df[numeric_reviews > 100]
                    st.session_state.results['⭐ Ulasan > 100'] = filtered
                    st.success(f"Ditemukan {len(filtered)} data")
                else:
                    st.error("Silakan pilih kolom Ulasan terlebih dahulu!")
        
        # Baris tombol 2
        btn_col4, btn_col5, btn_col6 = st.columns(3)
        
        with btn_col4:
            if st.button("⭐⭐ 4. Ulasan 50-100", use_container_width=True):
                if reviews_col:
                    numeric_reviews = pd.to_numeric(df[reviews_col], errors='coerce')
                    filtered = df[(numeric_reviews >= 50) & (numeric_reviews <= 100)]
                    st.session_state.results['⭐⭐ Ulasan 50-100'] = filtered
                    st.success(f"Ditemukan {len(filtered)} data")
                else:
                    st.error("Silakan pilih kolom Ulasan terlebih dahulu!")
        
        with btn_col5:
            if st.button("⭐⭐⭐ 5. Ulasan 10-50", use_container_width=True):
                if reviews_col:
                    numeric_reviews = pd.to_numeric(df[reviews_col], errors='coerce')
                    filtered = df[(numeric_reviews >= 10) & (numeric_reviews < 50)]
                    st.session_state.results['⭐⭐⭐ Ulasan 10-50'] = filtered
                    st.success(f"Ditemukan {len(filtered)} data")
                else:
                    st.error("Silakan pilih kolom Ulasan terlebih dahulu!")
        
        with btn_col6:
            if st.button("🚫 6. Profil Tanpa Website", use_container_width=True):
                if website_col:
                    filtered = df[df[website_col].isna() | (df[website_col].astype(str).str.strip() == '')]
                    st.session_state.results['🚫 Profil Tanpa Website'] = filtered
                    st.success(f"Ditemukan {len(filtered)} data")
                else:
                    st.error("Silakan pilih kolom Website terlebih dahulu!")
        
        # Tombol aksi
        st.markdown("---")
        action_col1, action_col2, action_col3 = st.columns(3)
        
        with action_col1:
            if st.button("🔄 Reset Semua Filter", use_container_width=True):
                st.session_state.results = {}
                st.success("Semua hasil filter telah direset!")
                st.rerun()
        
        with action_col2:
            if st.button("📋 Tampilkan Semua Hasil", use_container_width=True):
                if st.session_state.results:
                    for title, data in st.session_state.results.items():
                        st.subheader(title)
                        st.write(f"**Jumlah data:** {len(data)}")
                        st.dataframe(data)
                        
                        # Tombol download per kategori
                        csv = data.to_csv(index=False)
                        st.download_button(
                            label=f"📥 Download {title} (CSV)",
                            data=csv,
                            file_name=f"{title.replace(' ', '_')}.csv",
                            mime="text/csv"
                        )
                        st.markdown("---")
                else:
                    st.warning("Belum ada filter yang dijalankan. Klik tombol filter di atas!")
        
        with action_col3:
            if st.button("💾 Copy Semua ke Clipboard", use_container_width=True, type="primary"):
                if st.session_state.results:
                    all_text = ""
                    for title, data in st.session_state.results.items():
                        all_text += f"\n{'='*60}\n"
                        all_text += f"{title}\n"
                        all_text += f"{'='*60}\n"
                        all_text += f"Jumlah: {len(data)}\n\n"
                        all_text += data.to_csv(index=False)
                        all_text += "\n\n"
                    
                    st.code(all_text, language='csv')
                    st.info("📋 Silakan blok semua teks di atas (Ctrl+A) lalu copy (Ctrl+C)")
                else:
                    st.warning("Belum ada hasil filter untuk dicopy!")
        
        # Tampilkan hasil individual
        if st.session_state.results:
            st.markdown("---")
            st.subheader("📁 Hasil Filter per Kategori")
            
            for title, data in st.session_state.results.items():
                with st.expander(f"{title} ({len(data)} data)"):
                    st.dataframe(data)
                    csv = data.to_csv(index=False)
                    st.download_button(
                        label=f"Download {title}",
                        data=csv,
                        file_name=f"{title.replace(' ', '_')}.csv",
                        mime="text/csv"
                    )
    
    except Exception as e:
        st.error(f"Error membaca file: {e}")
        st.info("Pastikan file Anda adalah CSV yang valid")

else:
    # Tampilkan instruksi jika belum upload file
    st.info("👈 Silakan upload file CSV di sebelah kiri untuk memulai")
    
    st.markdown("""
    ### 📖 Panduan Penggunaan:
    
    1. **Upload file CSV** hasil scraping Google Maps
    2. **Pilih kolom** yang sesuai (Website, WhatsApp, Jumlah Ulasan)
    3. **Klik tombol filter** sesuai kebutuhan:
       - Profil dengan/tanpa website
       - Profil dengan WhatsApp
       - Filter berdasarkan jumlah ulasan
    4. **Download** hasil filter dalam format CSV
    5. **Copy** hasil ke clipboard jika diperlukan
    
    ### 📝 Format CSV yang Didukung:
    File CSV harus memiliki kolom seperti:
    - Nama Bisnis, Alamat, Website, WhatsApp, Rating, Jumlah Ulasan, dll.
    """)
