"""
# ==============================================================================
# [MODULE GOAL & ROLE]
#   Assignment Presentation PDF Generator for Week 3
#   Fulfills:
#     - User request: "klo assignment oppt tp di pdf ato y susia diminta buatin"
#     - Week 3 Assignment: Kelompok Prediction International Football
#     - High-aesthetic 12-slide landscape presentation PDF
# ==============================================================================
"""

import os
import shutil
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak

def build_assignment_pdf(output_pdf: str, artifacts_dir: str):
    # Landscape A4 (842 x 595 points)
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=landscape(A4),
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    slide_title = ParagraphStyle(
        'SlideTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=4
    )
    slide_subtitle = ParagraphStyle(
        'SlideSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#2563EB'),
        spaceAfter=14
    )
    body_text = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14.5,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=8
    )
    bullet_text = ParagraphStyle(
        'BulletText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=4
    )
    header_badge = ParagraphStyle(
        'HeaderBadge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        textColor=colors.HexColor('#64748B'),
        spaceAfter=6
    )

    story = []

    # SLIDE 1: Cover Slide
    story.append(Paragraph("WEEK 3 ASSIGNMENT • DIVISI ARTIFICIAL INTELLIGENCE (VINIX7)", header_badge))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Prediksi Hasil Pertandingan Sepak Bola Internasional & Probabilitas Juara ASEAN Cup", slide_title))
    story.append(Paragraph("Pemetaan Masalah, Eksplorasi Data (EDA), dan Pendekatan Machine Learning Berbasis Statistik Historis", slide_subtitle))
    story.append(Spacer(1, 15))
    
    cover_data = [
        [Paragraph("<b>Target SDG</b>", bullet_text), Paragraph(": <b>SDG 9: Industri, Inovasi, dan Infrastruktur</b>", bullet_text)],
        [Paragraph("<b>Dosen / Mentor</b>", bullet_text), Paragraph(": <b>Pak Aslan</b> (Sesi Mentoring Hari Jumat)", bullet_text)],
        [Paragraph("<b>Kelompok</b>", bullet_text), Paragraph(": <b>Kelompok 1 - Artificial Intelligence</b>", bullet_text)],
        [Paragraph("<b>Anggota Tim</b>", bullet_text), Paragraph(
            ": 1. <b>Kenny Helim</b> - BINUS University (Information System & Management)<br/>"
            "  2. <b>Arya Wicaksana</b> - Universitas Esa Unggul (Teknik Informatika)<br/>"
            "  3. <b>Muhammad Ihram Syahputra</b> - Universitas Halu Oleo (Ilmu Komputer)<br/>"
            "  4. <b>Gisela Venska Millennia</b> - President University (Information System)<br/>"
            "  5. <b>Christian</b> - BINUS University (Information Systems)", bullet_text)],
        [Paragraph("<b>Periode Program</b>", bullet_text), Paragraph(": 6 Oktober - 6 November 2026", bullet_text)]
    ]
    t_cover = Table(cover_data, colWidths=[120, 640])
    t_cover.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
    ]))
    story.append(t_cover)
    story.append(PageBreak())

    # SLIDE 2: Keterbatasan Analisis Manual vs Pendekatan AI
    story.append(Paragraph("SLIDE 02 / 15 • LATAR BELAKANG MASALAH", header_badge))
    story.append(Paragraph("Keterbatasan Analisis Manual vs. Skalabilitas Otomasi AI", slide_title))
    story.append(Paragraph("Mengapa Analisis Tradisional Gagal Menghadapi Volume Data Sepak Bola Modern?", slide_subtitle))
    
    comp_data = [
        [Paragraph("<b>Kondisi Analisis Manual (Tradisional)</b>", bullet_text), Paragraph("<b>Pendekatan Machine Learning (Modern AI)</b>", bullet_text)],
        [Paragraph("• <b>Proses Lambat:</b> Membuka spreadsheet CSV puluhan ribu baris secara manual.", bullet_text),
         Paragraph("• <b>Otomatisasi Penuh:</b> Ekstraksi fitur instan (form 5 laga, H2H, selisih gol).", bullet_text)],
        [Paragraph("• <b>Rentan Kesalahan:</b> Perhitungan agregasi rawan keliru akibat human error.", bullet_text),
         Paragraph("• <b>Presisi & Konsisten:</b> Terstandarisasi melalui formula matematis yang dapat diuji ulang.", bullet_text)],
        [Paragraph("• <b>Bias Subjektif:</b> Sangat terpengaruh oleh fanatisme atau intuisi suporter semata.", bullet_text),
         Paragraph("• <b>Objektif & Terukur:</b> Keputusan didasarkan pada bobot probabilitas empiris data historis.", bullet_text)]
    ]
    t_comp = Table(comp_data, colWidths=[380, 380])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#FEF2F2')),
        ('BACKGROUND', (1,0), (1,-1), colors.HexColor('#F0FDF4')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#E2E8F0')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_comp)
    story.append(PageBreak())

    # SLIDE 3: Ruang Lingkup dan Ekspektasi Sistem
    story.append(Paragraph("SLIDE 03 / 15 • RUANG LINGKUP & TARGET PENGGUNA", header_badge))
    story.append(Paragraph("Mendefinisikan Ruang Lingkup dan Ekspektasi Sistem", slide_title))
    story.append(Paragraph("Pertanyaan Inti, Batasan Realitas (Scope), dan Pihak Terdampak", slide_subtitle))
    story.append(Paragraph("<b>1. Pertanyaan Inti Penelitian:</b> Dapatkah data pertandingan historis membantu memperkirakan hasil pertandingan internasional berikutnya dan memetakan probabilitas juara turnamen regional secara objektif?", body_text))
    story.append(Paragraph("<b>2. Batasan Realitas (Scope):</b> Sistem berfungsi murni sebagai <i>analitik baseline dan decision-support system</i>. Sistem ini tidak dirancang sebagai ramalan mutlak atau instrumen perjudian, melainkan kalkulasi probabilitas matematis.", body_text))
    story.append(Paragraph("<b>3. Pihak Terdampak (Audiens Sasaran):</b>", body_text))
    story.append(Paragraph("• <b>Analis & Staf Kepelatihan Federasi:</b> Menilai komparasi performa lawan sebelum laga kompetitif.", bullet_text))
    story.append(Paragraph("• <b>Jurnalis & Media Olahraga:</b> Menyajikan ringkasan statistik berbobot bagi pembaca.", bullet_text))
    story.append(Paragraph("• <b>Pengembang Aplikasi Sepak Bola:</b> Integrasi API prediksi skor dan turnamen berbasis AI.", bullet_text))
    story.append(PageBreak())

    
    # SLIDE 04: Workflow AI/ML yang Profesional (VINIX7 Standard)
    story.append(Paragraph("SLIDE 04 / 15 - STANDAR WORKFLOW VINIX7", header_badge))
    story.append(Paragraph("Workflow AI/ML yang Profesional (Sesi Mentoring Live)", slide_title))
    story.append(Paragraph("Gunakan alur ini agar proyek tidak hanya 'jalan', tetapi juga bisa dipertanggungjawabkan", slide_subtitle))
    
    wf_data = [
        [Paragraph("<b>01. DEFINE</b><br/>Problem &amp; Goal: Menentukan target prediksi (Win/Draw/Loss) dan dampak bagi SDG 9 serta federasi.", bullet_text),
         Paragraph("<b>02. PREPARE</b><br/>Clean Data: Pembersihan 49.945 laga, penanganan missing values, dan audit anti-leakage temporal.", bullet_text),
         Paragraph("<b>03. MODEL</b><br/>Train &amp; Compare: Benchmarking multi-model (Logistic Regression, Random Forest, Gradient Boosting).", bullet_text)],
        [Paragraph("<b>04. EVALUATE</b><br/>Metric &amp; Error: Analisis F1-Score Macro, Confusion Matrix, dan evaluasi bias imbalanced classes.", bullet_text),
         Paragraph("<b>05. EXPLAIN</b><br/>Insight &amp; Limitation: Penjelasan Feature Importance, dampak home advantage, dan limitasi cedera pemain.", bullet_text),
         Paragraph("<b>06. PRESENT</b><br/>Actionable Solution: Aplikasi web interaktif 1-click, REST API lokal, dan simulasi turnamen Monte Carlo.", bullet_text)]
    ]
    t_wf = Table(wf_data, colWidths=[253, 253, 253])
    t_wf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_wf)
    story.append(Spacer(1, 10))
    story.append(Paragraph("<i>Catatan Kuliah Live: Disampaikan langsung oleh Mentor Bimo Rizki Abdusshamad &amp; Pak Aslan pada sesi Fast Track MSIB.</i>", body_text))
    story.append(PageBreak())

    # SLIDE 05: Kriteria Model AI/ML yang Bagus
    story.append(Paragraph("SLIDE 05 / 15 - KRITERIA KUALITAS MODEL", header_badge))
    story.append(Paragraph("Kriteria Model AI/ML yang Bagus &amp; Bertanggung Jawab", slide_title))
    story.append(Paragraph("Model yang bagus bukan hanya akurasinya tinggi (Prinsip Integritas VINIX7)", slide_subtitle))
    
    crit_data = [
        [Paragraph("<b>1. Problem-fit</b><br/>Sesuai dengan masalah analitik olahraga dan target pengguna (analis, pelatih, audiens).", bullet_text),
         Paragraph("<b>2. Data Sehat</b><br/>Sumber data jelas (Kaggle martj42), bersih dari anomali, dan tidak bocor temporal.", bullet_text)],
        [Paragraph("<b>3. Evaluasi Valid</b><br/>Memakai metrik komprehensif (F1-score, Precision, Recall) dibandingkan baseline naif.", bullet_text),
         Paragraph("<b>4. Bisa Dijelaskan</b><br/>Insight dan limitasi disampaikan secara jujur; membuka bobot fitur penentu hasil laga.", bullet_text)],
        [Paragraph("<b>5. Bermanfaat</b><br/>Rekomendasi realistik dan dapat ditindaklanjuti untuk simulasi turnamen ASEAN Cup.", bullet_text),
         Paragraph("<b>6. Etis &amp; Sport Science</b><br/>Bebas bias algoritma; murni untuk sains data olahraga tanpa kaitan dengan platform perjudian.", bullet_text)]
    ]
    t_crit = Table(crit_data, colWidths=[380, 380])
    t_crit.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_crit)
    story.append(PageBreak())
# SLIDE 4: Anatomi Dataset Historis
    story.append(Paragraph("SLIDE 14 / 15 • BAHAN BAKAR MODEL", header_badge))
    story.append(Paragraph("Anatomi Dataset Historis Internasional (1872 - 2026)", slide_title))
    story.append(Paragraph("Dataset Resmi Kaggle martj42 (International Football Results from 1872 to Present)", slide_subtitle))
    
    stat_boxes = [
        [Paragraph("<b>TOTAL PERTANDINGAN</b><br/><font size=16 color='#2563EB'><b>49.945</b></font><br/>Baris Valid Riil", bullet_text),
         Paragraph("<b>RENTANG HISTORIS</b><br/><font size=16 color='#10B981'><b>154 Tahun</b></font><br/>1872 s.d. Okt 2026", bullet_text),
         Paragraph("<b>TIM NASIONAL</b><br/><font size=16 color='#F59E0B'><b>337 Negara</b></font><br/>Seluruh Konfederasi", bullet_text),
         Paragraph("<b>PERTANDINGAN ASEAN</b><br/><font size=16 color='#8B5CF6'><b>3.782 Laga</b></font><br/>Termasuk 839 AFF Cup", bullet_text)]
    ]
    t_stats = Table(stat_boxes, colWidths=[190, 190, 190, 190])
    t_stats.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_stats)
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>Atribut Kunci yang Digunakan:</b>", body_text))
    story.append(Paragraph("• <code>date</code>: Tanggal resmi pertandingan (menjadi dasar pemisahan temporal anti-leakage).", bullet_text))
    story.append(Paragraph("• <code>home_team</code> & <code>away_team</code>: Identitas tim kandang dan tandang.", bullet_text))
    story.append(Paragraph("• <code>home_score</code> & <code>away_score</code>: Jumlah gol aktual yang dicetak kedua tim.", bullet_text))
    story.append(Paragraph("• <code>tournament</code>: Turnamen resmi (Piala Dunia, Kualifikasi, AFF Cup) vs Friendly match.", bullet_text))
    story.append(Paragraph("• <code>neutral</code>: Status boolean apakah laga dimainkan di tempat netral.", bullet_text))
    story.append(PageBreak())

    # SLIDE 5: EDA - Target Distribution & Home Advantage
    story.append(Paragraph("SLIDE 13 / 15 • EKSPLORASI DATA (EDA)", header_badge))
    story.append(Paragraph("Distribusi Target & Evaluasi Home Advantage", slide_title))
    story.append(Paragraph("Temuan Empiris pada 49.945 Pertandingan Sepak Bola Internasional", slide_subtitle))
    
    eda_img1 = os.path.join(artifacts_dir, "eda_target_distribution.png")
    if os.path.exists(eda_img1):
        story.append(Image(eda_img1, width=420, height=230))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Insight Utama:</b>", body_text))
    story.append(Paragraph("• <b>Home Win (49.00%):</b> Kemenangan tim kandang mendominasi hampir setengah dari seluruh laga sejarah.", bullet_text))
    story.append(Paragraph("• <b>Away Win (28.29%):</b> Kemenangan tandang relatif lebih sulit diraih.", bullet_text))
    story.append(Paragraph("• <b>Draw (22.71%):</b> Hasil seri memiliki frekuensi terkecil dan merupakan kelas paling sulit diprediksi.", bullet_text))
    story.append(Paragraph("• <b>Home Advantage Multiplier:</b> Tim kandang <b>1.73x lebih berpeluang menang</b> dibandingkan tim tandang.", bullet_text))
    story.append(PageBreak())

    # SLIDE 6: EDA - Neutral Venue Impact & Era Goals
    story.append(Paragraph("SLIDE 06 / 15 • EKSPLORASI DATA (EDA)", header_badge))
    story.append(Paragraph("Pengaruh Venue Netral & Pola Produktivitas Gol", slide_title))
    story.append(Paragraph("Bagaimana Lokasi Pertandingan Mengubah Probabilitas Kemenangan?", slide_subtitle))
    
    eda_img2 = os.path.join(artifacts_dir, "eda_match_context_and_neutral.png")
    if os.path.exists(eda_img2):
        story.append(Image(eda_img2, width=440, height=240))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Temuan Krusial:</b>", body_text))
    story.append(Paragraph("• <b>Runtuhnya Keuntungan Kandang:</b> Pada stadion normal, Home Win mencapai 50.73%. Namun pada venue netral, Home Win turun drastis ke 44.22%, sedangkan Away Win melonjak ke 33.40%.", bullet_text))
    story.append(Paragraph("• <b>Rata-rata Gol:</b> Sepanjang sejarah, rata-rata 2.94 gol tercipta per laga (Kandang: 1.76 vs Tandang: 1.18).", bullet_text))
    story.append(PageBreak())

    # SLIDE 7: Formulasi Output Multiclass
    story.append(Paragraph("SLIDE 07 / 15 • FORMULASI MASALAH", header_badge))
    story.append(Paragraph("Formulasi Output: Multiclass Classification (W - D - L)", slide_title))
    story.append(Paragraph("Klasifikasi Probabilistik 3 Kategori Mutlak", slide_subtitle))
    
    classes_data = [
        [Paragraph("<font size=14 color='#10B981'><b>W (Home Win)</b></font><br/>Skor Kandang > Skor Tandang", bullet_text),
         Paragraph("<font size=14 color='#F59E0B'><b>D (Draw / Seri)</b></font><br/>Skor Kandang == Skor Tandang", bullet_text),
         Paragraph("<font size=14 color='#EF4444'><b>L (Away Win)</b></font><br/>Skor Kandang < Skor Tandang", bullet_text)]
    ]
    t_cls = Table(classes_data, colWidths=[250, 250, 250])
    t_cls.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor('#F0FDF4')),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor('#FEFCE8')),
        ('BACKGROUND', (2,0), (2,0), colors.HexColor('#FEF2F2')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 15),
        ('BOTTOMPADDING', (0,0), (-1,-1), 15),
    ]))
    story.append(t_cls)
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>Alasan Mengapa Memilih Klasifikasi Kategorikal:</b>", body_text))
    story.append(Paragraph("• Model tidak memprediksi angka skor pasti (misal 2-1) yang memiliki variansi tinggi, melainkan probabilitas kumulatif kemenangan.", bullet_text))
    story.append(Paragraph("• Format ini sesuai dengan standar analitik olahraga dunia dan memudahkan estimasi probabilitas juara turnamen.", bullet_text))
    story.append(PageBreak())

    # SLIDE 8: Rekayasa Fitur Temporal Anti-Leakage
    story.append(Paragraph("SLIDE 08 / 15 • FEATURE ENGINEERING", header_badge))
    story.append(Paragraph("Rekayasa Fitur Temporal & Barrier Anti-Leakage", slide_title))
    story.append(Paragraph("Hanya Menggunakan Data Pra-Laga Sebelum Waktu (T)", slide_subtitle))
    story.append(Paragraph("<b>Daftar 19 Fitur Prediktor yang Dibangun Secara Mandiri:</b>", body_text))
    story.append(Paragraph("1. <b>Recent Form Points (5 Laga):</b> Akumulasi poin 5 laga terakhir tim kandang dan tandang (W=3, D=1, L=0).", bullet_text))
    story.append(Paragraph("2. <b>Recent Scoring & Conceding:</b> Rata-rata gol memasukkan dan kemasukan 5 laga terakhir.", bullet_text))
    story.append(Paragraph("3. <b>Cumulative Historical Win Rate:</b> Rasio kemenangan sepanjang masa kedua tim hingga waktu T-1.", bullet_text))
    story.append(Paragraph("4. <b>Cumulative Goal Power:</b> Rata-rata produktivitas gol dan kebobolan kumulatif pra-laga.", bullet_text))
    story.append(Paragraph("5. <b>Head-to-Head (H2H):</b> Rasio kemenangan pertemuan langsung antar kedua negara di masa lalu.", bullet_text))
    story.append(Paragraph("6. <b>Comparative Differentials:</b> Selisih form poin, selisih win rate, dan selisih daya serang tim.", bullet_text))
    story.append(Paragraph("7. <b>Konteks Laga:</b> Status venue netral (<code>is_neutral</code>) dan jenis turnamen (<code>is_friendly</code>).", bullet_text))
    story.append(PageBreak())

    # SLIDE 9: Time-Based Split
    story.append(Paragraph("SLIDE 09 / 15 • VALIDASI METODOLOGIS", header_badge))
    story.append(Paragraph("Mitigasi Ancaman Data Leakage: Time-Based Split", slide_title))
    story.append(Paragraph("Menolak Random Split Demi Keabsahan Real-World Model", slide_subtitle))
    story.append(Paragraph("<b>Mengapa Pengacakan Standar (Random Split) Dilarang Keras?</b><br/>"
                           "Dalam data time-series, random split akan menyebabkan kebocoran masa depan (misal: strategi tim tahun 2024 bocor ke fase pelatihan 1990-an). Model akan terlihat sangat akurat di lab namun gagal total di dunia nyata.", body_text))
    story.append(Spacer(1, 10))
    
    split_boxes = [
        [Paragraph("<b>TRAINING SET (ERA HISTORIS LAMA)</b><br/><font size=14 color='#2563EB'><b>38.288 Pertandingan</b></font><br/>Rentang: 1960 s.d. 31 Desember 2020", bullet_text),
         Paragraph("<b>TESTING SET (OUT-OF-TIME VALIDATION)</b><br/><font size=14 color='#10B981'><b>6.162 Pertandingan Riil</b></font><br/>Rentang: 1 Januari 2021 s.d. Oktober 2026", bullet_text)]
    ]
    t_split = Table(split_boxes, colWidths=[380, 380])
    t_split.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_split)
    story.append(Spacer(1, 10))
    story.append(Paragraph("Testing set mencakup turnamen modern riil: Euro 2020/2024, Piala Dunia 2022, AFF Mitsubishi Electric Cup, dan Kualifikasi Piala Dunia 2026.", bullet_text))
    story.append(PageBreak())

    # SLIDE 10: Model Comparison & Confusion Matrix
    story.append(Paragraph("SLIDE 10 / 15 • HASIL EVALUASI MODEL", header_badge))
    story.append(Paragraph("Perbandingan Kinerja Algoritma & Confusion Matrix", slide_title))
    story.append(Paragraph("Hasil Pengujian pada Out-of-Time Test Set (2021 - 2026)", slide_subtitle))
    
    model_table_data = [
        [Paragraph("<b>Algoritma</b>", bullet_text), Paragraph("<b>Akurasi</b>", bullet_text), Paragraph("<b>Macro F1</b>", bullet_text), Paragraph("<b>Weighted F1</b>", bullet_text), Paragraph("<b>Keterangan</b>", bullet_text)],
        [Paragraph("Naive Majority Baseline", bullet_text), Paragraph("47.89%", bullet_text), Paragraph("0.2159", bullet_text), Paragraph("0.3102", bullet_text), Paragraph("Tebakan naif selalu tebak Home", bullet_text)],
        [Paragraph("Decision Tree (depth=6)", bullet_text), Paragraph("57.43%", bullet_text), Paragraph("0.4116", bullet_text), Paragraph("0.4925", bullet_text), Paragraph("Pohon keputusan transparan", bullet_text)],
        [Paragraph("Logistic Regression", bullet_text), Paragraph("58.00%", bullet_text), Paragraph("0.4192", bullet_text), Paragraph("0.4990", bullet_text), Paragraph("Linear baseline terstandarisasi", bullet_text)],
        [Paragraph("<b>Random Forest (150 trees) ⭐</b>", bullet_text), Paragraph("<b>58.05%</b>", bullet_text), Paragraph("<b>0.4153</b>", bullet_text), Paragraph("<b>0.4964</b>", bullet_text), Paragraph("<b>Model Terpilih (Presisi Away 60%)</b>", bullet_text)],
        [Paragraph("Gradient Boosting", bullet_text), Paragraph("57.85%", bullet_text), Paragraph("0.4312", bullet_text), Paragraph("0.5072", bullet_text), Paragraph("Macro F1 tertinggi untuk Draw", bullet_text)]
    ]
    t_mod = Table(model_table_data, colWidths=[180, 80, 80, 90, 330])
    t_mod.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('BACKGROUND', (0,4), (-1,4), colors.HexColor('#EFF6FF')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_mod)
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Keunggulan (Lift):</b> Random Forest mengungguli tebakan naif sebesar <b>+10.16% akurasi</b> dan <b>+0.20 Macro F1</b>.", body_text))
    story.append(PageBreak())

    # SLIDE 11: ASEAN Cup Simulation
    story.append(Paragraph("SLIDE 11 / 15 • SIMULASI JUARA TURNAMEN", header_badge))
    story.append(Paragraph("Simulasi Probabilitas Juara ASEAN Cup (10.000 Iterasi Monte Carlo)", slide_title))
    story.append(Paragraph("Integrasi Model Random Forest ke Format Resmi Turnamen AFF Cup 10 Tim", slide_subtitle))
    
    sim_data = [
        [Paragraph("<b>Rank</b>", bullet_text), Paragraph("<b>Negara ASEAN</b>", bullet_text), Paragraph("<b>Peluang Juara</b>", bullet_text), Paragraph("<b>Peluang Finalis</b>", bullet_text), Paragraph("<b>Peluang Semifinal</b>", bullet_text), Paragraph("<b>Gugur Fase Grup</b>", bullet_text)],
        [Paragraph("1", bullet_text), Paragraph("<b>Vietnam</b>", bullet_text), Paragraph("<font color='#10B981'><b>26.52%</b></font>", bullet_text), Paragraph("48.40%", bullet_text), Paragraph("86.72%", bullet_text), Paragraph("13.28%", bullet_text)],
        [Paragraph("2", bullet_text), Paragraph("<b>Thailand</b>", bullet_text), Paragraph("<font color='#10B981'><b>24.48%</b></font>", bullet_text), Paragraph("48.22%", bullet_text), Paragraph("85.79%", bullet_text), Paragraph("14.21%", bullet_text)],
        [Paragraph("3", bullet_text), Paragraph("<b>Indonesia</b>", bullet_text), Paragraph("<font color='#10B981'><b>21.23%</b></font>", bullet_text), Paragraph("40.78%", bullet_text), Paragraph("75.71%", bullet_text), Paragraph("24.29%", bullet_text)],
        [Paragraph("4", bullet_text), Paragraph("<b>Malaysia</b>", bullet_text), Paragraph("<font color='#10B981'><b>21.04%</b></font>", bullet_text), Paragraph("40.91%", bullet_text), Paragraph("83.08%", bullet_text), Paragraph("16.92%", bullet_text)],
        [Paragraph("5", bullet_text), Paragraph("Myanmar", bullet_text), Paragraph("3.96%", bullet_text), Paragraph("10.39%", bullet_text), Paragraph("25.35%", bullet_text), Paragraph("74.65%", bullet_text)],
        [Paragraph("6", bullet_text), Paragraph("Singapura", bullet_text), Paragraph("2.15%", bullet_text), Paragraph("7.57%", bullet_text), Paragraph("24.64%", bullet_text), Paragraph("75.36%", bullet_text)],
        [Paragraph("7", bullet_text), Paragraph("Filipina", bullet_text), Paragraph("0.50%", bullet_text), Paragraph("2.77%", bullet_text), Paragraph("11.70%", bullet_text), Paragraph("88.30%", bullet_text)],
        [Paragraph("8", bullet_text), Paragraph("Kamboja", bullet_text), Paragraph("0.12%", bullet_text), Paragraph("0.93%", bullet_text), Paragraph("6.35%", bullet_text), Paragraph("93.65%", bullet_text)]
    ]
    t_sim = Table(sim_data, colWidths=[40, 160, 120, 120, 140, 180])
    t_sim.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_sim)
    story.append(Spacer(1, 8))
    story.append(Paragraph("Struktur Turnamen: Fase Grup A & B (Round-Robin 2 Home 2 Away), Semifinal 2 Leg, dan Final 2 Leg dengan resolusi agregat gol dan penalti.", bullet_text))
    story.append(PageBreak())

    
    # SLIDE 12: Visual Chart of Monte Carlo ASEAN Cup
    sim_chart_path = os.path.join(artifacts_dir, "asean_cup_simulation_chart.png")
    if os.path.exists(sim_chart_path):
        story.append(Paragraph("SLIDE 12 / 15 - GRAFIK SIMULASI MONTE CARLO", header_badge))
        story.append(Paragraph("Visualisasi Probabilitas Juara & Peluang Bertahan per Tahapan", slide_title))
        story.append(Paragraph("Distribusi Peluang Juara 10 Negara ASEAN dari 10.000 Iterasi Turnamen Monte Carlo", slide_subtitle))
        story.append(Image(sim_chart_path, width=720, height=340))
        story.append(PageBreak())

    # SLIDE 13: 90-Minute Match Simulation & Timeline Example
    match_chart_path = os.path.join(artifacts_dir, "match_simulation_example.png")
    if os.path.exists(match_chart_path):
        story.append(Paragraph("SLIDE 13 / 15 - CONTOH PREDIKSI & EVENT TICKER 90 MENIT", header_badge))
        story.append(Paragraph("Contoh Prediksi Head-to-Head & Animasi Laga 90 Menit (Tab 2 & 3)", slide_title))
        story.append(Paragraph("Simulasi Laga Indonesia vs Vietnam: Probabilitas Hasil, Prediksi Skor, dan Event Ticker", slide_subtitle))
        story.append(Image(match_chart_path, width=740, height=345))
        story.append(PageBreak())

    # SLIDE 14: Dokumentasi Mentoring Live Zoom
    zoom_img_path = r"C:\Users\Kenny\Desktop\Divisi Artificial Intelligence Starterpack kelompok 1\Bukti_Presensi_Real_Zoom_Senin_26_Okt_2026_1947.png"
    if os.path.exists(zoom_img_path):
        story.append(Paragraph("SLIDE 14 / 15 - DOKUMENTASI MENTORING LIVE", header_badge))
        story.append(Paragraph("Dokumentasi Perkuliahan Live & Penyelarasan Materi (26 Okt 2026)", slide_title))
        story.append(Paragraph("Sesi Kuliah Bersama Mentor Bimo Rizki Abdusshamad & Pak Aslan (Kehadiran Kenny Helim & Tim Kelompok 1)", slide_subtitle))
        story.append(Image(zoom_img_path, width=680, height=350))
        story.append(PageBreak())

    # SLIDE 12: Kesimpulan & Relevansi SDG 9
    story.append(Paragraph("SLIDE 15 / 15 • KESIMPULAN & SDG 9", header_badge))
    story.append(Paragraph("Kesimpulan Proyek & Kontribusi terhadap SDG 9", slide_title))
    story.append(Paragraph("Sintesis Capaian Kelompok 1 - Divisi Artificial Intelligence", slide_subtitle))
    story.append(Paragraph("<b>1. Kesimpulan Metodologis:</b> Pendekatan Machine Learning dengan Time-Based Split terbukti mampu menyaring sinyal objektif dari 49.945 pertandingan dan mengungguli tebakan naif sebesar +10.16% akurasi.", body_text))
    story.append(Paragraph("<b>2. Kontribusi Terhadap Target SDG 9 (Industri, Inovasi, dan Infrastruktur):</b>", body_text))
    story.append(Paragraph("• Membangun infrastruktur analitik olahraga berbasis kecerdasan buatan yang terbuka dan transparan.", bullet_text))
    story.append(Paragraph("• Mengubah proses estimasi intuitif menjadi sistem pendukung keputusan (Decision Support System) yang terukur bagi ekosistem olahraga regional.", bullet_text))
    story.append(Paragraph("<b>3. Artefak Lengkap yang Telah Selesai:</b>", body_text))
    story.append(Paragraph("• Aplikasi Web Interaktif (6 Tab) berjalan pada port 38800.", bullet_text))
    story.append(Paragraph("• Jupyter Notebook resmi: <code>football_prediction_eda_and_ml.ipynb</code>.", bullet_text))
    story.append(Paragraph("• Logbook Mingguan (Docx & PDF) dan Kartu Presensi Kehadiran Lengkap.", bullet_text))

    doc.build(story)
    print(f"Saved Assignment PDF: {output_pdf}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_dir = os.path.join(base_dir, "UPLOAD_BERKAS_FORM_MINGGU_3")
    artifacts_dir = os.path.join(base_dir, "artifacts")
    os.makedirs(out_dir, exist_ok=True)

    pdf_file = os.path.join(out_dir, "Assignment_Week_3_Kelompok_1_AI_International_Football_Prediction.pdf")
    build_assignment_pdf(pdf_file, artifacts_dir)

    # Also copy jupyter notebook into the upload folder for completeness
    nb_src = os.path.join(base_dir, "notebook", "football_prediction_eda_and_ml.ipynb")
    nb_dst = os.path.join(out_dir, "football_prediction_eda_and_ml.ipynb")
    shutil.copy2(nb_src, nb_dst)
    print(f"Copied Jupyter notebook to: {nb_dst}")
