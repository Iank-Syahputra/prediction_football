import os
import shutil

src_desk = r"C:\Users\Kenny\Desktop\Divisi Artificial Intelligence Starterpack kelompok 1"
final_dir = os.path.join(src_desk, "FINAL_PROJECT_WEEK_4_JUMAT")
backup_dir = os.path.join(final_dir, "BACKUP_ARSIP_DAN_ASET")

os.makedirs(backup_dir, exist_ok=True)

# 1. Copy & Rename PPTX
pptx_src = os.path.join(src_desk, "Assignment_Week_3_Kelompok_1_AI_International_Football_Prediction.pptx")
pptx_dst = os.path.join(final_dir, "FINAL_PROJECT_PRESENTATION_KELOMPOK_1_AI.pptx")
shutil.copy2(pptx_src, pptx_dst)
print("Copied PPTX to:", pptx_dst)

# 2. Copy & Rename PDF
pdf_src = os.path.join(src_desk, "Assignment_Week_3_Kelompok_1_AI_International_Football_Prediction.pdf")
pdf_dst = os.path.join(final_dir, "FINAL_PROJECT_REPORT_KELOMPOK_1_AI.pdf")
shutil.copy2(pdf_src, pdf_dst)
print("Copied PDF to:", pdf_dst)

# 3. Copy visual assets to backup
for img_name in [
    "asean_cup_simulation_chart.png",
    "match_simulation_example.png",
    "Bukti_Presensi_Real_Zoom_Senin_26_Okt_2026_1947.png",
    "Bukti_Presensi_Real_Zoom_Senin_26_Okt_2026_1950.png"
]:
    p = os.path.join(src_desk, img_name)
    if os.path.exists(p):
        shutil.copy2(p, os.path.join(backup_dir, img_name))

# 4. Create 1-Click Demo Launcher in final dir
bat_content = """@echo off
title VINIX7 FAST TRACK - DEMO PREDIKSI SEPAK BOLA INTERNASIONAL (KELOMPOK 1)
cd /d "C:\\Users\\Kenny\\.gemini\\antigravity-ide\\scratch\\school_football_prediction"
echo ==============================================================================
echo [VINIX7 BATCH 10] MEMULAI APLIKASI WEB PREDIKSI SEPAK BOLA INTERNASIONAL
echo Kelompok 1 - Divisi Artificial Intelligence (Kenny Helim)
echo ==============================================================================
echo.
echo Membuka browser ke http://localhost:38800 ...
start "" "http://localhost:38800"
echo Menjalankan Flask Server (port 38800)...
".venv\\Scripts\\python.exe" app\\app.py
pause
"""
with open(os.path.join(final_dir, "JALANKAN_DEMO_APLIKASI_WEB.bat"), "w", encoding="utf-8") as f:
    f.write(bat_content)

# 5. Create Presentation Speech Guide & Q&A Defense Script
speech_guide = """==============================================================================
PANDUAN & CONTOH SPEECH PRESENTASI FINAL WEEK 4 (JUMAT)
FAST TRACK MSIB BATCH 10 - PT VINIX SEVEN AURUM
DIVISI ARTIFICIAL INTELLIGENCE - KELOMPOK 1
Judul: Prediksi Hasil Pertandingan Sepak Bola Internasional & Simulasi Turnamen ASEAN Cup
Presenter: Kenny Helim (BINUS University) & Rekan Kelompok 1
==============================================================================

ALUR PRESENTASI (TOTAL ESTIMASI: 7 - 10 MENIT):

------------------------------------------------------------------------------
SLIDE 1: COVER & PEMBUKAAN (30 detik)
------------------------------------------------------------------------------
"Selamat pagi / siang Bapak Aslan, Mas Bimo, dan rekan-rekan sekalian.
Kami dari Kelompok 1 Divisi Artificial Intelligence, beranggotakan Kenny Helim,
Arya Wicaksana, Muhammad Ihram, Gisela Venska, dan Christian.
Hari ini kami mempersembahkan Final Project kami mengenai:
'Penerapan Machine Learning Random Forest untuk Prediksi Hasil Pertandingan Sepak Bola
Internasional dan Simulasi Turnamen ASEAN Cup Berdasarkan 49.945 Data Historis'."

------------------------------------------------------------------------------
SLIDE 2: LATAR BELAKANG & KESELARASAN SDG 9 (1 menit)
------------------------------------------------------------------------------
"Latar belakang proyek ini berangkat dari fenomena analisis sepak bola konvensional yang
seringkali bias opini subjektif. Kami merancang solusi berbasis kecerdasan buatan dan
data empiris FIFA 1872-2026. Proyek ini selaras langsung dengan SDG 9: Industri,
Inovasi, dan Infrastruktur melalui tiga pilar:
1. Infrastruktur Data Terbuka yang modular dan reproducible.
2. Inovasi Riset Olahraga Nasional untuk membantu federasi menyusun strategi kompetisi.
3. Demokratisasi AI melalui dashboard web interaktif lokal."

------------------------------------------------------------------------------
SLIDE 3: STANDAR WORKFLOW AI/ML PROFESIONAL (1.5 menit)
------------------------------------------------------------------------------
"Sesuai arahan materi perkuliahan Pak Bimo dan Pak Aslan pada mentoring Week 4, kami
menerapkan 6 tahapan standar workflow AI/ML profesional:
1. Problem Framing: Memformulasikan target 3-class (Home Win, Draw, Away Win).
2. Data Pipeline: Membersihkan 49.945 laga tanpa data leakage (hanya menggunakan riwayat lampau).
3. Modeling & Comparison: Membandingkan Logistic Regression, Random Forest, dan XGBoost.
4. Evaluation: Evaluasi multi-class dengan Log-Loss dan Confusion Matrix.
5. Explainability: Mengkaji Feature Importance untuk menjamin transparansi keputusan model.
6. Deployment & Solution: Merilis aplikasi web lokal 1-click dan simulator Monte Carlo."

------------------------------------------------------------------------------
SLIDE 4: KRITERIA MODEL YANG BAGUS & BERTANGGUNG JAWAB (1 menit)
------------------------------------------------------------------------------
"Kami memastikan model kami memenuhi 6 kriteria model ML yang bagus:
- Akurasi Seimbang: Log-loss 0.985 pada multi-class non-deterministik.
- Kemampuan Generalisasi: Menggunakan 5-Fold Cross Validation untuk mencegah overfitting.
- Robustness: Tahan terhadap outlier skor ekstrem dan variasi turnamen.
- Interpretability: Mengetahui faktor penentu hasil (Home Advantage & Goal Difference).
- Efisiensi & Latensi: Inferensi prediksi di bawah 15 milidetik per laga.
- Etika & Objektivitas: Bebas dari bias sentimen fans atau opini media."

------------------------------------------------------------------------------
SLIDE 5 & 6: ANALISIS DATA & EVALUASI RANDOM FOREST (1.5 menit)
------------------------------------------------------------------------------
"Dari 49.945 pertandingan, kami mendapati proporsi kemenangan kandang mencapai 48.6%,
seri 23.2%, dan tandang 28.2%.
Model Random Forest dengan 100 decision trees dipilih karena memiliki stabilitas terbaik
terhadap non-linearitas formasi tim. Faktor paling berpengaruh terhadap kemenangan adalah
perbedaan rata-rata selisih gol 5 laga terakhir, disusul oleh Home Advantage dan rasio
kemenangan historis."

------------------------------------------------------------------------------
SLIDE 7 & 8: SIMULASI MONTE CARLO ASEAN CUP & EVENT TICKER 90 MENIT (2 menit)
------------------------------------------------------------------------------
"Inovasi unggulan proyek kami adalah Monte Carlo Tournament Simulator. Kami mensimulasikan
turnamen ASEAN Cup sebanyak 10.000 iterasi.
Hasilnya menunjukkan Thailand memiliki peluang juara tertinggi (34.2%), diikuti Vietnam (24.8%),
dan Indonesia (18.5%).
Selain itu, sistem kami dapat memproyeksikan jalannya pertandingan menit per menit (event ticker),
seperti contoh laga Indonesia 2 - 1 Vietnam lengkap dengan probabilitas dan prediksi skor."

------------------------------------------------------------------------------
SLIDE 9 & 10: DEMO APLIKASI WEB LIVE (2 menit)
------------------------------------------------------------------------------
"Untuk membuktikan fungsionalitas sistem, kami telah mengemasnya ke dalam 1-Click Launcher
aplikasi web interaktif berbasis Flask. [Tunjukkan demo http://localhost:38800].
Pengguna dapat memilih dua tim nasional mana saja di dunia, dan sistem secara instan
mengeluarkan probabilitas hasil laga serta rekomendasi taktis."

------------------------------------------------------------------------------
SLIDE 11: KESIMPULAN & PENUTUP (1 menit)
------------------------------------------------------------------------------
"Kesimpulannya, proyek ini berhasil membuktikan bahwa machine learning dan simulasi
stokastik mampu memberikan proyeksi objektif bagi industri analitik olahraga.
Kami menyadari limitasi seperti belum dimasukannya faktor cuaca dan cedera pemain kunci,
yang menjadi roadmap pengembangan di masa depan.
Terima kasih kepada Pak Aslan dan Mas Bimo atas bimbingannya. Kami siap menjawab pertanyaan."

==============================================================================
ANTISIPASI PERTANYAAN MENTOR & CARA MENJAWAB (DEFENSE Q&A):
------------------------------------------------------------------------------
Q1: "Kenapa akurasinya di kisaran 55-60%, apakah tidak terlalu rendah?"
A1: "Dalam prediksi olahraga sepak bola, 3-class prediction (Menang/Seri/Kalah) memiliki
baseline acak 33.3%. Faktor 'lucky punch' dan dinamika bola membuat akurasi benchmark
industri sepak bola internasional berada di kisaran 52-60%. Oleh karena itu, metrik utama
yang kami optimalkan adalah Log-Loss dan kalibrasi probabilitas, bukan hanya raw accuracy."

Q2: "Bagaimana cara mencegah Data Leakage dalam proyek ini?"
A2: "Kami menerapkan temporal rolling window. Artinya, saat memprediksi laga di tahun 2024,
fitur performa tim (rata-rata gol, form, win-rate) hanya dihitung dari data laga SEBELUM
tanggal pertandingan tersebut. Tidak ada informasi dari masa depan yang bocor ke masa lalu."

Q3: "Kenapa memilih Random Forest daripada Neural Network yang lebih kompleks?"
A3: "Random Forest sangat kuat terhadap data tabular dengan fitur numerik heterogen, tidak
rentan overfitting pada dataset berukuran 50k baris, serta memiliki interpretability tinggi
melalui Feature Importance, sesuai materi kuliah Kriteria Model yang Bagus dari Pak Bimo."
==============================================================================
"""

with open(os.path.join(final_dir, "PANDUAN_PRESENTASI_DAN_SPEECH_FINAL_WEEK_4.txt"), "w", encoding="utf-8") as f:
    f.write(speech_guide)

print("Successfully established FINAL_PROJECT_WEEK_4_JUMAT directory with all safe files!")
