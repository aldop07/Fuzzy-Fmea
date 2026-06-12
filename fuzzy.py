import numpy as np
import streamlit as st
import pandas as pd
import math
from datetime import datetime
import io
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

# Konfigurasi Halaman Utama
st.set_page_config(page_title="Engineering Tools & LPI Report", layout="wide")

# =======================================================================================
# FUNGSI PEMBANTU FORMATTING XML (UNTUK PAGINATION & LAYOUT TINGKAT LANJUT)
# =======================================================================================
def set_cell_margins(cell, top=100, bottom=100, start=100, end=100):
    """Mengatur padding di dalam cell tabel (dalam dxa)"""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', start), ('w:right', end)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_background(cell, fill_hex):
    """Mengatur warna latar belakang cell"""
    shading_elm = parse_xml(r'<w:shd {} w:fill="{}"/>'.format(nsdecls('w'), fill_hex))
    cell._tc.get_or_add_tcPr().append(shading_elm)

def prevent_row_split(row):
    """Mencegah baris tabel terpotong di antara dua halaman"""
    trPr = row._tr.get_or_add_trPr()
    trPr.append(parse_xml(r'<w:cantSplit {}/>'.format(nsdecls('w'))))

def set_repeat_header(row):
    """Mengatur baris tabel agar otomatis diulang di halaman berikutnya"""
    trPr = row._tr.get_or_add_trPr()
    trPr.append(parse_xml(r'<w:tblHeader {}/>'.format(nsdecls('w'))))

def add_xml_field(run, field_name):
    """Menyisipkan field kode dinamis MS Word (PAGE / NUMPAGES)"""
    fldChar1 = parse_xml(r'<w:fldChar {} w:fldCharType="begin"/>'.format(nsdecls('w')))
    instrText = parse_xml(r'<w:instrText {} xml:space="preserve"> {} </w:instrText>'.format(nsdecls('w'), field_name))
    fldChar2 = parse_xml(r'<w:fldChar {} w:fldCharType="separate"/>'.format(nsdecls('w')))
    fldChar3 = parse_xml(r'<w:fldChar {} w:fldCharType="end"/>'.format(nsdecls('w')))
    run._r.extend([fldChar1, instrText, fldChar2, fldChar3])

# =======================================================================================
# FUNGSI UNTUK GENERATE FILE WORD (.DOCX) DENGAN KOP STANDAR & FOTO DOKUMENTASI
# =======================================================================================
def generate_docx_report(logo_left_bytes, logo_right_top_bytes, logo_right_bottom_bytes, 
                         photo_penetrant_bytes, photo_developer_bytes,
                         client, project, equipment, auto_form_no, date_str, doc_no, rev_no,
                         drawing_no, standard, description, penetrant_method, removal_method, 
                         brand_name, penetrant_type, developer_type, cleaner_type, 
                         surface_prep, time_exam, scope_exam, data_df, logo_width_inch):
    
    doc = Document()
    
    # Atur Margin Halaman Cetak Standar Internasional A4
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(2.4)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)
        section.header_distance = Inches(0.4)
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)

    # -----------------------------------------------------------------------------------
    # 1. INTEGRASI KOP SURAT KE NATIVE WORD HEADER (UKURAN KOLOM SIMETRIS)
    # -----------------------------------------------------------------------------------
    header = doc.sections[0].header
    for p in header.paragraphs:
        p.text = ""
        
    kop_table = header.add_table(3, 4, Inches(6.77))
    kop_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    kop_table.style = 'Table Grid'
    
    col_widths = [Inches(1.85), Inches(3.07), Inches(0.85), Inches(1.00)]
    for row in kop_table.rows:
        prevent_row_split(row)
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = width

    # Proses Merging Kolom Sesuai Blueprint
    cell_left = kop_table.cell(0, 0).merge(kop_table.cell(1, 0))          
    cell_center = kop_table.cell(0, 1).merge(kop_table.cell(1, 1))        
    cell_right_top = kop_table.cell(0, 2).merge(kop_table.cell(0, 3))     
    cell_right_bottom = kop_table.cell(1, 2).merge(kop_table.cell(1, 3))  

    # Mengisi Konten Logo Kiri
    cell_left.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    p_left = cell_left.paragraphs[0]
    p_left.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if logo_left_bytes is not None:
        p_left.add_run().add_picture(logo_left_bytes, width=Inches(logo_width_inch))
    else:
        p_left.add_run("[ LOGO KIRI ]").font.color.rgb = RGBColor(160, 160, 160)

    # Mengisi Konten Judul Tengah
    cell_center.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    p_center = cell_center.paragraphs[0]
    p_center.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_center = p_center.add_run(str(project).upper())
    run_center.bold = True
    run_center.font.size = Pt(11)
    run_center.font.name = 'Arial'

    # Mengisi Konten Logo Kanan Atas
    cell_right_top.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    p_rt = cell_right_top.paragraphs[0]
    p_rt.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if logo_right_top_bytes is not None:
        p_rt.add_run().add_picture(logo_right_top_bytes, width=Inches(logo_width_inch))
    else:
        p_rt.add_run("[ LOGO KANAN ATAS ]").font.color.rgb = RGBColor(160, 160, 160)

    # Mengisi Konten Logo Kanan Bawah
    cell_right_bottom.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    p_rb = cell_right_bottom.paragraphs[0]
    p_rb.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if logo_right_bottom_bytes is not None:
        p_rb.add_run().add_picture(logo_right_bottom_bytes, width=Inches(logo_width_inch))
    else:
        p_rb.add_run("[ LOGO KANAN BAWAH ]").font.color.rgb = RGBColor(160, 160, 160)

    # Mengisi Baris ke-3 (Metadata Dokumen Kontrol)
    meta_cells = kop_table.rows[2].cells
    for cell in meta_cells:
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        set_cell_margins(cell, top=60, bottom=60, start=100, end=100)

    meta_cells[0].paragraphs[0].text = f"Date: {date_str}"
    meta_cells[1].paragraphs[0].text = f"Doc No.: {doc_no if doc_no else '-'}"
    meta_cells[2].paragraphs[0].text = f"Rev. {rev_no}"
    
    # Dynamic Page Numbering
    p_page = meta_cells[3].paragraphs[0]
    p_page.text = "Page "
    add_xml_field(p_page.add_run(), "PAGE")
    p_page.add_run(" of ")
    add_xml_field(p_page.add_run(), "NUMPAGES")
    
    for cell in meta_cells:
        p = cell.paragraphs[0]
        p.runs[0].font.size = Pt(9.5)
        p.runs[0].font.name = 'Arial'
    meta_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    meta_cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    # -----------------------------------------------------------------------------------
    # BODY CONTENT AREA
    # -----------------------------------------------------------------------------------
    h1 = doc.add_paragraph()
    h1_run = h1.add_run("FINAL LIQUID PENETRANT INSPECTION REPORT")
    h1_run.bold = True
    h1_run.font.size = Pt(13)
    h1_run.font.name = 'Arial'
    h1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    h1.paragraph_format.space_after = Pt(12)

    # Tabel Informasi Umum
    table_header = doc.add_table(rows=5, cols=4)
    table_header.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_header.style = 'Table Grid'
    
    info_widths = [Inches(1.5), Inches(2.0), Inches(1.5), Inches(1.77)]
    headers_data = [
        ["CLIENT", client, "FORM NO", auto_form_no],
        ["PROJECT", project, "DATE", date_str],
        ["EQUIPMENT / SYSTEM", equipment, "PENETRANT METHOD", f"☑ {penetrant_method}"],
        ["DRAWING NO", drawing_no, "REMOVAL METHOD", f"☑ {removal_method}"],
        ["STANDARD / DESC", f"{standard} / {description}", "BRAND & MATERIALS", f"{brand_name} ({penetrant_type}/{developer_type})"]
    ]
    
    for row_idx, row_data in enumerate(headers_data):
        row_cells = table_header.rows[row_idx].cells
        prevent_row_split(table_header.rows[row_idx])
        for col_idx, text in enumerate(row_data):
            row_cells[col_idx].width = info_widths[col_idx]
            row_cells[col_idx].text = str(text)
            row_cells[col_idx].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_margins(row_cells[col_idx], top=80, bottom=80, start=100, end=100)
            
            p = row_cells[col_idx].paragraphs[0]
            p.runs[0].font.size = Pt(9.5)
            p.runs[0].font.name = 'Arial'
            if col_idx in [0, 2]:
                p.runs[0].font.bold = True
                set_cell_background(row_cells[col_idx], "F8F9FA")

    # Parameter Pengujian
    p_param = doc.add_paragraph()
    p_param.paragraph_format.space_before = Pt(10)
    p_param.paragraph_format.space_after = Pt(12)
    
    params = [
        ("Surface Prep: ", f"☑ {surface_prep}   |   "),
        ("Time of Exam: ", f"☑ {time_exam}   |   "),
        ("Scope: ", f"☑ {scope_exam}")
    ]
    for lbl, val in params:
        r_lbl = p_param.add_run(lbl)
        r_lbl.bold = True
        r_lbl.font.size = Pt(9.5)
        r_lbl.font.name = 'Arial'
        r_val = p_param.add_run(val)
        r_val.font.size = Pt(9.5)
        r_val.font.name = 'Arial'

    h2 = doc.add_paragraph()
    h2_run = h2.add_run("Inspection Results Table")
    h2_run.bold = True
    h2_run.font.size = Pt(11)
    h2_run.font.name = 'Arial'
    h2.paragraph_format.space_after = Pt(6)
    
    # Tabel Hasil Utama (Auto Repeat Header)
    table_res = doc.add_table(rows=1, cols=7)
    table_res.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_res.style = 'Table Grid'
    
    res_widths = [Inches(1.8), Inches(0.7), Inches(1.1), Inches(0.5), Inches(0.6), Inches(1.2), Inches(0.87)]
    
    hdr_cells = table_res.rows[0].cells
    set_repeat_header(table_res.rows[0]) 
    prevent_row_split(table_res.rows[0])
    
    headers_col = ["PART NAME", "WELD NO", "THICKNESS (MM)", "ACC", "REJECT", "TYPES OF DISCONTINUITIES", "REMARKS"]
    for i, title_text in enumerate(headers_col):
        hdr_cells[i].width = res_widths[i]
        hdr_cells[i].text = title_text
        hdr_cells[i].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        set_cell_margins(hdr_cells[i], top=100, bottom=100, start=60, end=60)
        set_cell_background(hdr_cells[i], "EFEFEF")
        
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.runs[0].font.bold = True
        p.runs[0].font.size = Pt(9)
        p.runs[0].font.name = 'Arial'

    for index, row in data_df.iterrows():
        new_row = table_res.add_row()
        prevent_row_split(new_row)
        row_cells = new_row.cells
        
        for idx in range(7):
            row_cells[idx].width = res_widths[idx]
            row_cells[idx].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_margins(row_cells[idx], top=80, bottom=80, start=60, end=60)
            
        row_cells[0].text = str(row["PART NAME"])
        row_cells[1].text = str(row["WELD NO"])
        row_cells[2].text = f"{row['THICKNESS (MM)']:.2f}" if isinstance(row['THICKNESS (MM)'], (int, float)) else str(row['THICKNESS (MM)'])
        row_cells[3].text = "☑" if row["RESULT"] == "ACC" else "☐"
        row_cells[4].text = "☑" if row["RESULT"] == "REJECT" else "☐"
        row_cells[5].text = str(row["TYPES OF DISCONTINUITIES"])
        row_cells[6].text = str(row["REMARKS"])
        
        for col_idx in [1, 2, 3, 4]:
            row_cells[col_idx].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            
        for idx in range(7):
            p = row_cells[idx].paragraphs[0]
            p.runs[0].font.size = Pt(9)
            p.runs[0].font.name = 'Arial'
            
    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # -----------------------------------------------------------------------------------
    # NEW FEATURE: FOTO DOKUMENTASI PENGUJIAN (SIDE BY SIDE SEJAJAR)
    # -----------------------------------------------------------------------------------
    if photo_penetrant_bytes is not None or photo_developer_bytes is not None:
        h3 = doc.add_paragraph()
        h3_run = h3.add_run("Inspection Photographs / Documentation")
        h3_run.bold = True
        h3_run.font.size = Pt(11)
        h3_run.font.name = 'Arial'
        h3.paragraph_format.space_before = Pt(12)
        h3.paragraph_format.space_after = Pt(6)
        
        # Grid Tabel Khusus Foto (1 Baris x 2 Kolom) agar layout terkunci simetris
        photo_table = doc.add_table(1, 2, Inches(6.77))
        photo_table.alignment = WD_TABLE_ALIGNMENT.CENTER
        photo_table.style = None # Kosong tanpa border agar minimalis bersih
        prevent_row_split(photo_table.rows[0])
        
        photo_table.rows[0].cells[0].width = Inches(3.38)
        photo_table.rows[0].cells[1].width = Inches(3.39)
        
        # Slot 1: Foto Aplikasi Penetran (Red Apply)
        cell_p = photo_table.rows[0].cells[0]
        cell_p.vertical_alignment = WD_ALIGN_VERTICAL.TOP
        p_photo1 = cell_p.paragraphs[0]
        p_photo1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if photo_penetrant_bytes is not None:
            p_photo1.add_run().add_picture(photo_penetrant_bytes, width=Inches(3.0))
            p_cap1 = cell_p.add_paragraph()
            p_cap1.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap1.paragraph_format.space_before = Pt(4)
            r_cap1 = p_cap1.add_run("Figure 1: Penetrant Application (Red Apply)")
            r_cap1.font.size = Pt(8.5)
            r_cap1.font.italic = True
            r_cap1.font.name = 'Arial'
        else:
            p_photo1.add_run("[ Foto Penetran Belum Diunggah ]").font.color.rgb = RGBColor(180, 180, 180)
            
        # Slot 2: Foto Aplikasi Developer
        cell_d = photo_table.rows[0].cells[1]
        cell_d.vertical_alignment = WD_ALIGN_VERTICAL.TOP
        p_photo2 = cell_d.paragraphs[0]
        p_photo2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if photo_developer_bytes is not None:
            p_photo2.add_run().add_picture(photo_developer_bytes, width=Inches(3.0))
            p_cap2 = cell_d.add_paragraph()
            p_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap2.paragraph_format.space_before = Pt(4)
            r_cap2 = p_cap2.add_run("Figure 2: Developer Application")
            r_cap2.font.size = Pt(8.5)
            r_cap2.font.italic = True
            r_cap2.font.name = 'Arial'
        else:
            p_photo2.add_run("[ Foto Developer Belum Diunggah ]").font.color.rgb = RGBColor(180, 180, 180)

        doc.add_paragraph().paragraph_format.space_after = Pt(16)

    # Bagian 4 Kolom Tanda Tangan Paralel
    table_sig = doc.add_table(rows=2, cols=4)
    table_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_sig.style = None 
    prevent_row_split(table_sig.rows[0])
    prevent_row_split(table_sig.rows[1])
    
    sig_widths = [Inches(1.69), Inches(1.69), Inches(1.69), Inches(1.70)]
    sig_titles =
