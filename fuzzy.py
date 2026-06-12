import numpy as np
import streamlit as st
import pandas as pd
import math
from datetime import datetime

# Konfigurasi Halaman Utama
st.set_page_config(page_title="Engineering Tools & LPI Report", layout="wide")

# =======================================================================================
# MENU UTAMA APLIKASI
# =======================================================================================
st.sidebar.title("Navigation Menu")
main_menu = st.sidebar.radio("PILIH MODUL APLIKASI:", ["LIQUID PENETRANT REPORT", "CONSUMABLE CALCULATE"])

st.sidebar.markdown("---")
st.sidebar.info("Aplikasi Integrasi: LPI Generator & Volume Cutting/Welding/Coating Calculator.")

# =======================================================================================
# MODUL 1: LIQUID PENETRANT INSPECTION (LPI) REPORT GENERATOR
# =======================================================================================
if main_menu == "LIQUID PENETRANT REPORT":
    st.title("📋 Liquid Penetrant Inspection Report Generator")
    st.write("Aplikasi untuk men-generate report hasil pengujian Liquid Penetrant secara otomatis.")

    # -----------------------------------------------------------------------------------
    # FITUR INPUT KOP LOGO PERUSAHAAN
    # -----------------------------------------------------------------------------------
    st.subheader("Logo Perusahaan (Kop Surat)")
    uploaded_logo = st.file_uploader("Unggah Logo untuk Kop Report (Format: PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])
    
    if uploaded_logo is not None:
        st.image(uploaded_logo, width=200, caption="Preview Logo Kop Surat")
    else:
        st.info("💡 Anda belum mengunggah logo. Cetakan report akan menggunakan teks standar tanpa logo.")

    st.markdown("---")

    # Otomatisasi Form Number & Tanggal berdasarkan waktu berjalan
    current_date = datetime.now()
    date_str = current_date.strftime("%d %B %Y").upper() 
    month_year_slug = current_date.strftime("%B/%Y").upper() 
    auto_form_no = f"05/LPI/DAMAC/{month_year_slug}" # Sesuai format dokumen asli 

    st.subheader("Header Information")
    col1, col2, col3 = st.columns(3)

    with col1:
        client = st.text_input("Client", value="PT. TRAKINDO UTAMA")
        project = st.text_input("Project", value="DAMAC DIGITAL JKT01 DAY 2")
        equipment = st.text_input("Equipment / System", value="FUEL PIPE") # Diisi manual oleh user 

    with col2:
        st.text_input("Form No (Otomatis)", value=auto_form_no, disabled=True)
        st.text_input("Date (Otomatis)", value=date_str, disabled=True)
        drawing_no = st.text_input("Drawing No", value="ISO-JKT01-003") # Diisi manual oleh user 

    with col3:
        standard = st.text_input("Standard", value="ASME B31.3")
        description = st.text_input("Description", value="TYPE 1")

    st.markdown("---")
    st.subheader("Inspection Parameters")
    col_p1, col_p2, col_p3 = st.columns(3)

    with col_p1:
        penetrant_method = st.radio("Penetrant Method", ["VISIBLE", "FLUORECENT"], index=0)
        removal_method = st.radio("Removal Method", ["SOLVENT REMOVABLE", "WATER WASHABLE", "POST EMULSIFIEBLE"], index=0)

    with col_p2:
        brand_name = st.text_input("Brand Name", value="MAGNAFLUX")
        penetrant_type = st.text_input("Penetrant Code", value="SPL-SP2")
        developer_type = st.text_input("Developer Code", value="SKD-S2")
        cleaner_type = st.text_input("Cleaner Code", value="SKC-S")

    with col_p3:
        surface_prep = st.radio("Surface Preparation", ["AS WELDED", "MACHINING", "GRINDING", "OTHER"], index=0)
        time_exam = st.radio("Time of Examination", ["AFTER WELDING", "AFTER HYDROTEST", "AFTER PWHT", "OTHER"], index=0)
        scope_exam = st.radio("Scope of Examination", ["BASE METAL", "WELD METAL", "BACK CHIPPING", "OTHER"], index=1)

    st.markdown("---")
    st.subheader("Weld Inspection Results Data")

    # Inisialisasi session state untuk menampung tabel data pengujian las jika belum ada
    if 'weld_data' not in st.session_state:
        st.session_state.weld_data = pd.DataFrame([
            {"PART NAME": "PIPE – FLANGE", "WELD NO": "1", "THICKNESS (MM)": 3.91, "RESULT": "ACC", "TYPES OF DISCONTINUITIES": "-", "REMARKS": "-"},
            {"PART NAME": "PIPE – ELBOW", "WELD NO": "2", "THICKNESS (MM)": 3.91, "RESULT": "ACC", "TYPES OF DISCONTINUITIES": "-", "REMARKS": "-"},
            {"PART NAME": "PIPE – EQUAL TEE", "WELD NO": "6", "THICKNESS (MM)": 3.91, "RESULT": "ACC", "TYPES OF DISCONTINUITIES": "-", "REMARKS": "-"}
        ])

    with st.expander("➕ Tambah Baris Hasil Las Baru"):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            new_part = st.selectbox("Part Name", ["PIPE – FLANGE", "PIPE – ELBOW", "PIPE – EQUAL TEE"])
        with c2:
            new_weld_no = st.text_input("Weld No", value="3")
        with c3:
            new_thickness = st.number_input("Thickness (mm)", value=3.91, step=0.01)
        with c4:
            new_result = st.selectbox("Result", ["ACC", "REJECT"])
            
        if st.button("Masukkan ke Tabel"):
            new_row = {
                "PART NAME": new_part, "WELD NO": new_weld_no, "THICKNESS (MM)": new_thickness,
                "RESULT": new_result, "TYPES OF DISCONTINUITIES": "-", "REMARKS": "-"
            }
            st.session_state.weld_data = pd.concat([st.session_state.weld_data, pd.DataFrame([new_row])], ignore_index=True)
            st.success("Data baru berhasil ditambahkan ke tabel!")

    # Menggunakan st.data_editor agar user bisa memodifikasi cell layaknya excel spreadsheet
    edited_weld_df = st.data_editor(st.session_state.weld_data, num_rows="dynamic", use_container_width=True)

    st.markdown("---")
    
    # Tombol Aksi Cetak Report Hasil Pengujian
    if st.button("🚀 Generate Final Report Layout"):
        st.markdown("## 📄 FINAL LIQUID PENETRANT INSPECTION REPORT")
        
        # Tampilkan logo perusahaan di bagian atas kop surat jika file diunggah
        if uploaded_logo is not None:
            st.image(uploaded_logo, width=180)
            st.markdown("<br>", unsafe_allow_html=True)
        
        header_summary = pd.DataFrame({
            "FIELD A": ["CLIENT", "PROJECT", "EQUIPMENT / SYSTEM", "DRAWING NO", "STANDARD / DESC"],
            "VALUE A": [client, project, equipment, drawing_no, f"{standard} / {description}"],
            "FIELD B": ["FORM NO", "DATE", "PENETRANT METHOD", "REMOVAL METHOD", "BRAND & MATERIALS"],
            "VALUE B": [auto_form_no, date_str, f"☑ {penetrant_method}", f"☑ {removal_method}", f"{brand_name} ({penetrant_type}/{developer_type})"]
        })
        st.table(header_summary)
        
        st.write(f"**Surface Prep:** ☑ {surface_prep} | **Time of Exam:** ☑ {time_exam} | **Scope:** ☑ {scope_exam}")
        st.write("#### Inspection Results Table")
        
        display_df = edited_weld_df.copy()
        display_df["ACC"] = display_df["RESULT"].apply(lambda x: "☑" if x == "ACC" else "☐")
        display_df["REJECT"] = display_df["RESULT"].apply(lambda x: "☑" if x == "REJECT" else "☐")
        
        display_df = display_df[["PART NAME", "WELD NO", "THICKNESS (MM)", "ACC", "REJECT", "TYPES OF DISCONTINUITIES", "REMARKS"]]
        st.dataframe(display_df, use_container_width=True)
        
        st.write("#### Signatures")
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            st.write("**CHECKED BY**")
            st.write("\n\n\n__________________")
            st.write("Name:")
        with col_f2:
            st.write("**REVIEWED BY**")
            st.write("\n\n\n__________________")
            st.write("Name:")
        with col_f3:
            st.write("**WITNESSED BY**")
            st.write("\n\n\n__________________")
            st.write("Name:")
