import re

with open(r'C:\Users\Kenny\.gemini\antigravity-ide\scratch\school_football_prediction\scripts\generate_assignment_pdf.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace all '/ 12' with '/ 14'
text = text.replace('/ 12', '/ 14')

new_slides = '''
    # SLIDE 04: Workflow AI/ML yang Profesional (VINIX7 Standard)
    story.append(Paragraph("SLIDE 04 / 14 - STANDAR WORKFLOW VINIX7", header_badge))
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
    story.append(Paragraph("SLIDE 05 / 14 - KRITERIA KUALITAS MODEL", header_badge))
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
'''

marker = '# SLIDE 4: Anatomi Dataset Historis'
pos = text.find(marker)
if pos != -1:
    new_text = text[:pos] + new_slides + text[pos:]
    replacements = [
        ('SLIDE 04 / 14', 'SLIDE 06 / 14'),
        ('SLIDE 05 / 14', 'SLIDE 07 / 14'),
        ('SLIDE 06 / 14', 'SLIDE 08 / 14'),
        ('SLIDE 07 / 14', 'SLIDE 09 / 14'),
        ('SLIDE 08 / 14', 'SLIDE 10 / 14'),
        ('SLIDE 09 / 14', 'SLIDE 11 / 14'),
        ('SLIDE 10 / 14', 'SLIDE 12 / 14'),
        ('SLIDE 11 / 14', 'SLIDE 13 / 14'),
        ('SLIDE 12 / 14', 'SLIDE 14 / 14'),
    ]
    # Apply replacements carefully on the later section
    marker2 = '# SLIDE 04: Workflow AI/ML'
    p_lead = new_text.find(marker2)
    p_body = new_text.find(marker, p_lead)
    part_head = new_text[:p_body]
    part_tail = new_text[p_body:]
    for old_s, new_s in replacements:
        part_tail = part_tail.replace(old_s, new_s, 1)
    final_text = part_head + part_tail
    with open(r'C:\Users\Kenny\.gemini\antigravity-ide\scratch\school_football_prediction\scripts\generate_assignment_pdf.py', 'w', encoding='utf-8') as f:
        f.write(final_text)
    print('Updated generate_assignment_pdf.py successfully!')
else:
    print('Marker not found!')
