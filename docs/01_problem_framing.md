# 01 — Problem Framing: Prediksi Hasil Pertandingan & Probabilitas Juara ASEAN Cup

Dokumen ini adalah bagian 1 dari seri dokumentasi project portofolio AI Engineer. Isinya hanya perumusan masalah: definisi komponen, aturan target dan anti-leakage, metrik, baseline, serta rencana evaluasi. Belum ada hasil eksperimen di sini. Semua angka berasal dari inspeksi langsung terhadap file dataset di `data/`; hal yang belum diperiksa ditandai `[perlu diverifikasi]`. Rekap angka EDA deskriptif (subbagian 4.1 notebook) dikumpulkan sebagai lampiran di bagian 9 — itu rangkuman data, bukan hasil model.

## 1. Latar belakang dan tujuan

Project ini memakai dataset *International Football Results* (martj42) yang tersedia lokal di folder `data/`:

| File | Kolom |
|---|---|
| `data/results.csv` | `date, home_team, away_team, home_score, away_score, tournament, city, country, neutral` |
| `data/shootouts.csv` | `date, home_team, away_team, winner, first_shooter` |
| `data/former_names.csv` | `current, former, start_date, end_date` |

Hasil inspeksi `results.csv`:

- Jumlah baris data (tanpa header): **49.945**
- Rentang tanggal: **1872-11-30 – 2026-10-06**

Tujuan project (dua deliverable):

1. **Model klasifikasi hasil pertandingan** yang mengeluarkan probabilitas untuk tiga hasil — menang tuan rumah (H), seri (D), menang tamu (A) — untuk laga di konteks turnamen ASEAN.
2. **Simulasi Monte Carlo** yang memakai probabilitas tiap laga untuk memperkirakan **probabilitas juara** tiap tim pada suatu edisi turnamen ASEAN.

## 2. Definisi dua komponen

### (a) Model klasifikasi H/D/A dengan output probabilitas

- Tugas: klasifikasi tiga kelas untuk satu laga: `H` (home win), `D` (draw), `A` (away win).
- Output model: vektor probabilitas `(p_H, p_D, p_A)` dengan `p_H + p_D + p_A = 1` (softmax), bukan sekadar label hard.
- Input: fitur yang seluruhnya diketahui sebelum tanggal laga (bagian 3).
- Output probabilitas inilah yang menjadi masukan simulasi Monte Carlo.

### (b) Simulasi Monte Carlo untuk probabilitas juara

Konsep: satu edisi turnamen disimulasikan berulang kali sebanyak **10.000 simulasi per edisi** (keputusan desain; jumlah dapat ditinjau ulang bila perlu), dan **galat Monte Carlo** (misalnya standard error dari proporsi juara) dilaporkan bersama setiap probabilitas juara. Pada tiap simulasi:

1. Setiap laga diundi sesuai probabilitas H/D/A dari model, dengan struktur sesuai aturan turnamen edisi terkait: pertandingan round-robin di fase grup, lalu knockout di fase gugur (format umum grup+knockout; format edisi spesifik `[perlu diverifikasi]`).
2. Klasemen grup dan jalur knockout ditentukan dari hasil undian tersebut. Laga knockout yang berakhir seri setelah waktu tambahan ditentukan pemenangnya lewat model adu penalti sederhana (lihat bagian 3).
3. Juara pada simulasi tersebut dicatat.

**Keputusan terbuka — tiebreaker klasemen grup:** model H/D/A tidak menghasilkan skor, sehingga tiebreaker klasemen grup (misalnya selisih gol) tidak dapat dihitung dari hasil undian laga. Opsi yang tersedia: (a) tiebreaker **diundi acak**, atau (b) **menambah model skor** tersendiri. **Keputusan ini belum diputuskan** (tercatat di bagian 7).

Probabilitas juara sebuah tim = jumlah simulasi tempat tim tersebut menang dibagi total jumlah simulasi. Simulasi hanya bermakna bila format turnamen edisi terkait diketahui (pertanyaan terbuka, bagian 7).

## 3. Definisi target dan aturan anti-leakage

### Target

- Label per laga: **hasil akhir setelah waktu tambahan, tanpa adu penalti**, yaitu nilai `home_score`/`away_score` di `results.csv`, dikategorikan menjadi H / D / A.
- **Keterbatasan pasti:** skor di `results.csv` sudah mencakup perpanjangan waktu, sehingga **hasil pada 90 menit regulasi tidak tersedia** di dataset. Konsekuensinya tidak dapat dihindari dan wajib dilaporkan: target tidak membedakan hasil 90 menit vs hasil setelah perpanjangan waktu, dan definisi alternatif berbasis 90 menit tidak dapat dibangun dari kolom yang ada tanpa sumber data tambahan.
- Untuk laga knockout yang masih seri setelah waktu tambahan, pemenangnya hanya tercatat di `shootouts.csv` (kolom `winner`). Dalam simulasi, laga knockout yang seri ditentukan pemenangnya lewat **model adu penalti sederhana** berbasis riwayat `shootouts.csv` (misalnya frekuensi menang adu penalti) `[perlu diverifikasi]` — detail model, kecukupan data, dan cara validasinya belum diperiksa.

### Aturan anti-leakage

Semua fitur untuk memprediksi laga pada tanggal `t` **hanya boleh memakai informasi yang tersedia sebelum tanggal `t`**:

- **Dilarang:** skor/hasil laga pada tanggal `t` atau sesudahnya; agregat statistik yang mengikutkan laga setelah `t`; informasi yang baru diketahui setelah kickoff (hasil undian, klasemen akhir, dll.).
- **Boleh:** rekor, rating (misalnya Elo), dan riwayat head-to-head yang dihitung dari laga ber-tanggal `< t`; informasi yang sudah ditetapkan sebelum laga (status kandang/tuan rumah, nilai `neutral`, edisi dan tahap turnamen bila sudah diumumkan sebelum kickoff).
- Pemisahan train/test bersifat **temporal** (data train selalu lebih dahulu dari data uji), bukan acak (bagian 6).
- Nama tim dapat berubah antar era. Harmonisasi memakai `data/former_names.csv` (`current`, `former`, `start_date`, `end_date`) agar agregasi lintas tahun tidak memecah satu tim menjadi dua entitas.

## 4. Metrik evaluasi

| Metrik | Peran | Alasan pilihan |
|---|---|---|
| **Log loss** | **Utama** | Menilai kualitas probabilitas secara langsung; hukuman logaritmik tegas untuk keyakinan yang keliru, sejalan dengan tujuan project (probabilitas, bukan sekadar tebakan) dan sensitif terhadap kalibrasi. |
| Brier score | Sekunder (probabilistik) | Error probabilitas berskala terbatas dan mudah diinterpretasikan (rata-rata kuadrat selisih probabilitas); pelengkap log loss yang tidak terlalu didominasi prediksi dengan keyakinan ekstrem. |
| RPS (Ranked Probability Score) | Sekunder (probabilistik) | Tepat untuk outcome berurutan H < D < A: kesalahan prediksi ke kategori yang lebih dekat dalam urutan dihukum lebih ringan daripada kesalahan yang melompati kategori, sesuai sifat hasil sepak bola. |
| Kalibrasi (reliability diagram per bin) | Wajib diperiksa | Memastikan "probabilitas 70%" benar-benar terjadi sekitar 70% dari waktu. Kalibrasi buruk membuat probabilitas juara hasil Monte Carlo tidak dapat dipercaya meski log loss terlihat baik. |
| Accuracy & macro-F1 | Sekunder (hard label) | Ringkasan performa pada label hard (argmax); macro-F1 menjaga kinerja kelas minoritas (misalnya seri/away) tetap terlihat. Tidak diutamakan karena membuang informasi probabilitas yang jadi fokus project. |

Catatan pelaporan metrik:

- **Interval kepercayaan bootstrap:** semua metrik pada laga ASEAN dilaporkan beserta **interval kepercayaan bootstrap** (resampling per laga atau per edisi), karena jumlah laga ASEAN terbatas.
- **Kalibrasi lintas cakupan:** kalibrasi diperiksa tidak hanya pada laga ASEAN, tetapi juga pada **laga internasional lain di periode uji yang sama**, untuk memastikan probabilitas model konsisten di dalam dan di luar ASEAN.

## 5. Baseline

1. **Prior kelas** — probabilitas prediksi tetap = frekuensi historis kelas H/D/A yang dihitung **hanya dari data train**. Menjadi ambang bawah: model apa pun harus mengalahkannya, sekaligus menunjukkan seberapa sulit tugas di data tersebut.
2. **Elo murni** — rating Elo kumulatif dari hasil laga, dikonversi ke probabilitas H/D/A. **Probabilitas seri harus dimodelkan secara eksplisit** (misalnya fungsi probabilitas seri sebagai fungsi selisih Elo), karena Elo dasar tidak menghasilkan probabilitas seri dengan sendirinya. **Seluruh parameter — konversi rating→probabilitas dan parameter fungsi seri — hanya boleh dicocokkan pada data train**, tidak pernah pada data uji, agar baseline ini bebas leakage.
3. **Logistic Regression** — model linear pada fitur sederhana (misalnya selisih Elo, indikator kandang/netral, rekor terakhir tim) sebagai baseline terlatih yang murah, stabil, dan mudah diinterpretasikan.

## 6. Rencana evaluasi backtest per edisi

- **Cakupan data latih — Pilihan A:** model dilatih pada **seluruh laga internasional** di `results.csv` (1872–2026), bukan hanya laga ASEAN. Alasannya: jumlah laga ASEAN relatif kecil (angka per turnamen di bagian 7) sehingga melatih hanya pada laga ASEAN membuat model kekurangan data, padahal sinyal kekuatan tim global (rating Elo, rekor) tetap relevan untuk memprediksi laga di level ASEAN. Seluruh data latih tetap tunduk pada aturan anti-leakage tanggal (bagian 3).
- **Fokus evaluasi:** seluruh metrik (bagian 4) dan seluruh backtest **difokuskan pada laga ASEAN** — konteks aplikasi project ini adalah prediksi dan probabilitas juara ASEAN Cup. Laga non-ASEAN berperan sebagai data latih/pembentuk fitur, bukan sebagai target akhir evaluasi.
- **Skema backtest:** walk-forward per edisi — untuk tiap edisi turnamen ASEAN secara kronologis, model dilatih hanya pada laga ber-tanggal sebelum edisi tersebut, lalu dievaluasi pada seluruh laga edisi itu. Data edisi berikutnya tidak boleh dipakai untuk edisi yang sedang diuji.
- **Pemisahan peran edisi:** edisi-edisi lama dipakai untuk **validasi dan pemilihan model/hyperparameter**; satu atau dua edisi terbaru **dikunci sebagai test akhir** dan hanya dibuka **satu kali** untuk evaluasi akhir. Pemilihan model, hyperparameter, dan keputusan desain **tidak boleh memakai edisi test akhir**.
- **Pelaporan metrik:** metrik pada laga ASEAN dilaporkan dengan **interval kepercayaan bootstrap** (bagian 4); **kalibrasi juga diperiksa pada laga internasional lain di periode uji yang sama** sebagai pembanding.
- **Elo vs sampel latih:** rating **Elo dihitung dari seluruh sejarah** (1872–sekarang) karena sifatnya kumulatif, sehingga tidak terikat pada pemilihan sampel latih; **sampel latih model** boleh dibatasi ke era modern sebagai **eksperimen ablasi** di kemudian hari, bukan bagian dari setup utama.
- **Keterbatasan yang wajib dilaporkan bersama hasil:**
  - Jumlah edisi turnamen ASEAN terbatas → variance hasil backtest tinggi dan perbandingan antar-model sulit dibuktikan signifikan secara statistik.
  - Format dan jumlah peserta tidak seragam antar edisi (`[perlu diverifikasi]`, bagian 7) → metrik antar-edisi tidak sepenuhnya sebanding.
  - Non-stasioneritas: kekuatan tim, pemain, dan aturan berubah antar era; rating yang dihitung sejak 1872 tidak otomatis mewakili kondisi terkini.
  - Target tanpa hasil 90 menit (bagian 3) mengubah makna "seri" pada laga knockout.
  - Hasil agregat per edisi tidak menjamin keandalan prediksi pada satu laga tertentu.

## 7. Asumsi, batasan, dan pertanyaan terbuka

### Asumsi (keputusan yang sudah diambil)

- **Cakupan data latih = Pilihan A:** seluruh laga internasional untuk training; evaluasi dan backtest difokuskan pada laga ASEAN (alasan di bagian 6).
- **Label = hasil akhir setelah waktu tambahan tanpa penalti**; adu penalti hanya ditangani pada level simulasi knockout.
- Harmonisasi nama tim memakai `former_names.csv`.
- Istilah format turnamen memakai: round-robin (fase grup), knockout (fase gugur), grup+knockout (komposisi keduanya).

### Batasan pasti (hasil inspeksi)

- `results.csv`: **49.945 baris**, rentang **1872-11-30 – 2026-10-06**; skor mencakup perpanjangan waktu, tanpa hasil 90 menit.
- Nama turnamen terkait ASEAN di data beserta hasil inspeksi jumlah dan rentang tanggal:
  - `AFF Championship`: **291 laga**, 1996-09-01 – 2023-01-16
  - `ASEAN Championship`: **52 laga**, 2024-12-08 – 2026-08-26
  - `FIFA ASEAN Cup`: **14 laga**, 2026-09-25 – 2026-10-05
  - Kualifikasi: `AFF Championship qualification` **62 laga**, `ASEAN Championship qualification` **2 laga**

### Pertanyaan terbuka

Semua jawaban atas daftar ini harus diverifikasi dari sumber turnamen/sumber data resmi sebelum dijadikan asumsi analisis.

1. **Hubungan `AFF Championship`, `ASEAN Championship`, dan `FIFA ASEAN Cup`** — apakah ketiganya nama berbeda untuk kompetisi yang sama, edisi/era berbeda, atau kompetisi terpisah? Belum boleh diasumsikan `[perlu diverifikasi]`.
2. **Isi 14 laga `FIFA ASEAN Cup`** (2026-09-25 – 2026-10-05) — format, peserta, dan status laga (final resmi, laga uji coba, dsb.) belum diperiksa `[perlu diverifikasi]`.
3. **Format tiap edisi turnamen ASEAN** — jumlah tim, sistem round-robin di fase grup, sistem knockout (tunggal/ganda), jumlah laga per edisi, serta aturan waktu tambahan dan adu penalti per edisi `[perlu diverifikasi]`.
4. **Cakupan "ASEAN Cup"** — edisi dan babak kualifikasi mana yang dihitung sebagai target evaluasi dan masukan simulasi juara `[perlu diverifikasi]`.
5. **Status data terbaru** — laga hingga 2026-10-06: sudah final/resmi atau masih perlu pembaruan `[perlu diverifikasi]`.
6. **Model adu penalti** — jumlah dan representasi baris `shootouts.csv` untuk tim ASEAN; kelayakan model penalti sederhana yang dipakai simulasi `[perlu diverifikasi]`.
7. **Konvensi fitur** — penanganan `neutral`, status kandang/tandang pada laga turnamen netral, dan ketersediaan "tahap turnamen" sebagai fitur sebelum kickoff `[perlu diverifikasi]`.
8. **Tiebreaker klasemen grup** — model H/D/A tidak menghasilkan skor; opsi yang tersedia: tiebreaker diundi acak, atau menambah model skor tersendiri. **Keputusan ini belum diputuskan** (lihat juga bagian 2(b)).
9. **Rekonstruksi edisi** — kolom "edisi" tidak ada di `results.csv`; edisi harus direkonstruksi dari jeda tanggal antar laga. Rentang `ASEAN Championship` yang panjang (2024-12-08 – 2026-08-26) menandakan kemungkinan **lebih dari satu edisi** `[perlu diverifikasi]`.
10. **Pengecekan Tahap 2** — baris dengan skor kosong di `results.csv` (kemungkinan jadwal yang belum dimainkan) harus dicek dan ditangani sebelum analisis `[perlu diverifikasi]`.

## 8. Kriteria Sukses

Model dianggap memenuhi tujuan project bila pada evaluasi backtest (bagian 6) dengan pelaporan sesuai bagian 4:

- **Mengalahkan prior kelas dengan jelas** pada log loss (metrik utama) — selisihnya melebihi ketidakpastian dari interval kepercayaan bootstrap, bukan sekadar beda tipis di dalam noise.
- **Setidaknya menyamai baseline Elo murni** pada log loss dan kalibrasi.
- **Hasil negatif tetap dilaporkan** apa adanya: bila model tidak melewati baseline, temuan tersebut menjadi bagian dari dokumentasi project, bukan disembunyikan.

## 9. Lampiran — rekap angka EDA 4.1 (deskriptif)

Bagian ini merangkum angka dari subbagian **4.1 Pola Global** di `notebooks/asean_cup_prediction.ipynb`. Semua angka bersifat deskriptif (belum ada pemodelan) dan dihitung pada satu kerangka data yang sama.

**Cakupan sampel.** `data/processed/matches_merged.csv` dibaca apa adanya (**49.945** baris), lalu difilter `date < 2024-12-08` menjadi `df_eda` (**48.093** baris; **1.852** baris dibuang). Tanggal terakhir `df_eda` adalah **2024-11-19**, sehingga assert `date.max() < 2024-12-08` lolos; rentangnya **1872-11-30 – 2024-11-19** dengan **16 dekade**. Batas 2024-12-08 dipakai karena itu tanggal laga pertama `ASEAN Championship` (bagian 3.4), sehingga seluruh laga turnamen ASEAN yang menjadi fokus evaluasi tidak masuk EDA.

Dua catatan pembacaan: dekade **2020-an tidak penuh** (hanya sampai 2024-11-19, n = 4.687), dan dekade dengan **n < 200** ditandai *sampel kecil*.

### 9.1 Volume laga, gol, seri, netral, dan skor besar per dekade

| Dekade | Laga (n) | % dari `df_eda` | Rata-rata total gol | Median total gol | Tingkat seri | Proporsi laga netral | Proporsi \|selisih\| ≥ 5 | Sampel |
|---|---|---|---|---|---|---|---|---|
| 1870-an | 13 | 0,03% | 4,538 | 4 | 0,1538 | 0,0000 | 0,1538 | *sampel kecil* |
| 1880-an | 55 | 0,11% | 5,582 | 5 | 0,0909 | 0,0000 | 0,3818 | *sampel kecil* |
| 1890-an | 59 | 0,12% | 5,153 | 5 | 0,1525 | 0,0169 | 0,2712 | *sampel kecil* |
| 1900-an | 138 | 0,29% | 4,159 | 4 | 0,1739 | 0,0362 | 0,1377 | *sampel kecil* |
| 1910-an | 330 | 0,69% | 4,218 | 4 | 0,1606 | 0,1061 | 0,1182 | cukup |
| 1920-an | 831 | 1,73% | 3,884 | 4 | 0,1793 | 0,1252 | 0,1035 | cukup |
| 1930-an | 1.079 | 2,24% | 4,319 | 4 | 0,1594 | 0,1297 | 0,1084 | cukup |
| 1940-an | 833 | 1,73% | 4,345 | 4 | 0,1537 | 0,2101 | 0,1513 | cukup |
| 1950-an | 1.657 | 3,45% | 4,001 | 4 | 0,1835 | 0,2100 | 0,0935 | cukup |
| 1960-an | 2.971 | 6,18% | 3,479 | 3 | 0,1962 | 0,2487 | 0,0831 | cukup |
| 1970-an | 4.132 | 8,59% | 2,977 | 3 | 0,2183 | 0,2701 | 0,0634 | cukup |
| 1980-an | 5.026 | 10,45% | 2,526 | 2 | 0,2612 | 0,2557 | 0,0466 | cukup |
| 1990-an | 6.942 | 14,43% | 2,780 | 2 | 0,2429 | 0,2702 | 0,0624 | cukup |
| 2000-an | 9.540 | 19,84% | 2,802 | 2 | 0,2342 | 0,2541 | 0,0634 | cukup |
| 2010-an | 9.800 | 20,38% | 2,737 | 2 | 0,2324 | 0,2906 | 0,0603 | cukup |
| 2020-an | 4.687 | 9,75% | 2,669 | 2 | 0,2323 | 0,3284 | 0,0529 | cukup (belum penuh) |
| **Keseluruhan** | **48.093** | **100%** | **2,942** | **—** | **0,2273** | **0,2627** | **0,0666** | — |

Selisih gol `home_score - away_score` berpusat di **0** (median 0; rata-rata **0,578**) dengan rentang **-21 sampai 31**; laga dengan **|selisih| ≥ 5** berjumlah **3.201 laga (6,66%)**.

### 9.2 Proporsi H/D/A per dekade, terpisah `neutral=False` dan `neutral=True`

| Dekade | n non-netral | H | D | A | n netral | H | D | A |
|---|---|---|---|---|---|---|---|---|
| 1870-an | 13 | 0,6154 | 0,1538 | 0,2308 | — | — | — | — |
| 1880-an | 55 | 0,4909 | 0,0909 | 0,4182 | — | — | — | — |
| 1890-an | 58 | 0,5000 | 0,1552 | 0,3448 | 1 | 1,0000 | 0,0000 | 0,0000 |
| 1900-an | 133 | 0,4436 | 0,1805 | 0,3759 | 5 | 0,6000 | 0,0000 | 0,4000 |
| 1910-an | 295 | 0,5119 | 0,1763 | 0,3119 | 35 | 0,8286 | 0,0286 | 0,1429 |
| 1920-an | 727 | 0,4966 | 0,1967 | 0,3067 | 104 | 0,7692 | 0,0577 | 0,1731 |
| 1930-an | 939 | 0,5229 | 0,1704 | 0,3067 | 140 | 0,5357 | 0,0857 | 0,3786 |
| 1940-an | 658 | 0,5441 | 0,1581 | 0,2979 | 175 | 0,4914 | 0,1371 | 0,3714 |
| 1950-an | 1.309 | 0,4935 | 0,1895 | 0,3170 | 348 | 0,4770 | 0,1609 | 0,3621 |
| 1960-an | 2.232 | 0,5224 | 0,2101 | 0,2675 | 739 | 0,5264 | 0,1543 | 0,3194 |
| 1970-an | 3.016 | 0,5153 | 0,2221 | 0,2626 | 1.116 | 0,4624 | 0,2079 | 0,3297 |
| 1980-an | 3.741 | 0,4905 | 0,2622 | 0,2473 | 1.285 | 0,4171 | 0,2584 | 0,3245 |
| 1990-an | 5.066 | 0,5057 | 0,2469 | 0,2473 | 1.876 | 0,4728 | 0,2319 | 0,2953 |
| 2000-an | 7.116 | 0,5094 | 0,2397 | 0,2508 | 2.424 | 0,4216 | 0,2178 | 0,3606 |
| 2010-an | 6.952 | 0,5053 | 0,2267 | 0,2680 | 2.848 | 0,4154 | 0,2465 | 0,3381 |
| 2020-an | 3.148 | 0,5089 | 0,2252 | 0,2659 | 1.539 | 0,4048 | 0,2469 | 0,3483 |
| **Total** | **35.458** | — | — | — | **12.635** | — | — | — |

Dekade *sampel kecil* pada panel `neutral=False` adalah **1870-an–1900-an**; pada panel `neutral=True` adalah **1890-an–1940-an**.

### 9.3 Implikasi untuk keputusan yang sudah ada di dokumen ini

- **Split harus temporal (bagian 3 dan 6).** Volume laga tidak merata: 2000-an **9.540** laga (**19,84%**) dan 2010-an **9.800** laga (**20,38%**), sedangkan 1870-an hanya **13** laga (**0,03%**). Split acak akan mencampur era dan membocorkan pola antar-periode.
- **Sampel latih era modern sebagai eksperimen ablasi (bagian 6) punya dasar angka.** Rata-rata total gol turun dari **5,582** (1880-an) dan **4,345** (1940-an) ke **2,669** (2020-an); proporsi laga selisih ≥ 5 turun dari **0,3818** (1880-an) dan **0,1513** (1940-an) ke **0,0529** (2020-an). Model skor/simulasi yang dilatih pada seluruh sejarah akan menghasilkan ekor gol terlalu gemuk untuk era modern.
- **Prior kelas harus dihitung dari data train, dan berbeda antar era (bagian 5).** Tingkat seri naik dari **0,0909** (1880-an) ke **0,2612** (1980-an) lalu menetap di kisaran **0,2323–0,2429** (**2020-an 0,2323**); baseline prior kelas yang dihitung global tidak mewakili periode uji.
- **`neutral` perlu fitur dan interaksi dengan era (bagian 7 pertanyaan 7).** Proporsi laga netral naik dari **0,0000** (1870-an dan 1880-an) ke **0,3284** (2020-an). Pada laga netral, proporsi H cenderung menurun: **0,5264** (1960-an) menjadi **0,4048** (2020-an), sementara pada laga non-netral H relatif stabil (**0,4905–0,5441** pada dekade n ≥ 200).
- **Laga netral modern tidak boleh hanya dimodelkan lewat status tuan rumah.** Pada 2020-an `neutral=True`, H **0,4048** dan A **0,3483** berjarak tipis (**0,0565**), sehingga fitur kekuatan tim tetap diperlukan.
- **Metrik sebaiknya dilaporkan per periode (bagian 4), bukan hanya agregat.** Karena prior kelas bergeser menurut dekade, log loss agregat menyembunyikan perbedaan kesulitan antar-era.
- **Semua ini belum mengubah keputusan desain mana pun.** Angka di atas hanya menopang pilihan yang sudah tertulis di bagian 5–7 (split temporal, prior dari train, `neutral` sebagai fitur, ablasi era modern) dan tidak menambah asumsi baru.

### 9.4 Berkas grafik

Seluruh grafik tersimpan sebagai PNG, dpi 150, di `reports/figures/`:

| Berkas | Isi |
|---|---|
| `fig_01_jumlah_laga_per_tahun.png` | Jumlah laga per tahun (garis), 1872–2024 |
| `fig_02_rata_rata_gol_per_dekade.png` | Rata-rata total gol per laga per dekade |
| `fig_03_proporsi_hda_per_dekade_neutral.png` | Proporsi H/D/A per dekade, 2 panel (`neutral=False`, `neutral=True`) |
| `fig_04_tingkat_seri_per_dekade.png` | Tingkat seri per dekade |
| `fig_05_proporsi_laga_netral_per_dekade.png` | Proporsi laga netral per dekade |
| `fig_06_distribusi_selisih_gol.png` | Distribusi selisih gol tuan rumah − tamu (seluruh `df_eda`) |
| `fig_07_proporsi_selisih_besar_per_dekade.png` | Proporsi laga selisih ≥ 5 per dekade |
