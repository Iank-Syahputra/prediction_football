# -*- coding: utf-8 -*-
"""
[MODULE GOAL & ROLE]
Master Generator for Combined 20-Slide Defense Presentation Deck.
Merges Ian's 12 ML Blueprint Slides with Kenny's 8 Application Integration Slides.
Rule VQ-335, VQ-338 & VQ-515 Compliant:
- Slides 1 to 12: 100% Ian's original ML Blueprint (unmodified).
- Slides 13 to 20: Kenny's Application Integration & Decision Support Studio:
    Slide 13: Transisi & Arsitektur Integrasi Sistem (Handoff dari Ian)
    Slide 14: Menjawab Batasan 1 - Pemodelan Skor Poisson & Tab 1 (Match Predictor)
    Slide 15: Menjawab Batasan 2 - Ingesti CSV Dinamis & Rekalibrasi Elo (Tab 2)
    Slide 16: Tab 3 - Simulasi Turnamen Monte Carlo Interaktif (10k Iterasi)
    Slide 17: Tab 4 - Evaluasi 52 Laga AFF & Monograf Komparasi vs YOLO11
    Slide 18: Tab 5 - Target Penerima Manfaat & Underdog Counter-Tactics Lab (SDG 9)
    Slide 19: Standar Rekayasa Perangkat Lunak: 42 Real Unittest & Video Walkthrough
    Slide 20: Kesimpulan, Penutup & Sesi Tanya Jawab (Q&A)
- Embeds real Streamlit UI screenshots from artifacts/
- Populates word-for-word spoken Indonesian script in speaker notes of each slide.
"""

import os
import sys
import shutil
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

ROOT = Path(__file__).resolve().parent.parent
IAN_PPTX = Path(r"C:\Users\Kenny\Downloads\ASEAN_Football_Prediction_Blueprint_(2).pptx")
OUTPUT_DESKTOP_PPTX = Path(r"C:\Users\Kenny\Desktop\FINAL_COMBINED_PRESENTATION_IAN_AND_KENNY.pptx")
OUTPUT_ROOT_PPTX = ROOT / "FINAL_PROJECT_PRESENTATION_REVISED_PARADIGM.pptx"
OUTPUT_KENNY_DIR = Path(r"C:\Users\Kenny\Desktop\KENNY_VERSION_UNTUK_GITHUB")
ARTIFACTS_DIR = ROOT / "artifacts"

# Color Palette (Matching Ian's Technical Blueprint Aesthetic)
BG_COLOR = RGBColor(248, 249, 250)         # Off-white / technical paper
NAVY_PRIMARY = RGBColor(15, 23, 42)        # Deep slate navy (#0F172A)
NAVY_BORDER = RGBColor(30, 41, 59)         # Card border (#1E293B)
TEXT_MUTED = RGBColor(71, 85, 105)         # Muted description (#475569)
CARD_BG = RGBColor(255, 255, 255)          # Pure white (#FFFFFF)
AMBER_ACCENT = RGBColor(180, 83, 9)        # Ochre / Amber (#B45309)
AMBER_BG = RGBColor(254, 243, 199)         # Light amber badge bg
BLUE_ACCENT = RGBColor(29, 78, 216)        # Rich cobalt blue (#1D4ED8)
GREEN_ACCENT = RGBColor(5, 150, 105)       # Emerald green (#059669)
GRID_LINE = RGBColor(203, 213, 225)        # Blueprint grid line (#CBD5E1)

def apply_blueprint_background(slide, width, height, slide_num_str):
    """Draw technical blueprint grid border and header coordinate box."""
    # Main outer border (Technical Drawing Margin)
    margin = Inches(0.4)
    outer_box = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, margin, margin, width - (margin * 2), height - (margin * 2)
    )
    outer_box.fill.solid()
    outer_box.fill.fore_color.rgb = BG_COLOR
    outer_box.line.color.rgb = NAVY_BORDER
    outer_box.line.width = Pt(1.5)
    
    # Corner Crosshairs
    for cx, cy in [
        (margin, margin),
        (width - margin, margin),
        (margin, height - margin),
        (width - margin, height - margin)
    ]:
        cross_size = Inches(0.2)
        h_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx - cross_size/2, cy, cross_size, Pt(1))
        h_line.fill.solid()
        h_line.fill.fore_color.rgb = GRID_LINE
        h_line.line.fill.background()
        
        v_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx, cy - cross_size/2, Pt(1), cross_size)
        v_line.fill.solid()
        v_line.fill.fore_color.rgb = GRID_LINE
        v_line.line.fill.background()
        
    # Footer Metadata Bar
    footer_box = slide.shapes.add_textbox(Inches(0.6), height - Inches(0.65), width - Inches(1.2), Inches(0.35))
    tf = footer_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = f"Kelompok 1 AI (PT Vinix Seven Aurum) | Bagian II: Integrasi Aplikasi (Kenny Helim - BINUS) | Slide {slide_num_str} / 20"
    p.font.size = Pt(9)
    p.font.color.rgb = TEXT_MUTED
    p.font.bold = False

def create_header(slide, title_text, category_badge="BAGIAN II: INTEGRASI APLIKASI"):
    """Create unified technical header box with badge."""
    # Category badge
    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(0.55), Inches(3.2), Inches(0.32))
    badge.fill.solid()
    badge.fill.fore_color.rgb = AMBER_BG
    badge.line.color.rgb = AMBER_ACCENT
    badge.line.width = Pt(1)
    tf_b = badge.text_frame
    tf_b.word_wrap = True
    p_b = tf_b.paragraphs[0]
    p_b.text = category_badge
    p_b.font.size = Pt(10)
    p_b.font.bold = True
    p_b.font.color.rgb = AMBER_ACCENT
    p_b.alignment = PP_ALIGN.CENTER
    
    # Title
    tb = slide.shapes.add_textbox(Inches(0.6), Inches(0.85), Inches(16.5), Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY

def add_speaker_note(slide, script_text):
    """Add word-for-word spoken Indonesian script to slide notes."""
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.text = script_text

def build_presentation():
    print(f"[*] Loading base presentation: {IAN_PPTX}", flush=True)
    if not IAN_PPTX.exists():
        raise FileNotFoundError(f"Input presentation not found: {IAN_PPTX}")
        
    prs = Presentation(str(IAN_PPTX))
    width = prs.slide_width
    height = prs.slide_height
    blank_layout = prs.slide_layouts[6]
    
    print(f"[+] Loaded {len(prs.slides)} original slides from Ian (Width={width}, Height={height}).", flush=True)
    print("[*] Appending Slides 13 to 20 for Kenny's Application Integration...", flush=True)
    
    # ==============================================================================
    # SLIDE 13: Transisi & Arsitektur Integrasi Sistem (Handoff dari Ian)
    # ==============================================================================
    s13 = prs.slides.add_slide(blank_layout)
    apply_blueprint_background(s13, width, height, "13")
    create_header(s13, "Tahap 10: Transisi Model ML Menuju Antarmuka Keputusan Interaktif")
    
    # Left Card: Transisi & Filosofi Solusi
    c13_left = s13.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.8), Inches(8.0), Inches(7.0))
    c13_left.fill.solid()
    c13_left.fill.fore_color.rgb = CARD_BG
    c13_left.line.color.rgb = NAVY_BORDER
    c13_left.line.width = Pt(1.5)
    tf13_l = c13_left.text_frame
    tf13_l.word_wrap = True
    
    p = tf13_l.paragraphs[0]
    p.text = "Solusi Nyata Terhadap 3 Batasan ML (Slide 12):"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY
    
    points_13 = [
        ("1. Batasan Tanpa Model Skor:", "Model ML hanya memprediksi H/D/A. Solusi: Kami mengintegrasikan pemodelan Poisson untuk menghasilkan ekspektasi gol (Expected Goals - xG) dan tebakan skor realistis."),
        ("2. Batasan Fitur Statis:", "Model ML membekukan rating Elo pra-turnamen. Solusi: Kami merancang slider penyesuaian Elo dinamis (+/-200) dan pipeline ingesti CSV untuk memperbarui ranking secara real-time."),
        ("3. Batasan Bukan Sistem Keputusan (DSS):", "Model ML belum memberikan taktik terapan. Solusi: Kami membangun Laboratorium Taktik Underdog untuk tim kuda hitam (Kamboja, Laos) dan federasi di bawah naungan UN SDG 9.")
    ]
    for title, desc in points_13:
        p1 = tf13_l.add_paragraph()
        p1.text = f"\n{title}"
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = AMBER_ACCENT
        
        p2 = tf13_l.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_MUTED

    # Right Card: Arsitektur 4 Pilar Produksi
    c13_right = s13.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.9), Inches(1.8), Inches(8.2), Inches(7.0))
    c13_right.fill.solid()
    c13_right.fill.fore_color.rgb = CARD_BG
    c13_right.line.color.rgb = NAVY_BORDER
    c13_right.line.width = Pt(1.5)
    tf13_r = c13_right.text_frame
    tf13_r.word_wrap = True
    
    p = tf13_r.paragraphs[0]
    p.text = "Arsitektur Integrasi Sistem Produksi (End-to-End):"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY
    
    arch_points = [
        ("[Pilar 1] Model Core:", "Serialized Pipeline models/football_model.pkl (Multinomial Logistic Regression terkalibrasi)."),
        ("[Pilar 2] Mesin Elo Dinamis:", "scripts/elo_module.py menghitung perubahan peringkat secara real-time (k=32, Home Advantage=+100)."),
        ("[Pilar 3] Stochastic Simulator:", "scripts/04_asean_cup_simulator.py menjalankan 10.000 iterasi turnamen dalam 2 detik melalui matriks probabilitas in-memory."),
        ("[Pilar 4] Antarmuka Interaktif:", "Streamlit Decision Studio (app/streamlit_app.py) dengan 5 tab fungsional responsif, zero-leakage, dan monitoring real-time.")
    ]
    for title, desc in arch_points:
        p1 = tf13_r.add_paragraph()
        p1.text = f"\n{title}"
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = BLUE_ACCENT
        
        p2 = tf13_r.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_MUTED

    add_speaker_note(s13, (
        "NASKAH PEMBICARA KENNY HELIM (Slide 13):\n"
        "'Terima kasih banyak kepada rekan saya, Ian, atas pemaparan yang sangat komprehensif mengenai fondasi data "
        "dan alur Machine Learning yang telah kami bangun.\n\n"
        "Selamat pagi/siang Bapak Aslan Alwi dan Bapak Bimo Rizki. Melanjutkan penjelasan Ian, pada Slide 12 tadi rekan saya "
        "telah memetakan 3 batasan utama dari model ML murni: model tidak memiliki tebakan skor, fiturnya statis sebelum kickoff, "
        "dan belum menjadi alat pengambil keputusan.\n\n"
        "Di Bagian Kedua ini, saya—Kenny Helim—akan mempresentasikan bagaimana saya mengintegrasikan seluruh bobot matematis "
        "tersebut ke dalam aplikasi produksi interaktif (Streamlit Decision Support Studio) yang secara tuntas menjawab "
        "ketiga batasan tersebut di bawah pilar UN SDG 9.'"
    ))

    # ==============================================================================
    # SLIDE 14: Menjawab Batasan 1 - Pemodelan Skor Poisson & Tab 1 (Match Predictor)
    # ==============================================================================
    s14 = prs.slides.add_slide(blank_layout)
    apply_blueprint_background(s14, width, height, "14")
    create_header(s14, "Tab 1: Match Predictor Real-Time & Solusi Model Skor Poisson")
    
    # Left Card: Konsep & Rumus Poisson
    c14_left = s14.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.8), Inches(7.5), Inches(7.0))
    c14_left.fill.solid()
    c14_left.fill.fore_color.rgb = CARD_BG
    c14_left.line.color.rgb = NAVY_BORDER
    c14_left.line.width = Pt(1.5)
    tf14_l = c14_left.text_frame
    tf14_l.word_wrap = True
    
    p = tf14_l.paragraphs[0]
    p.text = "Solusi Batasan 1: Pemodelan Skor Poisson Dinamis"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY
    
    p1 = tf14_l.add_paragraph()
    p1.text = (
        "\nRegresi logistik standar hanya mengeluarkan probabilitas P(H), P(D), P(A), "
        "namun pelatih dan analis membutuhkan estimasi skor riil (Expected Goals - xG). "
        "Kami memecahkannya dengan memadukan ekspektasi Poisson:"
    )
    p1.font.size = Pt(11)
    p1.font.color.rgb = TEXT_MUTED
    
    p_box = tf14_l.add_paragraph()
    p_box.text = (
        "\nλ_home = max(0.6, AvgGF_home × 1.15) [Non-Netral]\n"
        "λ_away = max(0.5, AvgGF_away × 0.85) [Non-Netral]"
    )
    p_box.font.size = Pt(11)
    p_box.font.bold = True
    p_box.font.color.rgb = BLUE_ACCENT
    
    p2 = tf14_l.add_paragraph()
    p2.text = (
        "\nFitur Interaktif di Tab 1:\n"
        "• Slider Elo Offset (+/-200 poin): Simulasi instan pemain cedera / pilar baru.\n"
        "• Slider Form 5 Laga (0-15 poin): Penyesuaian momentum psikologis terkini.\n"
        "• Checkbox Lokasi Netral: Otomatis menghapus bonus tuan rumah (+100 poin Elo).\n"
        "• Prediksi Instan: Menghasilkan persentase Menang/Seri/Kalah dan estimasi skor "
        "(contoh: Indonesia vs Thailand: 1-1 atau 2-1) dalam hitungan milidetik."
    )
    p2.font.size = Pt(11)
    p2.font.color.rgb = TEXT_MUTED
    
    # Right Image: Tab 1 Screenshot
    img_tab1 = ARTIFACTS_DIR / "walkthrough_tab1_match_predictor.png"
    if img_tab1.exists():
        s14.shapes.add_picture(str(img_tab1), Inches(8.4), Inches(1.8), Inches(8.7), Inches(7.0))
        
    add_speaker_note(s14, (
        "NASKAH PEMBICARA KENNY HELIM (Slide 14):\n"
        "'Bapak Penguji, pada Slide 12 Ian menyebutkan bahwa model ML murni kita hanya mampu memprediksi Menang, Seri, atau Kalah "
        "tanpa bisa memperkirakan skor akhir. Di Tab 1 Match Predictor ini, saya menyelesaikan kelemahan tersebut dengan mengintegrasikan "
        "pemodelan distribusi Poisson Expected Goals (λ).\n\n"
        "Ketika pengguna memilih laga, misalnya Indonesia melawan Thailand, sistem tidak hanya menghitung peluang kemenangan terkalibrasi, "
        "tetapi juga menghitung ekspektasi gol kandang dan tandang. Kami juga menyematkan slider dinamis sehingga pelatih dapat "
        "mengubah nilai Elo sebesar +/-200 poin secara langsung—misalnya jika ada pemain naturalisasi baru yang masuk—dan hasilnya "
        "langsung terhitung ulang secara instan tanpa perlu melatih ulang model.'"
    ))

    # ==============================================================================
    # SLIDE 15: Menjawab Batasan 2 - Ingesti CSV Dinamis & Rekalibrasi Elo (Tab 2)
    # ==============================================================================
    s15 = prs.slides.add_slide(blank_layout)
    apply_blueprint_background(s15, width, height, "15")
    create_header(s15, "Tab 2: Ingesti Data Dinamis & Rekalibrasi Peringkat Tanpa Retrain")
    
    c15_left = s15.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.8), Inches(7.5), Inches(7.0))
    c15_left.fill.solid()
    c15_left.fill.fore_color.rgb = CARD_BG
    c15_left.line.color.rgb = NAVY_BORDER
    c15_left.line.width = Pt(1.5)
    tf15_l = c15_left.text_frame
    tf15_l.word_wrap = True
    
    p = tf15_l.paragraphs[0]
    p.text = "Solusi Batasan 2: Pembaruan Data Real-Time Tanpa Retrain"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY
    
    p1 = tf15_l.add_paragraph()
    p1.text = (
        "\nPada penelitian ML umum, jika ada 2 atau 3 pertandingan baru yang selesai digelar, "
        "keseluruhan model harus dilatih ulang dari awal (expensive & slow). Di Tab 2 ini, "
        "kami membangun Ingestion Pipeline cerdas:"
    )
    p1.font.size = Pt(11)
    p1.font.color.rgb = TEXT_MUTED
    
    features_15 = [
        ("1. Validasi Skema Otomatis:", "Memeriksa kelengkapan kolom wajib (home_team, away_team, skor, tanggal), menolak skor negatif atau data korup."),
        ("2. Anti-Leakage Chronological Sort:", "Pertandingan diurutkan berdasarkan tanggal secara absolut sebelum dieksekusi."),
        ("3. Rekalibrasi Elo Instan:", "Mesin Elo Engine (k=32) memperbarui rating kedua tim dan menyimpannya langsung ke sesi memori aktif."),
        ("4. Template CSV Siap Pakai:", "Pengguna dapat mengunduh format CSV resmi hanya dengan satu klik.")
    ]
    for t, d in features_15:
        p_t = tf15_l.add_paragraph()
        p_t.text = f"\n{t}"
        p_t.font.size = Pt(11)
        p_t.font.bold = True
        p_t.font.color.rgb = GREEN_ACCENT
        p_d = tf15_l.add_paragraph()
        p_d.text = d
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = TEXT_MUTED

    img_tab2 = ARTIFACTS_DIR / "walkthrough_tab2_csv_ingestion.png"
    if img_tab2.exists():
        s15.shapes.add_picture(str(img_tab2), Inches(8.4), Inches(1.8), Inches(8.7), Inches(7.0))
        
    add_speaker_note(s15, (
        "NASKAH PEMBICARA KENNY HELIM (Slide 15):\n"
        "'Batasan kedua yang dipaparkan Ian adalah bahwa fitur ML bersifat statis sebelum turnamen dimulai. Di dunia nyata, "
        "turnamen berlangsung selama beberapa minggu dan kekuatan tim terus berkembang setiap kali sebuah laga selesai.\n\n"
        "Di Tab 2 ini, saya merancang Dynamic CSV Ingestion Pipeline. Analis federasi dapat memasukkan data hasil pertandingan baru "
        "cukup dengan mengunggah file CSV. Sistem secara cerdas memvalidasi format data, mengurutkannya secara kronologis agar tidak "
        "terjadi data leakage, dan mesin Elo secara otomatis merekalibrasi rating tim di memori aktif. Hasilnya: seluruh prediksi di tab "
        "lainnya langsung terbarukan tanpa perlu melatih ulang model selama berjam-jam.'"
    ))

    # ==============================================================================
    # SLIDE 16: Tab 3 - Simulasi Turnamen Monte Carlo Interaktif (10k Iterasi)
    # ==============================================================================
    s16 = prs.slides.add_slide(blank_layout)
    apply_blueprint_background(s16, width, height, "16")
    create_header(s16, "Tab 3: Simulasi Turnamen Monte Carlo Interaktif (10.000 Iterasi)")
    
    c16_left = s16.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.8), Inches(7.5), Inches(7.0))
    c16_left.fill.solid()
    c16_left.fill.fore_color.rgb = CARD_BG
    c16_left.line.color.rgb = NAVY_BORDER
    c16_left.line.width = Pt(1.5)
    tf16_l = c16_left.text_frame
    tf16_l.word_wrap = True
    
    p = tf16_l.paragraphs[0]
    p.text = "Eksplorasi Stokastik 10.000 Alam Semesta Paralel"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY
    
    p1 = tf16_l.add_paragraph()
    p1.text = (
        "\nJika di Slide 10 dan 11 Ian memaparkan hasil simulasi statis di notebook, "
        "di Tab 3 ini kami mengubahnya menjadi simulator interaktif berbasis web:"
    )
    p1.font.size = Pt(11)
    p1.font.color.rgb = TEXT_MUTED
    
    points_16 = [
        ("Eksekusi Cepat (Sub-2 Detik):", "180 kombinasi probabilitas antar-tim ASEAN di-cache di memori, sehingga 10.000 iterasi selesai seketika dengan progress bar live."),
        ("Format Turnamen Riil AFF:", "Mensimulasikan Fase Grup round-robin (Grup A & B), Semifinal 2 Leg, dan Final 2 Leg dengan agregat gol."),
        ("Konsistensi Hierarki Big 4 (100% Stabil):", "Thailand (30.80%), Indonesia (27.22%), Vietnam (23.88%), Malaysia (15.56%), dan Underdogs (~2.54%)."),
        ("Transparansi Jalur Turnamen:", "Menampilkan pohon bagan turnamen lengkap untuk memantau perjalanan tim unggulan vs kejutan underdog.")
    ]
    for t, d in points_16:
        p_t = tf16_l.add_paragraph()
        p_t.text = f"\n{t}"
        p_t.font.size = Pt(11)
        p_t.font.bold = True
        p_t.font.color.rgb = BLUE_ACCENT
        p_d = tf16_l.add_paragraph()
        p_d.text = d
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = TEXT_MUTED

    img_tab3 = ARTIFACTS_DIR / "walkthrough_tab3_monte_carlo.png"
    if img_tab3.exists():
        s16.shapes.add_picture(str(img_tab3), Inches(8.4), Inches(1.8), Inches(8.7), Inches(7.0))
        
    add_speaker_note(s16, (
        "NASKAH PEMBICARA KENNY HELIM (Slide 16):\n"
        "'Pada Tab 3, kami membawa simulasi Monte Carlo 10.000 iterasi yang dijelaskan Ian langsung ke hadapan pengguna. "
        "Dengan sekali klik pada tombol interaktif, pengguna dapat menyaksikan progress bar berjalan real-time dan melihat bagaimana "
        "10.000 skenario turnamen diundi secara stokastik.\n\n"
        "Hasilnya terbukti sangat konsisten: Thailand memimpin dengan 30.8%, disusul ketat oleh Indonesia 27.2%, Vietnam 23.9%, "
        "dan Malaysia 15.6%. Di tabel aplikasi, pengguna juga dapat melihat probabilitas masing-masing tim untuk lolos fase grup, semifinal, "
        "hingga partai puncak. Ini membuktikan bahwa probabilitas yang kami hasilkan tidak hanya berupa angka tunggal, melainkan "
        "sebuah spektrum risiko turnamen yang utuh.'"
    ))

    # ==============================================================================
    # SLIDE 17: Tab 4 - Evaluasi 52 Laga AFF & Monograf Komparasi vs YOLO11
    # ==============================================================================
    s17 = prs.slides.add_slide(blank_layout)
    apply_blueprint_background(s17, width, height, "17")
    create_header(s17, "Tab 4: Evaluasi 52 Laga AFF & Komparasi Ilmiah vs YOLO11")
    
    c17_left = s17.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.8), Inches(7.5), Inches(7.0))
    c17_left.fill.solid()
    c17_left.fill.fore_color.rgb = CARD_BG
    c17_left.line.color.rgb = NAVY_BORDER
    c17_left.line.width = Pt(1.5)
    tf17_l = c17_left.text_frame
    tf17_l.word_wrap = True
    
    p = tf17_l.paragraphs[0]
    p.text = "Integritas Evaluasi & Perbandingan Paradigma AI"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY
    
    p1 = tf17_l.add_paragraph()
    p1.text = (
        "\n1. Pembuktian Metrik Uji 52 Laga AFF:\n"
        "• Log Loss: 0.5966 (Jauh mengungguli threshold <= 0.8198 & Naive 1.0686)\n"
        "• Akurasi Klasifikasi: 75.00% (39 dari 52 laga benar)\n"
        "• Brier Score: 0.3331 (Terkalibrasi ketat tanpa overconfidence)"
    )
    p1.font.size = Pt(11)
    p1.font.color.rgb = TEXT_MUTED
    
    p2 = tf17_l.add_paragraph()
    p2.text = "\n2. Komparasi Metodologi vs YOLO11 (Computer Vision):"
    p2.font.size = Pt(12)
    p2.font.bold = True
    p2.font.color.rgb = AMBER_ACCENT
    
    yolo_comp = [
        ("YOLO11 (Spatial / Computer Vision):", "Fokus pada deteksi bola & koordinat pemain 90 menit per frame. Butuh GPU ribuan watt, kamera multi-sudut berbiaya miliaran, dan tidak mampu memprediksi pemenang sebelum laga dimulai."),
        ("Tabular DSS (Model Kami):", "Hemat energi (berjalan di CPU biasa), mencakup 49.945 pertandingan lintas dekade, dan langsung memberikan estimasi probabilitas juara turnamen untuk federasi (SDG 9).")
    ]
    for t, d in yolo_comp:
        p_t = tf17_l.add_paragraph()
        p_t.text = f"\n{t}"
        p_t.font.size = Pt(10.5)
        p_t.font.bold = True
        p_t.font.color.rgb = NAVY_PRIMARY
        p_d = tf17_l.add_paragraph()
        p_d.text = d
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = TEXT_MUTED

    img_tab4 = ARTIFACTS_DIR / "walkthrough_tab4_model_evaluation.png"
    if img_tab4.exists():
        s17.shapes.add_picture(str(img_tab4), Inches(8.4), Inches(1.8), Inches(8.7), Inches(7.0))
        
    add_speaker_note(s17, (
        "NASKAH PEMBICARA KENNY HELIM (Slide 17):\n"
        "'Bapak Penguji, pada Tab 4 kami menyajikan evaluasi model pada 52 laga AFF Championship. Di sini terlihat jelas bahwa "
        "model kami mencatat Log Loss 0.5966, yang membuktikan kualitas kalibrasi tinggi karena berhasil melampaui ambang batas 0.8198 "
        "dengan tingkat akurasi 75%.\n\n"
        "Selain itu, kami menyusun monograf ilmiah perbandingan terhadap Computer Vision YOLO11. Sering muncul pertanyaan: 'Mengapa tidak "
        "memakai YOLO11 saja?' Di sini kami jawab dengan tegas: YOLO11 luar biasa untuk melacak pemain selama 90 menit pertandingan, "
        "namun butuh GPU mahal dan tidak bisa meramal hasil sebelum kickoff. Sebaliknya, pendekatan Tabular Decision Support System kami "
        "sangat efisien, inklusif di bawah SDG 9, dan mampu memprediksi dinamika turnamen jangka panjang.'"
    ))

    # ==============================================================================
    # SLIDE 18: Tab 5 - Target Penerima Manfaat & Underdog Counter-Tactics Lab (SDG 9)
    # ==============================================================================
    s18 = prs.slides.add_slide(blank_layout)
    apply_blueprint_background(s18, width, height, "18")
    create_header(s18, "Tab 5: Target Penerima Manfaat & Playbook Kontra-Taktik (SDG 9)")
    
    c18_left = s18.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.8), Inches(7.5), Inches(7.0))
    c18_left.fill.solid()
    c18_left.fill.fore_color.rgb = CARD_BG
    c18_left.line.color.rgb = NAVY_BORDER
    c18_left.line.width = Pt(1.5)
    tf18_l = c18_left.text_frame
    tf18_l.word_wrap = True
    
    p = tf18_l.paragraphs[0]
    p.text = "Inovasi & Dampak Terapan di Bawah UN SDG 9"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY
    
    p1 = tf18_l.add_paragraph()
    p1.text = (
        "\nSesuai mandat UN SDG 9 (Industri, Inovasi, dan Infrastruktur), kami tidak "
        "membiarkan hasil riset berhenti sebagai teori. Kami merancang 3 kluster penerima manfaat:"
    )
    p1.font.size = Pt(11)
    p1.font.color.rgb = TEXT_MUTED
    
    beneficiaries = [
        ("1. Tim Kuda Hitam (Kamboja, Laos, Myanmar):", "Mengetahui batas realistis, mengeksploitasi laga kandang (Home Advantage), dan mengunci poin seri."),
        ("2. Federasi Nasional (PSSI, FAT, VFF):", "Panduan rotasi skuad di fase grup berisiko rendah dan seleksi lawan uji coba untuk mendongkrak poin Elo FIFA."),
        ("3. Media & Broadcaster:", "Panduan liputan berbasis Upset Probability Index untuk menaikkan nilai keterlibatan audiens.")
    ]
    for t, d in beneficiaries:
        p_t = tf18_l.add_paragraph()
        p_t.text = f"\n{t}"
        p_t.font.size = Pt(11)
        p_t.font.bold = True
        p_t.font.color.rgb = GREEN_ACCENT
        p_d = tf18_l.add_paragraph()
        p_d.text = d
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = TEXT_MUTED
        
    p_lab = tf18_l.add_paragraph()
    p_lab.text = (
        "\nLaboratorium Taktik Interaktif:\n"
        "Slider kedalaman bertahan (Low Block) & serangan balik membuktikan bahwa tim underdog "
        "mampu menaikkan peluang poin hingga +14.2% melawan raksasa ASEAN."
    )
    p_lab.font.size = Pt(10.5)
    p_lab.font.bold = True
    p_lab.font.color.rgb = AMBER_ACCENT

    img_tab5 = ARTIFACTS_DIR / "walkthrough_tab5_tactical_optimizer.png"
    if img_tab5.exists():
        s18.shapes.add_picture(str(img_tab5), Inches(8.4), Inches(1.8), Inches(8.7), Inches(7.0))
        
    add_speaker_note(s18, (
        "NASKAH PEMBICARA KENNY HELIM (Slide 18):\n"
        "'Bapak Penguji, inilah puncak dari integrasi sistem kami di Tab 5: menjawab mandat UN SDG 9. "
        "Alat analitik elit di industri sepak bola seperti Opta atau StatsBomb berharga miliaran rupiah dan hanya bisa diakses "
        "oleh klub raksasa Eropa. Melalui Decision Support Studio terbuka ini, kami mendemokratisasi akses analitik canggih untuk "
        "tiga kelompok penerima manfaat.\n\n"
        "Khususnya bagi tim kuda hitam seperti Kamboja, Laos, atau Myanmar, pelatih mereka dapat membuka Laboratorium Taktik kami, "
        "mengatur slider pertahanan Low Block, dan melihat secara terukur bahwa strategi pertahanan rapat mampu meningkatkan probabilitas "
        "mereka meraih poin seri sebesar 14.2% saat berhadapan dengan raksasa seperti Thailand atau Vietnam.'"
    ))

    # ==============================================================================
    # SLIDE 19: Standar Rekayasa Perangkat Lunak: 42 Real Unittest & Video Walkthrough
    # ==============================================================================
    s19 = prs.slides.add_slide(blank_layout)
    apply_blueprint_background(s19, width, height, "19")
    create_header(s19, "Kualitas Rekayasa: 42 Real Unittest, Video Walkthrough & Repositori")
    
    # 3 Column Layout
    col_w = Inches(5.0)
    col_gap = Inches(0.4)
    c19_top = Inches(1.8)
    c19_h = Inches(7.0)
    
    # Col 1: 42 Real Unittest
    col1 = s19.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), c19_top, col_w, c19_h)
    col1.fill.solid()
    col1.fill.fore_color.rgb = CARD_BG
    col1.line.color.rgb = NAVY_BORDER
    col1.line.width = Pt(1.5)
    tf1 = col1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "1. 42 Real Unittests\n(100% Passing)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = GREEN_ACCENT
    
    p1 = tf1.add_paragraph()
    p1.text = (
        "\n• Test Suite Lengkap:\n"
        "  - test_model_and_simulation.py\n"
        "  - test_elo.py & test_features.py\n"
        "  - test_streamlit_app.py\n"
        "  - test_compliance_and_invariants.py\n\n"
        "• Adversarial Stress Test:\n"
        "  Menguji skenario ekstrem: delta Elo +/-10.000, data kosong (OOV), dan stabilitas stokastik Monte Carlo (5 seed berbeda).\n\n"
        "• Waktu Eksekusi: 3.294 detik (Zero Failures)."
    )
    p1.font.size = Pt(10.5)
    p1.font.color.rgb = TEXT_MUTED

    # Col 2: Video Walkthrough
    col2 = s19.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6) + col_w + col_gap, c19_top, col_w, c19_h)
    col2.fill.solid()
    col2.fill.fore_color.rgb = CARD_BG
    col2.line.color.rgb = NAVY_BORDER
    col2.line.width = Pt(1.5)
    tf2 = col2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "2. Video Walkthrough\n(Full HD 30 FPS)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = BLUE_ACCENT
    
    p2 = tf2.add_paragraph()
    p2.text = (
        "\n• Perekaman Otomatis Robot:\n"
        "  Menggunakan Playwright Chromium headless untuk menelusuri kelima tab aplikasi secara mulus.\n\n"
        "• Transcoding FFmpeg:\n"
        "  Format MP4 (H.264 / 1280x800) berukuran 3.03 MB siap putar saat sidang.\n\n"
        "• Tangkapan Layar HD:\n"
        "  5 bukti tangkapan layar resolusi tinggi diarsipkan langsung di folder docs/ dan Desktop."
    )
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = TEXT_MUTED

    p_link2 = tf2.add_paragraph()
    r_lbl2 = p_link2.add_run()
    r_lbl2.text = "\n▶ Link Google Drive (Video & App ZIP):"
    r_lbl2.font.bold = True
    r_lbl2.font.size = Pt(9.5)
    r_lbl2.font.color.rgb = BLUE_ACCENT

    p_url2 = tf2.add_paragraph()
    r_url2 = p_url2.add_run()
    r_url2.text = "Buka Folder Google Drive Resmi"
    r_url2.hyperlink.address = "https://drive.google.com/drive/folders/1jqriPVp8YfardBAeW4K0WoVlVqcjP2f6?usp=sharing"
    r_url2.font.bold = True
    r_url2.font.underline = True
    r_url2.font.size = Pt(9.5)
    r_url2.font.color.rgb = BLUE_ACCENT

    p_raw2 = tf2.add_paragraph()
    r_raw2 = p_raw2.add_run()
    r_raw2.text = "drive.google.com/drive/folders/\n1jqriPVp8YfardBAeW4K0WoVlVqcjP2f6"
    r_raw2.font.size = Pt(8)
    r_raw2.font.color.rgb = TEXT_MUTED

    # Col 3: Repositori GitHub
    col3 = s19.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6) + (col_w * 2) + (col_gap * 2), c19_top, col_w, c19_h)
    col3.fill.solid()
    col3.fill.fore_color.rgb = CARD_BG
    col3.line.color.rgb = NAVY_BORDER
    col3.line.width = Pt(1.5)
    tf3 = col3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "3. Repositori GitHub\n(Branch main Resmi)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = AMBER_ACCENT
    
    p3 = tf3.add_paragraph()
    p3.text = (
        "\n• Isolasi Mandiri kenny_version/:\n"
        "  112 berkas kode, model, naskah, dan batch runner tersimpan rapi tanpa merusak berkas asli Ihram.\n\n"
        "• Root README Resmi:\n"
        "  Dilengkapi lencana kelayakan, petunjuk 1-klik, dan tabel pembagian tugas tim."
    )
    p3.font.size = Pt(9.5)
    p3.font.color.rgb = TEXT_MUTED

    p_link3 = tf3.add_paragraph()
    r_lbl3 = p_link3.add_run()
    r_lbl3.text = "\n▶ Link Repositori GitHub (main):"
    r_lbl3.font.bold = True
    r_lbl3.font.size = Pt(9.5)
    r_lbl3.font.color.rgb = AMBER_ACCENT

    p_url3 = tf3.add_paragraph()
    r_url3 = p_url3.add_run()
    r_url3.text = "Buka Repositori GitHub Kelompok 1"
    r_url3.hyperlink.address = "https://github.com/Iank-Syahputra/prediction_football"
    r_url3.font.bold = True
    r_url3.font.underline = True
    r_url3.font.size = Pt(9.5)
    r_url3.font.color.rgb = AMBER_ACCENT

    p_raw3 = tf3.add_paragraph()
    r_raw3 = p_raw3.add_run()
    r_raw3.text = "github.com/Iank-Syahputra/\nprediction_football"
    r_raw3.font.size = Pt(8)
    r_raw3.font.color.rgb = TEXT_MUTED

    add_speaker_note(s19, (
        "NASKAH PEMBICARA KENNY HELIM (Slide 19):\n"
        "'Untuk membuktikan bahwa sistem ini memenuhi standar rekayasa perangkat lunak profesional, seluruh kode kami "
        "dilindungi oleh 42 unit test dan adversarial stress test yang menguji skenario batas ekstrim. Seluruh pengujian "
        "lulus 100% dalam waktu 3,2 detik.\n\n"
        "Kami juga telah merekam video demo aplikasi secara otomatis beresolusi Full HD menggunakan robot browser Playwright "
        "dan FFmpeg, sehingga demonstrasi dapat diputar kapan saja secara offline. Berkas video demo dan arsip aplikasi .zip "
        "telah kami simpan di Google Drive resmi Kelompok 1. Dan yang terpenting, seluruh 112 berkas kode kami telah terunggah "
        "resmi di GitHub pada branch main dalam folder mandiri kenny_version tanpa merusak berkas rekan saya.'"
    ))

    # ==============================================================================
    # SLIDE 20: Kesimpulan, Penutup & Sesi Tanya Jawab (Closing & Q&A)
    # ==============================================================================
    s20 = prs.slides.add_slide(blank_layout)
    apply_blueprint_background(s20, width, height, "20")
    create_header(s20, "Kesimpulan: Dari Model Teoritis Menuju Solusi Nyata Berbasis SDG 9")
    
    # Upper Card: Synthesis & Contributions
    c20 = s20.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.8), Inches(16.0), Inches(4.7))
    c20.fill.solid()
    c20.fill.fore_color.rgb = CARD_BG
    c20.line.color.rgb = NAVY_BORDER
    c20.line.width = Pt(1.5)
    tf20 = c20.text_frame
    tf20.word_wrap = True
    
    p = tf20.paragraphs[0]
    p.text = "Rangkuman Kontribusi Kelompok 1 (Divisi Artificial Intelligence):"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY
    
    concl_points = [
        ("1. Keberhasilan Metodologis:", "Mengubah 49.945 data sejarah FIFA menjadi model multinomial terkalibrasi dengan Log Loss 0.5966 pada 52 laga AFF (melampaui target ambang batas <= 0.8198)."),
        ("2. Keberhasilan Rekayasa Sistem:", "Menjawab ketiga batasan model ML murni melalui integrasi distribusi Poisson, slider adaptabilitas real-time, dan penyerapan dataset dinamis tanpa biaya re-training."),
        ("3. Dampak Terapan Berkelanjutan (SDG 9):", "Menghadirkan Decision Support Studio gratis bagi federasi dan tim underdog untuk mengoptimasi strategi olahraga secara terukur."),
        ("4. Kepatuhan Akademik Penuh:", "Memenuhi seluruh persyaratan penilaian Tugas Akhir Magang MSIB Batch 10 (PT Vinix Seven Aurum) dengan durasi magang 4 Bulan (MUTLAK).")
    ]
    for t, d in concl_points:
        p_t = tf20.add_paragraph()
        p_t.text = f"\n{t}"
        p_t.font.size = Pt(11)
        p_t.font.bold = True
        p_t.font.color.rgb = BLUE_ACCENT
        p_d = tf20.add_paragraph()
        p_d.text = d
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = TEXT_MUTED

    # Lower Card: Official Digital Archive Resource Hub (Google Drive & GitHub)
    c_res = s20.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(6.7), Inches(16.0), Inches(2.1))
    c_res.fill.solid()
    c_res.fill.fore_color.rgb = RGBColor(241, 245, 249)  # Slate 100
    c_res.line.color.rgb = BLUE_ACCENT
    c_res.line.width = Pt(1.5)
    tf_res = c_res.text_frame
    tf_res.word_wrap = True

    p_rh = tf_res.paragraphs[0]
    p_rh.text = "PUSAT ARSIP DIGITAL KELOMPOK 1 (SIAP AKSES DEWAN PENGUJI & MENTOR):"
    p_rh.font.size = Pt(11.5)
    p_rh.font.bold = True
    p_rh.font.color.rgb = NAVY_PRIMARY

    # Google Drive Link
    p_gd = tf_res.add_paragraph()
    r_gdl = p_gd.add_run()
    r_gdl.text = "1. Google Drive (Video Walkthrough Full HD + Standalone Application ZIP): "
    r_gdl.font.bold = True
    r_gdl.font.size = Pt(10)
    r_gdl.font.color.rgb = BLUE_ACCENT

    r_gdu = p_gd.add_run()
    r_gdu.text = "https://drive.google.com/drive/folders/1jqriPVp8YfardBAeW4K0WoVlVqcjP2f6?usp=sharing"
    r_gdu.hyperlink.address = "https://drive.google.com/drive/folders/1jqriPVp8YfardBAeW4K0WoVlVqcjP2f6?usp=sharing"
    r_gdu.font.bold = True
    r_gdu.font.underline = True
    r_gdu.font.size = Pt(9.5)
    r_gdu.font.color.rgb = BLUE_ACCENT

    # GitHub Link
    p_gh = tf_res.add_paragraph()
    r_ghl = p_gh.add_run()
    r_ghl.text = "2. Repositori GitHub Resmi Kelompok 1 (Branch main): "
    r_ghl.font.bold = True
    r_ghl.font.size = Pt(10)
    r_ghl.font.color.rgb = AMBER_ACCENT

    r_ghu = p_gh.add_run()
    r_ghu.text = "https://github.com/Iank-Syahputra/prediction_football"
    r_ghu.hyperlink.address = "https://github.com/Iank-Syahputra/prediction_football"
    r_ghu.font.bold = True
    r_ghu.font.underline = True
    r_ghu.font.size = Pt(9.5)
    r_ghu.font.color.rgb = AMBER_ACCENT

    p_sync = tf_res.add_paragraph()
    p_sync.text = (
        "Terima kasih kepada Dosen Pembimbing & Dewan Penguji: Bapak Aslan Alwi & Bapak Bimo Rizki Abdusshamad "
        "— Sesi Diskusi & Tanya Jawab Dibuka —"
    )
    p_sync.font.size = Pt(10)
    p_sync.font.bold = True
    p_sync.font.color.rgb = GREEN_ACCENT
    p_sync.alignment = PP_ALIGN.CENTER

    add_speaker_note(s20, (
        "NASKAH PEMBICARA KENNY HELIM (Slide 20):\n"
        "'Sebagai penutup, proyek ini membuktikan bahwa Machine Learning bukan sekadar eksperimen matematika di dalam notebook, "
        "melainkan instrumen rekayasa perangkat lunak yang mampu menghasilkan dampak nyata bagi industri olahraga nasional.\n\n"
        "Saya, Kenny Helim dari BINUS University, bersama rekan saya Muhammad Ihram Syahputra, mengucapkan terima kasih yang sebesar-besarnya "
        "kepada Bapak Aslan Alwi dan Bapak Bimo Rizki Abdusshamad atas seluruh bimbingan berharga selama 4 bulan masa magang di PT Vinix Seven Aurum.\n\n"
        "Sekian presentasi dari Kelompok 1 AI. Kami sangat siap dan menyambut baik pertanyaan serta masukan dari Dewan Penguji. "
        "Terima kasih.'"
    ))

    # Save to all target paths
    print(f"[*] Saving combined presentation to: {OUTPUT_DESKTOP_PPTX}", flush=True)
    prs.save(str(OUTPUT_DESKTOP_PPTX))
    
    print(f"[*] Mirroring to root project: {OUTPUT_ROOT_PPTX}", flush=True)
    prs.save(str(OUTPUT_ROOT_PPTX))
    
    if OUTPUT_KENNY_DIR.exists():
        target_kenny = OUTPUT_KENNY_DIR / "FINAL_PROJECT_PRESENTATION_REVISED_PARADIGM.pptx"
        prs.save(str(target_kenny))
        print(f"[*] Mirrored to export folder: {target_kenny}", flush=True)
        
    print(f"[+] SUCCESS! Combined presentation generated with {len(prs.slides)} slides!", flush=True)

if __name__ == "__main__":
    build_presentation()

