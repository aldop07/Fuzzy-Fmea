import numpy as np
import streamlit as st
import pandas as pd
import math
from datetime import datetime
import io
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

# Konfigurasi Halaman Utama
st.set_page_config(page_title="Engineering Tools & LPI Report", layout="wide")

# =======================================================================================
# FUNGSI UNTUK GENERATE FILE WORD (.DOCX)
# =======================================================================================
def generate_docx_report(logo_bytes, client, project, equipment, auto_form_no, date_str, 
                         drawing_no, standard, description, penetrant_method, removal_method, 
                         brand_name, penetrant_type, developer_type, cleaner_type, 
                         surface_prep, time_exam, scope_exam, data_df):
    
    doc = Document()
    
    # Atur Margin Halaman (Standard 1 Inch)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # 1. HANDLE LOGO KOP SURAT
    if logo_bytes is not None:
        # Tambah logo jika diupload oleh user
        doc.add_picture(logo_bytes, width=Inches(1.8))
        p_space = doc.add_paragraph()
        p_space.paragraph_format.space_after = Pt(12)
    else:
        # Jika tidak ada logo, buat judul teks standar kop
        title = doc.add_paragraph()
        title_run = title.add_run("LIQUID PENETRANT INSPECTION REPORT")
        title_run.bold = True
        title_run.font.size = Pt(18)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Judul Dokumen Utama
    h1 = doc.add_paragraph()
    h1_run = h1.add_run("FINAL LIQUID PENETRANT INSPECTION REPORT")
    h1_run.bold = True
    h1_run.font.size = Pt(14)
    h1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    h1.paragraph_format.space_after = Pt(18)

    # 2. HEADER INFORMATION TABLE (Grid 5 baris x 4 kolom)
    table_header = doc.add_table(rows=5, cols=4)
    table_header.style = 'Table Grid'
    
    headers_data = [
        ["CLIENT", client, "FORM NO", auto_form_no],
        ["PROJECT", project, "DATE", date_str],
        ["EQUIPMENT / SYSTEM", equipment, "PENETRANT METHOD", f"[x] {penetrant_method}"],
        ["DRAWING NO", drawing_no, "REMOVAL METHOD", f"[x] {removal_method}"],
        ["STANDARD / DESC", f"{standard} / {description}", "BRAND & MATERIALS", f"{brand_name} ({penetrant_type}/{developer_type})"]
    ]
    
    for row_idx, row_data in enumerate(headers_data):
        row_cells = table_header.rows[row_idx].cells
        for col_idx, text in enumerate(row_data):
            row_cells[col_idx].text = str(text)
            # Buat label FIELD A dan FIELD B menjadi Bold
            if col_idx in [0, 2]:
                row_cells[col_idx].paragraphs[0].runs[0].font.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # 3. INSPECTION PARAMETERS SUMMARY TEXT
    p_param = doc.add_paragraph()
    p_param.add_run("Surface Prep: ").bold = True
    p_param.add_run(f"[x] {surface_prep}   |   ")
    p_param.add_run("Time of Exam: ").bold = True
    p_param.add_run(f"[x] {time_exam}   |   ")
    p_param.add_run("Scope: ").bold = True
    p_param.add_run(f"[x] {scope_exam}")
    p_param.paragraph_format.space_after = Pt(18)

    # Sub-heading tabel hasil pengujian
    h2 = doc.add_paragraph()
    h2_run = h2.add_run("Inspection Results Table")
    h2_run.bold = True
    h2_run.font.size = Pt(12)
    
    # 4. DATA RESULT TABLE
    # Kolom: PART NAME, WELD NO, THICKNESS, ACC, REJECT, DISCONTINUITIES, REMARKS
    table_res = doc.add_table(rows=1, cols=7)
    table_res.style = 'Table Grid'
    
    # Atur Judul Kolom Tabel
    hdr_cells = table_res.rows[0].cells
    headers_col = ["PART NAME", "WELD NO", "THICKNESS (MM)", "ACC", "REJECT", "TYPES OF DISCONTINUITIES", "REMARKS"]
    for i, title_text in enumerate(headers_col):
        hdr_cells[i].text = title_text
        hdr_cells[i].paragraphs[0].runs[0].font.bold = True
        
        # Tambahkan warna abu-abu tipis pada latar belakang judul tabel (Shading XML)
        shading_elm = parse_xml(r'<w:shd {} w:fill="EFEFEF"/>'.format(nsdecls('w')))
        hdr_cells[i]._tc.get_or_add_tcPr().append(shading_elm)

    # Masukkan baris data dari DataFrame
    for index, row in data_df.iterrows():
        row_cells = table_res.add_row().cells
        row_cells[0].text = str(row["PART NAME"])
        row_cells[1].text = str(row["WELD NO"])
        row_cells[2].text = str(row["THICKNESS (MM)"])
        row_cells[3].text = "☑" if row["RESULT"] == "ACC" else "☐"
        row_cells[4].text = "☑" if row["RESULT"] == "REJECT" else "☐"
        row_cells[5].text = str(row["TYPES OF DISCONTINUITIES"])
        row_cells[6].text = str(row["REMARKS"])
        
    doc.add_paragraph().paragraph_format.space_after = Pt(24)

    # 5. SIGNATURE SECTION (3 Kolom Sejajar)
    table_sig = doc.add_table(rows=2, cols=3)
    # Hapus border luar agar terlihat seperti struktur layout kosong
    table_sig.style = None 
    
    sig_titles = ["CHECKED BY", "REVIEWED BY", "WITNESSED BY"]
    for idx, title_text in enumerate(sig_titles):
        table_sig.rows[0].cells[idx].text = title_text
        table_sig.rows[0].cells[idx].paragraphs[0].runs[0].font.bold = True
        table_sig.rows[0].cells[idx].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Jarak vertikal tanda tangan kosong
        p_sig_blank = table_sig.rows[1].cells[idx].paragraphs[0]
        p_sig_blank.text = "\n\n\n\n__________________\nName:"
        p_sig_blank.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Simpan dokumen ke memory byte stream buffer agar bisa didownload via Streamlit
    bio = io.BytesIO()
    doc.save(bio)
    bio.seek(0)
    return bio


# =======================================================================================
# MENU UTAMA APLIKASI STREAMLIT
# =======================================================================================
st.sidebar.title("Navigation Menu")
main_menu = st.sidebar.radio("PILIH MODUL APLIKASI:", ["LIQUID PENETRANT REPORT", "CONSUMABLE CALCULATE"])

st.sidebar.markdown("---")
st.sidebar.info("Aplikasi Integrasi: LPI Generator & Volume Cutting/Welding/Coating Calculator.")

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
    auto_form_no = f"05/LPI/DAMAC/{month_year_slug}" 

    st.subheader("Header Information")
    col1, col2, col3 = st.columns(3)

    with col1:
        client = st.text_input("Client", value="PT. TRAKINDO UTAMA")
        project = st.text_input("Project", value="DAMAC DIGITAL JKT01 DAY 2")
        equipment = st.text_input("Equipment / System", value="FUEL PIPE") 

    with col2:
        st.text_input("Form No (Otomatis)", value=auto_form_no, disabled=True)
        st.text_input("Date (Otomatis)", value=date_str, disabled=True)
        drawing_no = st.text_input("Drawing No", value="ISO-JKT01-003") 

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

    part_options_1 = ["PIPE", "PLATE", "ELBOW", "TEE", "FLANGE"]
    part_options_2 = ["FLANGE", "ELBOW", "EQUAL TEE", "PIPE", "VALVE"]
    discontinuity_options = ["Crack", "Porosity", "Slag Inclusion", "Incomplete Fusion", "Incomplete Penetration", "Undercut", "Linear Indication", "Rounded Indication"]

    if 'weld_data' not in st.session_state:
        st.session_state.weld_data = pd.DataFrame([
            {"PART NAME": "PIPE – FLANGE", "WELD NO": "1", "THICKNESS (MM)": 3.91, "RESULT": "ACC", "TYPES OF DISCONTINUITIES": "-", "REMARKS": "-"},
            {"PART NAME": "PIPE – ELBOW", "WELD NO": "2", "THICKNESS (MM)": 3.91, "RESULT": "ACC", "TYPES OF DISCONTINUITIES": "-", "REMARKS": "-"},
            {"PART NAME": "PIPE – EQUAL TEE", "WELD NO": "6", "THICKNESS (MM)": 3.91, "RESULT": "ACC", "TYPES OF DISCONTINUITIES": "-", "REMARKS": "-"}
        ])

    with st.expander("➕ Tambah Baris Hasil Las Baru"):
        c1_a, c1_b, c2, c3, c4 = st.columns([2, 2, 1.5, 1.5, 2])
        
        with c1_a:
            part_1 = st.selectbox("Pilihan 1 (Base)", part_options_1)
        with c1_b:
            part_2 = st.selectbox("Pilihan 2 (Joint)", part_options_2)
            
        with c2:
            new_weld_no = st.text_input("Weld No", value="3")
        with c3:
            new_thickness = st.number_input("Thickness (mm)", value=3.91, step=0.01)
        with c4:
            new_result = st.selectbox("Result", ["ACC", "REJECT"])
            
        new_discontinuity = "-"
        if new_result == "REJECT":
            new_discontinuity = st.selectbox("Types of Discontinuities", discontinuity_options)
            new_remarks = st.text_input("Remarks", value="Repair Required")
        else:
            new_remarks = "-"

        if st.button("Masukkan ke Tabel"):
            combined_part_name = f"{part_1} – {part_2}"
            new_row = {
                "PART NAME": combined_part_name, "WELD NO": new_weld_no, "THICKNESS (MM)": new_thickness,
                "RESULT": new_result, "TYPES OF DISCONTINUITIES": new_discontinuity, "REMARKS": new_remarks
            }
            st.session_state.weld_data = pd.concat([st.session_state.weld_data, pd.DataFrame([new_row])], ignore_index=True)
            st.success(f"Data baru '{combined_part_name}' berhasil ditambahkan ke tabel!")

    all_combined_options = [f"{p1} – {p2}" for p1 in part_options_1 for p2 in part_options_2]
    existing_parts = st.session_state.weld_data["PART NAME"].unique().tolist()
    final_part_config_options = list(set(all_combined_options + existing_parts))

    edited_weld_df = st.data_editor(
        st.session_state.weld_data, 
        num_rows="dynamic", 
        use_container_width=True,
        column_config={
            "PART NAME": st.column_config.SelectboxColumn("PART NAME", options=final_part_config_options, required=True),
            "RESULT": st.column_config.SelectboxColumn("RESULT", options=["ACC", "REJECT"], required=True),
            "TYPES OF DISCONTINUITIES": st.column_config.SelectboxColumn("TYPES OF DISCONTINUITIES", options=["-"] + discontinuity_options, required=True)
        }
    )

    st.markdown("---")
    
    # Aksi Layouting dan Download Dokumen Word (.docx)
    col_btn1, col_btn2 = st.columns([2, 8])
    
    with col_btn1:
        generate_layout = st.button("🚀 Generate Screen Layout")
        
    with col_btn2:
        # Convert UploadedLogo ke format bytes stream jika ada berkas terunggah
        logo_bytes_stream = io.BytesIO(uploaded_logo.getvalue()) if uploaded_logo is not None else None
        
        # Proses pembuatan dokumen Word langsung di background
        docx_buffer = generate_docx_report(
            logo_bytes=logo_bytes_stream, client=client, project=project, equipment=equipment,
            auto_form_no=auto_form_no, date_str=date_str, drawing_no=drawing_no, standard=standard,
            description=description, penetrant_method=penetrant_method, removal_method=removal_method,
            brand_name=brand_name, penetrant_type=penetrant_type, developer_type=developer_type,
            cleaner_type=cleaner_type, surface_prep=surface_prep, time_exam=time_exam,
            scope_exam=scope_exam, data_df=edited_weld_df
        )
        
        # Tombol Download File Word (.docx) resmi hasil generate dokumen
        st.download_button(
            label="📥 Download Word Report (.docx)",
            data=docx_buffer,
            file_name=f"LPI_Report_{auto_form_no.replace('/', '_')}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    # Menampilkan Layout Preview di Browser jika Tombol ditekan
    if generate_layout:
        st.markdown("## 📄 FINAL LIQUID PENETRANT INSPECTION REPORT")
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
