import streamlit as st
import pandas as pd
import joblib
import os
import base64

# ==========================
# Fungsi untuk background
# ==========================
import base64, os
def set_background(image_path, header_image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            encoded_bg = base64.b64encode(image_file.read()).decode()

        header_encoded = ""
        if os.path.exists(header_image_path):
            with open(header_image_path, "rb") as header_file:
                header_encoded = base64.b64encode(header_file.read()).decode()

        page_bg = f"""
        <style>
        /* =========================
        LATAR BELAKANG HALAMAN
        =========================*/
        [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/png;base64,{encoded_bg}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
            background-color: #F4F4F4;
        }}

        /* =========================
        HEADER DENGAN PNG TRANSPARAN & MENEMPEL KE ATAS
        =========================*/

        /* Hilangkan toolbar dan semua jarak di atas */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], .main {{
            margin: 0 !important;
            padding: 0 !important;
            top: 0 !important;
        }}

        [data-testid="stToolbar"] {{
            display: none !important; /* Hilangkan toolbar Streamlit */
        }}

        header[data-testid="stHeader"] {{
            background: transparent !important;
            height: 110px !important;
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100% !important;
            border: none !important;
            box-shadow: none !important;
            margin: 0 !important;
            padding: 0 !important;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999 !important;
        }}

        header[data-testid="stHeader"]::before {{
            content: "";
            position: absolute;
            top: 0 !important;
            left: 0 !important;
            right: 0 !important;
            bottom: 0 !important;
            background-image: url("data:image/png;base64,{header_encoded}");
            background-repeat: no-repeat;
            background-position: top center;
            background-size: contain;
            z-index: 0;
        }}

        header[data-testid="stHeader"] * {{
            position: relative;
            z-index: 1;
        }}

        /* Hapus padding dari container utama agar konten tidak terdorong ke bawah */
        .block-container {{
            padding-top: 120px !important; /* beri jarak biar konten ga ketimpa */
        }}

        /* =========================
        FONT FORMAL SELURUH APLIKASI
        =========================*/
        html, body, .main, .block-container, h1, h2, h3, h4, h5, h6, p, label, span, td, th, input, select, textarea, button {{
            font-family: "Roboto", "Helvetica", "Arial", sans-serif !important;
            color: #003366 !important;
        }}

        /* Judul */
        h1, h2, h3, h4, h5, h6 {{
            font-weight: 700 !important;
        }}

        /* Paragraf & label */
        p, label, span {{
            font-weight: 400 !important;
            font-size: 14px !important;
            line-height: 1.5 !important;
            color: #004080 !important;
        }}

        /* Tabel */
        .stDataFrame td, .stDataFrame th {{
            font-size: 13px !important;
            color: white !important;
        }}

        /* Tombol */
        .stButton > button {{
            font-family: "Roboto", "Helvetica", "Arial", sans-serif !important;
            font-weight: 600 !important;
            background-color: #00A2B9 !important;
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
            transition: all 0.2s ease-in-out;
        }}
        .stButton > button:hover {{
            background-color: #0E5A71 !important;
            transform: scale(1.05);
        }}

        /* Form input */
        input, select, textarea {{
            font-family: "Roboto", "Helvetica", "Arial", sans-serif !important;
            font-size: 14px !important;
        }}

        /* Tooltip / info */
        .stInfo, .stWarning, .stError, .stSuccess {{
            font-family: "Roboto", "Helvetica", "Arial", sans-serif !important;
        }}

        html {{
            background-color: transparent !important;
        }}
        </style>
        

        """
        st.markdown(page_bg, unsafe_allow_html=True)
    else: 
        st.warning("⚠️ Background image tidak ditemukan!")


# ==========================
# Konfigurasi halaman
# ==========================
st.set_page_config(page_title="Prisma AI", layout="centered")
set_background("background.png", "HEADER.png")

st.markdown("""
<style>
/* === Form Input Putih === */
input[type="text"],
input[type="number"],
input[type="email"],
input[type="password"],
textarea,
select {
    background-color: white !important;
    color: #003366 !important;
    border: 1px solid #cccccc !important;
    border-radius: 6px !important;
    box-shadow: none !important;
}

input[type="text"]:focus,
input[type="number"]:focus,
textarea:focus,
select:focus {
    background-color: white !important;
    border-color: #00A8B8 !important;
    box-shadow: 0 0 5px rgba(0,168,184,0.4);
    outline: none !important;
}

/* === File Uploader Putih === */
div[data-testid="stFileUploader"] > section {
    background-color: white !important;
    border: 1px solid #cccccc !important;
    border-radius: 8px !important;
}
div[data-testid="stFileUploaderDropzone"] {
    background-color: white !important;
    border: 2px dashed #cccccc !important;
    border-radius: 8px !important;
}
div[data-testid="stFileUploaderDropzone"] p {
    color: #003366 !important;
}

/* === Label & Selectbox === */
label, .st-emotion-cache-9ycgxx, .st-emotion-cache-1kyxreq {
    color: #003366 !important;
}
.stSelectbox [data-baseweb="select"] > div {
    background-color: white !important;
    color: #003366 !important;
}

/* === Tabel Putih (baik st.table maupun st.dataframe) === */
.dataframe, table, .stDataFrame {
    background-color: white !important;
    color: #003366 !important;
    border: 1px solid #cccccc !important;
    border-radius: 8px !important;
}

.dataframe th, .dataframe td, table th, table td {
    background-color: white !important;
    color: #003366 !important;
    border: 1px solid #cccccc !important;
    padding: 6px 10px !important;
    text-align: left !important;
}

/* Header tabel sedikit abu lembut */
.dataframe thead th, table thead th {
    background-color: #f4f6fa !important;
    color: #003366 !important;
    font-weight: bold !important;
}

/* Patch tambahan untuk Streamlit 1.38+ */
div[data-testid="stTable"] {
    background-color: white !important;
    color: #003366 !important;
    border-radius: 8px !important;
}
div[data-testid="stDataFrame"] {
    background-color: white !important;
    color: #003366 !important;
}

/* Hapus efek gelap global di tabel */
.st-emotion-cache-1yycg88, .st-emotion-cache-1v0mbdj, .st-emotion-cache-1inwz65 {
    background-color: white !important;
    color: #003366 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* === PATCH TOTAL: Putihkan semua jenis tabel di Streamlit === */

/* st.table klasik */
.dataframe, table {
    background-color: white !important;
    color: #003366 !important;
    border: 1px solid #cccccc !important;
    border-radius: 8px !important;
}

.dataframe th, .dataframe td, table th, table td {
    background-color: white !important;
    color: #003366 !important;
    border: 1px solid #cccccc !important;
}

/* st.dataframe modern (React grid) */
div[data-testid="stDataFrame"] {
    background-color: white !important;
    color: #003366 !important;
    border-radius: 8px !important;
}

div[data-testid="stDataFrame"] div[role="gridcell"],
div[data-testid="stDataFrame"] div[role="columnheader"] {
    background-color: white !important;
    color: #003366 !important;
    border: 1px solid #cccccc !important;
    font-size: 13px !important;
    text-align: left !important;
}

div[data-testid="stDataFrame"] div[role="row"]:nth-child(even) div[role="gridcell"] {
    background-color: #f8f9fa !important; /* baris genap sedikit abu */
}

div[data-testid="stDataFrame"] div[role="row"]:hover div[role="gridcell"] {
    background-color: #eaf6ff !important; /* hover biru lembut */
}

div[data-testid="stTable"] {
    background-color: white !important;
    color: #003366 !important;
    border-radius: 8px !important;
}

/* hapus background gelap dari wrapper dataframe */
.st-emotion-cache-1yycg88,
.st-emotion-cache-1v0mbdj,
.st-emotion-cache-1inwz65,
.st-emotion-cache-1jicfl2,
.st-emotion-cache-1wmy9hl {
    background-color: white !important;
    color: #003366 !important;
}

/* border lembut di sekitar frame dataframe */
div[data-testid="stVerticalBlock"] div[role="region"] {
    background-color: white !important;
    border: 1px solid #cccccc !important;
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* ==== TOMBOL PREDIKSI CLUSTER ==== */
div[data-testid="stFormSubmitButton"] button {
    background-color: #00A8B8 !important;   /* Biru utama */
    color: #FFFFFF !important;               /* Font putih */
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 26px !important;
    font-size: 16px !important;
    text-align: center !important;
    transition: all 0.25s ease-in-out;
    box-shadow: 0px 4px 10px rgba(0, 122, 204, 0.4);
}

/* Hover efek */
div[data-testid="stFormSubmitButton"] button:hover {
    background-color: #00A8B8 !important;
    color: #FFFFFF !important;               /* tetap putih saat hover */
    transform: scale(1.05);
    box-shadow: 0px 6px 14px rgba(0, 90, 153, 0.5);
}

/* Paksa seluruh elemen dalam tombol tetap putih */
div[data-testid="stFormSubmitButton"] button * {
    color: #FFFFFF !important;
}
            
</style>
            
""", unsafe_allow_html=True)

st.title("PRISMA AI: Customer Priority Profiling at PLN UP3 Surabaya Barat")

# ==========================
# SEARCHING TUNGGAL PADA KEDUA TABEL (DIPINDAH KE ATAS)
# ==========================

st.markdown("---")
st.subheader("Cari Hasil Prediksi Berdasarkan NAMA / IDPEL")

# Input kata kunci
search_text = st.text_input("Masukkan NAMA atau IDPEL lalu tekan ENTER untuk mencari")

# Jalankan pencarian otomatis ketika user menekan Enter (input terisi)
if search_text:
    # Pastikan data CSV sudah tersedia
    df = st.session_state.get("df", pd.DataFrame())
    uploaded_file = st.session_state.get("uploaded_file", None)

    # Filter hasil prediksi CSV
    if uploaded_file and not df.empty and 'idpel' in df.columns and 'nama' in df.columns:
        df_csv_filtered = df[
            df['idpel'].astype(str).str.contains(search_text, case=False) |
            df['nama'].astype(str).str.contains(search_text, case=False)
        ]
    else:
        df_csv_filtered = pd.DataFrame()

    # Filter hasil prediksi manual
    if 'tabel_hasil' in st.session_state and not st.session_state.tabel_hasil.empty:
        df_manual_filtered = st.session_state.tabel_hasil[
            st.session_state.tabel_hasil['idpel'].astype(str).str.contains(search_text, case=False) |
            st.session_state.tabel_hasil['nama'].astype(str).str.contains(search_text, case=False)
        ]
    else:
        df_manual_filtered = pd.DataFrame()

    # Gabungkan hasil
    df_all_filtered = pd.concat([df_csv_filtered, df_manual_filtered], ignore_index=True)

    # Tampilkan hasil
    st.write("Hasil Prediksi :")
    if not df_all_filtered.empty:
        st.dataframe(df_all_filtered)
        # Tombol unduh hasil
        csv_all_filtered = df_all_filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Unduh Hasil Prediksi (Filtered)",
            data=csv_all_filtered,
            file_name="hasil_prediksi_filtered.csv",
            mime="text/csv"
        )
    else:
        st.warning("Tidak ada data yang sesuai dengan pencarian Anda.")

# ==========================
# Upload CSV dan Prediksi Otomatis
# ==========================
uploaded_file = st.file_uploader("Unggah file CSV untuk diprediksi", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.session_state.df = df
        st.session_state.uploaded_file = uploaded_file


        model_path = "Random_Forest_model.pkl"
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            #st.success("Model Random Forest berhasil dimuat.")
        else:
            st.error("❌ File model 'Random_Forest_model.pkl' tidak ditemukan di folder ini.")
            st.stop()

        fitur = ['beban_penyulang', 'jn']
        if not all(f in df.columns for f in fitur):
            st.error("❌ Kolom 'beban_penyulang' dan 'jn' tidak ditemukan di CSV.")
            st.write("Kolom yang tersedia:", df.columns.tolist())
        else:
            with st.spinner("🔄 Sedang memproses prediksi otomatis..."):
                X = df[fitur]
                y_pred = model.predict(X)
                df['Hasil_Prediksi'] = y_pred

            st.success("Prediksi otomatis berhasil dilakukan!")
            st.write("Hasil Prediksi:")
            st.dataframe(df)  # tampilkan seluruh hasil prediksi

            # Tombol unduh hasil
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Unduh Hasil Prediksi CSV",
                data=csv,
                file_name="prediksi_Prisma_AI.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error("⚠️ Terjadi kesalahan saat memproses file:")
        st.exception(e)

else:
    st.info("Silakan unggah file CSV terlebih dahulu untuk melakukan klasifikasi otomatis.")
import streamlit as st
import pandas as pd

# ==========================
# Data Dictionary penyulang & rata_rata
# ==========================
data_dict = {
    'SSG 2': 126, 'SSG 1': 119, 'Ngasinan': 115, 'SPK': 99, 'Kelopo Sepuluh': 181,
    'Jatisuma': 204, 'Jemundo': 48, 'Gilang': 142, 'Beringin Bendo': 67,
    'Garuda Food': 14, 'Santos': 96, 'Sambibulu': 103, 'Anggaswangi': 129,
    'Sambungrejo': 115, 'Pondok Jati': 174, 'Plumbungan': 201, 'Tawangsari': 28,
    'Kemendung': 100, 'Iwatani': 4, 'Semeru': 58, 'Merapi': 149, 'Kedawung': 65,
    'PDAM': 64, 'Samator 02': 126, 'Rinjani': 109, 'Puncak Jaya': 202, 'Antares': 82,
    'Himalaya': 153, 'Everest': 147, 'Bukit Bambe': 70, 'Ngambar': 69,
    'Bulu Pinggir': 77, 'Rusun': 89, 'Gunungsari Indah': 148, 'Evertex': 30,
    'Cangkir': 169, 'Wing Surya': 76, 'Segoro Mulyo': 41, 'Boboh': 124,
    'Cahaya Baru': 154, 'Jeruk': 147, 'Mekabox': 80, 'Waru Gunung': 54,
    'GH Kebraon': 156, 'CBD': 87, 'Wiyung': 48, 'Kedurus': 175, 'Marinir': 69,
    'Sumur Welut': 144, 'Kemlaten': 67, 'Balekambang': 39, 'Lembah Harapan': 171,
    'Kotabaru': 79, 'Randegansari': 78, 'Domas': 108, 'Bringkang': 178,
    'Kesamben': 46, 'Banjar Anyar': 49, 'Samator 01': 62, 'Timur Megah': 144,
    'Diamond': 5, 'Mulung': 96, 'Guwo': 40, 'Annur': 90, 'Sumput Asri': 91,
    'Sambalan': 58, 'Purnomo Sejati 2': 66, 'UPB 2': 6, 'Wonocolo': 92,
    'Kalijaten': 146, 'Trosobo': 80, 'Kramayudha': 94, 'Pagesangan': 194,
    'Suparma 2': 72, 'Suparma 1': 175, 'Proteina': 159, 'Platinum 2': 81,
    'Platinum 1': 80, 'Kalibader': 22, 'Purnomo Sejati 1': 161
}

# Konversi key jadi list untuk selectbox
penyulang_list = sorted(list(data_dict.keys()))

# === Input Manual Dinamis dengan Simpan ke Tabel ===
st.markdown("---")
st.subheader("Input Data Manual")
st.write("Masukkan data pelanggan secara manual untuk diprediksi tanpa mengunggah CSV.")

# Inisialisasi session_state untuk tabel hasil prediksi
if "tabel_hasil" not in st.session_state:
    st.session_state.tabel_hasil = pd.DataFrame(
        columns=["idpel", "nama", "penyulang", "beban_penyulang", "jn", "Hasil_Prediksi"]
    )

# === Pilih penyulang ===
penyulang = st.selectbox("Pilih PENYULANG", penyulang_list, key="penyulang_select")

# Ambil nilai rata-rata dari dictionary
if penyulang:
    st.session_state.rata_rata_value = data_dict.get(penyulang)
else:
    st.session_state.rata_rata_value = None

# Tampilkan info rata-rata
if st.session_state.rata_rata_value is not None:
    st.info(f"Rata-rata beban untuk **{penyulang}**: {st.session_state.rata_rata_value}")
else:
    st.warning("⚠️ Nilai rata-rata belum tersedia, pilih penyulang terlebih dahulu.")

# === Form input lainnya ===
with st.form("form_prediksi", clear_on_submit=True):
    idpel = st.text_input("ID_PELANGGAN")
    nama = st.text_input("NAMA")
    alamat  = st.text_input("ALAMAT")
    keperuntukan = st.text_input("KEPERUNTUKAN")
    jenis_industri = st.text_input("JENIS INDUSTRI")
    unitup = st.text_input("UNITUP")
    tarif =st.text_input("TARIF")
    daya = st.text_input("DAYA")
    
    # Ambil rata-rata dari session_state
    rata_rata_value = st.session_state.get("rata_rata_value", None)
    
    jn = st.text_input("JN (gunakan koma, tanpa titik)")

    # Tombol submit (Prediksi)
    submitted = st.form_submit_button("Prediksi Cluster")

# Jika tombol ditekan → lakukan prediksi
if submitted:
    model_path = "Random_Forest_model.pkl"
    if not os.path.exists(model_path):
        st.error("❌ File model 'Random_Forest_model.pkl' tidak ditemukan di folder ini.")
    else:
        try:
            # Load model dengan try-except
            try:
                model = joblib.load(model_path)
                st.success("Model Random Forest berhasil dimuat untuk prediksi manual.")
            except Exception as e:
                st.error("⚠️ Terjadi kesalahan saat memuat model:")
                st.exception(e)
                st.stop()  # hentikan jika model gagal dimuat

            if rata_rata_value is None:
                st.error("⚠️ Nilai rata-rata beban tidak ditemukan.")
            else:
                try:
                    # Konversi input ke float
                    beban_float = float(str(rata_rata_value).replace(",", "."))
                    jn_float = float(jn.replace(",", "."))
                except ValueError:
                    st.error("⚠️ Pastikan input angka valid (gunakan koma untuk desimal).")
                    st.stop()

                try:
                    # Siapkan data input
                    # Siapkan data input
                    input_data = pd.DataFrame({
                        "idpel": [idpel],
                        "nama": [nama],
                        "alamat": [alamat],
                        "keperuntukan": [keperuntukan],
                        "jenis_industri": [jenis_industri],
                        "unitup": [unitup],
                        "tarif": [tarif],
                        "daya": [daya],
                        "penyulang": [penyulang],
                        "beban_penyulang": [beban_float],
                        "jn": [jn_float]
                    })

                    # Prediksi
                    X = input_data[["beban_penyulang", "jn"]]
                    hasil_pred = model.predict(X)
                    input_data["Hasil_Prediksi"] = hasil_pred

                    # Tambahkan hasil ke tabel session_state
                    st.session_state.tabel_hasil = pd.concat(
                        [st.session_state.tabel_hasil, input_data],
                        ignore_index=True
                    )

                    # Tampilkan hasil prediksi
                    st.success(f"Prediksi berhasil! Priority Blok: **{hasil_pred[0]}**")

                except Exception as e:
                    st.error("⚠️ Terjadi kesalahan saat melakukan prediksi:")
                    st.exception(e)

        except Exception as e:
            st.error("⚠️ Terjadi kesalahan umum:")
            st.exception(e)

# Tampilkan tabel hasil prediksi manual
if not st.session_state.tabel_hasil.empty:
    st.markdown("---")
    st.subheader("Tabel Hasil Prediksi Manual")
    st.dataframe(st.session_state.tabel_hasil)

    # Tombol unduh semua hasil
    csv_data = st.session_state.tabel_hasil.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Unduh Semua Hasil Manual",
        data=csv_data,
        file_name="hasil_prediksi_manual.csv",
        mime="text/csv"
    )

# atur suara dan prioritas#
from gtts import gTTS
import io

# ==========================
# GABUNGKAN DATA DARI UPLOAD CSV & INPUT MANUAL
# ==========================
if "tabel_hasil" not in st.session_state:
    st.session_state.tabel_hasil = pd.DataFrame()

if "df" not in st.session_state:
    df = pd.DataFrame()
else:
    df = st.session_state.df

uploaded_file = st.session_state.get("uploaded_file", None)

# Gabungkan data CSV + manual (tanpa upload ulang)
if uploaded_file and not df.empty:
    df_combined = pd.concat([df, st.session_state.tabel_hasil], ignore_index=True)
elif not st.session_state.tabel_hasil.empty:
    df_combined = st.session_state.tabel_hasil.copy()
else:
    df_combined = pd.DataFrame()

# ==========================
# ATUR SUARA DAN PRIORITAS (DENGAN LOGIKA TOGGLE BUTTON)
# ==========================
from gtts import gTTS
import io
import base64
import random
import streamlit as st
import pandas as pd

# ==========================
# CSS tombol prioritas (warna ijo)
# ==========================
st.markdown("""
<style>
button[kind="secondary"] {
    border-radius: 10px !important;
    background-color: #00A8B8 !important;
    color: white !important;
    font-weight: bold !important;
    border: none !important;
    margin: 4px !important;
    transition: all 0.2s ease-in-out;
}
button[kind="secondary"] * {
    color: white !important;
}
button[kind="secondary"]:hover {
    background-color: #00A8B8 !important;
    transform: scale(1.05);
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================
# GABUNGKAN DATA DARI UPLOAD CSV & INPUT MANUAL
# ==========================
if "tabel_hasil" not in st.session_state:
    st.session_state.tabel_hasil = pd.DataFrame()

if "df" not in st.session_state:
    df = pd.DataFrame()
else:
    df = st.session_state.df

uploaded_file = st.session_state.get("uploaded_file", None)

# Gabungkan data CSV + manual (tanpa upload ulang)
if uploaded_file and not df.empty:
    df_combined = pd.concat([df, st.session_state.tabel_hasil], ignore_index=True)
elif not st.session_state.tabel_hasil.empty:
    df_combined = st.session_state.tabel_hasil.copy()
else:
    df_combined = pd.DataFrame()

# ==========================
# HAPUS DATA OTOMATIS JIKA FILE CSV DITUTUP
# ==========================
if uploaded_file is None and 'df_combined' in st.session_state:
    del st.session_state['df_combined']


#simpan ke df baru#
if not df_combined.empty and 'Hasil_Prediksi' in df_combined.columns:
    df_baru = df_combined.copy()  # Simpan otomatis di backend
    prioritas_list = sorted(df_combined['Hasil_Prediksi'].dropna().unique().tolist())
    # lanjutkan proses lain tanpa menampilkan df_baru
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# ==========================
# Pastikan df_combined selalu ada
# ==========================
if "tabel_hasil" not in st.session_state:
    st.session_state.tabel_hasil = pd.DataFrame()

if "df" not in st.session_state:
    df = pd.DataFrame()
else:
    df = st.session_state.df

uploaded_file = st.session_state.get("uploaded_file", None)

# Gabungkan data CSV + manual (tanpa upload ulang)
if uploaded_file and not df.empty:
    df_combined = pd.concat([df, st.session_state.tabel_hasil], ignore_index=True)
elif not st.session_state.tabel_hasil.empty:
    df_combined = st.session_state.tabel_hasil.copy()
else:
    df_combined = pd.DataFrame()

# ==========================
# Buat df_baru hanya jika data ada
# ==========================
df_baru = pd.DataFrame()
if not df_combined.empty and 'Hasil_Prediksi' in df_combined.columns:
    df_baru = df_combined.copy()
    prioritas_list = sorted(df_baru['Hasil_Prediksi'].dropna().unique().tolist())

# ==========================
# Plot blok prioritas hanya jika df_baru ada
# ==========================
required_cols = ["jn", "beban_penyulang"]
if not df_baru.empty and all(col in df_baru.columns for col in required_cols):

    # Bersihkan data & konversi
    df_baru = df_baru.dropna(subset=required_cols)
    df_baru["jn"] = df_baru["jn"].astype(str).str.replace(",", "").astype(float)
    df_baru["beban_penyulang"] = df_baru["beban_penyulang"].astype(str).str.replace(",", "").astype(float)

    # Range & blok
    range_x, range_y = 390, 720
    blok_x, blok_y = range_x / 3, range_y / 3
    x_edges = [0, blok_x, blok_x*2, range_x]
    y_edges = [0, blok_y, blok_y*2, range_y]

    blok_matrix = np.array([
        [6, 8, 9],
        [3, 5, 7],
        [1, 2, 4]
    ])

    def get_block(x, y):
        col = int(x // blok_x)
        row = int(y // blok_y)
        col = min(max(col, 0), 2)
        row = min(max(row, 0), 2)
        return blok_matrix[row, col]

    df_baru["blok"] = df_baru.apply(lambda r: get_block(r["beban_penyulang"], r["jn"]), axis=1)

    # Plot
    fig, ax = plt.subplots(figsize=(8, 6))
    for x in x_edges: ax.axvline(x=x, color='black', linewidth=1)
    for y in y_edges: ax.axhline(y=y, color='black', linewidth=1)

    for i in range(3):
        for j in range(3):
            x_center = x_edges[j] + blok_x / 2
            y_center = y_edges[i] + blok_y / 2
            ax.text(x_center, y_center, str(blok_matrix[i][j]),
                    ha='center', va='center', fontsize=16, fontweight='bold', color='gray')

    unique_blocks = sorted(df_baru["blok"].unique())
    colors = plt.cm.Set3(np.linspace(0, 1, len(unique_blocks)))

    for block, color in zip(unique_blocks, colors):
        subset = df_baru[df_baru["blok"] == block]
        ax.scatter(subset["beban_penyulang"], subset["jn"], color=color, alpha=0.8, s=60, label=f"Blok {block}")

    ax.set_xlim(0, range_x)
    ax.set_ylim(0, range_y)
    ax.set_xlabel("Beban Penyulang (X)")
    ax.set_ylabel("JN (Y)")
    ax.set_title("Tabel Prioritas Probing Scoring")
    ax.invert_xaxis()
    ax.set_xticks(x_edges)
    ax.set_yticks(y_edges)
    ax.legend(title="Blok", bbox_to_anchor=(1.05, 1), loc='upper left')

    st.pyplot(fig)
else:
    st.info("Belum ada data untuk menampilkan plot blok prioritas.")


# ==========================
# FILTER BERDASARKAN PRIORITAS (DENGAN TOGGLE)
# ==========================
# ==========================
# CSS tombol prioritas
# ==========================
st.markdown("---")
st.subheader("Filter Berdasarkan Prioritas")
st.markdown("""
<style>
button[kind="secondary"] {
    border-radius: 10px !important;
    background-color: #00A8B8 !important;
    color: white !important;
    font-weight: bold !important;
    border: none !important;
    margin: 4px !important;
    transition: all 0.2s ease-in-out;
}
button[kind="secondary"] * {
    color: white !important;
}
button[kind="secondary"]:hover {
    background-color: #00A8B8 !important;
    transform: scale(1.05);
    color: white !important;
}
</style>
""", unsafe_allow_html=True)


if not df_combined.empty and 'Hasil_Prediksi' in df_combined.columns:
    prioritas_list = sorted(df_combined['Hasil_Prediksi'].dropna().unique().tolist())

    st.write("Klik tombol untuk menampilkan data berdasarkan prioritas:")
    col_buttons = st.columns(len(prioritas_list))

    # Simpan status toggle di session_state
    if "tombol_aktif" not in st.session_state:
        st.session_state.tombol_aktif = None

    for i, prio in enumerate(prioritas_list):
        if col_buttons[i].button(f"P. {prio}"):
            # Toggle logika
            if st.session_state.tombol_aktif == prio:
                st.session_state.tombol_aktif = None  # klik lagi → tutup
            else:
                st.session_state.tombol_aktif = prio  # klik baru → buka

    # ==========================
    # TAMPILKAN DATA SESUAI TOMBOL YANG AKTIF
    # ==========================
    if st.session_state.tombol_aktif is not None:
        prio = st.session_state.tombol_aktif
        df_filtered_prio = df_combined[df_combined['Hasil_Prediksi'] == prio]

        st.write(f"### Hasil Prediksi Prioritas {prio}:")
        st.dataframe(df_filtered_prio)

        # ==========================
        # BUAT TEKS UNTUK DIBACAKAN (VERSI JUMLAH BLOK)
        # ==========================
        jumlah_data = len(df_filtered_prio)

        if jumlah_data == 0:
            combined_text = f"Tidak ada pelanggan dengan prioritas {prio}."
        elif jumlah_data == 1:
            combined_text = f"Terdapat satu pelanggan dengan prioritas {prio}."
        else:
            combined_text = f"Terdapat {jumlah_data} pelanggan dengan prioritas {prio}."

        # ==========================
        # KONVERSI TEKS KE SUARA
        # ==========================
        tts = gTTS(text=combined_text, lang='id')
        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)

        # ==========================
        # PUTAR AUDIO OTOMATIS SETIAP GANTI PRIORITAS
        # ==========================
        audio_base64 = base64.b64encode(audio_bytes.read()).decode()
        random_key = random.randint(0, 999999)

        audio_tag = f"""
            <audio autoplay key="{random_key}">
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
        """
        st.markdown(audio_tag, unsafe_allow_html=True)

else:
    st.info("Belum ada data untuk menampilkan prioritas.")