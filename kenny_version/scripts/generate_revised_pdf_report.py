import os
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether

def build_pdf_report(out_path: str):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    doc = SimpleDocTemplate(
        out_path,
        pagesize=landscape(A4),
        leftMargin=40,
        rightMargin=40,
        topMargin=36,
        bottomMargin=36
    )
    styles = getSampleStyleSheet()

    header_badge = ParagraphStyle('HdrBadge', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor('#0284C7'), spaceAfter=4)
    slide_title = ParagraphStyle('SlideTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=18, textColor=colors.HexColor('#0F172A'), spaceAfter=4)
    slide_subtitle = ParagraphStyle('SlideSub', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11, textColor=colors.HexColor('#EA580C'), spaceAfter=14)
    card_title = ParagraphStyle('CardTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10.5, textColor=colors.HexColor('#0F172A'), spaceAfter=6)
    body_text = ParagraphStyle('BodyTextCustom', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=12, textColor=colors.HexColor('#334155'), spaceAfter=4)
    body_bold = ParagraphStyle('BodyBoldCustom', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, leading=12, textColor=colors.HexColor('#0F172A'), spaceAfter=4)

    def create_card(title, paragraphs, bg_color='#F8FAFC', border_color='#CBD5E1'):
        content = [Paragraph(title, card_title)]
        for p in paragraphs:
            content.append(Paragraph(p, body_text))
        t = Table([[content]], colWidths=[360])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(bg_color)),
            ('BOX', (0,0), (-1,-1), 1.2, colors.HexColor(border_color)),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ]))
        return t

    def create_two_column_cards(card1, card2):
        t = Table([[card1, card2]], colWidths=[375, 375])
        t.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        return t

    story = []

    # PAGE 1: COVER
    story.append(Paragraph("VINIX7 | FAST TRACK MSIB BATCH 10 (ARTIFICIAL INTELLIGENCE)", header_badge))
    story.append(Paragraph("Panduan Metodologi: Dari Data Mentah ke Probabilitas Juara", slide_title))
    story.append(Paragraph("Membedah Mesin Prediksi ASEAN Cup: Menghitung Peluang Secara Transparan, Jujur, dan Logis Tanpa Ilusi Kepastian", slide_subtitle))
    
    cover_info = [
        "<b>Program:</b> Fast Track MSIB Batch 10 — Divisi Artificial Intelligence (PT Vinix Seven Aurum)",
        "<b>SDG Alignment:</b> SDG 9: Industri, Inovasi, dan Infrastruktur (Inovasi Analitik Data Olahraga Terbuka)",
        "<b>Tim Penyusun (Kelompok 1):</b><br/>"
        "• Kenny Helim — Information System and Management (Universitas Bina Nusantara / BINUS)<br/>"
        "• Arya Wicaksana — Teknik Informatika (Universitas Esa Unggul)<br/>"
        "• Muhammad Ihram Syahputra — Ilmu Komputer (Universitas Halu Oleo)<br/>"
        "• Gisela Venska Millennia — Information System (President University)<br/>"
        "• Christian — Information Systems (Universitas Bina Nusantara / BINUS)",
        "<b>Dosen & Mentor Pembimbing:</b> Pak Aslan Alwi & Bimo Rizki Abdusshamad",
        "<b>Periode Evaluasi:</b> Pekan 4 Menuju Sidang Akhir (2 - 6 November 2026)"
    ]
    t_cover = create_card("INFORMASI PROYEK & ANGGOTA KELOMPOK 1", cover_info, bg_color='#F0F9FF', border_color='#0284C7')
    story.append(t_cover)
    story.append(PageBreak())

    # PAGE 2: RANTAI PROBABILITAS
    story.append(Paragraph("BAB 1: ARSITEKTUR RANTAI PROBABILITAS", header_badge))
    story.append(Paragraph("Rantai Probabilitas: Mengubah Sejarah Menjadi Peluang", slide_title))
    story.append(Paragraph("Mengatasi Bias Subjektif Penggemar dan Komentator dengan Rantai Logika 5 Tahap", slide_subtitle))
    
    c1 = create_card("Problem Statement: Ilusi Kepastian vs Probabilitas Murni", [
        "<b>Kelemahan Analisis Konvensional:</b> Analisis sepak bola konvensional seringkali terjebak pada ilusi kepastian ('Tim A PASTI MENANG!') atau bias opini subjektif fans dan komentator.",
        "<b>Pendekatan AI Kelompok 1:</b> Kami tidak menjual kepastian palsu, melainkan membangun rantai logika yang mengubah 49.945 rekam jejak pertandingan menjadi mesin undian turnamen virtual yang jujur, terkalibrasi, dan logis.",
        "<b>Penyelarasan SDG 9:</b> Membangun infrastruktur pemodelan data olahraga yang terbuka, modular, dan dapat direproduksi oleh federasi olahraga regional."
    ], bg_color='#FEF2F2', border_color='#EF4444')
    
    c2 = create_card("5 Tahapan Rantai Probabilitas (Pipeline Logika)", [
        "<b>1. Sejarah Laga:</b> 49.945 pertandingan masa lalu resmi FIFA (1872 - 2024).",
        "<b>2. Fitur Pra-Laga:</b> Rating kekuatan dinamis (Elo), momentum form 5 laga, dan rekor H2H.",
        "<b>3. Probabilitas Laga:</b> Model Logistic Full Interaksi menghitung persentase Menang (H), Seri (D), Kalah (A).",
        "<b>4. 10.000 Simulasi Monte Carlo:</b> Mengundi rute turnamen berulang kali dalam 10.000 dunia paralel.",
        "<b>5. Probabilitas Juara:</b> Frekuensi angkat trofi dari total iterasi dengan interval kepercayaan 95%."
    ], bg_color='#F0FDF4', border_color='#10B981')
    
    story.append(create_two_column_cards(c1, c2))
    story.append(PageBreak())

    # PAGE 3: ATURAN TANPA MESIN WAKTU (ANTI LEAKAGE)
    story.append(Paragraph("BAB 2: DATA INTEGRITY & TEMPORAL BARRIER", header_badge))
    story.append(Paragraph("Langkah 1: Bahan Baku & Aturan Besi 'Tanpa Mesin Waktu'", slide_title))
    story.append(Paragraph("Disiplin Ketat Pencegahan Data Leakage dengan Cut-off 2024-12-08", slide_subtitle))
    
    c3 = create_card("Bahan Baku Data Primer", [
        "<b>results.csv:</b> 49.945 rekaman pertandingan internasional resmi (tanggal, kandang, tandang, skor, turnamen, dan venue netral).",
        "<b>former_names.csv:</b> Penyelarasan kontinuitas historis tim nasional yang mengalami pergantian nama resmi.",
        "<b>shootouts.csv:</b> Data adu penalti diisolasi secara ketat dari fitur latihan.",
        "<b>Dataset Evaluasi Khusus:</b> 52 pertandingan kompetisi ASEAN Championship aktual."
    ], bg_color='#F8FAFC', border_color='#64748B')
    
    c4 = create_card("Aturan Besi 'Tanpa Mesin Waktu'", [
        "<b>Larangan Data Leakage:</b> Model dilarang keras melihat informasi setelah laga dimulai.",
        "<b>Batas Waktu Tegas (Cut-off):</b> 8 Desember 2024 (48.093 laga dialokasikan sebagai masa lalu untuk kalibrasi pra-turnamen).",
        "<b>Kunci Data Shootout:</b> Hasil adu penalti dikunci dan tidak dimasukkan ke dalam fitur pra-laga agar model tidak 'menyontek' hasil akhir sebelum laga berjalan.",
        "<b>Integritas Ilmiah:</b> Semua fitur waktu T murni dihitung dari data historis sebelum T."
    ], bg_color='#FFFBEB', border_color='#F59E0B')
    
    story.append(create_two_column_cards(c3, c4))
    story.append(PageBreak())

    # PAGE 4: SINYAL PRA-LAGA
    story.append(Paragraph("BAB 3: FEATURE ENGINEERING", header_badge))
    story.append(Paragraph("Langkah 2: Meracik Sinyal Pra-Laga (Anatomy of a Match)", slide_title))
    story.append(Paragraph("Empat Pilar Informasi Murni yang Dibekukan Sebelum Peluit Pertandingan Dimulai", slide_subtitle))
    
    c5 = create_card("Pilar 1 & 2: Kekuatan Murni & Momentum Terkini", [
        "<b>1. Kekuatan Murni (Elo Rating Dinamis):</b><br/>"
        "• Sistem rating yang terkalibrasi dari 48.093 pertandingan lampau.<br/>"
        "• Nilai rating naik saat menang melawan tim berbobot tinggi, dan tergerus saat kalah.<br/>"
        "• Menjadi jangkar utama kekuatan objektif sebuah tim nasional.",
        "<b>2. Momentum Terkini (Rolling Form 5 Laga):</b><br/>"
        "• Rata-rata poin per laga dari 5 pertandingan terakhir.<br/>"
        "• Rata-rata selisih gol (goal difference) terkini.<br/>"
        "• Menangkap tren positif atau krisis performa skuad sebelum turnamen."
    ], bg_color='#F8FAFC', border_color='#0284C7')
    
    c6 = create_card("Pilar 3 & 4: Rekor Head-to-Head & Konteks Laga", [
        "<b>3. Sejarah Head-to-Head (H2H):</b><br/>"
        "• Rekam jejak pertemuan langsung spesifik antara kedua negara.<br/>"
        "• Mengukur kecocokan gaya main dan dominasi historis psikologis antar tim.",
        "<b>4. Konteks Laga (Home Advantage vs Netral):</b><br/>"
        "• Menilai apakah pertandingan digelar di kandang murni atau tempat netral.<br/>"
        "• Pada tempat netral, keunggulan tuan rumah runtuh dan probabilitas tim tamu melonjak secara statistik."
    ], bg_color='#F8FAFC', border_color='#10B981')
    
    story.append(create_two_column_cards(c5, c6))
    story.append(PageBreak())

    # PAGE 5: UJI KEJUJURAN MODEL (LOG LOSS)
    story.append(Paragraph("BAB 4: MODEL BENCHMARKING & LOG LOSS", header_badge))
    story.append(Paragraph("Langkah 3: Uji Kejujuran Model di Laga Final", slide_title))
    story.append(Paragraph("Evaluasi Kuantitatif Menggunakan Metrik Multi-Class Log Loss pada 52 Pertandingan ASEAN", slide_subtitle))
    
    c7 = create_card("Hasil Benchmark Log Loss pada 52 Laga ASEAN", [
        "<b>1. Tebakan Buta (Prior Baseline): 1.0686 ❌</b><br/>"
        "Hanya menebak frekuensi tanpa memedulikan siapa lawannya. Baseline dasar yang wajib dikalahkan.",
        "<b>2. Faktor Tunggal (Elo Murni): 0.8340 ➖</b><br/>"
        "Hanya bersandar pada selisih Elo rating. Berhasil memangkas log loss secara signifikan.",
        "<b>3. Model Final (Logistic Regression Full Interaksi): 0.8198 ✔️</b><br/>"
        "Mengkombinasikan Elo + Form + H2H + Konteks Netral dengan interaksi penuh. Menghasilkan skor terbaik 0.8198."
    ], bg_color='#F0FDF4', border_color='#10B981')
    
    c8 = create_card("Analisis & Kesimpulan Evaluasi Model", [
        "<b>Transparansi Sinyal Prediktif:</b> Sinyal terkuat tetap bersumber dari rating kekuatan murni tim (Elo), sementara fitur form dan H2H memberikan keunggulan presisi marjinal yang penting.",
        "<b>Mengapa Log Loss?</b> Berbeda dengan akurasi persentase sederhana, Log Loss menghukum penalti eksponensial terhadap model yang 'terlalu yakin tetapi salah'.",
        "<b>Kesiapan Turnamen:</b> Model terbukti solid, stabil terhadap kelas Draw (22.7%), dan siap memandu mesin simulasi turnamen virtual."
    ], bg_color='#F8FAFC', border_color='#64748B')
    
    story.append(create_two_column_cards(c7, c8))
    story.append(PageBreak())

    # PAGE 6: MESIN MONTE CARLO & HASIL SIMULASI 2026
    story.append(Paragraph("BAB 5: SIMULASI MONTE CARLO & PROBABILITAS JUARA", header_badge))
    story.append(Paragraph("Langkah 4: Mesin Monte Carlo 10.000 Putaran Virtual", slide_title))
    story.append(Paragraph("Distribusi Peluang Juara ASEAN Championship 2026 dari 10.000 Skenario Paralel", slide_subtitle))
    
    c9 = create_card("Peta Kekuatan Probabilitas Juara ASEAN 2026", [
        "<b>1. 🇹🇭 Thailand: 30.97% [Interval 30.07% - 31.88%]</b> (3.097 Kali Juara)<br/>"
        "Kandidat terkuat berkat konsistensi Elo rating tertinggi dan kedalaman riwayat turnamen.",
        "<b>2. 🇮🇩 Indonesia: 27.34% [Interval 26.48% - 28.22%]</b> (2.734 Kali Juara)<br/>"
        "Penantang utama dengan tren momentum form positif dan peningkatan efisiensi gol.",
        "<b>3. 🇻🇳 Vietnam: 21.73% [Interval 20.93% - 22.55%]</b> (2.173 Kali Juara)<br/>"
        "Kekuatan defensif solid dengan rekor pertemuan H2H regional yang tangguh.",
        "<b>4. 🇲🇾 Malaysia: 15.40% [Interval 14.71% - 16.12%]</b> (1.540 Kali Juara)<br/>"
        "Potensi kejutan tinggi pada fase semifinal."
    ], bg_color='#FFF7ED', border_color='#EA580C')
    
    c10 = create_card("Bukti Validasi Empiris Masa Lalu (Backtest)", [
        "<b>1 dari 5 Juara Tepat:</b> Pilihan nomor satu model berhasil keluar sebagai juara aktual.",
        "<b>4 dari 5 Juara di Top-3:</b> Dalam 4 dari 5 edisi turnamen masa lalu (2018-2024), tim yang mengangkat trofi nyata selalu berada di Top-3 simulasi kami.",
        "<b>25.22% Peluang Rata-Rata:</b> Rata-rata peluang yang diberikan simulasi kepada tim yang akhirnya juara adalah 25.22% (jauh melampaui tebakan acak 10 negara yaitu 10.00%).",
        "<b>Anomali 2024:</b> Turnamen singkat memiliki variansi acak tinggi yang membuktikan pentingnya proyeksi berbasis probabilitas, bukan angka mutlak."
    ], bg_color='#F0F9FF', border_color='#0284C7')
    
    story.append(create_two_column_cards(c9, c10))
    story.append(PageBreak())

    # PAGE 7: TRUST TRIAD & ARSITEKTUR AI (VS YOLO11)
    story.append(Paragraph("BAB 6: TRUST TRIAD & KOMPARASI ARSITEKTUR AI", header_badge))
    story.append(Paragraph("Tiga Lapis Kepercayaan & Perbandingan Model AI", slide_title))
    story.append(Paragraph("Membangun Kepercayaan Solusi AI: Dari Computer Vision Hingga Pemodelan Stokastik", slide_subtitle))
    
    c11 = create_card("Tiga Lapis Kepercayaan (The Trust Triad)", [
        "<b>1. Data & Waktu (No Leakage):</b> Pemotongan waktu tegas pada 2024-12-08 menjamin tidak ada 'mesin waktu' yang mengintip masa depan.",
        "<b>2. Model (Probabilistik Log Loss):</b> Diuji pada 52 laga nyata ASEAN dengan metrik Log Loss 0.8198 yang menghukum overconfidence.",
        "<b>3. Simulasi (Monte Carlo 10.000 Putaran):</b> Mematuhi regulasi tiebreak dan struktur turnamen resmi (Grup, Semifinal 2 Leg, Final 2 Leg)."
    ], bg_color='#F0FDF4', border_color='#10B981')
    
    c12 = create_card("Perbandingan AI: Prediksi Sepak Bola vs YOLO11 Jalan Berlubang", [
        "<b>Kelompok Jalan Berlubang (YOLO11):</b><br/>"
        "• Problem: Deteksi objek fisik cacat aspal jalan.<br/>"
        "• Model: CNN / Computer Vision mendeteksi koordinat piksel bounding box.<br/>"
        "• Karakter: Spasial dan visual resolusi tinggi.",
        "<b>Kelompok Sepak Bola (AI Kami):</b><br/>"
        "• Problem: Memetakan ketidakpastian non-linear hasil olahraga.<br/>"
        "• Model: Logistic Interaction + Stochastic Monte Carlo Simulator.<br/>"
        "• Karakter: Temporal, probabilistik, dan kalkulasi risiko dinamis."
    ], bg_color='#F8FAFC', border_color='#0284C7')
    
    story.append(create_two_column_cards(c11, c12))
    story.append(PageBreak())

    # PAGE 8: STAKEHOLDER TERBANTU & ROADMAP (WEEK 4 MANDATE)
    story.append(Paragraph("BAB 7: PENERIMA MANFAAT & ROADMAP PENGEMBANGAN", header_badge))
    story.append(Paragraph("Pihak yang Paling Terbantu & Limitasi Transparan", slide_title))
    story.append(Paragraph("Memenuhi Mandat Mentoring Week 4 Pak Aslan Menuju Sidang Akhir 2 - 6 November 2026", slide_subtitle))
    
    c13 = create_card("Target Penerima Manfaat Utama (Underdogs & Federasi)", [
        "<b>1. Tim Liga & Tim Nasional Underdogs:</b><br/>"
        "Tim dengan probabilitas rendah dapat melihat secara transparan celah kekuatan lawan, menghitung target poin realistis di fase grup, dan menyiapkan kontra-strategi yang berbeda dari turnamen sebelumnya.",
        "<b>2. Federasi Sepak Bola Nasional:</b><br/>"
        "Mendukung pengambilan keputusan berbasis bukti empiris dalam penjadwalan uji coba internasional untuk mendongkrak Elo rating dan poin FIFA.",
        "<b>3. Pengamat & Media Olahraga:</b><br/>"
        "Menggantikan sensasionalisme opini dengan literasi analitik probabilitas."
    ], bg_color='#FFFBEB', border_color='#F59E0B')
    
    c14 = create_card("Limitasi Transparan & Evolusi Berikutnya", [
        "<b>Batasan Saat Ini:</b><br/>"
        "• Belum memodelkan skor spesifik babak perpanjangan waktu.<br/>"
        "• Statistik kekuatan dibekukan pra-turnamen; belum ada pembaruan form dinamis in-tournament.<br/>"
        "• Parameter pembobotan Elo masih menggunakan standar default.",
        "<b>Evolusi Berikutnya:</b><br/>"
        "• Prediksi skor spesifik berbasis Distribusi Poisson untuk selisih gol.<br/>"
        "• Penyertaan faktor cedera pemain kunci dan kedalaman rotasi skuad.<br/>"
        "• Antarmuka web interaktif lokal berbasis Streamlit/Flask yang adaptif terhadap data baru."
    ], bg_color='#F8FAFC', border_color='#64748B')
    
    story.append(create_two_column_cards(c13, c14))

    doc.build(story)
    print(f"Successfully generated revised master report PDF: {out_path}")

if __name__ == "__main__":
    desk_dir = r"C:\Users\Kenny\Desktop\DESKTOP_ORGANIZED_HUB\06_Folders_And_Packages\Divisi Artificial Intelligence Starterpack kelompok 1"
    os.makedirs(desk_dir, exist_ok=True)
    
    pdf_out1 = os.path.join(desk_dir, "FINAL_PROJECT_REPORT_KELOMPOK_1_AI_REVISI_METODOLOGI.pdf")
    pdf_out2 = os.path.join(desk_dir, "FINAL_PROJECT_WEEK_4_JUMAT", "FINAL_PROJECT_REPORT_KELOMPOK_1_AI.pdf")
    pdf_out3 = r"C:\Users\Kenny\Desktop\BERKAS_UPLOAD_SEKARANG_KENNY\3_ASSIGNMENT_WEEK_4_FINAL_REPORT.pdf"
    
    proj_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pdf_out4 = os.path.join(proj_root, "UPLOAD_BERKAS_FORM_MINGGU_4", "FINAL_PROJECT_REPORT_KELOMPOK_1_AI.pdf")
    pdf_out5 = os.path.join(proj_root, "docs", "FINAL_PROJECT_REPORT_KELOMPOK_1_AI.pdf")
    
    for p in [pdf_out1, pdf_out2, pdf_out3, pdf_out4, pdf_out5]:
        build_pdf_report(p)


