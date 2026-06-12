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

    # Otomatisasi Form Number & Tanggal berdasarkan waktu berjalan
    current_date = datetime.now()
    date_str = current_date.strftime("%d %B %Y").upper() 
    month_year_slug = current_date.strftime("%B/%Y").upper() 
    auto_form_no = f"05/LPI/DAMAC/{month_year_slug}" # Sesuai format dokumen asli 

    st.subheader("Header Information")
    col1, col2, col3 = st.columns(3)

    with col1:
        client = st.text_input("Client", value="PT. TRAKINDO UTAMA") [cite: 1]
        project = st.text_input("Project", value="DAMAC DIGITAL JKT01 DAY 2") [cite: 1]
        equipment = st.text_input("Equipment / System", value="FUEL PIPE") # Diisi manual oleh user 

    with col2:
        st.text_input("Form No (Otomatis)", value=auto_form_no, disabled=True) [cite: 1]
        st.text_input("Date (Otomatis)", value=date_str, disabled=True) [cite: 1]
        drawing_no = st.text_input("Drawing No", value="ISO-JKT01-003") # Diisi manual oleh user 

    with col3:
        standard = st.text_input("Standard", value="ASME B31.3") [cite: 1]
        description = st.text_input("Description", value="TYPE 1") [cite: 1]

    st.markdown("---")
    st.subheader("Inspection Parameters")
    col_p1, col_p2, col_p3 = st.columns(3)

    with col_p1:
        penetrant_method = st.radio("Penetrant Method", ["VISIBLE", "FLUORECENT"], index=0) [cite: 1]
        removal_method = st.radio("Removal Method", ["SOLVENT REMOVABLE", "WATER WASHABLE", "POST EMULSIFIEBLE"], index=0) [cite: 1]

    with col_p2:
        brand_name = st.text_input("Brand Name", value="MAGNAFLUX") [cite: 1]
        penetrant_type = st.text_input("Penetrant Code", value="SPL-SP2") [cite: 1]
        developer_type = st.text_input("Developer Code", value="SKD-S2") [cite: 1]
        cleaner_type = st.text_input("Cleaner Code", value="SKC-S") [cite: 1]

    with col_p3:
        surface_prep = st.radio("Surface Preparation", ["AS WELDED", "MACHINING", "GRINDING", "OTHER"], index=0) [cite: 1]
        time_exam = st.radio("Time of Examination", ["AFTER WELDING", "AFTER HYDROTEST", "AFTER PWHT", "OTHER"], index=0) [cite: 1]
        scope_exam = st.radio("Scope of Examination", ["BASE METAL", "WELD METAL", "BACK CHIPPING", "OTHER"], index=1) [cite: 1]

    st.markdown("---")
    st.subheader("Weld Inspection Results Data")

    # Inisialisasi session state untuk menampung tabel data pengujian las jika belum ada [cite: 2]
    if 'weld_data' not in st.session_state:
        st.session_state.weld_data = pd.DataFrame([
            {"PART NAME": "PIPE – FLANGE", "WELD NO": "1", "THICKNESS (MM)": 3.91, "RESULT": "ACC", "TYPES OF DISCONTINUITIES": "-", "REMARKS": "-"}, [cite: 2]
            {"PART NAME": "PIPE – ELBOW", "WELD NO": "2", "THICKNESS (MM)": 3.91, "RESULT": "ACC", "TYPES OF DISCONTINUITIES": "-", "REMARKS": "-"}, [cite: 2]
            {"PART NAME": "PIPE – EQUAL TEE", "WELD NO": "6", "THICKNESS (MM)": 3.91, "RESULT": "ACC", "TYPES OF DISCONTINUITIES": "-", "REMARKS": "-"} [cite: 2]
        ])

    with st.expander("➕ Tambah Baris Hasil Las Baru"):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            new_part = st.selectbox("Part Name", ["PIPE – FLANGE", "PIPE – ELBOW", "PIPE – EQUAL TEE"]) [cite: 2]
        with c2:
            new_weld_no = st.text_input("Weld No", value="3") [cite: 2]
        with c3:
            new_thickness = st.number_input("Thickness (mm)", value=3.91, step=0.01) [cite: 2]
        with c4:
            new_result = st.selectbox("Result", ["ACC", "REJECT"]) [cite: 2]
            
        if st.button("Masukkan ke Tabel"):
            new_row = {
                "PART NAME": new_part, "WELD NO": new_weld_no, "THICKNESS (MM)": new_thickness,
                "RESULT": new_result, "TYPES OF DISCONTINUITIES": "-", "REMARKS": "-"
            }
            st.session_state.weld_data = pd.concat([st.session_state.weld_data, pd.DataFrame([new_row])], ignore_index=True)
            st.success("Data baru berhasil ditambahkan ke tabel!")

    # Menggunakan st.data_editor agar user bisa memodifikasi cell layaknya excel spreadsheet [cite: 2]
    edited_weld_df = st.data_editor(st.session_state.weld_data, num_rows="dynamic", use_container_width=True)

    st.markdown("---")
    
    # Tombol Aksi Cetak Report Hasil Pengujian
    if st.button("🚀 Generate Final Report Layout"):
        st.subheader("📄 PREVIEW LIQUID PENETRANT INSPECTION REPORT") [cite: 1]
        
        header_summary = pd.DataFrame({
            "FIELD A": ["CLIENT", "PROJECT", "EQUIPMENT / SYSTEM", "DRAWING NO", "STANDARD / DESC"], [cite: 1]
            "VALUE A": [client, project, equipment, drawing_no, f"{standard} / {description}"], [cite: 1]
            "FIELD B": ["FORM NO", "DATE", "PENETRANT METHOD", "REMOVAL METHOD", "BRAND & MATERIALS"], [cite: 1]
            "VALUE B": [auto_form_no, date_str, f"☑ {penetrant_method}", f"☑ {removal_method}", f"{brand_name} ({penetrant_type}/{developer_type})"] [cite: 1]
        })
        st.table(header_summary)
        
        st.write(f"**Surface Prep:** ☑ {surface_prep} | **Time of Exam:** ☑ {time_exam} | **Scope:** ☑ {scope_exam}") [cite: 1]
        st.write("#### Inspection Results Table") [cite: 2]
        
        display_df = edited_weld_df.copy()
        display_df["ACC"] = display_df["RESULT"].apply(lambda x: "☑" if x == "ACC" else "☐") [cite: 2]
        display_df["REJECT"] = display_df["RESULT"].apply(lambda x: "☑" if x == "REJECT" else "☐") [cite: 2]
        
        display_df = display_df[["PART NAME", "WELD NO", "THICKNESS (MM)", "ACC", "REJECT", "TYPES OF DISCONTINUITIES", "REMARKS"]] [cite: 2]
        st.dataframe(display_df, use_container_width=True)
        
        st.write("#### Signatures") [cite: 3]
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            st.write("**CHECKED BY**") [cite: 3]
            st.write("\n\n\n__________________")
            st.write("Name:") [cite: 3]
        with col_f2:
            st.write("**REVIEWED BY**") [cite: 3]
            st.write("\n\n\n__________________")
            st.write("Name:") [cite: 3]
        with col_f3:
            st.write("**WITNESSED BY**") [cite: 3]
            st.write("\n\n\n__________________")
            st.write("Name:") [cite: 3]

# =======================================================================================
# MODUL 2: CONSUMABLE CALCULATOR (LOGIKA DARI USER)
# =======================================================================================
elif main_menu == "CONSUMABLE CALCULATE":
    st.title("🧮 Consumable Calculate & Volume Estimation")
    st.write("Hitung volume material yang harus dipotong/di-weld serta estimasi kebutuhan penunjangnya.")

    CCALCULATE = st.selectbox('CONSUMABLE CALCULATE', ['CUTTING DISC','GRINDING DISC', 'FLAP DISC', 'FILLER WELD', 'COATING'])

    if CCALCULATE == 'CUTTING DISC':
        JMATERIAL = st.selectbox('JENIS MATERIAL', ['Pipe','Plate','UNP','WF','H BEAM'])

        if JMATERIAL == 'Pipe':
            NPS = st.selectbox('NPS', [
                '1/4','3/8','1/2','3/4','1','1 1/4','1 1/2','2','2 1/2','3',
                '3 1/2','4','5','6','8','10','12','14','16','18','20','22',
                '24','26','28','30'
            ])
            SCH = st.selectbox('SCH', ['10','20','30','40','60','80'])
            JPOTONG = st.number_input('Jumlah Pipe Dipotong', min_value=0)

            if st.button('HITUNG'):
                KERF = 3  
                data_pipe = {
                    "1/4": {"OD":13.7,"30":10,"40":9.22,"80":7.66},
                    "3/8": {"OD":17.1,"30":13.4,"40":12.48,"80":10.7},
                    "1/2": {"OD":21.3,"10":17.08,"40":15.76,"80":13.84},
                    "3/4": {"OD":26.7,"10":22.48,"40":20.96,"80":18.88},
                    "1": {"OD":33.4,"10":27.86,"40":26.64,"80":24.3},
                    "1 1/4": {"OD":42.2,"10":36.66,"40":35.08,"80":32.5},
                    "1 1/2": {"OD":48.3,"10":42.76,"40":40.94,"80":38.14},
                    "2": {"OD":60.3,"10":54.76,"40":52.48,"80":49.22},
                    "2 1/2": {"OD":73,"10":66.9,"40":62.68,"80":58.98},
                    "3": {"OD":88.9,"10":82.8,"40":77.92,"80":73.66},
                    "4": {"OD":114.3,"10":108.2,"40":102.26,"80":97.18},
                    "5": {"OD":141.3,"40":128.2,"80":122.24},
                    "6": {"OD":168.3,"40":154.08,"80":146.36}
                }

                pipe = data_pipe.get(NPS)
                if pipe and SCH in pipe:
                    OD = pipe["OD"]
                    ID = pipe[SCH]
                    volume_cut = (math.pi/4) * (OD**2 - ID**2) * KERF
                    total_volume = volume_cut * JPOTONG
                    volume_disc = 12280.77
                    kebutuhan_disc = total_volume / volume_disc
                    kebutuhan_disc_bulat = math.ceil(kebutuhan_disc)

                    st.write(f"Total volume potong : {total_volume:,.2f} mm3")
                    st.write(f"Kebutuhan cutting disc : {kebutuhan_disc:,.2f} pcs")
                    st.write(f"Kebutuhan aktual : {kebutuhan_disc_bulat} pcs")
                else:
                    st.warning("Data ukuran pipe tidak tersedia")

    elif CCALCULATE == 'GRINDING DISC':
        JMATERIAL = st.selectbox('JENIS MATERIAL', ['Pipe','Plate'])

        if JMATERIAL == 'Pipe':
            NPS = st.selectbox('NPS', [
                '1/8','1/4','3/8','1/2','3/4','1','1 1/4','1 1/2','2','2 1/2','3',
                '3 1/2','4','5','6','8','10','12'
            ])
            SCH = st.selectbox('SCH', ['10','20','30','40','60','80'])
            JBEVEL = st.number_input('Jumlah Joint yang di-Bevel', min_value=0)

            if st.button('HITUNG'):
                data_pipe = {
                    "1/8":  {"OD": 10.3,  "40": 6.8,   "80": 4.8},
                    "1/4":  {"OD": 13.7,  "40": 9.2,   "80": 7.7},
                    "3/8":  {"OD": 17.1,  "40": 12.5,  "80": 10.7},
                    "1/2":  {"OD": 21.3,  "40": 15.8,  "80": 13.9},
                    "3/4":  {"OD": 26.7,  "40": 21.0,  "80": 18.9},
                    "1":    {"OD": 33.4,  "40": 26.6,  "80": 24.3},
                    "1 1/4": {"OD": 42.2,  "40": 35.1,  "80": 32.5},
                    "1 1/2": {"OD": 48.3,  "40": 40.9,  "80": 38.1},
                    "2":    {"OD": 60.3,  "40": 52.5,  "80": 49.3},
                    "2 1/2": {"OD": 73.0,  "40": 62.7,  "80": 59.0},
                    "3":    {"OD": 88.9,  "40": 77.9,  "80": 73.7},
                    "3 1/2": {"OD": 101.6, "40": 90.1,  "80": 85.4},
                    "4":    {"OD": 114.3, "10": 108.2, "30": 104.7, "40": 102.26, "80": 97.18},
                    "5":    {"OD": 141.3, "40": 128.2, "80": 122.24},
                    "6":    {"OD": 168.3, "40": 154.08, "80": 146.36},
                    "8":    {"OD": 219.1, "10": 211.58, "20": 206.4, "30": 205.02, "40": 202.74, "60": 198.48, "80": 193.7},
                    "10":   {"OD": 273.1, "10": 266.3, "20": 260.3, "30": 257.5, "40": 254.5, "60": 247.7, "80": 242.9},
                    "12":   {"OD": 323.9, "10": 317.5, "20": 311.1, "30": 307.1, "40": 304.8, "60": 298.5, "80": 288.9}
                }

                pipe = data_pipe.get(NPS)
                if pipe and SCH in pipe:
                    OD = pipe["OD"]
                    ID = pipe[SCH]
                    T = (OD - ID) / 2
                    luas_segitiga = 0.5 * (T * math.tan(math.radians(30))) * T
                    keliling_pipa = math.pi * OD
                    volume_bevel = luas_segitiga * keliling_pipa
                    total_volume = volume_bevel * JBEVEL
                    volume_disc = 18626.9

                    kebutuhan_disc = total_volume / volume_disc
                    kebutuhan_disc_bulat = math.ceil(kebutuhan_disc)

                    st.write(f"Total volume bevel : {total_volume:,.2f} mm3")
                    st.write(f"Kebutuhan grinding disc : {kebutuhan_disc:,.2f} pcs")
                    st.write(f"*Kebutuhan aktual : {kebutuhan_disc_bulat} pcs*")
                else:
                    st.warning("Data ukuran pipe tidak tersedia")

    elif CCALCULATE == 'FLAP DISC':
        JMATERIAL = st.selectbox('JENIS MATERIAL', ['Pipe','Plate'])

        if JMATERIAL == 'Pipe':
            NPS = st.selectbox('NPS', [
                '1/8','1/4','3/8','1/2','3/4','1','1 1/4','1 1/2','2','2 1/2','3',
                '3 1/2','4','5','6','8','10','12','14','16','18','20'
            ])
            SCH = st.selectbox('SCH', ['10','20','30','40','60','80'])
            JBUFFING = st.number_input('Jumlah Joint yang di-Buffing', min_value=0)

            if st.button('HITUNG'):
                data_pipe = {
                    "1/8":  {"OD": 10.3,  "40": 6.8,   "80": 4.8},
                    "1/4":  {"OD": 13.7,  "40": 9.2,   "80": 7.7},
                    "3/8":  {"OD": 17.1,  "40": 12.5,  "80": 10.7},
                    "1/2":  {"OD": 21.3,  "40": 15.8,  "80": 13.9},
                    "3/4":  {"OD": 26.7,  "40": 21.0,  "80": 18.9},
                    "1":    {"OD": 33.4,  "40": 26.6,  "80": 24.3},
                    "1 1/4": {"OD": 42.2,  "40": 35.1,  "80": 32.5},
                    "1 1/2": {"OD": 48.3,  "40": 40.9,  "80": 38.1},
                    "2":    {"OD": 60.3,  "40": 52.5,  "80": 49.3},
                    "2 1/2": {"OD": 73.0,  "40": 62.7,  "80": 59.0},
                    "3":    {"OD": 88.9,  "40": 77.9,  "80": 73.7},
                    "3 1/2": {"OD": 101.6, "40": 90.1,  "80": 85.4},
                    "4":    {"OD": 114.3, "10": 108.2, "30": 104.7, "40": 102.26, "80": 97.18},
                    "5":    {"OD": 141.3, "40": 128.2, "80": 122.24},
                    "6":    {"OD": 168.3, "40": 154.08, "80": 146.36},
                    "8":    {"OD": 219.1, "10": 211.58, "20": 206.4, "30": 205.02, "40": 202.74, "60": 198.48, "80": 193.7},
                    "10":   {"OD": 273.1, "10": 266.3, "20": 260.3, "30": 257.5, "40": 254.5, "60": 247.7, "80": 242.9},
                    "12":   {"OD": 323.9, "10": 317.5, "20": 311.1, "30": 307.1, "40": 304.8, "60": 298.5, "80": 288.9},
                    "20":   {"OD": 508.0, "10": 495.3, "20": 488.94, "30": 482.6, "40": 477.82, "80": 455.62}
                }

                pipe = data_pipe.get(NPS)
                if pipe and SCH in pipe:
                    OD = pipe["OD"]
                    ID = pipe[SCH]
                    T = (OD - ID) / 2
                    panjang_miring = T / math.cos(math.radians(30))
                    area_buffing_per_joint = (math.pi * OD) * panjang_miring
                    total_area = area_buffing_per_joint * JBUFFING

                    ref_OD = 114.3
                    ref_T = (114.3 - 102.26) / 2
                    area_ref_1_joint = (math.pi * ref_OD) * (ref_T / math.cos(math.radians(30)))
                    area_disc_buffing = area_ref_1_joint * 10

                    kebutuhan_disc = total_area / area_disc_buffing
                    kebutuhan_disc_bulat = math.ceil(kebutuhan_disc)

                    st.write(f"Area buffing per joint : {area_buffing_per_joint:,.2f} mm2")
                    st.write(f"Total area buffing : {total_area:,.2f} mm2")
                    st.write(f"Kebutuhan flap disc : {kebutuhan_disc:,.2f} pcs")
                    st.write(f"*Kebutuhan aktual : {kebutuhan_disc_bulat} pcs*")
                else:
                    st.warning("Data ukuran pipe tidak tersedia")
        
    elif CCALCULATE == "FILLER WELD":
        JPROSESS = st.selectbox('PROCESS', ['GTAW / TIG', 'SMAW / MMA'])
        
        if JPROSESS == 'GTAW / TIG':
            JMATERIAL = st.selectbox('JENIS MATERIAL', ['Pipe', 'Plate'])
        
            if JMATERIAL == 'Pipe':
                NPS = st.selectbox('NPS', [
                    '1/8','1/4','3/8','1/2','3/4','1','1 1/4','1 1/2','2','2 1/2','3',
                    '3 1/2','4','5','6','8','10','12','14','16','18','20'
                ])
                SCH = st.selectbox('SCH', ['10','20','30','40','60','80'])
                JJOINT = st.number_input('Jumlah Joint Pengelasan', min_value=0, value=2)
        
                if st.button('HITUNG'):
                    data_pipe = {
                        "1/8":  {"OD": 10.3,  "40": 6.8,   "80": 4.8},
                        "1/4":  {"OD": 13.7,  "40": 9.2,   "80": 7.7},
                        "3/8":  {"OD": 17.1,  "40": 12.5,  "80": 10.7},
                        "1/2":  {"OD": 21.3,  "40": 15.8,  "80": 13.9},
                        "3/4":  {"OD": 26.7,  "40": 21.0,  "80": 18.9},
                        "1":    {"OD": 33.4,  "40": 26.6,  "80": 24.3},
                        "1 1/4": {"OD": 42.2,  "40": 35.1,  "80": 32.5},
                        "1 1/2": {"OD": 48.3,  "40": 40.9,  "80": 38.1},
                        "2":    {"OD": 60.3,  "40": 52.5,  "80": 49.3},
                        "2 1/2": {"OD": 73.0,  "40": 62.7,  "80": 59.0},
                        "3":    {"OD": 88.9,  "40": 77.9,  "80": 73.7},
                        "3 1/2": {"OD": 101.6, "40": 90.1,  "80": 85.4},
                        "4":    {"OD": 114.3, "10": 108.2, "30": 104.7, "40": 102.26, "80": 97.18},
                        "5":    {"OD": 141.3, "40": 128.2, "80": 122.24},
                        "6":    {"OD": 168.3, "40": 154.08, "80": 146.36},
                        "8":    {"OD": 219.1, "10": 211.58, "20": 206.4, "30": 205.02, "40": 202.74, "60": 198.48, "80": 193.7},
                        "10":   {"OD": 273.1, "10": 266.3, "20": 260.3, "30": 257.5, "40": 254.5, "60": 247.7, "80": 242.9},
                        "12":   {"OD": 323.9, "10": 317.5, "20": 311.1, "30": 307.1, "40": 304.8, "60": 298.5, "80": 288.9},
                        "20":   {"OD": 508.0, "10": 495.3, "20": 488.94, "30": 482.6, "40": 477.82, "80": 455.62}
                    }
        
                    pipe = data_pipe.get(NPS)
                    if pipe and SCH in pipe:
                        ref_OD = 114.3
                        ref_ID = 102.26
                        ref_T = (ref_OD - ref_ID) / 2
                        ref_area = (ref_T**2) * math.tan(math.radians(30)) 
                        ref_volume_total_mm3 = (math.pi * ref_OD) * ref_area * 2
                        
                        current_OD = pipe["OD"]
                        current_ID = pipe[SCH]
                        current_T = (current_OD - current_ID) / 2
                        current_area = (current_T**2) * math.tan(math.radians(30))
                        volume_mm3 = (math.pi * current_OD) * current_area * JJOINT
        
                        ratio = volume_mm3 / ref_volume_total_mm3
                        filler_needed = 0.6 * ratio
                        argon_needed = 300 * ratio
                        batang_filler = math.ceil(filler_needed / 0.044)
        
                        st.write(f"Volume Pengelasan (Total): {volume_mm3:,.2f} mm3")
                        st.write(f"Filler Rod: {filler_needed:.3f} kg")
                        st.write(f"Estimasi: *{batang_filler} batang* (dia 2.4mm)")
                        st.write(f"Argon Consumption: {argon_needed:.1f} PSI")
                    else:
                        st.error("Data spesifikasi pipa/SCH tidak ditemukan di database.")
                        
        elif JPROSESS == 'SMAW / MMA':
            JMATERIAL = st.selectbox('JENIS MATERIAL', ['Pipe', 'Plate'])
        
            if JMATERIAL == 'Pipe':
                NPS = st.selectbox('NPS', [
                    '1/8','1/4','3/8','1/2','3/4','1','1 1/4','1 1/2','2','2 1/2','3',
                    '3 1/2','4','5','6','8','10','12','14','16','18','20'
                ])
                SCH = st.selectbox('SCH', ['10','20','30','40','60','80'])
                JJOINT = st.number_input('Jumlah Joint Pengelasan', min_value=0, value=2)
        
                if st.button('HITUNG'):
                    data_pipe = {
                        "1/8":  {"OD": 10.3,  "40": 6.8,   "80": 4.8},
                        "1/4":  {"OD": 13.7,  "40": 9.2,   "80": 7.7},
                        "3/8":  {"OD": 17.1,  "40": 12.5,  "80": 10.7},
                        "1/2":  {"OD": 21.3,  "40": 15.8,  "80": 13.9},
                        "3/4":  {"OD": 26.7,  "40": 21.0,  "80": 18.9},
                        "1":    {"OD": 33.4,  "40": 26.6,  "80": 24.3},
                        "1 1/4": {"OD": 42.2,  "40": 35.1,  "80": 32.5},
                        "1 1/2": {"OD": 48.3,  "40": 40.9,  "80": 38.1},
                        "2":    {"OD": 60.3,  "40": 52.5,  "80": 49.3},
                        "2 1/2": {"OD": 73.0,  "40": 62.7,  "80": 59.0},
                        "3":    {"OD": 88.9,  "40": 77.9,  "80": 73.7},
                        "3 1/2": {"OD": 101.6, "40": 90.1,  "80": 85.4},
                        "4":    {"OD": 114.3, "10": 108.2, "30": 104.7, "40": 102.26, "80": 97.18},
                        "5":    {"OD": 141.3, "40": 128.2, "80": 122.24},
                        "6":    {"OD": 168.3, "40": 154.08, "80": 146.36},
                        "8":    {"OD": 219.1, "10": 211.58, "20": 206.4, "30": 205.02, "40": 202.74, "60": 198.48, "80": 193.7},
                        "10":   {"OD": 273.1, "10": 266.3, "20": 260.3, "30": 257.5, "40": 254.5, "60": 247.7, "80": 242.9},
                        "12":   {"OD": 323.9, "10": 317.5, "20": 311.1, "30": 307.1, "40": 304.8, "60": 298.5, "80": 288.9},
                        "20":   {"OD": 508.0, "10": 495.3, "20": 488.94, "30": 482.6, "40": 477.82, "80": 455.62}
                    }
        
                    pipe = data_pipe.get(NPS)
                    if pipe and SCH in pipe:
                        ref_OD = 114.3
                        ref_ID = 102.26
                        ref_T = (ref_OD - ref_ID) / 2
                        ref_area = (ref_T**2) * math.tan(math.radians(30)) 
                        ref_volume_total_mm3 = (math.pi * ref_OD) * ref_area * 2
                        
                        current_OD = pipe["OD"]
                        current_ID = pipe[SCH]
                        current_T = (current_OD - current_ID) / 2
                        current_area = (current_T**2) * math.tan(math.radians(30))
                        volume_mm3 = (math.pi * current_OD) * current_area * JJOINT
        
                        ratio = volume_mm3 / ref_volume_total_mm3
                        filler_needed = 0.8 * ratio
                        batang_filler = math.ceil(filler_needed / 0.035)
        
                        st.write(f"Volume Pengelasan (Total): {volume_mm3:,.2f} mm3")
                        st.write(f"Filler Metal / Electrode: {filler_needed:.3f} kg")
                        st.write(f"Estimasi: *{batang_filler} batang* (Electrode 3.2mm)")
                    else:
                        st.error("Data spesifikasi pipa/SCH tidak ditemukan di database.")
        
    elif CCALCULATE == 'COATING':
        JMATERIAL = st.selectbox('JENIS MATERIAL', ['Pipe','Plate','UNP','WF','H BEAM'])

        if JMATERIAL == 'Pipe':
            JCOATING = st.selectbox(
                'JENIS CAT',
                ['Cat jotun futura classic clay brown ral 8003','Cat Jotun Solvalit Black','Cat jotun easy prime grey ral 38']
            )
            NPS = st.selectbox('NPS', ['1/2"','1"','1 1/2"','2"','2 1/2"','3"','4"'])
            JPANJANG = st.number_input('Masukan panjang pipe yang akan di coating (mm)', min_value=0)

            if st.button('HITUNG'):
                keliling_data = {
                    '1/2"'  : 66.882, '1"'    : 108.876, '1 1/2"': 151.662,
                    '2"'    : 189.342, '2 1/2"': 229.2, '3"'    : 279.146, '4"'    : 358.902
                }
                keliling_pipe = keliling_data.get(NPS)
                
                coating_data = {
                    'Cat jotun futura classic clay brown ral 8003'  : 1633140,
                    'Cat jotun easy prime grey ral 38'  : 3408156,
                    'Cat Jotun Solvalit Black'    : 3190240
                }
                coating = coating_data.get(JCOATING, 0)

                if keliling_pipe:
                    total_luas = JPANJANG * keliling_pipe
                    kebutuhan_cat = total_luas / coating
                    kebutuhan_coating = math.ceil(kebutuhan_cat)
                    
                    st.write(f"Total Luas Coating : {total_luas:,.2f} mm2")
                    st.write(f"Kebutuhan Coating : {kebutuhan_cat:,.2f} kg")
                    st.write(f"Kebutuhan Aktual (dibulatkan) : {kebutuhan_coating} kg")
                else:
                    st.warning("Data ukuran pipe tidak tersedia")
