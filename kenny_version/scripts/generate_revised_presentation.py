"""
# ==============================================================================
# [MODULE GOAL & ROLE]
# scripts/generate_revised_presentation.py
#
# Generates the authoritative 11-Slide Defense Presentation Deck:
#   - FINAL_PROJECT_PRESENTATION_REVISED_PARADIGM.pptx (Root & docs/)
# Adheres strictly to the 16:9 widescreen executive design standard
# (Navy #0F172A, Slate #1E293B, Crisp White #F8FAFC, Emerald #10B981, Amber #F59E0B)
# for the final defense scheduled between 2 - 6 November 2026.
#
# [INTENTIONAL DESIGN DECISIONS - DO NOT REMOVE]
# 1. 16:9 Widescreen standard (13.333" x 7.5" = 12192000 x 6858000 EMU).
# 2. Strict 11-Slide revised paradigm structure mapped directly to Survey Specs Section 6.
# 3. Verified empirical numbers from Worker M2 handoff & artifacts:
#    - Kaggle dataset: 49,945 total matches, 44,450 modern era (>=1960).
#    - Train split: 38,288 matches (1960-2020); Test split: 6,162 matches (2021-2026).
#    - 52 AFF Championship evaluation matches: Log Loss 0.5966 vs Baseline 1.0686 (<=0.8198 target).
#    - Accuracy on 52 matches: 75.00%, Brier Score 0.3331, Macro F1 0.5490, Weighted F1 0.6796.
#    - Monte Carlo 10,000 runs: Thailand 31.26%, Indonesia 27.99%, Vietnam 22.79%, Malaysia 15.08%, Underdogs 2.88%.
# 4. Academic Invariants strictly enforced:
#    - Presenter: Kenny Helim (BINUS University, Information System and Management).
#    - Kelompok 1 (Prediction International Football), Divisi Artificial Intelligence.
#    - Host: PT Vinix Seven Aurum, Fast Track MSIB Batch 10.
#    - Mentors: Pak Aslan Alwi & Bimo Rizki Abdusshamad.
#    - Periode Magang: 4 Bulan MUTLAK.
#    - UN SDG Alignment: SDG 9 (Industri, Inovasi, dan Infrastruktur).
#
# [SOLVED PAST MISTAKES & ANTIDOTES - NEVER REPEAT]
# 1. In PPTX text boxes, python-pptx default margins can push text outside shapes.
#    Antidote: Explicitly set margin_top/bottom/left/right to compact values (0.05"-0.1").
# 2. Windows CP1252 console unicode errors on emoji symbols in stdout.
#    Antidote: Clean text or handle encoding cleanly in Python.
# 3. Slide shape overlap and text wrapping failure.
#    Antidote: Word wrap enabled on every text frame, calculated geometry constraints.
#
# [SESSION REVISION & CHAT MILESTONE LEDGER]
# - 2026-10-30T15:45:00Z: Initial synthesis of revised paradigm 11-slide presentation generator.
# ==============================================================================
"""

import os
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ------------------------------------------------------------------------------
# COLOR PALETTE SPECIFICATION (Executive Dark Theme)
# ------------------------------------------------------------------------------
COLOR_BG_NAVY = RGBColor(15, 23, 42)        # #0F172A (Deep Slate Navy)
COLOR_CARD_SLATE = RGBColor(30, 41, 59)     # #1E293B (Slate 800)
COLOR_CARD_ALT = RGBColor(24, 33, 47)       # #18212F (Slate 850)
COLOR_BORDER = RGBColor(51, 65, 85)         # #334155 (Slate 700)
COLOR_BORDER_LIGHT = RGBColor(71, 85, 105)  # #475569 (Slate 600)

COLOR_TEXT_WHITE = RGBColor(248, 250, 252)  # #F8FAFC (White 50)
COLOR_TEXT_MUTED = RGBColor(148, 163, 184)  # #94A3B8 (Slate 400)
COLOR_TEXT_BODY = RGBColor(203, 213, 225)   # #CBD5E1 (Slate 300)
COLOR_TEXT_SUBTLE = RGBColor(100, 116, 139) # #64748B (Slate 500)

COLOR_EMERALD = RGBColor(16, 185, 129)      # #10B981 (Success / Lift)
COLOR_EMERALD_BG = RGBColor(6, 78, 59)      # #064E3B (Dark Emerald Container)
COLOR_AMBER = RGBColor(245, 158, 11)        # #F59E0B (Highlight / Caution)
COLOR_AMBER_BG = RGBColor(120, 53, 15)      # #78350F (Dark Amber Container)
COLOR_SKY = RGBColor(56, 189, 248)          # #38BDF8 (Cyan / Info)
COLOR_SKY_BG = RGBColor(12, 74, 110)        # #0C4A6E (Dark Sky Container)
COLOR_PURPLE = RGBColor(168, 85, 247)       # #A855F7 (Specialized)
COLOR_ROSE = RGBColor(244, 63, 94)          # #F43F5E (Alert / Blind spot)

FONT_FAMILY = "Segoe UI"


def create_slide_header(slide, badge_text, title_text, subtitle_text, slide_num):
    """Adds standardized header, category badge, titles, and bottom footer."""
    # 1. Slide full-bleed background
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLOR_BG_NAVY
    bg.line.fill.background()

    # 2. Category / Track Pill Badge
    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.42), Inches(6.8), Inches(0.34))
    badge.fill.solid()
    badge.fill.fore_color.rgb = COLOR_CARD_SLATE
    badge.line.color.rgb = COLOR_BORDER
    badge.line.width = Pt(1)
    tf_b = badge.text_frame
    tf_b.word_wrap = True
    tf_b.margin_top = Inches(0.04)
    tf_b.margin_bottom = Inches(0.04)
    tf_b.margin_left = Inches(0.12)
    tf_b.margin_right = Inches(0.12)
    p_b = tf_b.paragraphs[0]
    p_b.text = badge_text.upper()
    p_b.font.name = FONT_FAMILY
    p_b.font.size = Pt(9.5)
    p_b.font.bold = True
    p_b.font.color.rgb = COLOR_SKY

    # 3. Main Slide Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.82), Inches(11.733), Inches(0.55))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_top = Inches(0.0)
    tf_t.margin_bottom = Inches(0.0)
    tf_t.margin_left = Inches(0.0)
    tf_t.margin_right = Inches(0.0)
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.name = FONT_FAMILY
    p_t.font.size = Pt(21)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_TEXT_WHITE

    # 4. Slide Subtitle
    sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.38), Inches(11.733), Inches(0.35))
    tf_s = sub_box.text_frame
    tf_s.word_wrap = True
    tf_s.margin_top = Inches(0.0)
    tf_s.margin_bottom = Inches(0.0)
    tf_s.margin_left = Inches(0.0)
    tf_s.margin_right = Inches(0.0)
    p_s = tf_s.paragraphs[0]
    p_s.text = subtitle_text
    p_s.font.name = FONT_FAMILY
    p_s.font.size = Pt(11.5)
    p_s.font.color.rgb = COLOR_TEXT_MUTED

    # 5. Footer divider and text
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.96), Inches(11.733), Pt(1))
    line.fill.solid()
    line.fill.fore_color.rgb = COLOR_BORDER
    line.line.fill.background()

    footer_left = slide.shapes.add_textbox(Inches(0.8), Inches(7.04), Inches(8.0), Inches(0.32))
    tf_fl = footer_left.text_frame
    tf_fl.margin_top = Inches(0.0)
    tf_fl.margin_left = Inches(0.0)
    p_fl = tf_fl.paragraphs[0]
    p_fl.text = "PT Vinix Seven Aurum • Fast Track MSIB Batch 10 (Divisi AI - Kelompok 1) • Kenny Helim (BINUS University)"
    p_fl.font.name = FONT_FAMILY
    p_fl.font.size = Pt(8.5)
    p_fl.font.color.rgb = COLOR_TEXT_SUBTLE

    footer_right = slide.shapes.add_textbox(Inches(9.0), Inches(7.04), Inches(3.533), Inches(0.32))
    tf_fr = footer_right.text_frame
    tf_fr.margin_top = Inches(0.0)
    tf_fr.margin_right = Inches(0.0)
    p_fr = tf_fr.paragraphs[0]
    p_fr.alignment = PP_ALIGN.RIGHT
    p_fr.text = f"Slide {slide_num} of 11 • Sidang Evaluasi: 2 - 6 November 2026"
    p_fr.font.name = FONT_FAMILY
    p_fr.font.size = Pt(8.5)
    p_fr.font.color.rgb = COLOR_TEXT_SUBTLE


def add_container_card(slide, left, top, width, height, bg_color=COLOR_CARD_SLATE, border_color=COLOR_BORDER):
    """Creates a rounded container card shape for structured content."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1)
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_top = Inches(0.12)
    tf.margin_bottom = Inches(0.12)
    tf.margin_left = Inches(0.14)
    tf.margin_right = Inches(0.14)
    return card


def add_stat_pill(slide, left, top, width, height, value_text, label_text, sub_text="", accent_color=COLOR_EMERALD):
    """Creates a high-impact metric KPI card."""
    card = add_container_card(slide, left, top, width, height, bg_color=COLOR_CARD_SLATE, border_color=COLOR_BORDER)
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_top = Inches(0.1)
    tf.margin_bottom = Inches(0.08)
    tf.margin_left = Inches(0.12)
    tf.margin_right = Inches(0.12)

    # Paragraph 1: Large Metric Value
    p1 = tf.paragraphs[0]
    p1.text = value_text
    p1.font.name = FONT_FAMILY
    p1.font.size = Pt(22)
    p1.font.bold = True
    p1.font.color.rgb = accent_color

    # Paragraph 2: Metric Label
    p2 = tf.add_paragraph()
    p2.text = label_text
    p2.font.name = FONT_FAMILY
    p2.font.size = Pt(10.5)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_TEXT_WHITE

    # Paragraph 3: Context / Subtext
    if sub_text:
        p3 = tf.add_paragraph()
        p3.text = sub_text
        p3.font.name = FONT_FAMILY
        p3.font.size = Pt(8.5)
        p3.font.color.rgb = COLOR_TEXT_MUTED

    return card


def append_bullet_point(text_frame, title, body, bold_title=True, font_size=Pt(10), title_color=COLOR_TEXT_WHITE, body_color=COLOR_TEXT_BODY):
    """Appends a structured bullet entry with colored bold lead and explanation."""
    p = text_frame.add_paragraph()
    p.space_after = Pt(4)
    p.font.name = FONT_FAMILY
    p.font.size = font_size

    run_title = p.add_run()
    run_title.text = "• " + title + (" — " if body else "")
    run_title.font.bold = bold_title
    run_title.font.color.rgb = title_color

    if body:
        run_body = p.add_run()
        run_body.text = body
        run_body.font.bold = False
        run_body.font.color.rgb = body_color


# ==============================================================================
# SLIDE BUILDERS (11 STRICT REVISED PARADIGM SLIDES)
# ==============================================================================

def build_slide_1(prs):
    """Slide 1: Executive Title & Academic Governance."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    create_slide_header(
        slide,
        badge_text="FAST TRACK MSIB BATCH 10 • FINAL PROJECT DEFENSE • DIVISI ARTIFICIAL INTELLIGENCE",
        title_text="Prediksi Hasil Pertandingan Sepak Bola Internasional & Probabilitas Juara ASEAN Cup",
        subtitle_text="Pemodelan Probabilistik Berbasis Dynamic Elo Engine, Logistic Regression & 10.000 Simulasi Stokastik Monte Carlo",
        slide_num=1
    )

    # Hero Box: Executive Overview
    hero = add_container_card(slide, Inches(0.8), Inches(1.85), Inches(11.733), Inches(1.7), bg_color=COLOR_CARD_ALT, border_color=COLOR_SKY)
    tf_h = hero.text_frame
    p0 = tf_h.paragraphs[0]
    p0.text = "PROYEK AKHIR DIVISI ARTIFICIAL INTELLIGENCE — PT VINIX SEVEN AURUM"
    p0.font.name = FONT_FAMILY
    p0.font.size = Pt(11)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_SKY

    p1 = tf_h.add_paragraph()
    p1.space_before = Pt(4)
    p1.text = "Membangun Decision Support System (DSS) berbasis Sport Science untuk mengeliminasi bias emosional dan intuisi subjektif dalam analisis sepak bola internasional. Menggabungkan data historis 49.000+ pertandingan resmi, pemodelan zero-leakage, kalibrasi Cross-Entropy Log Loss (0.5966 pada 52 laga AFF), dan 10.000 iterasi Monte Carlo."
    p1.font.name = FONT_FAMILY
    p1.font.size = Pt(10.5)
    p1.font.color.rgb = COLOR_TEXT_BODY

    # 4 Metadata Cards Across the Bottom
    card_w = Inches(2.78)
    card_gap = Inches(0.20)
    top_pos = Inches(3.72)
    card_h = Inches(3.05)

    # Card 1: Student & Academic Affiliation
    c1 = add_container_card(slide, Inches(0.8) + 0 * (card_w + card_gap), top_pos, card_w, card_h)
    tf1 = c1.text_frame
    p = tf1.paragraphs[0]
    p.text = "PENYUSUN & KELOMPOK"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD

    append_bullet_point(tf1, "Nama Mahasiswa", "Kenny Helim", title_color=COLOR_TEXT_WHITE)
    append_bullet_point(tf1, "Universitas", "Bina Nusantara (BINUS University)", title_color=COLOR_TEXT_WHITE)
    append_bullet_point(tf1, "Program Studi", "Information System & Management", title_color=COLOR_TEXT_WHITE)
    append_bullet_point(tf1, "Kontak / Email", "kenny.helim@binus.ac.id", title_color=COLOR_TEXT_WHITE)
    append_bullet_point(tf1, "Divisi / Grup", "AI — Kelompok 1 (Prediction International Football)", title_color=COLOR_TEXT_WHITE)

    # Card 2: Kelompok 1 Roster
    c2 = add_container_card(slide, Inches(0.8) + 1 * (card_w + card_gap), top_pos, card_w, card_h)
    tf2 = c2.text_frame
    p = tf2.paragraphs[0]
    p.text = "ANGGOTA KELOMPOK 1"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_SKY

    append_bullet_point(tf2, "Kenny Helim", "BINUS University", title_color=COLOR_TEXT_WHITE)
    append_bullet_point(tf2, "Arya Wicaksana", "Universitas Esa Unggul", title_color=COLOR_TEXT_WHITE)
    append_bullet_point(tf2, "M. Ihram Syahputra", "Universitas Halu Oleo", title_color=COLOR_TEXT_WHITE)
    append_bullet_point(tf2, "Gisela Venska M.", "President University", title_color=COLOR_TEXT_WHITE)
    append_bullet_point(tf2, "Christian", "BINUS University", title_color=COLOR_TEXT_WHITE)

    # Card 3: Host Company & Mentorship
    c3 = add_container_card(slide, Inches(0.8) + 2 * (card_w + card_gap), top_pos, card_w, card_h)
    tf3 = c3.text_frame
    p = tf3.paragraphs[0]
    p.text = "TATA KELOLA & MENTOR"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMBER

    append_bullet_point(tf3, "Host Mitra", "PT Vinix Seven Aurum", title_color=COLOR_TEXT_WHITE)
    append_bullet_point(tf3, "Program", "Fast Track MSIB Batch 10", title_color=COLOR_TEXT_WHITE)
    append_bullet_point(tf3, "Mentor 1", "Pak Aslan Alwi", title_color=COLOR_TEXT_WHITE)
    append_bullet_point(tf3, "Mentor 2", "Bimo Rizki Abdusshamad", title_color=COLOR_TEXT_WHITE)
    append_bullet_point(tf3, "Periode Magang", "4 Bulan MUTLAK (Academic Invariant)", title_color=COLOR_TEXT_WHITE)

    # Card 4: Academic Alignment & Scope Disclaimer
    c4 = add_container_card(slide, Inches(0.8) + 3 * (card_w + card_gap), top_pos, card_w, card_h)
    tf4 = c4.text_frame
    p = tf4.paragraphs[0]
    p.text = "DAMPAK & DISCLAIMER"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_PURPLE

    append_bullet_point(tf4, "Keselarasan SDG", "UN SDG 9: Industri, Inovasi, & Infrastruktur", title_color=COLOR_TEXT_WHITE)
    append_bullet_point(tf4, "Klasifikasi Solusi", "Decision Support System (DSS) untuk Sport Science", title_color=COLOR_TEXT_WHITE)
    append_bullet_point(tf4, "Jadwal Evaluasi", "Sidang Akhir: 2 - 6 November 2026", title_color=COLOR_TEXT_WHITE)
    append_bullet_point(tf4, "Batasan Etis", "Bukan ramalan mutlak atau perjudian komersial", title_color=COLOR_TEXT_WHITE)


def build_slide_2(prs):
    """Slide 2: Core Problem Statement & The Imperative for Objectivity."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    create_slide_header(
        slide,
        badge_text="FOUNDATIONAL FRAMING • THE IMPERATIVE FOR OBJECTIVITY • SDG 9",
        title_text="Mengeliminasi Bias Subjektif, Opini Pundit & Distorsi Emosional dalam Prediksi Olahraga",
        subtitle_text="Transformasi dari Punditry Intuitif Menjadi Decision Support System (DSS) Berbasis Sains Probabilistik",
        slide_num=2
    )

    col_w = Inches(5.72)
    top_pos = Inches(1.85)
    col_h = Inches(4.92)

    # Left Column: The Problem (Emotional Punditry & Subjective Bias)
    left_card = add_container_card(slide, Inches(0.8), top_pos, col_w, col_h, bg_color=COLOR_CARD_SLATE, border_color=COLOR_ROSE)
    tf_l = left_card.text_frame
    p_lh = tf_l.paragraphs[0]
    p_lh.text = "KRISIS ANALISIS OLAHRAGA TRADISIONAL (PUNDITRY BIAS)"
    p_lh.font.name = FONT_FAMILY
    p_lh.font.size = Pt(12)
    p_lh.font.bold = True
    p_lh.font.color.rgb = COLOR_ROSE

    append_bullet_point(
        tf_l, "Heuristic Availability & Recency Bias",
        "Pundit dan fans kerap melebih-lebihkan peluang tim hanya karena satu kemenangan dramatis terakhir atau transfer pemain baru, mengabaikan tren jangka panjang.",
        font_size=Pt(9.5)
    )
    append_bullet_point(
        tf_l, "Ilusi Determinisme Biner ('Pasti Menang!')",
        "Opini konvensional terjebak dalam tebakan mutlak biner (Menang vs Kalah), mengaburkan variansi inheren olahraga di mana peluang seri (Draw) mencapai 22.7%. Keunggulan marjinal 51% disalahartikan sebagai kepastian 100%.",
        font_size=Pt(9.5)
    )
    append_bullet_point(
        tf_l, "Distorsi Emosional & Rasionalisasi Retrospektif",
        "Setelah pertandingan usai, analis menciptakan narasi pasca-fakta ('tim kurang berhasrat') untuk menjelaskan hasil yang secara fundamental dipengaruhi oleh stokastisitas taktis.",
        font_size=Pt(9.5)
    )
    append_bullet_point(
        tf_l, "Keterbatasan Spreadsheet Manual",
        "Navigasi tabulasi manual rawan salah hitung, tidak mampu memperbarui rating kekuatan dinamis, dan tidak memiliki protokol evaluasi ilmiah out-of-time.",
        font_size=Pt(9.5)
    )

    # Right Column: The Solution & UN SDG 9 Alignment
    right_card = add_container_card(slide, Inches(6.81), top_pos, col_w, col_h, bg_color=COLOR_CARD_SLATE, border_color=COLOR_EMERALD)
    tf_r = right_card.text_frame
    p_rh = tf_r.paragraphs[0]
    p_rh.text = "TRANSFORMASI SAINS & TIGA PILAR KESELARASAN UN SDG 9"
    p_rh.font.name = FONT_FAMILY
    p_rh.font.size = Pt(12)
    p_rh.font.bold = True
    p_rh.font.color.rgb = COLOR_EMERALD

    append_bullet_point(
        tf_r, "Pilar 1: Infrastruktur Data Terbuka (Open Data Infrastructure)",
        "Membangun pipeline komputasi olahraga modular, terstandarisasi, dan 100% reproducible menggunakan 49.000+ pertandingan resmi tanpa terkunci di balik vendor berbayar mahal.",
        font_size=Pt(9.5)
    )
    append_bullet_point(
        tf_r, "Pilar 2: Inovasi Riset Olahraga Nasional (Sport Science Innovation)",
        "Menggantikan tebakan intuisi dengan model probabilistik terkalibrasi halus (Log Loss 0.5966) dan simulasi turnamen 10.000 putaran, memungkinkan federasi (PSSI/AFF) dan tim nasional merancang kontra-strategi berbasis bukti empiris.",
        font_size=Pt(9.5)
    )
    append_bullet_point(
        tf_r, "Pilar 3: Demokratisasi Kecerdasan Buatan (AI Democratization)",
        "Menyediakan aplikasi web analitik interaktif gratis (Streamlit) yang dapat diakses oleh pelatih lokal, analis independen, mahasiswa, dan jurnalis tanpa memerlukan lisensi komersial ribuan dolar.",
        font_size=Pt(9.5)
    )
    append_bullet_point(
        tf_r, "Prinsip Sport Science Modern",
        "Outcome = Kekuatan Sejati (Latent Elo) + Momentum Form + Faktor Venue + Variansi Stokastik. Model tidak pernah mengklaim ramalan mutlak, melainkan estimasi probabilitas terkalibrasi.",
        font_size=Pt(9.5)
    )


def build_slide_3(prs):
    """Slide 3: Scope, Data Foundation & Temporal Barrier."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    create_slide_header(
        slide,
        badge_text="DATASET ARCHITECTURE • STRICT ZERO-LEAKAGE TIME SPLIT • KAGGLE MARTJ42",
        title_text="Pondasi Data 49.000+ Pertandingan & Disiplin Anti-Leakage 'Tanpa Mesin Waktu'",
        subtitle_text="Larangan Keras Random Split: Membagi Data Latih, Uji Out-of-Time, dan Evaluasi Spesifik ASEAN",
        slide_num=3
    )

    col_w = Inches(3.72)
    gap = Inches(0.28)
    top_pos = Inches(1.85)
    col_h = Inches(4.92)

    # Box 1: Dataset Anatomy & Hygiene
    b1 = add_container_card(slide, Inches(0.8) + 0 * (col_w + gap), top_pos, col_w, col_h, border_color=COLOR_SKY)
    tf1 = b1.text_frame
    p1 = tf1.paragraphs[0]
    p1.text = "1. ANATOMI DATASET RESMI"
    p1.font.name = FONT_FAMILY
    p1.font.size = Pt(11.5)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_SKY

    append_bullet_point(tf1, "Sumber Data Utama", "Kaggle martj42 (Database pertandingan sepak bola internasional resmi 1872 - 2026).", font_size=Pt(9))
    append_bullet_point(tf1, "Skala & Cakupan", "49.945 baris pertandingan, 337 tim nasional resmi, 225 jenis turnamen internasional.", font_size=Pt(9))
    append_bullet_point(tf1, "Kondisi Integritas", "0 missing values pada kolom krusial (date, home_team, away_team, home_score, away_score).", font_size=Pt(9))
    append_bullet_point(tf1, "Penyelarasan Nama", "Normalisasi entitas historis tim nasional (misal: Burma -> Myanmar, Malaya -> Malaysia).", font_size=Pt(9))
    append_bullet_point(tf1, "Filter Era Modern", "Hanya mencakup laga era modern (>= 1960) dengan tim beranggotakan >= 3 laga, menghasilkan 44.450 pertandingan berintegritas tinggi.", font_size=Pt(9))

    # Box 2: Chronological Train-Test Division
    b2 = add_container_card(slide, Inches(0.8) + 1 * (col_w + gap), top_pos, col_w, col_h, border_color=COLOR_EMERALD)
    tf2 = b2.text_frame
    p2 = tf2.paragraphs[0]
    p2.text = "2. STRATEGI PEMBAGIAN WAKTU"
    p2.font.name = FONT_FAMILY
    p2.font.size = Pt(11.5)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_EMERALD

    append_bullet_point(tf2, "Larangan Keras Random Split", "Random train_test_split dilarang mutlak karena mengizinkan model 'melihat masa depan' untuk memprediksi masa lalu.", font_size=Pt(9))
    append_bullet_point(tf2, "Dataset Latih Historis", "1960 s.d. 31 Des 2020 (38.288 baris pertandingan) sebagai basis estimasi parameter model.", font_size=Pt(9))
    append_bullet_point(tf2, "Dataset Uji Out-of-Time", "1 Jan 2021 s.d. Okt 2026 (6.162 baris pertandingan) untuk validasi performa generalisasi di masa depan.", font_size=Pt(9))
    append_bullet_point(tf2, "Target Evaluasi Spesifik", "Tepat 52 pertandingan kompetitif AFF Championship (Desember 2021 s.d. Januari 2023) sebagai benchmark final regional.", font_size=Pt(9))
    append_bullet_point(tf2, "Isolasi Adu Penalti", "Skor adu penalti (shootouts) dikunci terpisah; target 3-class dimodelkan murni dari waktu normal/extra-time.", font_size=Pt(9))

    # Box 3: Anti-Leakage Golden Rule
    b3 = add_container_card(slide, Inches(0.8) + 2 * (col_w + gap), top_pos, col_w, col_h, border_color=COLOR_AMBER)
    tf3 = b3.text_frame
    p3 = tf3.paragraphs[0]
    p3.text = "3. PROTOKOL ANTI-LEAKAGE"
    p3.font.name = FONT_FAMILY
    p3.font.size = Pt(11.5)
    p3.font.bold = True
    p3.font.color.rgb = COLOR_AMBER

    append_bullet_point(tf3, "Aturan Besi Garis Waktu", "Semua fitur prediktor untuk pertandingan pada waktu T dihitung STRICTLY sebelum peluit kick-off laga T berbunyi.", font_size=Pt(9))
    append_bullet_point(tf3, "Pembaruan Pasca-Laga", "Rating Elo dan poin form baru diperbarui ke dalam sistem setelah peluit panjang ditiup.", font_size=Pt(9))
    append_bullet_point(tf3, "Pencegahan Hindsight Bias", "Model diuji dalam kondisi nyata seolah-olah sedang berdiri di hari H pertandingan tanpa mengetahui hasil akhir.", font_size=Pt(9))
    append_bullet_point(tf3, "Standardisasi Skalar", "StandardScaler dilatih HANYA pada data latih (1960-2020) lalu diterapkan pada data uji tanpa data leakage mean/std.", font_size=Pt(9))
    append_bullet_point(tf3, "Validitas Ilmiah Mutlak", "Memenuhi standar forensik data science ketat arahan Pak Aslan & Bimo Rizki Abdusshamad.", font_size=Pt(9))


def build_slide_4(prs):
    """Slide 4: AI Methodology Architecture & Feature Engineering."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    create_slide_header(
        slide,
        badge_text="AI METHODOLOGY • DYNAMIC ELO RATING • 24 TABULAR PREDICTORS",
        title_text="Arsitektur Metodologi AI & Rekayasa 24 Fitur Prediktor Pra-Laga",
        subtitle_text="Integrasi Dinamis Kekuatan Sejati (Elo Engine), Momentum Form 5 Laga, Head-to-Head & Konteks Venue",
        slide_num=4
    )

    col_w = Inches(3.72)
    gap = Inches(0.28)
    top_pos = Inches(1.85)
    col_h = Inches(4.92)

    # Box 1: Dynamic Elo Engine
    b1 = add_container_card(slide, Inches(0.8) + 0 * (col_w + gap), top_pos, col_w, col_h, border_color=COLOR_SKY)
    tf1 = b1.text_frame
    p1 = tf1.paragraphs[0]
    p1.text = "1. DYNAMIC ELO ENGINE"
    p1.font.name = FONT_FAMILY
    p1.font.size = Pt(11.5)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_SKY

    append_bullet_point(tf1, "Formulasi Matematis", "R_new = R_old + K * (S - E), dengan K=32.0 dan R0=1500.0 baseline kekuatan global.", font_size=Pt(9))
    append_bullet_point(tf1, "Home Advantage Offset", "R_home_eff = R_home + (1 - is_neutral) * H, dengan H=100.0 poin Elo (rasio win kandang 1.73x).", font_size=Pt(9))
    append_bullet_point(tf1, "Ekspektasi Logistik", "E_A = 1 / (1 + 10^((R_B - R_A_eff)/400)), menghitung peluang teoritis menang.", font_size=Pt(9))
    append_bullet_point(tf1, "5 Variabel Elo", "home_elo, away_elo, diff_elo, elo_expected_home, elo_expected_away diekstraksi pra-laga.", font_size=Pt(9))
    append_bullet_point(tf1, "Non-Stationary Tracking", "Menangkap kebangkitan atau kemerosotan performa tim lintas dekade secara dinamis.", font_size=Pt(9))

    # Box 2: Momentum Form & H2H Matrix
    b2 = add_container_card(slide, Inches(0.8) + 1 * (col_w + gap), top_pos, col_w, col_h, border_color=COLOR_EMERALD)
    tf2 = b2.text_frame
    p2 = tf2.paragraphs[0]
    p2.text = "2. FORM 5 LAGA & HISTORIS"
    p2.font.name = FONT_FAMILY
    p2.font.size = Pt(11.5)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_EMERALD

    append_bullet_point(tf2, "Rolling Form Window (5 Laga)", "Akumulasi poin 5 laga terakhir (W=3, D=1, L=0) untuk mengukur momentum teraktual tim.", font_size=Pt(9))
    append_bullet_point(tf2, "Goal Scoring & Defense", "Rata-rata gol memasukkan (avg_gf_5) dan gol kemasukan (avg_ga_5) dalam 5 pertandingan terakhir.", font_size=Pt(9))
    append_bullet_point(tf2, "Head-to-Head (H2H) Rekor", "h2h_home_win_rate menangkap sejarah pertemuan langsung spesifik kedua negara (kecocokan taktik).", font_size=Pt(9))
    append_bullet_point(tf2, "Pondasi Sepanjang Masa", "home_hist_wr dan away_hist_wr menghitung rasio kemenangan kumulatif sejak era 1960.", font_size=Pt(9))
    append_bullet_point(tf2, "Struktur Deque Efisien", "Perhitungan rolling window menggunakan antrean FIFO berkecepatan tinggi O(1).", font_size=Pt(9))

    # Box 3: Differentials & Match Context
    b3 = add_container_card(slide, Inches(0.8) + 2 * (col_w + gap), top_pos, col_w, col_h, border_color=COLOR_AMBER)
    tf3 = b3.text_frame
    p3 = tf3.paragraphs[0]
    p3.text = "3. DIFFERENTIALS & KONTEKS"
    p3.font.name = FONT_FAMILY
    p3.font.size = Pt(11.5)
    p3.font.bold = True
    p3.font.color.rgb = COLOR_AMBER

    append_bullet_point(tf3, "Sinyal Diferensial", "diff_form_pts, diff_hist_wr, diff_goal_power, dan diff_recent_gd mengukur jurang kualitas kedua tim.", font_size=Pt(9))
    append_bullet_point(tf3, "Konteks Tempat Netral", "is_neutral (1 jika laga di tempat netral). Menangkap fenomena degradasi home advantage dari 50.7% ke 44.2%.", font_size=Pt(9))
    append_bullet_point(tf3, "Uji Coba vs Turnamen", "is_friendly memisahkan pertandingan eksibisi/persahabatan dari turnamen kompetitif resmi.", font_size=Pt(9))
    append_bullet_point(tf3, "24 Dimensi Lengkap", "Membentuk vektor fitur tabular padat tanpa nilai null yang siap diproses oleh model klasifikasi.", font_size=Pt(9))
    append_bullet_point(tf3, "Transparansi Penuh", "Setiap fitur memiliki makna domain fisik nyata (Explainable AI) sesuai arahan Pak Bimo.", font_size=Pt(9))


def build_slide_5(prs):
    """Slide 5: Deep Technical Divergence: Tabular Probabilistic Forecasting vs YOLO11 Road Damage Object Detection."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    create_slide_header(
        slide,
        badge_text="CROSS-PARADIGM ANALYSIS • CURRICULUM SYNTHESIS GUIDED BY PAK ASLAN • AI DIVISION",
        title_text="Divergensi Paradigma AI: Tabular Forecasting vs YOLO11 Road Damage Detection",
        subtitle_text="Membedah Perbedaan Mendasar Topologi Masalah, Fungsi Kerugian (Loss), Kalibrasi, dan Eliminasi Distraktor",
        slide_num=5
    )

    col_w = Inches(2.78)
    gap = Inches(0.20)
    top_pos = Inches(1.85)
    col_h = Inches(4.92)

    # Column 1: Problem Space & Data Representation
    c1 = add_container_card(slide, Inches(0.8) + 0 * (col_w + gap), top_pos, col_w, col_h, border_color=COLOR_SKY)
    tf1 = c1.text_frame
    p1 = tf1.paragraphs[0]
    p1.text = "1. TOPOLOGI & DATA"
    p1.font.name = FONT_FAMILY
    p1.font.size = Pt(11)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_SKY

    append_bullet_point(tf1, "Prediksi Sepak Bola", "Stokastik multi-agen dinamis dalam deret waktu.", font_size=Pt(8.5), title_color=COLOR_EMERALD)
    append_bullet_point(tf1, "Format Input Tabular", "Vektor 1D terstruktur (D=24 fitur) dari rekam jejak historis.", font_size=Pt(8.5))
    append_bullet_point(tf1, "YOLO11 Aspal Jalanan", "Deteksi objek deterministik spasial 2D.", font_size=Pt(8.5), title_color=COLOR_AMBER)
    append_bullet_point(tf1, "Format Input Gambar", "Tensor piksel 3D (3 x 640 x 640) dari kamera kendaraan.", font_size=Pt(8.5))
    append_bullet_point(tf1, "Arsitektur Model", "Football: Calibrated Logistic + Monte Carlo DAG vs YOLO11: Deep CNN CSPNet/C3k2.", font_size=Pt(8.5))

    # Column 2: Loss Function & Optimization
    c2 = add_container_card(slide, Inches(0.8) + 1 * (col_w + gap), top_pos, col_w, col_h, border_color=COLOR_EMERALD)
    tf2 = c2.text_frame
    p2 = tf2.paragraphs[0]
    p2.text = "2. LOSS & OPTIMASI"
    p2.font.name = FONT_FAMILY
    p2.font.size = Pt(11)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_EMERALD

    append_bullet_point(tf2, "Football Loss Function", "Cross-Entropy / Multi-Class Log Loss (L_log = -sum y_c ln p_c).", font_size=Pt(8.5), title_color=COLOR_EMERALD)
    append_bullet_point(tf2, "Penalti Overconfidence", "Menghukum keras prediksi yang 'terlalu yakin tetapi salah'. Menghasilkan probabilitas realistis.", font_size=Pt(8.5))
    append_bullet_point(tf2, "YOLO11 Compound Loss", "L_CIoU (overlap geometris) + L_DFL (koordinat kontur) + L_BCE (klasifikasi boks).", font_size=Pt(8.5), title_color=COLOR_AMBER)
    append_bullet_point(tf2, "Target Optimasi", "Football: Kalibrasi probabilitas kontinu vs YOLO11: Regresi koordinat piksel [x, y, w, h].", font_size=Pt(8.5))

    # Column 3: Uncertainty vs NMS
    c3 = add_container_card(slide, Inches(0.8) + 2 * (col_w + gap), top_pos, col_w, col_h, border_color=COLOR_AMBER)
    tf3 = c3.text_frame
    p3 = tf3.paragraphs[0]
    p3.text = "3. KALIBRASI VS NMS"
    p3.font.name = FONT_FAMILY
    p3.font.size = Pt(11)
    p3.font.bold = True
    p3.font.color.rgb = COLOR_AMBER

    append_bullet_point(tf3, "Kebutuhan Kalibrasi", "Football: Kalibrasi probabilitas mutlak wajib karena p langsung menjadi parameter distribusi multinomial Monte Carlo.", font_size=Pt(8.5), title_color=COLOR_EMERALD)
    append_bullet_point(tf3, "Metrik Evaluasi", "Football: Log Loss (<=0.8198), Brier Score, Multiclass Accuracy.", font_size=Pt(8.5))
    append_bullet_point(tf3, "YOLO11 Confidence", "Confidence score hanya ranking heuristic tanpa kalibrasi empiris mutlak.", font_size=Pt(8.5), title_color=COLOR_AMBER)
    append_bullet_point(tf3, "Post-Processing NMS", "YOLO11 menerapkan Non-Maximum Suppression (IoU > 0.45) untuk memangkas boks ganda.", font_size=Pt(8.5))
    append_bullet_point(tf3, "Metrik Evaluasi Vision", "mAP@0.5, mAP@0.5:0.95, Precision-Recall AUC.", font_size=Pt(8.5))

    # Column 4: Distractors & Negative Samples
    c4 = add_container_card(slide, Inches(0.8) + 3 * (col_w + gap), top_pos, col_w, col_h, border_color=COLOR_PURPLE)
    tf4 = c4.text_frame
    p4 = tf4.paragraphs[0]
    p4.text = "4. SAMPEL NEGATIF"
    p4.font.name = FONT_FAMILY
    p4.font.size = Pt(11)
    p4.font.bold = True
    p4.font.color.rgb = COLOR_PURPLE

    append_bullet_point(tf4, "Dilema Hasil Seri (Draw)", "Football: Seri (22.7%) bukan kesalahan label, melainkan ekuilibrium taktis menit akhir.", font_size=Pt(8.5), title_color=COLOR_EMERALD)
    append_bullet_point(tf4, "Edge Distraktor Jalanan", "YOLO11: Bayangan pohon, genangan aspal basah, dan tutup gorong-gorong (manhole) mirip lubang jalan.", font_size=Pt(8.5), title_color=COLOR_AMBER)
    append_bullet_point(tf4, "Solusi Vision", "Augmentasi Mosaic, MixUp, dan hard negative mining untuk membedakan tekstur semu.", font_size=Pt(8.5))
    append_bullet_point(tf4, "Hardware Inference", "Football: CPU ringan (<0.1ms/laga) vs YOLO11: GPU/Edge TPU (TensorRT 30+ FPS).", font_size=Pt(8.5))
    append_bullet_point(tf4, "Kesimpulan Bersama", "Keduanya menuntaskan masalah nyata SDG 9 melalui sains AI yang tepat sasaran.", font_size=Pt(8.5))


def build_slide_6(prs):
    """Slide 6: Rigorous Model Evaluation on 52 ASEAN Matches."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    create_slide_header(
        slide,
        badge_text="EMPIRICAL BENCHMARK • OUT-OF-TIME EVALUATION • 52 AFF MATCHES",
        title_text="Evaluasi Kinerja Model: Keberhasilan Memangkas Log Loss pada 52 Laga AFF",
        subtitle_text="Verifikasi Out-of-Time: Mengalahkan Baseline Tanpa Informasi dan Melampaui Batas Target Evaluasi",
        slide_num=6
    )

    # Row of 4 KPI Metric Pills
    pill_w = Inches(2.78)
    pill_gap = Inches(0.20)
    top_pills = Inches(1.85)
    pill_h = Inches(1.35)

    add_stat_pill(
        slide, Inches(0.8) + 0 * (pill_w + pill_gap), top_pills, pill_w, pill_h,
        value_text="0.5966",
        label_text="LOG LOSS TERCAPAI",
        sub_text="Target: <= 0.8198 | Baseline: 1.0686 (Lift: -0.4720)",
        accent_color=COLOR_EMERALD
    )
    add_stat_pill(
        slide, Inches(0.8) + 1 * (pill_w + pill_gap), top_pills, pill_w, pill_h,
        value_text="75.00%",
        label_text="AKURASI PADA 52 LAGA",
        sub_text="Baseline Majority: 47.89% (Peningkatan: +27.11%)",
        accent_color=COLOR_SKY
    )
    add_stat_pill(
        slide, Inches(0.8) + 2 * (pill_w + pill_gap), top_pills, pill_w, pill_h,
        value_text="0.3331",
        label_text="BRIER MULTI-CLASS SCORE",
        sub_text="Kalibrasi probabilitas ketat mendekati realitas",
        accent_color=COLOR_AMBER
    )
    add_stat_pill(
        slide, Inches(0.8) + 3 * (pill_w + pill_gap), top_pills, pill_w, pill_h,
        value_text="0.6796",
        label_text="WEIGHTED F1-SCORE",
        sub_text="Macro F1: 0.5490 pada 3 kelas target seimbang",
        accent_color=COLOR_PURPLE
    )

    # Two Large Bottom Containers
    col_w = Inches(5.72)
    top_bottom = Inches(3.38)
    bot_h = Inches(3.38)

    # Bottom Left: Benchmark Comparison
    b_left = add_container_card(slide, Inches(0.8), top_bottom, col_w, bot_h, border_color=COLOR_EMERALD)
    tf_bl = b_left.text_frame
    p_blh = tf_bl.paragraphs[0]
    p_blh.text = "PERBANDINGAN TERHADAP BASELINE (LIFT ANALYSIS)"
    p_blh.font.name = FONT_FAMILY
    p_blh.font.size = Pt(11.5)
    p_blh.font.bold = True
    p_blh.font.color.rgb = COLOR_EMERALD

    append_bullet_point(
        tf_bl, "Uninformative Prior Baseline (Log Loss: 1.0686)",
        "Tebakan seragam tanpa informasi fitur (p=0.333 per kelas). Baseline paling naif yang membuktikan apakah model memiliki kecerdasan prediktif.",
        font_size=Pt(9)
    )
    append_bullet_point(
        tf_bl, "Empirical Majority Baseline (Log Loss: 1.0401)",
        "Hanya menebak frekuensi historis kemenangan tuan rumah tanpa memperhitungkan siapa tim yang bertanding.",
        font_size=Pt(9)
    )
    append_bullet_point(
        tf_bl, "Calibrated Logistic Regression (Log Loss: 0.5966)",
        "Mengombinasikan 24 fitur (Elo + Form + H2H + Venue). Berhasil memangkas log loss sebesar -0.4435 poin di bawah baseline empiris dan -0.4720 di bawah uninformative prior.",
        font_size=Pt(9)
    )
    append_bullet_point(
        tf_bl, "Status Validasi",
        "PASSED (Surpasses target: 0.5966 <= 0.8198). Terbukti mengungguli model Random Forest (0.8614) dan Gradient Boosting (0.8608) dalam menghasilkan probabilitas terkalibrasi.",
        font_size=Pt(9)
    )

    # Bottom Right: Class Breakdown & Draw Blind Spot Analysis
    b_right = add_container_card(slide, Inches(6.81), top_bottom, col_w, bot_h, border_color=COLOR_SKY)
    tf_br = b_right.text_frame
    p_brh = tf_br.paragraphs[0]
    p_brh.text = "DETAIL KELAS & ANALISIS BLIND SPOT SERI (DRAW)"
    p_brh.font.name = FONT_FAMILY
    p_brh.font.size = Pt(11.5)
    p_brh.font.bold = True
    p_brh.font.color.rgb = COLOR_SKY

    append_bullet_point(
        tf_br, "Away Win (18 Laga Aktual)",
        "Precision: 83.33% | Recall: 83.33% | F1: 83.33%. Model sangat tajam mengidentifikasi keunggulan tim tamu berkualitas tinggi.",
        font_size=Pt(9)
    )
    append_bullet_point(
        tf_br, "Home Win (25 Laga Aktual)",
        "Precision: 70.59% | Recall: 96.00% | F1: 81.36%. Model menangkap dominasi tim tuan rumah hampir sempurna (24 dari 25 laga terdeteksi).",
        font_size=Pt(9)
    )
    append_bullet_point(
        tf_br, "Analisis Kejujuran Ilmiah: Draw Blind Spot (9 Laga Aktual)",
        "Precision: 0.0% | Recall: 0.0%. Hasil seri merupakan 'blind spot' inheren dalam sports analytics karena hasil imbang sering kali dipengaruhi oleh strategi parkir bus menit ke-85 atau blunder acak yang tidak tercermin dalam data pra-laga.",
        font_size=Pt(9)
    )
    append_bullet_point(
        tf_br, "Justifikasi Mengapa Log Loss Lebih Penting dari Akurasi",
        "Akurasi dapat menipu; Log Loss memaksa probabilitas hasil seri tetap berada di angka wajar (20-25%) saat simulasi Monte Carlo, mencegah overconfidence yang merusak turnamen.",
        font_size=Pt(9)
    )


def build_slide_7(prs):
    """Slide 7: 10,000-Run Monte Carlo Stochastic Tournament Simulation."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    create_slide_header(
        slide,
        badge_text="TOURNAMENT SIMULATION • 10,000 STOCHASTIC RUNS • ASEAN CUP BRACKET",
        title_text="Simulasi Turnamen Stokastik: Peta Peluang Juara ASEAN Cup (10.000 Putaran)",
        subtitle_text="Menjual Probabilitas Jujur Berdasarkan Simulasi Lengkap: Fase Grup, Semifinal 2-Leg, dan Final",
        slide_num=7
    )

    # 4 Contender Cards across the top
    card_w = Inches(2.78)
    card_gap = Inches(0.20)
    top_pos = Inches(1.85)
    card_h = Inches(2.35)

    # Contender 1: Thailand
    c1 = add_container_card(slide, Inches(0.8) + 0 * (card_w + card_gap), top_pos, card_w, card_h, border_color=COLOR_EMERALD)
    tf1 = c1.text_frame
    p1 = tf1.paragraphs[0]
    p1.text = "1. THAILAND (WAR ELEPHANTS)"
    p1.font.name = FONT_FAMILY
    p1.font.size = Pt(11)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_EMERALD

    p1_stat = tf1.add_paragraph()
    p1_stat.text = "31.26%"
    p1_stat.font.name = FONT_FAMILY
    p1_stat.font.size = Pt(22)
    p1_stat.font.bold = True
    p1_stat.font.color.rgb = COLOR_TEXT_WHITE

    append_bullet_point(tf1, "Peluang Juara", "Thailand: 31.26%", font_size=Pt(8.5))
    append_bullet_point(tf1, "Peluang Finalis", "54.40%", font_size=Pt(8.5))
    append_bullet_point(tf1, "Peluang Semifinal", "92.72%", font_size=Pt(8.5))
    append_bullet_point(tf1, "Target Revisi", "~30.97% (CI [30.07% - 31.88%])", font_size=Pt(8.5), title_color=COLOR_EMERALD)
    append_bullet_point(tf1, "Analisis Kekuatan", "Rating Elo tertinggi di ASEAN didukung kedalaman skuad teruji.", font_size=Pt(8))

    # Contender 2: Indonesia
    c2 = add_container_card(slide, Inches(0.8) + 1 * (card_w + card_gap), top_pos, card_w, card_h, border_color=COLOR_SKY)
    tf2 = c2.text_frame
    p2 = tf2.paragraphs[0]
    p2.text = "2. INDONESIA (TIM GARUDA)"
    p2.font.name = FONT_FAMILY
    p2.font.size = Pt(11)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_SKY

    p2_stat = tf2.add_paragraph()
    p2_stat.text = "27.99%"
    p2_stat.font.name = FONT_FAMILY
    p2_stat.font.size = Pt(22)
    p2_stat.font.bold = True
    p2_stat.font.color.rgb = COLOR_TEXT_WHITE

    append_bullet_point(tf2, "Peluang Juara", "Indonesia: 27.99%", font_size=Pt(8.5))
    append_bullet_point(tf2, "Peluang Finalis", "49.31%", font_size=Pt(8.5))
    append_bullet_point(tf2, "Peluang Semifinal", "85.97%", font_size=Pt(8.5))
    append_bullet_point(tf2, "Target Revisi", "~27.34% (CI [26.48% - 28.22%])", font_size=Pt(8.5), title_color=COLOR_SKY)
    append_bullet_point(tf2, "Analisis Kekuatan", "Pesaing terberat, lonjakan form positif dan home advantage masif GBK.", font_size=Pt(8))

    # Contender 3: Vietnam
    c3 = add_container_card(slide, Inches(0.8) + 2 * (card_w + card_gap), top_pos, card_w, card_h, border_color=COLOR_AMBER)
    tf3 = c3.text_frame
    p3 = tf3.paragraphs[0]
    p3.text = "3. VIETNAM (GOLDEN STAR)"
    p3.font.name = FONT_FAMILY
    p3.font.size = Pt(11)
    p3.font.bold = True
    p3.font.color.rgb = COLOR_AMBER

    p3_stat = tf3.add_paragraph()
    p3_stat.text = "22.79%"
    p3_stat.font.name = FONT_FAMILY
    p3_stat.font.size = Pt(22)
    p3_stat.font.bold = True
    p3_stat.font.color.rgb = COLOR_TEXT_WHITE

    append_bullet_point(tf3, "Peluang Juara", "Vietnam: 22.79%", font_size=Pt(8.5))
    append_bullet_point(tf3, "Peluang Finalis", "47.50%", font_size=Pt(8.5))
    append_bullet_point(tf3, "Peluang Semifinal", "88.49%", font_size=Pt(8.5))
    append_bullet_point(tf3, "Target Revisi", "~21.73% (CI [20.93% - 22.55%])", font_size=Pt(8.5), title_color=COLOR_AMBER)
    append_bullet_point(tf3, "Analisis Kekuatan", "Pertahanan rapat dan efisiensi konversi gol konsisten.", font_size=Pt(8))

    # Contender 4: Malaysia
    c4 = add_container_card(slide, Inches(0.8) + 3 * (card_w + card_gap), top_pos, card_w, card_h, border_color=COLOR_PURPLE)
    tf4 = c4.text_frame
    p4 = tf4.paragraphs[0]
    p4.text = "4. MALAYSIA (HARIMAU MALAYA)"
    p4.font.name = FONT_FAMILY
    p4.font.size = Pt(11)
    p4.font.bold = True
    p4.font.color.rgb = COLOR_PURPLE

    p4_stat = tf4.add_paragraph()
    p4_stat.text = "15.08%"
    p4_stat.font.name = FONT_FAMILY
    p4_stat.font.size = Pt(22)
    p4_stat.font.bold = True
    p4_stat.font.color.rgb = COLOR_TEXT_WHITE

    append_bullet_point(tf4, "Peluang Juara", "Malaysia: 15.08%", font_size=Pt(8.5))
    append_bullet_point(tf4, "Peluang Finalis", "36.15%", font_size=Pt(8.5))
    append_bullet_point(tf4, "Peluang Semifinal", "79.80%", font_size=Pt(8.5))
    append_bullet_point(tf4, "Target Revisi", "~15.40% (CI [14.71% - 16.12%])", font_size=Pt(8.5), title_color=COLOR_PURPLE)
    append_bullet_point(tf4, "Analisis Kekuatan", "Kuda hitam utama dengan potensi kejutan tinggi di fase gugur.", font_size=Pt(8))

    # Bottom Container: Underdogs & Simulation Mechanics
    b_bot = add_container_card(slide, Inches(0.8), Inches(4.35), Inches(11.733), Inches(2.45), border_color=COLOR_BORDER_LIGHT)
    tf_b = b_bot.text_frame
    p_bh = tf_b.paragraphs[0]
    p_bh.text = "PROBABILITAS TIM UNDERDOG & MEKANISME SIMULASI MONTE CARLO"
    p_bh.font.name = FONT_FAMILY
    p_bh.font.size = Pt(11.5)
    p_bh.font.bold = True
    p_bh.font.color.rgb = COLOR_SKY

    append_bullet_point(
        tf_b, "Peta Probabilitas Tim Kuda Hitam (Kumulatif 2.88% Juara)",
        "Singapura: 1.35% (Finalis 6.37%) | Filipina: 1.21% (Finalis 4.67%) | Myanmar: 0.31% (Finalis 1.38%) | Kamboja: 0.01% (Semifinal 2.05%) | Timor-Leste: 0.00% (Semifinal 0.12%) | Laos: 0.00% (Semifinal 0.10%).",
        font_size=Pt(9)
    )
    append_bullet_point(
        tf_b, "Mekanisme Simulasi Turnamen Penuh",
        "10.000 iterasi stokastik menjalankan bagan resmi ASEAN Cup: Grup A (5 tim) & Grup B (5 tim) dengan perhitungan klasemen resmi (poin, selisih gol, head-to-head), Semifinal 2-leg agregat, hingga Grand Final dengan aturan adu penalti stokastik.",
        font_size=Pt(9)
    )
    append_bullet_point(
        tf_b, "Mengapa Menjual Probabilitas, Bukan Kepastian?",
        "Sepak bola modern tidak deterministik. Model yang mengklaim 100% kepastian adalah model yang cacat. Thailand 31.26% berarti dalam 10.000 dunia paralel turnamen, Thailand mengangkat piala 3.126 kali — menyisakan ruang nyata 68.74% bagi persaingan tim lain.",
        font_size=Pt(9)
    )


def build_slide_8(prs):
    """Slide 8: Interactive Streamlit Dashboard Walkthrough."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    create_slide_header(
        slide,
        badge_text="USER INTERFACE • STREAMLIT DASHBOARD • 5 MODULAR TABS",
        title_text="Demonstrasi Dashboard Interaktif: Visualisasi Prediksi & Simulasi Turnamen",
        subtitle_text="Arsitektur Modular `app/streamlit_app.py`: Antarmuka Web Responsif untuk Analis, Pelatih, dan Media",
        slide_num=8
    )

    # 3 Top Row Cards
    w3 = Inches(3.72)
    gap3 = Inches(0.28)
    top1 = Inches(1.85)
    h1 = Inches(2.35)

    # Tab 1: Match Predictor
    t1 = add_container_card(slide, Inches(0.8) + 0 * (w3 + gap3), top1, w3, h1, border_color=COLOR_SKY)
    tf1 = t1.text_frame
    p1 = tf1.paragraphs[0]
    p1.text = "TAB 1: MATCH PREDICTOR"
    p1.font.name = FONT_FAMILY
    p1.font.size = Pt(11)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_SKY

    append_bullet_point(tf1, "Pemilihan Negara Bebas", "Pilih 2 tim nasional mana saja di dunia secara instan dari database 337 tim.", font_size=Pt(8.5))
    append_bullet_point(tf1, "Probabilitas 3-Class", "Menampilkan estimasi persentase Home Win, Draw, dan Away Win secara visual.", font_size=Pt(8.5))
    append_bullet_point(tf1, "Visual Gauge & Bar", "Grafik probabilitas interaktif yang memperlihatkan perbandingan kekuatan tim.", font_size=Pt(8.5))
    append_bullet_point(tf1, "Sub-Detik Latensi", "Inference model berjalan di CPU lokal dalam waktu kurang dari 5 milidetik.", font_size=Pt(8.5))

    # Tab 2: ASEAN Cup Simulator
    t2 = add_container_card(slide, Inches(0.8) + 1 * (w3 + gap3), top1, w3, h1, border_color=COLOR_EMERALD)
    tf2 = t2.text_frame
    p2 = tf2.paragraphs[0]
    p2.text = "TAB 2: ASEAN CUP SIMULATOR"
    p2.font.name = FONT_FAMILY
    p2.font.size = Pt(11)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_EMERALD

    append_bullet_point(tf2, "Bagan Gugur Interaktif", "Visualisasi knockout bracket resmi ASEAN Cup dari fase grup hingga grand final.", font_size=Pt(8.5))
    append_bullet_point(tf2, "10.000 Putaran Instan", "Menjalankan 10.000 simulasi stokastik turnamen dalam waktu kurang dari 1.5 detik.", font_size=Pt(8.5))
    append_bullet_point(tf2, "Leaderboard Peluang", "Menampilkan probabilitas semifinalis, finalis, dan juara untuk seluruh 10 peserta.", font_size=Pt(8.5))
    append_bullet_point(tf2, "Confidence Interval 95%", "Menyajikan rentang keyakinan statistik yang dapat dipertanggungjawabkan.", font_size=Pt(8.5))

    # Tab 3: Interactive EDA
    t3 = add_container_card(slide, Inches(0.8) + 2 * (w3 + gap3), top1, w3, h1, border_color=COLOR_AMBER)
    tf3 = t3.text_frame
    p3 = tf3.paragraphs[0]
    p3.text = "TAB 3: INTERACTIVE EDA"
    p3.font.name = FONT_FAMILY
    p3.font.size = Pt(11)
    p3.font.bold = True
    p3.font.color.rgb = COLOR_AMBER

    append_bullet_point(tf3, "Pola Gol Masa Lalu", "Distribusi rata-rata gol era modern (2.93 gol/pertandingan) dan tren jangka panjang.", font_size=Pt(8.5))
    append_bullet_point(tf3, "Konteks Tempat Netral", "Visualisasi keruntuhan home advantage saat pertandingan digelar di venue netral.", font_size=Pt(8.5))
    append_bullet_point(tf3, "Target Distribution", "Grafik perbandingan kelas Home Win (47.9%), Away Win (28.4%), Draw (23.7%).", font_size=Pt(8.5))
    append_bullet_point(tf3, "Filter Era Dinamis", "Eksplorasi data historis berdasarkan rentang tahun dan jenis kompetisi.", font_size=Pt(8.5))

    # 2 Bottom Row Cards
    w2 = Inches(5.72)
    gap2 = Inches(0.28)
    top2 = Inches(4.35)
    h2 = Inches(2.45)

    # Tab 4: Model Diagnostics Lab
    t4 = add_container_card(slide, Inches(0.8) + 0 * (w2 + gap2), top2, w2, h2, border_color=COLOR_PURPLE)
    tf4 = t4.text_frame
    p4 = tf4.paragraphs[0]
    p4.text = "TAB 4: MODEL DIAGNOSTICS LAB (EXPLAINABLE AI)"
    p4.font.name = FONT_FAMILY
    p4.font.size = Pt(11)
    p4.font.bold = True
    p4.font.color.rgb = COLOR_PURPLE

    append_bullet_point(tf4, "Confusion Matrix Interaktif", "Membedah akurasi klasifikasi aktual vs prediksi pada 52 laga evaluasi ASEAN.", font_size=Pt(8.5))
    append_bullet_point(tf4, "Bobot Koefisien Fitur (Feature Importance)", "Menampilkan peringkat pengaruh variabel: Elo rating differential sebagai prediktor terkuat, diikuti momentum form dan H2H.", font_size=Pt(8.5))
    append_bullet_point(tf4, "Kurva Kalibrasi Probabilitas", "Membuktikan seberapa dekat estimasi probabilitas model dengan frekuensi kejadian riil.", font_size=Pt(8.5))
    append_bullet_point(tf4, "Transparansi Penuh", "Tidak ada 'black box'; semua koefisien matematis dapat diaudit secara ilmiah.", font_size=Pt(8.5))

    # Tab 5: Dynamic Adaptability & Ingestion Engine
    t5 = add_container_card(slide, Inches(0.8) + 1 * (w2 + gap2), top2, w2, h2, border_color=COLOR_EMERALD)
    tf5 = t5.text_frame
    p5 = tf5.paragraphs[0]
    p5.text = "TAB 5: DYNAMIC INGESTION & PARAMETER ENGINE"
    p5.font.name = FONT_FAMILY
    p5.font.size = Pt(11)
    p5.font.bold = True
    p5.font.color.rgb = COLOR_EMERALD

    append_bullet_point(tf5, "Live CSV Ingestion Engine", "Komponen st.file_uploader untuk mengunggah berkas pertandingan terbaru dari pengguna.", font_size=Pt(8.5))
    append_bullet_point(tf5, "Slider Kontrol Parameter", "Penyetelan live untuk bobot Home Advantage, jendela Form (3-10 laga), dan K-factor Elo.", font_size=Pt(8.5))
    append_bullet_point(tf5, "Perhitungan Ulang Reaktif", "Sistem langsung menghitung ulang Elo, form tim, dan probabilitas juara secara real-time.", font_size=Pt(8.5))
    append_bullet_point(tf5, "Stress-Tested Stability", "Eksekusi mulus tanpa memory leak, thread locking, atau crash pada browser pengguna.", font_size=Pt(8.5))


def build_slide_9(prs):
    """Slide 9: Dynamic Adaptability & Stress Testing."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    create_slide_header(
        slide,
        badge_text="REACTIVE ENGINE • LIVE CSV INGESTION • SUB-SECOND RECALCULATION",
        title_text="Adaptabilitas Dinamis: Pengunggahan Data Live & Penyetelan Parameter",
        subtitle_text="Sistem Reaktif Cerdas: Menghitung Ulang Elo, Form, dan Probabilitas Monte Carlo Tanpa Reload Server",
        slide_num=9
    )

    col_w = Inches(3.72)
    gap = Inches(0.28)
    top_pos = Inches(1.85)
    col_h = Inches(4.92)

    # Step 1: Live CSV Ingestion
    c1 = add_container_card(slide, Inches(0.8) + 0 * (col_w + gap), top_pos, col_w, col_h, border_color=COLOR_SKY)
    tf1 = c1.text_frame
    p1 = tf1.paragraphs[0]
    p1.text = "1. INGESTI CSV PERTANDINGAN"
    p1.font.name = FONT_FAMILY
    p1.font.size = Pt(11.5)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_SKY

    append_bullet_point(tf1, "Unggah Berkas Eksternal", "Pengguna dapat mengunggah CSV pertandingan baru melalui antarmuka st.file_uploader.", font_size=Pt(9))
    append_bullet_point(tf1, "Validasi Skema Otomatis", "Memeriksa ketersediaan kolom kunci: date, home_team, away_team, home_score, away_score, neutral.", font_size=Pt(9))
    append_bullet_point(tf1, "Pembaruan Ledger Elo Live", "Skor pertandingan baru langsung diproses oleh EloEngine untuk memperbarui rating kedua tim.", font_size=Pt(9))
    append_bullet_point(tf1, "Penanganan Tim Baru (Unseen)", "Jika tim baru belum memiliki riwayat, sistem menginisialisasi rating baseline 1500.0 secara aman tanpa KeyError.", font_size=Pt(9))
    append_bullet_point(tf1, "Integritas Kronologis", "Data baru diurutkan secara waktu untuk menjamin protokol anti-leakage tetap tegak.", font_size=Pt(9))

    # Step 2: Interactive Parameter Sliders
    c2 = add_container_card(slide, Inches(0.8) + 1 * (col_w + gap), top_pos, col_w, col_h, border_color=COLOR_EMERALD)
    tf2 = c2.text_frame
    p2 = tf2.paragraphs[0]
    p2.text = "2. PENYETELAN PARAMETER LIVE"
    p2.font.name = FONT_FAMILY
    p2.font.size = Pt(11.5)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_EMERALD

    append_bullet_point(tf2, "Slider Home Advantage (H)", "Rentang H in [0, 200] Elo points. Menguji skenario pertandingan tanpa penonton (H=0) vs stadion penuh (H=100-150).", font_size=Pt(9))
    append_bullet_point(tf2, "Slider Form Window (N Laga)", "Rentang N in [3, 10] laga. Menguji sensitivitas model terhadap tren jangka sangat pendek (3 laga) vs tren stabil (10 laga).", font_size=Pt(9))
    append_bullet_point(tf2, "Slider Elo K-Factor (Sensitivitas)", "Rentang K in [10, 60]. Mengatur seberapa agresif rating tim bergeser pasca setiap laga.", font_size=Pt(9))
    append_bullet_point(tf2, "Dropdown Status Venue", "Simulasi instan pertandingan kandang asli vs tempat netral untuk menguji degradasi keunggulan kandang.", font_size=Pt(9))
    append_bullet_point(tf2, "Eksperimen Interaktif Bebas", "Memberikan kebebasan bagi analis untuk menguji berbagai hipotesis taktis.", font_size=Pt(9))

    # Step 3: Instant Dynamic Recalculation
    c3 = add_container_card(slide, Inches(0.8) + 2 * (col_w + gap), top_pos, col_w, col_h, border_color=COLOR_AMBER)
    tf3 = c3.text_frame
    p3 = tf3.paragraphs[0]
    p3.text = "3. PENGHITUNGAN ULANG REAKTIF"
    p3.font.name = FONT_FAMILY
    p3.font.size = Pt(11.5)
    p3.font.bold = True
    p3.font.color.rgb = COLOR_AMBER

    append_bullet_point(tf3, "Respon Cepat (< 1.5 Detik)", "Begitu parameter digeser atau CSV diunggah, seluruh matriks fitur dan 10.000 simulasi langsung dihitung ulang seketika.", font_size=Pt(9))
    append_bullet_point(tf3, "Pembaruan Visual Otomatis", "Grafik probabilitas laga, klasemen grup, dan peluang juara turnamen ter-update otomatis tanpa me-refresh browser.", font_size=Pt(9))
    append_bullet_point(tf3, "Arsitektur Non-Blocking", "Komputasi dioptimalkan menggunakan vektorisasi NumPy dan struktur memoized dictionary.", font_size=Pt(9))
    append_bullet_point(tf3, "Stress Testing Teruji", "Telah diuji dengan puluhan perubahan parameter berturut-turut tanpa mengalami memory leak atau freeze.", font_size=Pt(9))
    append_bullet_point(tf3, "Kesiapan Produksi Penuh", "Dapat dijalankan secara mandiri pada laptop standar tanpa memerlukan server komputasi eksternal.", font_size=Pt(9))


def build_slide_10(prs):
    """Slide 10: Target Beneficiaries: Data-Driven Counter-Strategies for Underdog Teams."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    create_slide_header(
        slide,
        badge_text="TARGET BENEFICIARIES • WEEK 4 MENTOR MANDATE • STRATEGIC PLAYBOOKS",
        title_text="Penerima Manfaat Utama: Kontra-Strategi Berbasis Data untuk Tim Underdog",
        subtitle_text="Arahan Khusus Pak Aslan Alwi: Membantu Tim Kuda Hitam & Federasi Mengeksploitasi Celah Statistik Lawan",
        slide_num=10
    )

    col_w = Inches(3.72)
    gap = Inches(0.28)
    top_pos = Inches(1.85)
    col_h = Inches(4.92)

    # Beneficiary 1: Underdog National Teams
    b1 = add_container_card(slide, Inches(0.8) + 0 * (col_w + gap), top_pos, col_w, col_h, border_color=COLOR_EMERALD)
    tf1 = b1.text_frame
    p1 = tf1.paragraphs[0]
    p1.text = "1. TIM KUDA HITAM (UNDERDOGS)"
    p1.font.name = FONT_FAMILY
    p1.font.size = Pt(11.5)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_EMERALD

    append_bullet_point(tf1, "Target Spesifik", "Tim dengan probabilitas historis rendah: Kamboja, Laos, Myanmar, Timor-Leste, Filipina.", font_size=Pt(9))
    append_bullet_point(tf1, "Kontra-Taktik Realistis", "Menghindari taktik terbuka bunuh diri melawan raksasa regional (Thailand/Indonesia); menerapkan blok rendah (low-block) untuk memaksimalkan peluang Draw (25-30%) dan mencuri 1 poin krusial.", font_size=Pt(9))
    append_bullet_point(tf1, "Eksploitasi Laga Kandang", "Data membuktikan kandang mendongkrak peluang hingga 1.73x; fokus alokasi kebugaran pemain pilar pada laga home sebagai lumbung poin utama.", font_size=Pt(9))
    append_bullet_point(tf1, "Manajemen Rotasi Skuad", "Menjaga kebugaran skuad inti pada laga melawan rival selevel daripada memaksakan kelelahan di laga probabilitas sangat rendah (<5%).", font_size=Pt(9))
    append_bullet_point(tf1, "Target Kelolosan Terukur", "Menyusun skenario realistis 4-5 poin untuk lolos fase grup berdasarkan kalkulasi simulasi.", font_size=Pt(9))

    # Beneficiary 2: National Federations (PSSI & AFF)
    b2 = add_container_card(slide, Inches(0.8) + 1 * (col_w + gap), top_pos, col_w, col_h, border_color=COLOR_SKY)
    tf2 = b2.text_frame
    p2 = tf2.paragraphs[0]
    p2.text = "2. FEDERASI SEPAK BOLA NASIONAL"
    p2.font.name = FONT_FAMILY
    p2.font.size = Pt(11.5)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_SKY

    append_bullet_point(tf2, "Target Spesifik", "Komite teknik dan pengambil kebijakan federasi sepak bola (PSSI, AFF, federasi negara anggota).", font_size=Pt(9))
    append_bullet_point(tf2, "Target Turnamen Objektif", "Menetapkan target KPI manajer dan pelatih kepala berdasarkan probabilitas empiris, bukan ekspektasi buta publik atau desakan emosional fans.", font_size=Pt(9))
    append_bullet_point(tf2, "Optimasi Jadwal Uji Coba", "Mensimulasikan calon lawan uji coba internasional (FIFA Matchday) yang memaksimalkan penambahan poin rating Elo/FIFA dengan risiko kekalahan terukur.", font_size=Pt(9))
    append_bullet_point(tf2, "Alokasi Pemusatan Latihan", "Efisiensi penganggaran training camp dan rotasi pemain berdasarkan profil kelemahan taktis lawan di turnamen resmi.", font_size=Pt(9))
    append_bullet_point(tf2, "Evaluasi Jangka Panjang", "Melacak pertumbuhan latent power tim dari turnamen ke turnamen secara ilmiah.", font_size=Pt(9))

    # Beneficiary 3: Sports Media & Public Data Literacy
    b3 = add_container_card(slide, Inches(0.8) + 2 * (col_w + gap), top_pos, col_w, col_h, border_color=COLOR_AMBER)
    tf3 = b3.text_frame
    p3 = tf3.paragraphs[0]
    p3.text = "3. MEDIA & LITERASI PUBLIK"
    p3.font.name = FONT_FAMILY
    p3.font.size = Pt(11.5)
    p3.font.bold = True
    p3.font.color.rgb = COLOR_AMBER

    append_bullet_point(tf3, "Target Spesifik", "Jurnalis olahraga, analis taktik independen, kreator konten, dan komunitas penggemar sepak bola.", font_size=Pt(9))
    append_bullet_point(tf3, "Mengikis Jurnalisme Clickbait", "Menggantikan narasi sensasional berlebihan ('Pasti Membantai Lawan!') dengan laporan probabilistik objektif ('Model memberi peluang menang 48% dengan risiko seri 26%').", font_size=Pt(9))
    append_bullet_point(tf3, "Edukasi Literasi Statistik", "Membiasakan publik memahami bahwa olahraga modern penuh ketidakpastian dan bahwa probabilitas 30% tetap memiliki peluang nyata untuk terwujud.", font_size=Pt(9))
    append_bullet_point(tf3, "Pemberitaan Berbasis Bukti", "Menyediakan grafik interaktif dan bukti statistik siap pakai untuk memperkaya kualitas diskusi publik.", font_size=Pt(9))
    append_bullet_point(tf3, "Dampak Sosial Positif", "Mendukung iklim sportivitas yang lebih sehat dan dewasa di kalangan pendukung sepak bola nasional.", font_size=Pt(9))


def build_slide_11(prs):
    """Slide 11: Summary of Contributions, Production Impact, and Future Roadmap."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    create_slide_header(
        slide,
        badge_text="EXECUTIVE SUMMARY • PRODUCTION READINESS • DEFENSE TIMELINE 2-6 NOV 2026",
        title_text="Sintesis Kontribusi, Kesiapan Produksi, dan Rencana Pengembangan",
        subtitle_text="Memenuhi 100% Standar Akademik MSIB Batch 10 PT Vinix Seven Aurum & Kriteria Responsible AI",
        slide_num=11
    )

    col_w = Inches(5.72)
    top_pos = Inches(1.85)
    col_h = Inches(4.92)

    # Left Container: Summary of Deliverables & Rigor Checklist
    c_left = add_container_card(slide, Inches(0.8), top_pos, col_w, col_h, border_color=COLOR_EMERALD)
    tf_l = c_left.text_frame
    p_lh = tf_l.paragraphs[0]
    p_lh.text = "SINTESIS KONTRIBUSI & CHECKLIST KEPATUHAN AKADEMIK"
    p_lh.font.name = FONT_FAMILY
    p_lh.font.size = Pt(12)
    p_lh.font.bold = True
    p_lh.font.color.rgb = COLOR_EMERALD

    append_bullet_point(
        tf_l, "[x] Pipeline Data Zero-Leakage 49.000+ Laga",
        "Disiplin batas waktu ketat: 38.288 laga latih (1960-2020), 6.162 laga uji out-of-time (2021-2026), 0 missing values, standarisasi tanpa data future leakage.",
        font_size=Pt(9)
    )
    append_bullet_point(
        tf_l, "[x] Dynamic Elo Engine & 24 Fitur Pra-Laga",
        "Pembaruan rating dinamis K=32.0, R0=1500.0, Home Advantage offset H=100.0, rolling form 5 laga, dan rekor H2H sebelum kick-off.",
        font_size=Pt(9)
    )
    append_bullet_point(
        tf_l, "[x] Log Loss Terbaik 0.5966 pada 52 Laga AFF",
        "Melampaui target wajib (<= 0.8198) dan baseline naif (1.0686), akurasi 75.00%, Brier score 0.3331, membuktikan keunggulan informasi model.",
        font_size=Pt(9)
    )
    append_bullet_point(
        tf_l, "[x] 10.000 Putaran Simulasi Turnamen Monte Carlo",
        "Peta probabilitas juara ASEAN Cup terkalibrasi: Thailand 31.26%, Indonesia 27.99%, Vietnam 22.79%, Malaysia 15.08%, Underdogs 2.88%.",
        font_size=Pt(9)
    )
    append_bullet_point(
        tf_l, "[x] Dashboard Streamlit Dinamis & Responsif",
        "5 tab antarmuka interaktif dilengkapi fitur unggah CSV live, slider parameter dinamis, dan kalkulasi ulang sub-detik tanpa crash.",
        font_size=Pt(9)
    )
    append_bullet_point(
        tf_l, "[x] Kepatuhan Invarian Akademik Mutlak",
        "Nama Kenny Helim (BINUS), Kelompok 1 AI, PT Vinix Seven Aurum, Periode Magang 4 Bulan MUTLAK, Keselarasan UN SDG 9.",
        font_size=Pt(9)
    )

    # Right Container: Open Scientific Boundaries, Future Roadmap & Defense Readiness
    c_right = add_container_card(slide, Inches(6.81), top_pos, col_w, col_h, border_color=COLOR_SKY)
    tf_r = c_right.text_frame
    p_rh = tf_r.paragraphs[0]
    p_rh.text = "BATASAN ILMIAH, ROADMAP RISET & KESIAPAN SIDANG"
    p_rh.font.name = FONT_FAMILY
    p_rh.font.size = Pt(12)
    p_rh.font.bold = True
    p_rh.font.color.rgb = COLOR_SKY

    append_bullet_point(
        tf_r, "Batasan Ilmiah Terbuka (Honest Limitations)",
        "Model belum mencakup data spatio-temporal frekuensi tinggi (Expected Goals / xG koordinat tembakan), cedera pemain menit akhir, serta dinamika cuaca ekstrem saat pertandingan.",
        font_size=Pt(9)
    )
    append_bullet_point(
        tf_r, "Roadmap Pengembangan Riset Lanjutan",
        "1. Integrasi data pelacakan pemain terbuka (open tracking data seperti StatsBomb open data).\n2. Pembaruan peluang in-game Bayesian real-time seiring menit pertandingan berjalan.\n3. Integrasi kedalaman bangku cadangan dan riwayat kartu kuning/merah pemain.",
        font_size=Pt(9)
    )
    append_bullet_point(
        tf_r, "Kesiapan Sidang Evaluasi Akhir (2 - 6 November 2026)",
        "Seluruh artefak kode, dataset, model serial (.pkl), laporan teknis monograf, naskah presentasi pembicara, dan slide deck telah teruji 100% siap dipertanggungjawabkan di hadapan dosen penguji.",
        font_size=Pt(9)
    )
    append_bullet_point(
        tf_r, "Ucapan Terima Kasih & Penghormatan",
        "Terima kasih sebesar-besarnya kepada Dosen Mentor Pak Aslan Alwi & Bimo Rizki Abdusshamad atas bimbingan metodologi, sport science, dan etika AI yang sangat berharga selama program magang MSIB Fast Track Batch 10.",
        font_size=Pt(9)
    )


# ==============================================================================
# MAIN EXECUTION ROUTINE
# ==============================================================================

def main():
    print("=" * 80)
    print("STARTING REVISED PARADIGM 11-SLIDE PRESENTATION GENERATION")
    print("Author: Kenny Helim (BINUS University) | Kelompok 1 AI | PT Vinix Seven Aurum")
    print("=" * 80)

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    print("[1/11] Building Slide 1: Executive Title & Academic Governance...")
    build_slide_1(prs)

    print("[2/11] Building Slide 2: Core Problem Statement & The Imperative for Objectivity...")
    build_slide_2(prs)

    print("[3/11] Building Slide 3: Scope, Data Foundation & Temporal Barrier...")
    build_slide_3(prs)

    print("[4/11] Building Slide 4: AI Methodology Architecture & Feature Engineering...")
    build_slide_4(prs)

    print("[5/11] Building Slide 5: Deep Technical Divergence (Football vs YOLO11 Road Damage)...")
    build_slide_5(prs)

    print("[6/11] Building Slide 6: Rigorous Model Evaluation on 52 ASEAN Matches...")
    build_slide_6(prs)

    print("[7/11] Building Slide 7: 10,000-Run Monte Carlo Stochastic Tournament Simulation...")
    build_slide_7(prs)

    print("[8/11] Building Slide 8: Interactive Streamlit Dashboard Walkthrough...")
    build_slide_8(prs)

    print("[9/11] Building Slide 9: Dynamic Adaptability & Stress Testing...")
    build_slide_9(prs)

    print("[10/11] Building Slide 10: Target Beneficiaries & Counter-Strategies for Underdogs...")
    build_slide_10(prs)

    print("[11/11] Building Slide 11: Summary of Contributions, Production Impact, and Future Roadmap...")
    build_slide_11(prs)

    output_root = "FINAL_PROJECT_PRESENTATION_REVISED_PARADIGM.pptx"
    output_docs = os.path.join("docs", "FINAL_PROJECT_PRESENTATION_REVISED_PARADIGM.pptx")

    os.makedirs("docs", exist_ok=True)
    prs.save(output_root)
    print(f"[SUCCESS] Saved presentation at project root: {output_root}")

    shutil.copy2(output_root, output_docs)
    print(f"[SUCCESS] Mirrored presentation to docs folder: {output_docs}")

    # Integrity verification
    prs_check = Presentation(output_root)
    assert len(prs_check.slides) == 11, f"Expected 11 slides, found {len(prs_check.slides)}"
    print(f"[VERIFIED] Presentation contains exactly {len(prs_check.slides)} slides.")
    print("=" * 80)


if __name__ == "__main__":
    main()
