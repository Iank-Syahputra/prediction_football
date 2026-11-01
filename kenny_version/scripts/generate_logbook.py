"""
# ==============================================================================
# [MODULE GOAL & ROLE]
#   Official Logbook Generator for PT VINIX SEVEN AURUM (Week 3)
#   Fulfills:
#     - Template Google Doc: LOGBOOK MINGGUAN KEGIATAN MSIB BATCH 5 / FAST TRACK
#     - Student: Kenny Helim (BINUS University, Information System and Management)
#     - Divisi: Artificial Intelligence | Kelompok: 1
#     - Week: 3 (20 Oktober - 26 Oktober 2026)
#   Outputs:
#     - .docx (Word format matching template)
#     - .pdf (Formatted printable PDF)
#
# [INTENTIONAL DESIGN DECISIONS - DO NOT REMOVE]
#   - Zero internal leaks: Clean professional activity descriptions.
#   - Explicitly documents the Monday & Friday meetings (19.30 - 21.30 WIB).
# ==============================================================================
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def generate_logbook_docx(output_path: str):
    doc = docx.Document()
    
    # Page setup (A4, 1 inch margins)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    # Title Header
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
    
    # Instruction points
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
    
    # Student Info Table / Key-Values
    info_data = [
        ("Nama", ": Kenny Helim"),
        ("Universitas", ": Bina Nusantara University (BINUS University)"),
        ("Prodi", ": Information System and Management"),
        ("Divisi", ": Artificial Intelligence (Kelompok 1)"),
        ("Minggu ke", ": 3 (Tiga) - Periode: 20 Oktober s.d. 26 Oktober 2026")
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
    
    # Activities Table
    activities = [
        ("1", "Senin, 20 Oktober 2026", 
         "Briefing Awal Minggu & Meeting Kelompok 1 (19.30 - 21.30 WIB):\n"
         "• Mengikuti meeting koordinasi rutin kelompok via Google Meet untuk membahas pembagian tugas Week 3 Assignment: 'Kelompok Prediction International Football'.\n"
         "• Mendiskusikan rumusan masalah proyek: 'Prediksi Hasil Pertandingan dan Probabilitas Juara ASEAN Cup Menggunakan Algoritma Machine Learning Berdasarkan Statistik Historis Tim Nasional' (SDG 9: Industri, Inovasi, dan Infrastruktur).\n"
         "• Membagi peran teknis: saya ditugaskan untuk memimpin eksplorasi dataset Kaggle martj42 results.csv dan perancangan arsitektur pemodelan Machine Learning."),
         
        ("2", "Selasa, 21 Oktober 2026", 
         "Pengunduhan Dataset & Audit Integritas Skala Aktual:\n"
         "• Mengunduh dan memuat dataset riil international football results (1872 - 2026) yang terdiri dari 49.945 baris pertandingan.\n"
         "• Melakukan pemeriksaan missing values pada semua kolom (date, home_team, away_team, home_score, away_score, tournament, neutral) dan memastikan data 100% valid tanpa null.\n"
         "• Memfilter 3.782 pertandingan khusus yang melibatkan tim nasional regional ASEAN."),
         
        ("3", "Rabu, 22 Oktober 2026", 
         "Eksplorasi Data (EDA) Berbasis Hipotesis:\n"
         "• Menghitung distribusi target multiclass: Home Win (49.00%), Away Win (28.29%), dan Draw (22.71%).\n"
         "• Mengkuantifikasi Home Advantage Multiplier: tim tuan rumah secara statistik 1.73x lebih berpeluang menang dibandingkan tim tandang.\n"
         "• Menganalisis pengaruh status Venue Netral: saat bertanding di tempat netral, rasio Home Win turun dari 50.73% menjadi 44.22%, sedangkan Away Win melonjak ke 33.40%.\n"
         "• Menghasilkan grafik visualisasi EDA resolusi tinggi untuk bahan presentasi."),
         
        ("4", "Kamis, 23 Oktober 2026", 
         "Rekayasa Fitur Temporal & Barrier Anti-Leakage:\n"
         "• Merancang 19 fitur prediktor pra-laga yang mematuhi aturan ketat anti-leakage (semua fitur pada laga waktu T hanya boleh dihitung dari informasi sebelum T).\n"
         "• Menghitung rolling 5-match recent form points, rata-rata gol/kebobolan 5 laga terakhir, win rate historis kumulatif, serta rekor Head-to-Head (H2H).\n"
         "• Menerapkan Time-Based Split: Data era lama (1960 - 2020 / 38.288 laga) dialokasikan untuk Training Set, dan data era terbaru (2021 - 2026 / 6.162 laga riil) dialokasikan untuk Testing Set."),
         
        ("5", "Jumat, 24 Oktober 2026", 
         "Mentoring & Evaluasi Bersama Pak Aslan (19.30 - 21.30 WIB):\n"
         "• Menghadiri sesi kelas mentoring mingguan bersama Dosen/Mentor Pak Aslan.\n"
         "• Mempresentasikan progres EDA dan rancangan feature engineering kelompok 1.\n"
         "• Mendapatkan arahan dan masukan dari Pak Aslan mengenai penanganan bias kelas Draw, normalisasi fitur dengan StandardScaler, serta pemilihan model baseline pembanding (Decision Tree vs Random Forest).\n"
         "• Memulai pelatihan model multiclass classification di bawah supervisi mentor."),
         
        ("6", "Sabtu, 25 Oktober 2026", 
         "Benchmarking Model ML & Simulasi Juara ASEAN Cup:\n"
         "• Melatih 5 variasi model: Naive Majority Baseline (47.89%), Logistic Regression (58.00%), Decision Tree (57.43%), Gradient Boosting (57.85%), dan Random Forest (58.05%).\n"
         "• Model Random Forest (150 trees) terpilih sebagai model terbaik dengan presisi Away Win 60.0% dan recall Home Win 91.0% (+10.16% lift di atas baseline naif).\n"
         "• Membangun simulasi Monte Carlo 10.000 iterasi turnamen ASEAN Cup lengkap (Fase Grup A & B, Semifinal 2 Leg, dan Final 2 Leg) untuk menghasilkan leaderboard probabilitas juara."),
         
        ("7", "Minggu, 26 Oktober 2026", 
         "Finalisasi Laporan, Presentasi 12 Slide & Pengumpulan Form:\n"
         "• Menyelesaikan Jupyter Notebook resmi assignment (football_prediction_eda_and_ml.ipynb).\n"
         "• Menyusun naskah dan slide presentasi 12 slide mencakup latar belakang, metodologi, hasil EDA, evaluasi model, dan kontribusi terhadap target SDG 9.\n"
         "• Menguji jalannya aplikasi web interaktif simulasi pertandingan lokal.\n"
         "• Menyiapkan berkas logbook mingguan, kartu presensi kehadiran, dan bukti pengumpulan tugas mingguan.")
    ]
    
    table_act = doc.add_table(rows=len(activities) + 1, cols=3)
    table_act.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_act.autofit = False
    
    col_widths = [Inches(0.5), Inches(1.8), Inches(4.2)]
    headers = ["No", "Hari/Tanggal", "Deskripsi Kegiatan"]
    
    # Header row
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
        
        # Alternating background
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
    print(f"Saved DOCX logbook: {output_path}")

def generate_logbook_pdf(docx_path: str, output_pdf_path: str):
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
        spaceAfter=10
    )
    rule_style = ParagraphStyle(
        'RuleStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        textColor=colors.HexColor('#475569'),
        spaceAfter=3
    )
    meta_style = ParagraphStyle(
        'MetaStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12
    )
    meta_bold = ParagraphStyle(
        'MetaBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12
    )
    cell_style = ParagraphStyle(
        'CellStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5
    )
    cell_bold = ParagraphStyle(
        'CellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11
    )
    
    story = []
    story.append(Paragraph("LOGBOOK MINGGUAN KEGIATAN FAST TRACK", title_style))
    story.append(Paragraph("PT VINIX SEVEN AURUM", subtitle_style))
    story.append(Paragraph("1. Wajib diisi dengan kegiatan harian, contoh: briefing, apa yang dipelajari, mengerjakan tugas apa saja, diskusi kelompok, dll.", rule_style))
    story.append(Paragraph("2. Wajib dikumpulkan setiap minggu bersama dengan pengumpulan tugas.", rule_style))
    story.append(Spacer(1, 8))
    
    # Student metadata table
    meta_data = [
        [Paragraph("Nama", meta_bold), Paragraph(": Kenny Helim", meta_style)],
        [Paragraph("Universitas", meta_bold), Paragraph(": Bina Nusantara University (BINUS University)", meta_style)],
        [Paragraph("Prodi", meta_bold), Paragraph(": Information System and Management", meta_style)],
        [Paragraph("Divisi", meta_bold), Paragraph(": Artificial Intelligence (Kelompok 1)", meta_style)],
        [Paragraph("Minggu ke", meta_bold), Paragraph(": 3 (Tiga) - Periode: 20 Oktober s.d. 26 Oktober 2026", meta_style)],
    ]
    meta_t = Table(meta_data, colWidths=[100, 420])
    meta_t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(meta_t)
    story.append(Spacer(1, 10))
    
    # Activities data
    act_rows = [
        [Paragraph("<b>No</b>", cell_bold), Paragraph("<b>Hari/Tanggal</b>", cell_bold), Paragraph("<b>Deskripsi Kegiatan</b>", cell_bold)]
    ]
    
    activities_list = [
        ("1", "Senin, 20 Okt 2026", 
         "<b>Briefing Awal Minggu & Meeting Kelompok 1 (19.30 - 21.30 WIB):</b><br/>"
         "• Mengikuti meeting koordinasi kelompok via Zoom/Meet membahas pembagian tugas Week 3: International Football Prediction.<br/>"
         "• Menetapkan judul proyek: 'Prediksi Hasil Pertandingan dan Probabilitas Juara ASEAN Cup Menggunakan Machine Learning' (SDG 9: Industri, Inovasi, dan Infrastruktur).<br/>"
         "• Membagi peran teknis: saya ditugaskan memimpin eksplorasi dataset Kaggle martj42 dan perancangan pipeline ML."),
        ("2", "Selasa, 21 Okt 2026", 
         "<b>Pengunduhan Dataset & Audit Skala Aktual:</b><br/>"
         "• Mengunduh dan memuat dataset riil international football results (1872 - 2026) yang terdiri dari 49.945 baris pertandingan.<br/>"
         "• Memeriksa missing values (0 null), memverifikasi 337 tim nasional, dan memfilter 3.782 pertandingan regional ASEAN."),
        ("3", "Rabu, 22 Okt 2026", 
         "<b>Eksplorasi Data (EDA) Berbasis Hipotesis:</b><br/>"
         "• Menghitung distribusi target multiclass: Home Win (49.00%), Away Win (28.29%), dan Draw (22.71%).<br/>"
         "• Mengkuantifikasi Home Advantage Multiplier: tim kandang 1.73x lebih berpeluang menang.<br/>"
         "• Menganalisis penurunan kemenangan kandang di venue netral (turun ke 44.22%, Away Win naik ke 33.40%)."),
        ("4", "Kamis, 23 Okt 2026", 
         "<b>Rekayasa Fitur Temporal Anti-Leakage:</b><br/>"
         "• Merancang 19 fitur prediktor pra-laga yang mematuhi aturan ketat anti-leakage (semua fitur pada laga waktu T dihitung sebelum T).<br/>"
         "• Menghitung rolling 5-match form points, rata-rata gol/kebobolan, rasio kemenangan kumulatif, dan H2H.<br/>"
         "• Menerapkan Time-Based Split: Latih (1960 - 2020 / 38.288 laga) dan Uji (2021 - 2026 / 6.162 laga riil)."),
        ("5", "Jumat, 24 Okt 2026", 
         "<b>Mentoring & Evaluasi Bersama Pak Aslan (19.30 - 21.30 WIB):</b><br/>"
         "• Mengikuti sesi kelas mentoring mingguan bersama Dosen/Mentor Pak Aslan.<br/>"
         "• Mempresentasikan progres EDA dan rancangan rekayasa fitur temporal anti-leakage.<br/>"
         "• Mendapatkan masukan mentor mengenai penanganan draw bias, StandardScaler, dan pemilihan algoritma baseline.<br/>"
         "• Memulai pelatihan model multiclass classification di bawah supervisi mentor."),
        ("6", "Sabtu, 25 Okt 2026", 
         "<b>Benchmarking Model ML & Simulasi Juara ASEAN Cup:</b><br/>"
         "• Melatih 5 model: Naive Baseline (47.89%), Logistic Regression (58.00%), Decision Tree (57.43%), Gradient Boosting (57.85%), dan Random Forest (58.05%).<br/>"
         "• Model Random Forest meraih akurasi 58.05% (+10.16% lift di atas baseline naif).<br/>"
         "• Mengeksekusi simulasi Monte Carlo 10.000 iterasi turnamen ASEAN Cup 10 tim untuk memetakan probabilitas juara."),
        ("7", "Minggu, 26 Okt 2026", 
         "<b>Finalisasi Laporan, Presentasi 12 Slide & Pengumpulan:</b><br/>"
         "• Menyelesaikan Jupyter Notebook resmi assignment (football_prediction_eda_and_ml.ipynb).<br/>"
         "• Menyusun naskah presentasi 12 slide dan menguji aplikasi web interaktif di http://localhost:38800.<br/>"
         "• Mengompilasi berkas logbook mingguan, kartu presensi, dan bukti penyerahan form.")
    ]
    
    for no, day, desc in activities_list:
        act_rows.append([
            Paragraph(f"<para align=center>{no}</para>", cell_style),
            Paragraph(f"<b>{day}</b>", cell_bold),
            Paragraph(desc, cell_style)
        ])
        
    act_table = Table(act_rows, colWidths=[25, 110, 385])
    act_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
    ]))
    story.append(act_table)
    
    doc.build(story)
    print(f"Saved PDF logbook: {output_pdf_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_dir = os.path.join(base_dir, "UPLOAD_BERKAS_FORM_MINGGU_3")
    os.makedirs(out_dir, exist_ok=True)
    
    docx_file = os.path.join(out_dir, "Logbook_Minggu_3_Kenny_Helim_AI.docx")
    pdf_file = os.path.join(out_dir, "Logbook_Minggu_3_Kenny_Helim_AI.pdf")
    
    generate_logbook_docx(docx_file)
    generate_logbook_pdf(docx_file, pdf_file)
