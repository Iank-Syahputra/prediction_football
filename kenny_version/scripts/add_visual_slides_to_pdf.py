import os

with open(r'C:\Users\Kenny\.gemini\antigravity-ide\scratch\school_football_prediction\scripts\generate_assignment_pdf.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace any existing total slide references to / 15
text = text.replace('/ 14', '/ 15').replace('/ 12', '/ 15')

# Find slide 11 (ASEAN Cup simulation table) and add the visual chart slide right after it
target_marker = 'story.append(Paragraph("SLIDE 11 / 15'
pos = text.find(target_marker)

visual_slides = '''
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
    zoom_img_path = r"C:\\Users\\Kenny\\Desktop\\Divisi Artificial Intelligence Starterpack kelompok 1\\Bukti_Presensi_Real_Zoom_Senin_26_Okt_2026_1947.png"
    if os.path.exists(zoom_img_path):
        story.append(Paragraph("SLIDE 14 / 15 - DOKUMENTASI MENTORING LIVE", header_badge))
        story.append(Paragraph("Dokumentasi Perkuliahan Live & Penyelarasan Materi (26 Okt 2026)", slide_title))
        story.append(Paragraph("Sesi Kuliah Bersama Mentor Bimo Rizki Abdusshamad & Pak Aslan (Kehadiran Kenny Helim & Tim Kelompok 1)", slide_subtitle))
        story.append(Image(zoom_img_path, width=680, height=350))
        story.append(PageBreak())
'''

# Find the conclusion slide and update its header to SLIDE 15 / 15
text = text.replace('SLIDE 12 / 15 - KESIMPULAN & SDG 9', 'SLIDE 15 / 15 - KESIMPULAN & SDG 9')
text = text.replace('SLIDE 12 / 15', 'SLIDE 15 / 15')

# Insert the visual slides right before the conclusion slide
concl_marker = '# SLIDE 12: Kesimpulan & Relevansi SDG 9'
if concl_marker in text:
    idx_c = text.find(concl_marker)
    new_text = text[:idx_c] + visual_slides + "\n    " + text[idx_c:]
    with open(r'C:\Users\Kenny\.gemini\antigravity-ide\scratch\school_football_prediction\scripts\generate_assignment_pdf.py', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("Successfully added 3 visual slides into generate_assignment_pdf.py!")
else:
    print("Could not find conclusion marker!")
