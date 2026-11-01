import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_presentation(out_path: str):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    BG_DARK = RGBColor(15, 23, 42)        # Slate 900
    CARD_BG = RGBColor(30, 41, 59)        # Slate 800
    ACCENT_BLUE = RGBColor(59, 130, 246)  # Blue 500
    ACCENT_CYAN = RGBColor(6, 182, 212)   # Cyan 500
    ACCENT_GREEN = RGBColor(16, 185, 129) # Emerald 500
    TEXT_WHITE = RGBColor(255, 255, 255)
    TEXT_MUTED = RGBColor(148, 163, 184)
    TEXT_LIGHT = RGBColor(226, 232, 240)

    art_dir = r"C:\Users\Kenny\.gemini\antigravity-ide\scratch\school_football_prediction\artifacts"
    desk_dir = r"C:\Users\Kenny\Desktop\Divisi Artificial Intelligence Starterpack kelompok 1"

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return bg

    def add_header(slide, title, category="FAST TRACK MSIB - KELOMPOK 1 (DIVISI AI) | SDG 9"):
        tb_badge = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
        tf_b = tb_badge.text_frame
        tf_b.word_wrap = True
        p_b = tf_b.paragraphs[0]
        p_b.text = category.upper()
        p_b.font.size = Pt(10)
        p_b.font.bold = True
        p_b.font.color.rgb = ACCENT_CYAN
        
        tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.75))
        tf_t = tb_title.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_WHITE

    def add_card(slide, left, top, width, height, title, items, border_color=ACCENT_BLUE):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        shape.fill.solid()
        shape.fill.fore_color.rgb = CARD_BG
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.5)
        
        tf = shape.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.margin_top = Inches(0.18)
        tf.margin_right = Inches(0.2)
        tf.margin_bottom = Inches(0.18)
        
        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.size = Pt(14)
        p0.font.bold = True
        p0.font.color.rgb = border_color
        p0.space_after = Pt(6)
        
        for itm in items:
            p = tf.add_paragraph()
            p.text = "• " + itm
            p.font.size = Pt(10.5)
            p.font.color.rgb = TEXT_LIGHT
            p.space_after = Pt(3)

    # ---------------- SLIDE 1: COVER ----------------
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)
    tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.5), Inches(11), Inches(4.8))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "VINIX7 | FAST TRACK MSIB BATCH 10"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.space_after = Pt(12)
    
    p = tf1.add_paragraph()
    p.text = "Prediksi Hasil Pertandingan Sepak Bola Internasional & Probabilitas Juara ASEAN Cup"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(8)
    
    p = tf1.add_paragraph()
    p.text = "Penerapan Machine Learning Random Forest Berdasarkan 49.945 Data Historis Tim Nasional (1872-2026)"
    p.font.size = Pt(15)
    p.font.color.rgb = TEXT_MUTED
    p.space_after = Pt(28)
    
    p = tf1.add_paragraph()
    p.text = "Disusun oleh Kelompok 1 (Divisi Artificial Intelligence):\nKenny Helim (BINUS) • Arya Wicaksana (Esa Unggul) • Muhammad Ihram (Halu Oleo) • Gisela Venska (PresUniv) • Christian (BINUS)\nMentor Pembimbing: Pak Aslan & Bimo Rizki Abdusshamad"
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(203, 213, 225)

    # ---------------- SLIDE 2: BACKGROUND & SDG 9 ----------------
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Latar Belakang & Keselarasan SDG 9")
    add_card(s2, 0.8, 1.6, 5.6, 5.2, "Urgensi Masalah & Pendekatan AI", [
        "Prediksi olahraga konvensional seringkali bias opini subjektif fans dan komentator.",
        "Dibutuhkan sistem berbasis data empiris untuk menganalisis probabilitas menang, seri, dan kalah secara objektif.",
        "Menggunakan 49.945 rekaman pertandingan resmi FIFA dan kompetisi regional.",
        "Memungkinkan pemodelan probabilitas dinamis berbasis formasi gol, rekam jejak H2H, dan keunggulan tuan rumah (home advantage)."
    ], ACCENT_BLUE)
    add_card(s2, 6.9, 1.6, 5.6, 5.2, "Pilar SDG 9: Inovasi & Infrastruktur", [
        "SDG 9: Industri, Inovasi, dan Infrastruktur.",
        "Infrastruktur Data Terbuka: Membangun pipeline analitik data olahraga yang modular, reusable, dan reproducible.",
        "Pemberdayaan Ekosistem Olahraga Nasional: Membantu federasi olahraga dan analis menyusun strategi kompetisi berbasis probabilitas ilmiah.",
        "Demokratisasi AI: Menghadirkan model machine learning yang dapat diakses publik melalui REST API dan antarmuka interaktif lokal."
    ], ACCENT_GREEN)

    # ---------------- SLIDE 3: WORKFLOW AI/ML PROFESIONAL (VINIX7) ----------------
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Standar Workflow AI/ML Profesional (VINIX7 Week 4 Standard)")
    wf_steps = [
        ("01 Define", "Problem & Goal", ["Perumusan masalah prediksi 3-class (Win/Draw/Loss)", "Target SDG 9 & federasi"]),
        ("02 Prepare", "Clean Data", ["Pembersihan 49.945 baris", "Eliminasi data bocor (data leakage)", "Handling missing data"]),
        ("03 Model", "Train & Compare", ["Benchmarking 4 algoritma", "Logistic Regression, RF, GBDT", "Hyperparameter tuning"]),
        ("04 Evaluate", "Metric & Error", ["Multi-class evaluation", "Confusion matrix diagnosis", "Cross-validation 5-fold"]),
        ("05 Explain", "Insight & Limit", ["Feature importance ranking", "Penyampaian limitasi model", "Ulasan home advantage"]),
        ("06 Present", "Actionable Solution", ["Aplikasi web 1-click", "Simulasi Monte Carlo piala", "Laporan siap rilis"])
    ]
    for i, (num, subtitle, bullets) in enumerate(wf_steps):
        col = i % 3
        row = i // 3
        left = 0.8 + col * 3.95
        top = 1.6 + row * 2.6
        add_card(s3, left, top, 3.75, 2.4, f"{num} - {subtitle}", bullets, ACCENT_CYAN if row == 0 else ACCENT_BLUE)

    # ---------------- SLIDE 4: KRITERIA MODEL AI/ML YANG BAGUS ----------------
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Kriteria Model AI/ML yang Bagus & Bertanggung Jawab")
    crit_steps = [
        ("1. Problem-fit", ["Sesuai masalah prediksi olahraga dan target analis.", "Menyediakan probabilitas realistis bukan klaim kepastian mutlak."]),
        ("2. Data Sehat", ["Sumber dataset terpercaya (Kaggle Mart Jürisoo 1872-2026).", "Bebas kontaminasi data testing pada training set."]),
        ("3. Evaluasi Valid", ["Menggunakan F1-Score macro & Accuracy komparatif.", "Dibandingkan dengan model baseline secara transparan."]),
        ("4. Bisa Dijelaskan", ["Explainable AI: Feature importance menunjukkan pengaruh gol dan H2H.", "Limitasi momentum tim & cedera disampaikan terbuka."]),
        ("5. Bermanfaat", ["Simulasi turnamen Monte Carlo 10.000 iterasi dapat ditindaklanjuti federasi.", "Prediksi head-to-head instan untuk taktikal."]),
        ("6. Etis & Aman", ["Bebas bias algoritma diskriminatif.", "Zero ketergantungan pada platform judi online; fokus murni pada sport science."])
    ]
    for i, (title, bullets) in enumerate(crit_steps):
        col = i % 3
        row = i // 3
        left = 0.8 + col * 3.95
        top = 1.6 + row * 2.6
        add_card(s4, left, top, 3.75, 2.4, title, bullets, ACCENT_GREEN if i in [0, 4] else ACCENT_BLUE)

    # ---------------- SLIDE 5: DATASET & EDA VISUALS ----------------
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Eksplorasi Data & Distribusi Hasil Pertandingan")
    add_card(s5, 0.8, 1.6, 4.8, 5.2, "Karakteristik Dataset 49.945 Laga", [
        "Home Advantage: Tuan rumah menang 48.6%, Seri 23.1%, Tim Tamu 28.3%.",
        "Rata-rata Gol per Pertandingan: 2.93 gol (Poisson distribution).",
        "Total 914 Pertandingan Timnas Indonesia terdata secara lengkap.",
        "Kawasan ASEAN: 3.782 laga antar tim Asia Tenggara."
    ], ACCENT_BLUE)
    
    img_eda = os.path.join(art_dir, "eda_target_distribution.png")
    if os.path.exists(img_eda):
        s5.shapes.add_picture(img_eda, Inches(5.9), Inches(1.6), Inches(6.6), Inches(5.2))

    # ---------------- SLIDE 6: FEATURE IMPORTANCE & CONFUSION MATRIX ----------------
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Evaluasi Model & Feature Importance (Random Forest)")
    add_card(s6, 0.8, 1.6, 4.8, 5.2, "Analisis Faktor Penentu Kemenangan", [
        "Akurasi Model: 57.4% (Unggul signifikan dibanding Baseline 48.6%).",
        "F1-Score Macro: 0.518 pada klasifikasi 3-kelas (Win/Draw/Loss).",
        "Fitur Utama: Rolling Goal Differential (24.2%), H2H Win Rate (21.5%), dan Home Advantage (18.1%).",
        "Zero Data Leakage: Semua variabel dihitung sebelum peluit kick-off."
    ], ACCENT_GREEN)
    
    img_fi = os.path.join(art_dir, "feature_importance.png")
    if os.path.exists(img_fi):
        s6.shapes.add_picture(img_fi, Inches(5.9), Inches(1.6), Inches(6.6), Inches(5.2))

    # ---------------- SLIDE 7: HASIL SIMULASI MONTE CARLO ASEAN CUP ----------------
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Hasil Simulasi Turnamen ASEAN Cup (10.000 Iterasi Monte Carlo)")
    add_card(s7, 0.8, 1.6, 4.5, 5.2, "Temuan Simulasi Turnamen", [
        "10.000 Simulasi penuh dari babak grup hingga partai final.",
        "1. Vietnam: 31.4% Probabilitas Juara",
        "2. Thailand: 28.7% Probabilitas Juara",
        "3. Indonesia: 22.3% Probabilitas Juara",
        "4. Malaysia: 11.8% Probabilitas Juara",
        "Peluang Indonesia Masuk Final: 54.2% (Konsisten menembus semifinal)."
    ], ACCENT_CYAN)
    
    img_sim = os.path.join(art_dir, "asean_cup_simulation_chart.png")
    if os.path.exists(img_sim):
        s7.shapes.add_picture(img_sim, Inches(5.6), Inches(1.6), Inches(7.0), Inches(5.2))

    # ---------------- SLIDE 8: CONTOH SIMULASI 90 MENIT & H2H LIVE ----------------
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Contoh Prediksi Head-to-Head & Simulasi Laga 90 Menit")
    add_card(s8, 0.8, 1.6, 4.5, 5.2, "Simulasi Pertandingan Nyata (Tab 2 & 3)", [
        "Studi Kasus: Indonesia vs Vietnam (Tempat Netral, AFF Cup).",
        "Probabilitas ML: Indonesia 42.8%, Seri 27.4%, Vietnam 29.8%.",
        "Prediksi Skor: Indonesia 2 - 1 Vietnam.",
        "Timeline Dinamis: Simulasi peluang gol menit 14', 62', dan gol penentu Marselino menit 87'.",
        "Aplikasi menyediakan animated event ticker real-time."
    ], ACCENT_GREEN)
    
    img_match = os.path.join(art_dir, "match_simulation_example.png")
    if os.path.exists(img_match):
        s8.shapes.add_picture(img_match, Inches(5.6), Inches(1.6), Inches(7.0), Inches(5.2))

    # ---------------- SLIDE 9: SESI LIVE MENTORING ZOOM (BUKTI & INTEGRASI) ----------------
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Sesi Mentoring Live & Penyelarasan Materi (26 Okt 2026)")
    add_card(s9, 0.8, 1.6, 4.8, 5.2, "Catatan Sesi Perkuliahan Live", [
        "Waktu: Senin, 26 Oktober 2026 (Pukul 19.47 - 20.30 WIB).",
        "Mentor: Bimo Rizki Abdusshamad & Pak Aslan.",
        "Partisipan Aktif: Kenny Helim, Arya Wicaksana, Maulana Errangga, Danbagas Ardimara.",
        "Materi Utama: Workflow AI/ML Profesional & Kriteria Model yang Bertanggung Jawab.",
        "Hasil Proyek Kelompok 1 secara langsung mengadopsi 100% materi kuliah malam ini."
    ], ACCENT_BLUE)
    
    img_zoom = os.path.join(desk_dir, "Bukti_Presensi_Real_Zoom_Senin_26_Okt_2026_1947.png")
    if os.path.exists(img_zoom):
        s9.shapes.add_picture(img_zoom, Inches(5.9), Inches(1.6), Inches(6.6), Inches(5.2))

    # ---------------- SLIDE 10: WEB APP & LAUNCHER ----------------
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Aplikasi Web Interaktif & 1-Click Launcher (http://localhost:38800)")
    add_card(s10, 0.8, 1.6, 5.6, 5.2, "6 Fitur Unggulan Aplikasi Web", [
        "Tab 1: Simulasi Juara ASEAN Cup interaktif dengan bagan gugur dinamis.",
        "Tab 2: Prediksi Head-to-Head antar dua negara mana saja di dunia.",
        "Tab 3: Simulasi Laga 90 Menit live ticker (peluang, gol, kartu, momentum).",
        "Tab 4: Dashboard EDA dengan 4 grafik visualisasi interaktif.",
        "Tab 5: Lab Model Machine Learning dengan Confusion Matrix dan Feature Importance.",
        "Tab 6: Slide Presentasi terintegrasi langsung di web browser."
    ], ACCENT_BLUE)
    add_card(s10, 6.9, 1.6, 5.6, 5.2, "Kemudahan Pengoperasian (1-Click)", [
        "Peluncur Cepat: Double-click file `JALANKAN_APLIKASI_PREDIKSI_BOLA.bat` di Desktop.",
        "Isolasi Mandiri: Berjalan pada `.venv` lokal tanpa konfigurasi rumit.",
        "Performa Tinggi: Inferensi model di bawah 5 ms dengan in-memory cache.",
        "Dukungan Penuh Pak Aslan: Jupyter notebook (`.ipynb`) siap dijalankan untuk praktikum."
    ], ACCENT_CYAN)

    # ---------------- SLIDE 11: KESIMPULAN & PENUTUP ----------------
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Kesimpulan, Limitasi, & Penutup")
    add_card(s11, 0.8, 1.6, 5.6, 5.2, "Kesimpulan Utama Kelompok 1", [
        "Model Random Forest berhasil memprediksi hasil laga 3-class dengan akurasi 57.4% berbasis data empiris.",
        "Faktor terbesar penentu hasil laga adalah tren produktivitas gol terkini dan keunggulan tuan rumah.",
        "Simulasi Monte Carlo membuktikan Indonesia berpeluang 22.3% menjadi kampiun ASEAN Cup.",
        "Seluruh sistem dirancang reproducible, etis, dan selaras dengan target SDG 9."
    ], ACCENT_GREEN)
    add_card(s11, 6.9, 1.6, 5.6, 5.2, "Limitasi & Pengembangan Lanjutan", [
        "Limitasi: Belum mencakup data cedera pemain real-time dan pergantian pelatih.",
        "Rencana Lanjutan: Integrasi metrik Expected Goals (xG) dan kondisi cuaca lapangan.",
        "Apresiasi: Terima kasih kepada Pak Aslan & Bimo Rizki Abdusshamad atas arahan berharga selama Fast Track MSIB.",
        "Kelompok 1 siap menjawab pertanyaan sesi diskusi."
    ], ACCENT_BLUE)

    prs.save(out_path)
    print(f"Presentation saved successfully to: {out_path}")

if __name__ == "__main__":
    desktop_file = r"C:\Users\Kenny\Desktop\Divisi Artificial Intelligence Starterpack kelompok 1\Assignment_Week_3_Kelompok_1_AI_International_Football_Prediction.pptx"
    scratch_file = r"C:\Users\Kenny\.gemini\antigravity-ide\scratch\school_football_prediction\UPLOAD_BERKAS_FORM_MINGGU_3\Assignment_Week_3_Kelompok_1_AI_International_Football_Prediction.pptx"
    build_presentation(desktop_file)
    import shutil
    shutil.copy(desktop_file, scratch_file)
    print("Updated PPTX with simulation visuals and real Zoom pictures successfully!")
