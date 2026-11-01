"""
Official Logbook Generator for PT VINIX SEVEN AURUM (Week 4)
Student: Kenny Helim (BINUS University, Information System and Management)
Divisi: Artificial Intelligence | Kelompok: 1
Week: 4 (27 Oktober - 2 November 2026)
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def generate_logbook_week4_docx(output_path: str):
    doc = docx.Document()
    
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    p_title1 = doc.add_paragraph()
    p_title1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run1 = p_title1.add_run("LOGBOOK MINGGUAN KEGIATAN FAST TRACK")
    run1.bold = True
    run1.font.name = "Arial"
    run1.font.size = Pt(13)
    
    p_title2 = doc.add_paragraph()
    p_title2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run2 = p_title2.add_run("PT VINIX SEVEN AURUM")
    run2.bold = True
    run2.font.name = "Arial"
    run2.font.size = Pt(12)
    
    p_rule1 = doc.add_paragraph()
    p_rule1.paragraph_format.space_before = Pt(8)
    p_rule1.paragraph_format.space_after = Pt(2)
    r_rule1 = p_rule1.add_run("1. Wajib diisi dengan kegiatan harian, contoh: briefing, apa yang dipelajari, mengerjakan tugas apa saja, diskusi kelompok, dll.")
    r_rule1.font.name = "Arial"
    r_rule1.font.size = Pt(9.5)
    r_rule1.font.italic = True
    
    p_rule2 = doc.add_paragraph()
    p_rule2.paragraph_format.space_before = Pt(0)
    p_rule2.paragraph_format.space_after = Pt(14)
    r_rule2 = p_rule2.add_run("2. Wajib dikumpulkan setiap minggu bersama dengan pengumpulan tugas.")
    r_rule2.font.name = "Arial"
    r_rule2.font.size = Pt(9.5)
    r_rule2.font.italic = True
    
    info_data = [
        ("Nama", ": Kenny Helim"),
        ("Universitas", ": Bina Nusantara University (BINUS University)"),
        ("Prodi", ": Information System and Management"),
        ("Divisi", ": Artificial Intelligence (Kelompok 1)"),
        ("Periode Magang", ": 4 Bulan (MUTLAK)"),
        ("Minggu ke", ": 4 (Empat) - Periode: 27 Oktober s.d. 02 November 2026")
    ]
    
    table_info = doc.add_table(rows=len(info_data), cols=2)
    table_info.alignment = WD_TABLE_ALIGNMENT.LEFT
    table_info.autofit = False
    
    for idx, (label, val) in enumerate(info_data):
        row = table_info.rows[idx]
        cell_lbl, cell_val = row.cells[0], row.cells[1]
        cell_lbl.width = Inches(1.5)
        cell_val.width = Inches(5.0)
        
        p_l = cell_lbl.paragraphs[0]
        p_l.paragraph_format.space_after = Pt(2)
        r_l = p_l.add_run(label)
        r_l.bold = True
        r_l.font.name = "Arial"
        r_l.font.size = Pt(10)
        
        p_v = cell_val.paragraphs[0]
        p_v.paragraph_format.space_after = Pt(2)
        r_v = p_v.add_run(val)
        r_v.font.name = "Arial"
        r_v.font.size = Pt(10)
        
    doc.add_paragraph().paragraph_format.space_after = Pt(10)
    
    activities = [
        ("1", "Senin, 27 Oktober 2026", 
         "Evaluasi Mentoring & Penyelarasan Problem Statement:\n"
         "• Mengikuti mentoring pengantar Week 4 mengenai standar workflow AI/ML profesional dan kriteria model bertanggung jawab.\n"
         "• Menyelaraskan Problem Statement proyek: mengatasi bias subjektif komentator/fans dan ilusi kepastian prediksi sepak bola dengan membangun rantai logika probabilistik berbasis data historis (SDG 9).\n"
         "• Merancang arsitektur data pipeline dengan batas waktu tegas (cut-off: 2024-12-08) guna menjamin zero data leakage."),
         
        ("2", "Selasa, 28 Oktober 2026", 
         "Rekayasa Sinyal Pra-Laga & Pembobotan Elo:\n"
         "• Membangun sistem rating kekuatan tim dinamis (Elo rating) yang terkalibrasi dari 48.093 laga historis sebelum 8 Desember 2024.\n"
         "• Mengisolasi 4 pilar fitur pra-laga murni: Kekuatan Elo, Momentum Form (rata-rata poin & selisih gol 5 laga terakhir), Sejarah H2H, dan Konteks Laga (kandang vs netral).\n"
         "• Mengunci data adu penalti (shootouts) agar tidak bocor ke dalam fitur latihan model."),
         
        ("3", "Rabu, 29 Oktober 2026", 
         "Benchmarking Model Probabilistik & Metrik Log Loss:\n"
         "• Menguji model pada 52 laga kompetisi ASEAN menggunakan metrik evaluasi ketat Multi-Class Log Loss.\n"
         "• Hasil evaluasi: Tebakan Buta (Prior) mencatat Log Loss 1.0686, Faktor Tunggal Elo Murni 0.8340, dan Model Final (Logistic Full Interaksi) mencapai skor terbaik 0.8198.\n"
         "• Membuktikan bahwa interaksi fitur pra-laga memberikan sinyal prediktif nyata tanpa overconfidence."),
         
        ("4", "Kamis, 30 Oktober 2026", 
         "Eksperimen Monte Carlo 10.000 Iterasi & Backtesting:\n"
         "• Menjalankan mesin simulasi Monte Carlo 10.000 putaran virtual turnamen ASEAN Championship 2026.\n"
         "• Distribusi peluang juara: Thailand 30.97% [30.07%-31.88%], Indonesia 27.34% [26.48%-28.22%], Vietnam 21.73% [20.93%-22.55%], Malaysia 15.40% [14.71%-16.12%].\n"
         "• Melakukan backtest pada 5 edisi turnamen masa lalu (2018-2024): membuktikan 4 dari 5 juara aktual selalu berada di posisi Top-3 simulasi model (rata-rata peluang 25.22%)."),
         
        ("5", "Jumat, 30 Oktober 2026", 
         "Mentoring Sesi 6 Bersama Pak Aslan Alwi (19.30 - 21.30 WIB):\n"
         "• Menghadiri kelas mentoring live Jumat malam bersama Pak Aslan Alwi dan rekan-rekan Divisi AI.\n"
         "• Menganalisis arahan Pak Aslan terkait target pihak yang paling terbantu (tim nasional/liga underdogs yang memiliki probabilitas rendah agar dapat merancang taktik perlawanan baru berbasis data empiris).\n"
         "• Membandingkan arsitektur AI: pendekatan computer vision (YOLO11 deteksi lubang jalan) vs pendekatan probabilistik numerik sepak bola (Logistic Interaction + Monte Carlo)."),
         
        ("6", "Sabtu, 31 Oktober 2026", 
         "Pengembangan Dashboard Streamlit Interaktif & Adaptabilitas Data:\n"
         "• Membangun dashboard analitik interaktif berbasis Streamlit yang konsisten dengan problem statement.\n"
         "• Menambahkan fitur adaptabilitas dinamis: pengguna dapat mengunggah file CSV pertandingan baru atau memodifikasi parameter tim, dan sistem secara otomatis menghitung ulang Elo rating, form, serta probabilitas juara Monte Carlo secara instan tanpa error.\n"
         "• Mengintegrasikan visualisasi rantai probabilitas dan event ticker laga."),
         
        ("7", "Minggu, 01 November 2026", 
         "Finalisasi Slide Deck 11 Halaman & Persiapan Presentasi Akhir:\n"
         "• Menyusun slide deck presentasi final 11 halaman (format widescreen 16:9) sesuai panduan metodologi data-ke-probabilitas.\n"
         "• Mengompilasi laporan eksekutif master PDF lengkap dengan Trust Triad (Data, Model, Simulasi) dan transparansi limitasi model.\n"
         "• Menyiapkan skrip Q&A defense untuk jadwal presentasi final project (2 - 6 November 2026).")
    ]
    
    table_act = doc.add_table(rows=len(activities) + 1, cols=3)
    table_act.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_act.autofit = False
    
    col_widths = [Inches(0.5), Inches(1.8), Inches(4.2)]
    headers = ["No", "Hari/Tanggal", "Deskripsi Kegiatan"]
    
    hdr_cells = table_act.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].width = col_widths[i]
        set_cell_background(hdr_cells[i], "1E293B")
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h)
        run.bold = True
        run.font.name = "Arial"
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(255, 255, 255)
        
    for idx, (no, day, desc) in enumerate(activities):
        row_cells = table_act.rows[idx + 1].cells
        row_cells[0].width = col_widths[0]
        row_cells[1].width = col_widths[1]
        row_cells[2].width = col_widths[2]
        
        if idx % 2 == 1:
            set_cell_background(row_cells[0], "F8FAFC")
            set_cell_background(row_cells[1], "F8FAFC")
            set_cell_background(row_cells[2], "F8FAFC")
            
        p0 = row_cells[0].paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r0 = p0.add_run(no)
        r0.font.name = "Arial"
        r0.font.size = Pt(9)
        
        p1 = row_cells[1].paragraphs[0]
        r1 = p1.add_run(day)
        r1.bold = True
        r1.font.name = "Arial"
        r1.font.size = Pt(9)
        
        p2 = row_cells[2].paragraphs[0]
        r2 = p2.add_run(desc)
        r2.font.name = "Arial"
        r2.font.size = Pt(8.5)
        
    doc.save(output_path)
    print(f"Saved DOCX logbook Week 4: {output_path}")

def generate_logbook_week4_pdf(output_pdf_path: str):
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=12,
        alignment=1,
        spaceAfter=2
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        alignment=1,
        spaceAfter=8
    )
    rule_style = ParagraphStyle(
        'RuleStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        textColor=colors.HexColor('#475569'),
        spaceAfter=2
    )
    meta_style = ParagraphStyle(
        'MetaStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11
    )
    meta_bold = ParagraphStyle(
        'MetaBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11
    )
    cell_style = ParagraphStyle(
        'CellStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10
    )
    cell_bold = ParagraphStyle(
        'CellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5
    )
    header_style = ParagraphStyle(
        'HdrStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        textColor=colors.white,
        alignment=1
    )
    
    story = []
    story.append(Paragraph("LOGBOOK MINGGUAN KEGIATAN FAST TRACK", title_style))
    story.append(Paragraph("PT VINIX SEVEN AURUM", subtitle_style))
    story.append(Paragraph("1. Wajib diisi dengan kegiatan harian, contoh: briefing, apa yang dipelajari, mengerjakan tugas apa saja, diskusi kelompok, dll.", rule_style))
    story.append(Paragraph("2. Wajib dikumpulkan setiap minggu bersama dengan pengumpulan tugas.", rule_style))
    story.append(Spacer(1, 8))
    
    info_table_data = [
        [Paragraph("Nama", meta_bold), Paragraph(": Kenny Helim", meta_style)],
        [Paragraph("Universitas", meta_bold), Paragraph(": Bina Nusantara University (BINUS University)", meta_style)],
        [Paragraph("Prodi", meta_bold), Paragraph(": Information System and Management", meta_style)],
        [Paragraph("Divisi", meta_bold), Paragraph(": Artificial Intelligence (Kelompok 1)", meta_style)],
        [Paragraph("Periode Magang", meta_bold), Paragraph(": 4 Bulan (MUTLAK)", meta_style)],
        [Paragraph("Minggu ke", meta_bold), Paragraph(": 4 (Empat) - Periode: 27 Oktober s.d. 02 November 2026", meta_style)]
    ]
    t_info = Table(info_table_data, colWidths=[90, 430])
    t_info.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_info)
    story.append(Spacer(1, 10))
    
    activities = [
        ("1", "Senin, 27 Okt 2026", 
         "<b>Evaluasi Mentoring & Penyelarasan Problem Statement:</b><br/>"
         "• Mengikuti mentoring pengantar Week 4 mengenai standar workflow AI/ML profesional.<br/>"
         "• Menyelaraskan Problem Statement: mengatasi bias subjektif dan ilusi kepastian prediksi sepak bola dengan rantai logika probabilistik (SDG 9).<br/>"
         "• Merancang arsitektur pipeline data dengan cut-off 2024-12-08 (zero leakage)."),
         
        ("2", "Selasa, 28 Okt 2026", 
         "<b>Rekayasa Sinyal Pra-Laga & Pembobotan Elo:</b><br/>"
         "• Membangun sistem rating kekuatan tim dinamis (Elo) dari 48.093 laga historis sebelum 8 Des 2024.<br/>"
         "• Mengisolasi 4 pilar fitur pra-laga: Kekuatan Elo, Form 5 laga, Sejarah H2H, dan Konteks Laga (kandang vs netral).<br/>"
         "• Mengunci data adu penalti (shootouts) agar tidak bocor ke dalam data latih."),
         
        ("3", "Rabu, 29 Okt 2026", 
         "<b>Benchmarking Model Probabilistik & Metrik Log Loss:</b><br/>"
         "• Menguji model pada 52 laga kompetisi ASEAN menggunakan metrik ketat Multi-Class Log Loss.<br/>"
         "• Hasil evaluasi: Tebakan Buta (1.0686), Elo Murni (0.8340), dan <b>Model Final Logistic Full Interaksi mencapai skor terbaik 0.8198</b>.<br/>"
         "• Membuktikan interaksi fitur pra-laga memberi sinyal prediktif nyata tanpa overconfidence."),
         
        ("4", "Kamis, 30 Okt 2026", 
         "<b>Eksperimen Monte Carlo 10.000 Iterasi & Backtesting:</b><br/>"
         "• Menjalankan simulasi Monte Carlo 10.000 putaran turnamen ASEAN Championship 2026.<br/>"
         "• Peluang juara: Thailand 30.97%, Indonesia 27.34%, Vietnam 21.73%, Malaysia 15.40%.<br/>"
         "• Backtest 5 edisi (2018-2024): 4 dari 5 juara aktual berada di Top-3 simulasi (rata-rata peluang 25.22%)."),
         
        ("5", "Jumat, 30 Okt 2026", 
         "<b>Mentoring Sesi 6 Bersama Pak Aslan Alwi (19.30 - 21.30 WIB):</b><br/>"
         "• Menghadiri kelas mentoring live Jumat malam bersama Pak Aslan Alwi.<br/>"
         "• Menganalisis arahan Pak Aslan terkait target pihak yang paling terbantu (tim nasional/liga underdogs yang berpeluang rendah untuk merancang taktik perlawanan baru).<br/>"
         "• Membandingkan arsitektur AI: computer vision (YOLO11) vs model probabilistik numerik."),
         
        ("6", "Sabtu, 31 Okt 2026", 
         "<b>Dashboard Streamlit Interaktif & Adaptabilitas Dinamis:</b><br/>"
         "• Membangun dashboard analitik interaktif berbasis Streamlit yang selaras dengan problem statement.<br/>"
         "• Menambahkan fitur adaptabilitas dinamis: pengguna dapat mengunggah CSV data laga terbaru / mengubah parameter tim dengan kalkulasi ulang real-time pada Elo rating & simulasi Monte Carlo.<br/>"
         "• Visualisasi rantai probabilitas dan event ticker laga."),
         
        ("7", "Minggu, 01 Nov 2026", 
         "<b>Finalisasi Slide Deck 11 Halaman & Persiapan Sidang Akhir:</b><br/>"
         "• Menyusun slide deck presentasi final 11 halaman sesuai panduan metodologi data-ke-probabilitas.<br/>"
         "• Mengompilasi laporan eksekutif master PDF lengkap dengan Trust Triad dan transparansi limitasi.<br/>"
         "• Menyiapkan skrip Q&A defense untuk jadwal presentasi final project (2 - 6 November 2026).")
    ]
    
    table_data = [[
        Paragraph("No", header_style),
        Paragraph("Hari/Tanggal", header_style),
        Paragraph("Deskripsi Kegiatan", header_style)
    ]]
    
    for no, day, desc in activities:
        table_data.append([
            Paragraph(no, cell_bold),
            Paragraph(day, cell_bold),
            Paragraph(desc, cell_style)
        ])
        
    t_act = Table(table_data, colWidths=[25, 110, 385])
    t_act.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')])
    ]))
    story.append(t_act)
    
    doc.build(story)
    print(f"Saved PDF logbook Week 4: {output_pdf_path}")

if __name__ == "__main__":
    upload_dir = r"C:\Users\Kenny\.gemini\antigravity-ide\scratch\school_football_prediction\UPLOAD_BERKAS_FORM_MINGGU_4"
    os.makedirs(upload_dir, exist_ok=True)
    
    desk_dir = r"C:\Users\Kenny\Desktop\DESKTOP_ORGANIZED_HUB\06_Folders_And_Packages\Divisi Artificial Intelligence Starterpack kelompok 1"
    os.makedirs(desk_dir, exist_ok=True)
    
    desk_alt = r"C:\Users\Kenny\Desktop\Divisi Artificial Intelligence Starterpack kelompok 1"
    if os.path.exists(desk_alt):
        os.makedirs(desk_alt, exist_ok=True)
    
    filename_docx = "Logbook_Minggu_4_Kenny_Helim_AI.docx"
    filename_pdf = "LOGBOOK (Minggu 4) Kegiatan Fast Track - Divisi Artificial Intelligence - Kenny Helim.pdf"
    
    upload_docx = os.path.join(upload_dir, filename_docx)
    upload_pdf = os.path.join(upload_dir, filename_pdf)
    
    generate_logbook_week4_docx(upload_docx)
    generate_logbook_week4_pdf(upload_pdf)
    
    import shutil
    shutil.copy(upload_docx, os.path.join(desk_dir, filename_docx))
    shutil.copy(upload_pdf, os.path.join(desk_dir, filename_pdf))
    if os.path.exists(desk_alt):
        shutil.copy(upload_docx, os.path.join(desk_alt, filename_docx))
        shutil.copy(upload_pdf, os.path.join(desk_alt, filename_pdf))
    print("Logbook Week 4 generated and synchronized to all targets successfully.")

