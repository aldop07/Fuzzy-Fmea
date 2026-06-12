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

def keep_row_with_next(row):
    """Mengunci agar baris berjalan selalu satu halaman dengan baris di bawahnya"""
    for cell in row.cells:
        for paragraph in cell.paragraphs:
            paragraph.paragraph_format.keep_with_next = True

def add_xml_field(run, field_name):
    """Menyisipkan field kode dinamis MS Word (PAGE / NUMPAGES)"""
    fldChar1 = parse_xml(r'<w:fldChar {} w:fldCharType="begin"/>'.format(nsdecls('w')))
    instrText = parse_xml(r'<w:instrText {} xml:space="preserve"> {} </w:instrText>'.format(nsdecls('w'), field_name))
    fldChar2 = parse_xml(r'<w:fldChar {} w:fldCharType="separate"/>'.format(nsdecls('w')))
    fldChar3 = parse_xml(r'<w:fldChar {} w:fldCharType="end"/>'.format(nsdecls('w')))
    run._r.extend([fldChar1, instrText, fldChar2, fldChar3])

# =======================================================================================
# FUNGSI UTAMA GENERATE .DOCX
# =======================================================================================
def generate_docx_report(logo_left_bytes, logo_right_top_bytes, logo_right_bottom_bytes, 
                         client, project, equipment, auto_form_no, date_str, doc_no, rev_no,
                         drawing_no, standard, description, penetrant_method, removal_method, 
                         brand_name, penetrant_type, developer_type, cleaner_type, 
                         surface_prep, time_exam, scope_exam, data_df, logo_width_inch, 
                         dict_joint_photos, photo_width_inch):
    
    doc = Document()
    
    # Atur Margin Halaman Cetak Standar Internasional A4
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(2.1)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)
        section.header_distance = Inches(0.4)
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)

    # -----------------------------------------------------------------------------------
    # 1. INTEGRASI KOP SURAT KE NATIVE WORD HEADER
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

    cell_left = kop_table.cell(0, 0).merge(kop_table.cell(1, 0))          
    cell_center = kop_table.cell(0, 1).merge(kop_table.cell(1, 1))        
    cell_right_top = kop_table.cell(0, 2).merge(kop_table.cell(0, 3))     
    cell_right_bottom = kop_table.cell(1, 2).merge(kop_table.cell(1, 3))  

    cell_left.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    p_left = cell_left.paragraphs[0]
    p_left.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if logo_left_bytes is not None:
        p_left.add_run().add_picture(logo_left_bytes, width=Inches(logo_width_inch))
    else:
        p_left.add_run("[ LOGO KIRI ]").font.color.rgb = RGBColor(160, 160, 160)

    cell_center.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    p_center = cell_center.paragraphs[0]
    p_center.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_center = p_center.add_run(str(project).upper())
    run_center.bold = True
    run_center.font.size = Pt(11)
    run_center.font.name = 'Arial'

    cell_right_top.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    p_rt = cell_right_top.paragraphs[0]
    p_rt.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if logo_right_top_bytes is not None:
        p_rt.add_run().add_picture(logo_right_top_bytes, width=Inches(logo_width_inch))
    else:
        p_rt.add_run("[ LOGO KANAN ATAS ]").font.color.rgb = RGBColor(160, 160, 160)

    cell_right_bottom.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    p_rb = cell_right_bottom.paragraphs[0]
    p_rb.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if logo_right_bottom_bytes is not None:
        p_rb.add_run().add_picture(logo_right_bottom_bytes, width=Inches(logo_width_inch))
    else:
        p_rb.add_run("[ LOGO KANAN BAWAH ]").font.color.rgb = RGBColor(160, 160, 160)

    meta_cells = kop_table.rows[2].cells
    for cell in meta_cells:
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        set_cell_margins(cell, top=30, bottom=30, start=100, end=100)

    meta_cells[0].paragraphs[0].text = f"Date: {date_str}"
