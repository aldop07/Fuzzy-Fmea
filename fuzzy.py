import numpy as np
import streamlit as st
import pandas as pd
import math
from datetime import datetime
import io

# Import modul Word (python-docx)
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

# Konfigurasi Halaman Utama Streamlit
st.set_page_config(page_title="Engineering Tools & LPI Report", layout="wide")

# =======================================================================================
# FUNGSI PEMBANTU (HELPERS) UNTUK MODIFIKASI XML WORD (BORDER, MARGIN, & BACKGROUND)
# =======================================================================================
def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_borders(cell, top="single", bottom="single", left="single", right="single", color="000000", sz="4"):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for border_name in ['top', 'left', 'bottom', 'right']:
        border = OxmlElement(f'w:{border_name}')
        border.set(qn('w:val'), 'single')
        border.set(qn('w:sz'), sz)
        border.set(qn('w:space'), '0')
        border.set(qn('w:color'), color)
        tcBorders.append(border)
    tcPr.append(tcBorders)

def merge_cells_horizontally(row, start_idx, end_idx):
    base_cell = row.cells[start_idx]
    for idx in range(start_idx + 1, end_idx + 1):
        base_cell.merge(row.cells[idx])
    return base_cell

def Format_Check(target, current_value):
    return "[x]" if target == current_value else "[ ]"

# =======================================================================================
# FUNGSI CORE ENGINE GENERATOR REPORT WORD (.DOCX)
# =======================================================================================
def generate_docx_report(client, project, equipment, auto_form_no, date_str, 
                         drawing_no, standard, description, penetrant_method, removal_method, 
                         brand_name, penetrant_type, developer_type, cleaner_type, 
                         surface_prep, time_exam, scope_exam, data_df):
    
    doc = Document()
    
    # Atur Margin Halaman agar tipis dan presisi (Top/Bottom 0.5", Left/Right 0.4")
    for section in doc.sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.4)
        section.right_margin = Inches(0.4)

    # Set Default Font Global ke Arial 8.5 Pt (Standar Dokumen Teknis QA/QC)
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Arial'
    font.size = Pt(8.5)

    # --- TABLE 1: KOP LOGO PERUSAHAAN & ARSITEKTUR BRANDING UTAMA ---
    table_top = doc.add_table(rows=2, cols=4)
    table_top.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_top.autofit = False

    widths_top = [Inches(1.8), Inches(3.8), Inches(0.9), Inches(1.0)]
    for row in table_top.rows:
        for i, w in enumerate(widths_top):
            row.cells[i].width = w

    # Gabungkan kolom kanan atas untuk Sub-Logo Kontraktor/Consultant
    table_top.rows[0].cells[2].merge(table_top.rows[0].cells[3])

    # Isi Teks Kop Kiri (Logo/Nama Client Utama)
    p_logo = table_top.rows[0].cells[0].paragraphs[0]
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_logo = p_logo.add_run(client)
    r_logo.bold = True
    r_logo.font.size = Pt(11)

    # Isi Judul Tengah Kop (Nama Project)
    p_title = table_top.rows[0].cells[1].paragraphs[0]
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run(project)
    r_title.bold = True
    r_title.font.size = Pt(11)

    # Isi Kop Kanan (Sub Kontraktor / Consultant)
    p_rlogo = table_top.rows[0].cells[2].paragraphs[0]
    p_rlogo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_rlogo = p_rlogo.add_run("DAMAC DIGITAL\nCUSHMAN & WAKEFIELD")
    r_rlogo.font.size = Pt(8)

    # Baris Ke-2 Metadata Penomoran Kop Dokumen
    table_top.rows[1].cells[0].text = f"  Date: {date_str}"
    table_top.rows[1].cells[1].text = "  Doc No.:"
    table_top.rows[1].cells[2].text = "  Rev. 0"
    table_top.rows[1].cells[3].text = "  Page 2 of 5"

    for row in table_top.rows:
        for cell in row.cells:
            set_cell_borders(cell, sz="6", color="000000")
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # BANNER JUDUL UTAMA REPORT
    p_banner = doc.add_paragraph()
    p_banner.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_banner = p_banner.add_run("LIQUID PENETRANT INSPECTION REPORT")
    r_banner.bold = True
    r_banner.font.size = Pt(13)
    p_banner.paragraph_format.space_after = Pt(6)

    # --- TABLE 2: INSPECTION METADATA & PARAMETER CHECKBOXES ---
    table_meta = doc.add_table(rows=11, cols=4)
    table_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_meta.autofit = False

    widths_meta = [Inches(1.8), Inches(2.2), Inches(1.5), Inches(2.0)]
    for row in table_meta.rows:
        for i, w in enumerate(widths_meta):
            row.cells[i].width = w

    meta_rows_data = [
        ("CLIENT", client, "FORM NO", auto_form_no),
        ("PROJECT", project, "DATE", date_str),
        ("EQUIPMENT / SYSTEM", equipment, "STANDARD", standard),
        ("DRAWING NO", drawing_no, "DESCRIPTION", description),
    ]

    for row_idx, data in enumerate(meta_rows_data):
        row = table_meta.rows[row_idx]
        row.cells[0].text = " " + data[0]
        row.cells[1].text = " " + data[1]
        row.cells[2].text = " " + data[2]
        row.cells[3].text = " " + data[3]
        row.cells[0].paragraphs[0].runs[0].font.bold = True
        row.cells[2].paragraphs[0].runs[0].font.bold = True

    # Mapping parameter bertipe pilihan Checkbox [x] / [ ] secara dinamis
    param_configs = [
        ("PENETRANT METHOD", f"{Format_Check('VISIBLE', penetrant_method)} VISIBLE      {Format_Check('FLUORECENT', penetrant_method)} FLUORECENT"),
        ("REMOVAL METHOD", f"{Format_Check('SOLVENT REMOVABLE', removal_method)} SOLVENT REMOVABLE   {Format_Check('WATER WASHABLE', removal_method)} WATER WASHABLE   {Format_Check('POST EMULSIFIEBLE', removal_method)} POST EMULSIFIEBLE"),
        ("BRAND NAME", f"MAGNAFLUX   |   PENETRANT: {penetrant_type}   |   DEVELOPER: {developer_type}   |   CLEANER: {cleaner_type}"),
        ("SURFACE PREPARATION", f"{Format_Check('AS WELDED', surface_prep)} AS WELDED      {Format_Check('MACHINING', surface_prep)} MACHINING      {Format_Check('GRINDING', surface_prep)} GRINDING      {Format_Check('OTHER', surface_prep)} OTHER"),
        ("TIME OF EXAMINATION", f"{Format_Check('AFTER WELDING', time_exam)} AFTER WELDING      {Format_Check('AFTER HYDROTEST', time_exam)} AFTER HYDROTEST      {Format_Check('AFTER PWHT', time_exam)} AFTER PWHT      {Format_Check('OTHER', time_exam)} OTHER"),
        ("SCOPE OF EXAMINATION", f"{Format_Check('BASE METAL', scope_exam)} BASE METAL      {Format_Check('WELD METAL', scope_exam)} WELD METAL      {Format_Check('BACK CHIPPING', scope_exam)} BACK CHIPPING      {Format_Check('OTHER', scope_exam)} OTHER"),
    ]

    for idx, (label, val_string) in enumerate(param_configs):
        row = table_meta.rows[4 + idx]
        merged_cell = row.cells[1]
        merged_cell.merge(row.cells[2]).merge(row.cells[3])
        row.cells[0].text = " " + label
        row.cells[0].paragraphs[0].runs[0].font.bold = True
        merged_cell.text = " " + val_string

    # Kosongkan baris terakhir pembatas perimeter parameter
    row_last = table_meta.rows[10]
    row_last.cells[1].merge(row_last.cells[2]).merge(row_last.cells[3])

    for row in table_meta.rows:
        for cell in row.cells:
            set_cell_borders(cell, sz="4", color="000000")
            set_cell_margins(cell, top=50, bottom=50, left=80, right=80)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # --- TABLE 3: WELD INSPECTION RESULT DATA (Header Berjenjang Tingkat) ---
    table_data = doc.add_table(rows=2, cols=7)
    table_data.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_data.autofit = False

    widths_data = [Inches(1.8), Inches(0.8), Inches(1.1), Inches(0.6), Inches(0.6), Inches(1.6), Inches(1.0)]
    for row in table_data.rows:
        for i, w in enumerate(widths_data):
            row.cells[i].width = w

    # Setup Susunan Text Header Atas
    table_data.rows[0].cells[0].text = "PART NAME"
    table_data.rows[0].cells[1].text = "WELD NO"
    table_data.rows[0].cells[2].text = "THICKNESS (MM)"
    table_data.rows[0].cells[3].text = "RESULT"
    table_data.rows[0].cells[3].merge(table_data.rows[0].cells[4]) # Merge Horizontal untuk RESULT
    table_data.rows[0].cells[5].text = "TYPES OF DISCONTINUITIES"
    table_data.rows[0].cells[6].text = "REMARKS"

    # Setup Header Bawah khusus Split Result
    table_data.rows[1].cells[3].text = "ACC"
    table_data.rows[1].cells[4].text = "REJECT"

    # Jalankan Vertikal Merge otomatis untuk Kolom Non-Result
    for c_idx in [0, 1, 2, 5, 6]:
        table_data.rows[0].cells[c_idx].merge(table_data.rows[1].cells[c_idx])

    # Styling Shading Abu-Abu pada Header Tabel Las
    for r_idx in [0, 1]:
        for cell in table_data.rows[r_idx].cells:
            if cell.text:
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.runs[0].font.bold = True
            set_cell_background(cell, "F2F2F2")

    # Injeksi Baris Data Hasil Pengujian Las dari Streamlit Dataframe
    for index, row_data in data_df.iterrows():
        row = table_data.add_row()
        for i, w in enumerate(widths_data):
            row.cells[i].width = w
            
        row.cells[0].text = " " + str(row_data["PART NAME"])
        row.cells[1].text = str(row_data["WELD NO"])
        row.cells[2].text = str(row_data["THICKNESS (MM)"])
        row.cells[3].text = "[x]" if row_data["RESULT"] == "ACC" else "[ ]"
        row.cells[4].text = "[x]" if row_data["RESULT"] == "REJECT" else "[ ]"
        row.cells[5].text = str(row_data["TYPES OF DISCONTINUITIES"])
        row.cells[6].text = " " + str(row_data["REMARKS"])
        
        # Center alignment data kolom numerik/status
        for c_idx in [1, 2, 3, 4, 5]:
            row.cells[c_idx].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Menambahkan 10 baris kosong tambahan di bawahnya untuk tulisan tangan manual lapangan (Sesuai Layout Gambar)
    for _ in range(10):
        row = table_data.add_row()
        for i, w in enumerate(widths_data):
            row.cells[i].width = w
        row.cells[3].text = "[ ]"
        row.cells[4].text = "[ ]"
        row.cells[5].text = "-"
        for c_idx in [3, 4, 5]:
            row.cells[c_idx].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    for row in table_data.rows:
        for cell in row.cells:
            set_cell_borders(cell, sz="4", color="000000")
            set_cell_margins(cell, top=40, bottom=40, left=60, right=60)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # --- TABLE 4: SIGNATURE SIGN OFF BOXES (Blok Grid 4 Kolom Sesuai Gambar) ---
    table_sig = doc.add_table(rows=3, cols=4)
    table_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_sig.autofit = False

    widths_sig = [Inches(1.87), Inches(1.87), Inches(1.87), Inches(1.87)]
    for row in table_sig.rows:
        for i, w in enumerate(widths_sig):
            row.cells[i].width = w

    sig_headers = ["CHECKED BY", "REVIEWED BY", "REVIEWED / WITNESSED BY", "REVIEWED / WITNESSED BY"]
    for i, title in enumerate(sig_headers):
        cell = table_sig.rows[0].cells[i]
        cell.text = title
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.runs[0].font.bold = True
        set_cell_background(cell, "F2F2F2")

    # Baris kosong tinggi tempat tanda tangan basah/stempel
    table_sig.rows[1].cells[0].text = "\n\n\n\n"

    # Baris keterangan nama dan tanggal penandatanganan
    for i in range(4):
        cell = table_sig.rows[2].cells[i]
        cell.text = "Name:\nDate:"
        set_cell_margins(cell, top=60, bottom=60, left=80, right=80)

    for row in table_sig.rows:
        for cell in row.cells:
            set_cell_borders(cell, sz="4", color="000000")
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    # Simpan berkas ke dalam memory byte stream buffer
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

    st.subheader("Logo Perusahaan (Kop Surat)")
    uploaded_logo = st.file_uploader("Unggah Logo untuk Kop Report (Format: PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])
    
    if uploaded_logo is not None:
        st.image(uploaded_logo, width=200, caption="Preview Logo Kop Surat")
    else:
        st.info("💡 Berkas cetakan Word otomatis menggunakan layout Kop Teks Terstruktur sesuai gambar acuan.")

    st.markdown("---")

    # Otomatisasi Form Number & Tanggal berdasarkan waktu berjalan
    current_date = datetime.now()
    date_str = current_date.strftime("%d-%m-%Y").upper() 
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
            {"PART NAME": "PIPE – FLANGE", "WELD NO": "21", "THICKNESS (MM)": 3.91, "RESULT": "ACC", "TYPES OF DISCONTINUITIES": "-", "REMARKS": "-"},
            {"PART NAME": "PIPE – FLANGE", "WELD NO": "22", "THICKNESS (MM)": 3.91, "RESULT": "ACC", "TYPES OF DISCONTINUITIES": "-", "REMARKS": "-"},
            {"PART NAME": "PIPE – ELBOW", "WELD NO": "23", "THICKNESS (MM)": 3.91, "RESULT": "ACC", "TYPES OF DISCONTINUITIES": "-", "REMARKS": "-"},
            {"PART NAME": "PIPE – ELBOW", "WELD NO": "24", "THICKNESS (MM)": 3.91, "RESULT": "ACC", "TYPES OF DISCONTINUITIES": "-", "REMARKS": "-"},
            {"PART NAME": "PIPE – EQUAL TEE", "WELD NO": "26", "THICKNESS (MM)": 3.91, "RESULT": "ACC", "TYPES OF DISCONTINUITIES": "-", "REMARKS": "-"}
        ])

    with st.expander("➕ Tambah Baris Hasil Las Baru"):
        c1_a, c1_b, c2, c3, c4 = st.columns([2, 2, 1.5, 1.5, 2])
        
        with c1_a:
            part_1 = st.selectbox("Pilihan 1 (Base Component)", part_options_1)
        with c1_b:
            part_2 = st.selectbox("Pilihan 2 (Joint Component)", part_options_2)
            
        with c2:
            new_weld_no = st.text_input("Weld No", value="27")
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
            st.success(f"Data baru '{combined_part_name}' berhasil ditambahkan!")

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
    
    # Area Tombol Cetak Layar dan Download File Word Resmi (.docx)
    col_btn1, col_btn2 = st.columns([2, 8])
    
    with col_btn1:
        generate_layout = st.button("🚀 Generate Screen Preview Layout")
        
    with col_btn2:
        # Proses build data ke Word secara terintegrasi langsung
        docx_buffer = generate_docx_report(
            client=client, project=project, equipment=equipment, auto_form_no=auto_form_no,
            date_str=date_str, drawing_no=drawing_no, standard=standard, description=description,
            penetrant_method=penetrant_method, removal_method=removal_method, brand_name=brand_name,
            penetrant_type=penetrant_type, developer_type=developer_type, cleaner_type=cleaner_type,
            surface_prep=surface_prep, time_exam=time_exam, scope_exam=scope_exam, data_df=edited_weld_df
        )
        
        st.download_button(
            label="📥 Download Official Word Report (.docx)",
            data=docx_buffer,
            file_name=f"LPI_Report_{auto_form_no.replace('/', '_')}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    # Menampilkan Layout Preview di Halaman Browser jika tombol ditekan
    if generate_layout:
        st.markdown("## 📄 PREVIEW SCREEN LAYOUT")
        header_summary = pd.DataFrame({
            "FIELD A": ["CLIENT", "PROJECT", "EQUIPMENT / SYSTEM", "DRAWING NO", "STANDARD / DESC"],
            "VALUE A": [client, project, equipment, drawing_no, f"{standard} / {description}"],
            "FIELD B": ["FORM NO", "DATE", "PENETRANT METHOD", "REMOVAL METHOD", "BRAND & MATERIALS"],
            "VALUE B": [auto_form_no, date_str, f"☑ {penetrant_method}", f"☑ {removal_method}", f"{brand_name} ({penetrant_type}/{developer_type})"]
        })
        st.table(header_summary)
        
        display_df = edited_weld_df.copy()
        display_df["ACC"] = display_df["RESULT"].apply(lambda x: "☑" if x == "ACC" else "☐")
        display_df["REJECT"] = display_df["RESULT"].apply(lambda x: "☑" if x == "REJECT" else "☐")
        display_df = display_df[["PART NAME", "WELD NO", "THICKNESS (MM)", "ACC", "REJECT", "TYPES OF DISCONTINUITIES", "REMARKS"]]
        st.dataframe(display_df, use_container_width=True)
