def generate_docx_report(logo_bytes, client, project, equipment, auto_form_no, date_str, 
                         drawing_no, standard, description, penetrant_method, removal_method, 
                         brand_name, penetrant_type, developer_type, cleaner_type, 
                         surface_prep, time_exam, scope_exam, data_df):
    
    doc = Document()
    
    # 1. ATUR MARGIN HALAMAN LEBIH TIPIS (0.5 top/bottom, 0.4 left/right) AGAR PRESISI SEPERTI GAMBAR
    for section in doc.sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.4)
        section.right_margin = Inches(0.4)

    # Set Default Font Global ke Arial 8.5 Pt (Standar Dokumen Teknik)
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Arial'
    font.size = Pt(8.5)

    # -----------------------------------------------------------------------------------
    # TABLE 1: KOP LOGO PERUSAHAAN & ARSITEKTUR BRANDING UTAMA
    # -----------------------------------------------------------------------------------
    table_top = doc.add_table(rows=2, cols=4)
    table_top.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_top.autofit = False

    widths_top = [Inches(1.8), Inches(3.8), Inches(0.9), Inches(1.0)]
    for row in table_top.rows:
        for i, w in enumerate(widths_top):
            row.cells[i].width = w

    # Gabungkan baris kanan atas untuk Sub-Logo Kontraktor/Consultant
    base_cell = table_top.rows[0].cells[2]
    base_cell.merge(table_top.rows[0].cells[3])

    # Isi Teks Kop Kiri (Logo Trakindo Utama)
    p_logo = table_top.rows[0].cells[0].paragraphs[0]
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_logo = p_logo.add_run(client)
    r_logo.bold = True
    r_logo.font.size = Pt(11)

    # Isi Judul Tengah Kop
    p_title = table_top.rows[0].cells[1].paragraphs[0]
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run(project)
    r_title.bold = True
    r_title.font.size = Pt(11)

    # Isi Kop Kanan (Sub Kontraktor)
    p_rlogo = table_top.rows[0].cells[2].paragraphs[0]
    p_rlogo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_rlogo = p_rlogo.add_run("DAMAC DIGITAL\nCUSHMAN & WAKEFIELD")
    r_rlogo.font.size = Pt(8)

    # Baris Ke-2 Metadata Kop Dokumen
    table_top.rows[1].cells[0].text = f"  Date: {date_str}"
    table_top.rows[1].cells[1].text = "  Doc No.:"
    table_top.rows[1].cells[2].text = "  Rev. 0"
    table_top.rows[1].cells[3].text = "  Page 1 of 1"

    # Dekorasi Cell Kop Surat
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

    # -----------------------------------------------------------------------------------
    # TABLE 2: INSPECTION METADATA & PARAMETER CHECKBOXES (11 Baris)
    # -----------------------------------------------------------------------------------
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

    # Peta Parameter bertipe pilihan Checkbox [x] sesuai kondisi input user
    param_configs = [
        ("PENETRANT METHOD", f"{'[x]' if penetrant_method == 'VISIBLE' else '[ ]'} VISIBLE      {Format_Check('FLUORECENT', penetrant_method)} FLUORECENT"),
        ("REMOVAL METHOD", f"{Format_Check('SOLVENT REMOVABLE', removal_method)} SOLVENT REMOVABLE   {Format_Check('WATER WASHABLE', removal_method)} WATER WASHABLE   {Format_Check('POST EMULSIFIEBLE', removal_method)} POST EMULSIFIEBLE"),
        ("BRAND NAME", f"{brand_name}   |   PENETRANT: {penetrant_type}   |   DEVELOPER: {developer_type}   |   CLEANER: {cleaner_type}"),
        ("SURFACE PREPARATION", f"{Format_Check('AS WELDED', surface_prep)} AS WELDED      {Format_Check('MACHINING', surface_prep)} MACHINING      {Format_Check('GRINDING', surface_prep)} GRINDING      {Format_Check('OTHER', surface_prep)} OTHER"),
        ("TIME OF EXAMINATION", f"{Format_Check('AFTER WELDING', time_exam)} AFTER WELDING      {Format_Check('AFTER HYDROTEST', time_exam)} AFTER HYDROTEST      {Format_Check('AFTER PWHT', time_exam)} AFTER PWHT      {Format_Check('OTHER', time_exam)} OTHER"),
        ("SCOPE OF EXAMINATION", f"{Format_Check('BASE METAL', scope_exam)} BASE METAL      {Format_Check('WELD METAL', scope_exam)} WELD METAL      {Format_Check('BACK CHIPPING', scope_exam)} BACK CHIPPING      {Format_Check('OTHER', scope_exam)} OTHER"),
    ]

    for idx, (label, val_string) in enumerate(param_configs):
        row = table_meta.rows[4 + idx]
        # Gabungkan kolom 1, 2, dan 3 agar area kanan memanjang penuh
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

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # -----------------------------------------------------------------------------------
    # TABLE 3: WELD INSPECTION RESULT DATA (2 baris Header bertingkat)
    # -----------------------------------------------------------------------------------
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

    # Setup Header Bawah khusus Result Split
    table_data.rows[1].cells[3].text = "ACC"
    table_data.rows[1].cells[4].text = "REJECT"

    # Jalankan Vertikal Merge otomatis untuk Kolom Non-Result
    for c_idx in [0, 1, 2, 5, 6]:
        table_data.rows[0].cells[c_idx].merge(table_data.rows[1].cells[c_idx])

    # Styling Warna Abu-Abu Gelap pada Header Tabel Las
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
        # Set alignment lebar kolom baru agar konsisten
        for i, w in enumerate(widths_data):
            row.cells[i].width = w
            
        row.cells[0].text = " " + str(row_data["PART NAME"])
        row.cells[1].text = str(row_data["WELD NO"])
        row.cells[2].text = str(row_data["THICKNESS (MM)"])
        row.cells[3].text = "[x]" if row_data["RESULT"] == "ACC" else "[ ]"
        row.cells[4].text = "[x]" if row_data["RESULT"] == "REJECT" else "[ ]"
        row.cells[5].text = str(row_data["TYPES OF DISCONTINUITIES"])
        row.cells[6].text = " " + str(row_data["REMARKS"])
        
        # Center alignment data kolom tengah
        for c_idx in [1, 2, 3, 4, 5]:
            row.cells[c_idx].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Menambahkan 10 baris kosong tambahan di bawahnya untuk ruang tulis manual lapangan (Sesuai Gambar)
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

    # -----------------------------------------------------------------------------------
    # TABLE 4: SIGNATURE SIGN OFF BOXES (Blok Grid 4 Kolom)
    # -----------------------------------------------------------------------------------
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

    bio = io.BytesIO()
    doc.save(bio)
    bio.seek(0)
    return bio

# Fungsi pembantu untuk efisiensi marking checkbox dinamis
def Format_Check(target, current_value):
    return "[x]" if target == current_value else "[ ]"
