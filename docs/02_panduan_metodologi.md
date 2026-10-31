# 02 - Panduan Metodologi: Dari Data Mentah ke Probabilitas Juara

> Dokumen ini adalah bagian 2 dari dokumentasi project. Bagian 1 (`01_problem_framing.md`) merumuskan masalah dan aturan evaluasi. Dokumen ini menjawab pertanyaan yang lebih praktis: **bagaimana perjalanan data mentah sampai menjadi angka seperti "Thailand 30,97%"?**
>
> Angka di dokumen ini berasal dari notebook `notebooks/asean_cup_prediction.ipynb`, kode di `src/`, dan artefak di `data/processed/`. Tujuannya bukan menghafal angka, tetapi memahami **mengapa setiap langkah ada, apa yang dihitung, dan apa artinya**.

---

## 0. Ringkasan Satu Halaman

Bayangkan kita punya tiga buku catatan sejarah sepak bola:

1. `results.csv` - catatan hasil pertandingan;
2. `shootouts.csv` - catatan laga yang berakhir lewat adu penalti;
3. `former_names.csv` - kamus nama lama dan nama baru tim.

Project ini tidak langsung menebak "siapa juara". Ia membangun rantai yang lebih panjang:

```text
hasil pertandingan masa lalu
        |
        v
fitur pra-laga (Elo, form, head-to-head, konteks)
        |
        v
probabilitas tiap laga: (p_H, p_D, p_A)
        |
        v
simulasi 10.000 turnamen per edisi
        |
        v
probabilitas juara: p_juara = jumlah juara / 10.000
```

**Inti project dalam satu kalimat:** mengubah sejarah pertandingan menjadi probabilitas H/D/A yang hanya memakai informasi sebelum laga, lalu memakai probabilitas itu sebagai "mesin undian" untuk menjalankan format turnamen ASEAN berkali-kali.

Ada tiga lapis yang harus berhasil sekaligus:

| Lapis | Pertanyaan | Alat utama |
|---|---|---|
| 1. Data dan waktu | Apakah data bersih, dan apakah masa depan benar-benar dikunci? | audit, `match_id`, split temporal |
| 2. Model probabilitas | Seberapa baik model memberi peluang H/D/A? | Elo, form, H2H, logistic, baseline, log loss |
| 3. Simulasi | Jika laga diundi, seberapa sering tiap tim juara? | Monte Carlo, aturan grup/knockout, Wilson interval |

**Hasil besarnya:**

- Model final **jelas mengalahkan prior kelas** pada log loss, tetapi hanya **menyamai** Elo murni dan logistic baseline; belum ada bukti keunggulan yang stabil.
- Kalibrasi model final **cukup, tetapi tidak unggul** dibanding baseline.
- Simulasi **informatif**: rata-rata peluang untuk juara aktual 25,22%, jauh di atas 10% jika semua tim dianggap sama. Tetapi pilihan teratas hanya tepat **1 dari 5 edisi**; juara aktual masuk top-3 pada **4 dari 5 edisi**.

Jadi, nilai project ini bukan "model yang selalu benar menebak juara". Nilainya adalah **kerangka probabilistik yang jujur, dapat direproduksi, dan bisa dipakai untuk menyusun skenario**.

> **Istilah sederhana - probabilitas:** angka antara 0 dan 1 yang menyatakan seberapa besar keyakinan model, bukan kepastian. Probabilitas 0,30 berarti "dalam model ini, ada sekitar 30 dari 100 kemungkinan".

---

## 1. Tiga Data Mentah dan Perannya

### 1.1 `results.csv` - buku utama

File ini adalah sumber utama karena berisi satu baris untuk satu pertandingan:

| Kolom | Arti sederhana |
|---|---|
| `date` | tanggal pertandingan |
| `home_team` | tim di kolom "home" |
| `away_team` | tim di kolom "away" |
| `home_score`, `away_score` | skor akhir |
| `tournament` | nama turnamen |
| `city`, `country` | lokasi pertandingan |
| `neutral` | apakah venue netral |

Ukuran awalnya **49.945 baris x 9 kolom**, dengan rentang tanggal **1872-11-30 sampai 2026-10-06**.

Satu hal penting: kata "home" di sini adalah **posisi administratif di data**, bukan jaminan tim itu bermain di kandang. Pada laga netral, `home_team` tetap ada, tetapi `neutral=True` menandakan venue bukan kandang salah satu tim. Karena itu project menambahkan fitur `home_is_host` dan `away_is_host` untuk membedakan "tertulis di kolom home" dari "benar-benar tuan rumah".

### 1.2 `shootouts.csv` - catatan adu penalti

File ini berisi **700 baris** laga yang berakhir lewat adu penalti:

| Kolom | Arti sederhana |
|---|---|
| `date`, `home_team`, `away_team` | identitas laga |
| `winner` | pemenang adu penalti |
| `first_shooter` | tim yang menendang pertama |

File ini **bukan fitur model**. Adu penalti terjadi setelah pertandingan; kalau dipakai sebagai fitur, itu akan menjadi kebocoran informasi masa depan. Perannya:

- memahami laga yang berakhir seri lalu diselesaikan lewat penalti;
- memberi konteks pada kolom `has_shootout`, `shootout_winner`, dan `first_shooter`;
- menjadi cadangan untuk menentukan juara aktual pada final dua leg yang agregatnya imbang.

Dari 700 baris, **699 cocok** dengan `results.csv` dan **1 tidak cocok**: laga 2011-06-29 Saare County vs Åland Islands. Kandidat terkuat di data adalah laga 2011-06-26 Åland Islands 3-3 Saare County, tetapi tanggalnya berbeda; karena itu statusnya dicatat sebagai belum pasti, bukan dipaksa cocok.

### 1.3 `former_names.csv` - kamus nama tim

File ini berisi **36 nama lama** beserta nama barunya. Gunanya mencegah satu tim terpecah menjadi dua entitas hanya karena namanya berubah antar-era.

Hasil audit: **0 nama lama** dari file ini muncul di `results.csv` maupun `shootouts.csv`. Artinya, untuk dataset ini tidak ada penggantian nama yang harus dilakukan. File tetap disimpan sebagai aturan dan dokumentasi, bukan karena ada nama yang harus diperbaiki.

> **Istilah sederhana - entitas tim:** satu "tim" harus tetap dihitung sebagai tim yang sama meskipun namanya berganti, misalnya dari nama kolonial ke nama modern.

### 1.4 Mengapa ada data yang tidak dipakai?

Di `results.csv` ada tiga nama turnamen terkait ASEAN:

| Nama turnamen | Jumlah | Rentang | Peran dalam project |
|---|---:|---|---|
| `AFF Championship` | 291 | 1996-09-01 sampai 2023-01-16 | data latih, validasi, backtest |
| `ASEAN Championship` | 52 | 2024-12-08 sampai 2026-08-26 | fokus final test dan simulasi 2024/2026 |
| `FIFA ASEAN Cup` | 14 | 2026-09-25 sampai 2026-10-05 | **dikeluarkan** |

`FIFA ASEAN Cup` dikeluarkan karena format, peserta, dan status lagnya belum jelas dari data; 14 laga ini juga berada setelah periode utama. Project memilih lingkup yang lebih bersih: fokus pada `AFF Championship` dan `ASEAN Championship`.

Selain itu ada kualifikasi:

- `AFF Championship qualification`: 62 laga;
- `ASEAN Championship qualification`: 2 laga.

Keduanya **hanya menjadi data latih**, bukan target evaluasi, karena komposisi pesertanya berbeda dari putaran final.

> **Istilah sederhana - lingkup (scope):** batas masalah yang sengaja dipilih. Mengeluarkan `FIFA ASEAN Cup` bukan berarti laga itu tidak penting; ia dikeluarkan agar pertanyaan project tetap konsisten dan dapat dipertanggungjawabkan.

---

## 2. Audit Data: Sebelum Percaya, Periksa Dulu

Sebelum membangun fitur atau model, notebook memeriksa kualitas data. Ini penting karena model yang canggih tetap akan menghasilkan probabilitas yang salah jika datanya kotor.

### 2.1 Pemeriksaan dasar

| Pemeriksaan | Hasil |
|---|---:|
| Jumlah baris `results.csv` | 49.945 |
| Gagal parse tanggal | 0 |
| Skor kosong | 0 |
| Skor negatif | 0 |
| Nilai `neutral` selain True/False | 0 |
| Tanggal setelah 2026-10-23 | 0 |
| Duplikat kunci `(date, home_team, away_team)` | 1 pasang |
| Nama lama dari `former_names.csv` yang muncul | 0 |

Tidak ada baris yang dihapus dan tidak ada file mentah yang ditimpa. Prinsipnya: **audit dulu, baru memutuskan**.

### 2.2 Satu duplikat yang menarik

Ada satu pasangan aneh:

- 1974-02-17, Tahiti vs New Caledonia;
- satu baris mencatat 2-1;
- satu baris lain mencatat 1-2.

Apakah ini dua laga berbeda, salah input, atau laga dua leg? Data tidak cukup untuk memastikan. Karena itu kedua baris **dipertahankan**, lalu diberi `match_id` berbeda: **9650** dan **9651**.

Mengapa tidak dihapus saja? Karena menghapus data yang belum jelas bisa membuang informasi. Dengan `match_id` unik, kedua baris tetap bisa dilacak, dan model tidak bingung membedakan identitas laga.

> **Istilah sederhana - `match_id`:** nomor identitas unik untuk setiap baris laga. Ibarat nomor tanda pengenal: dua laga boleh punya tanggal dan tim yang sama, tetapi nomornya tetap berbeda.

### 2.3 Adu penalti dan bahaya kebocoran

Dari 700 shootout:

- **699** cocok dengan `results.csv`;
- **37** memiliki skor laga yang tidak seri, padahal ada shootout;
- **662** adalah shootout setelah laga seri;
- **1** tidak cocok sama sekali.

Angka 37 yang tidak seri kemungkinan berkaitan dengan aturan dua leg/agregat, tetapi project tidak menganggapnya sebagai fakta tanpa bukti. Semua 37 baris dicatat, tidak diubah.

Yang paling penting: `shootout_winner` **tidak dipakai sebagai fitur model**. Kalau dipakai, model akan "mengetahui" hasil adu penalti sebelum laga, itu leakage.

> **Istilah sederhana - data leakage:** informasi dari masa depan atau informasi yang seharusnya tidak diketahui saat prediksi ikut masuk ke model. Analoginya seperti membocorkan kunci jawaban ke peserta ujian.

---

## 3. Membentuk Tabel Dasar, Label, dan Konteks

### 3.1 Urutan, ID, dan label

Langkah pertama pada `results.csv`:

1. baca ulang data mentah;
2. simpan urutan asli sebagai `orig_row`;
3. ubah `date` menjadi tipe tanggal;
4. urutkan tanggal secara **stabil**;
5. beri `match_id` 0 sampai 49.944.

Sort stabil berarti jika beberapa laga punya tanggal sama, urutan aslinya tidak diacak. Ini penting untuk reproduksibilitas.

Label dibuat dari skor:

```text
home_score > away_score  -> H
home_score = away_score  -> D
home_score < away_score  -> A
```

Hasilnya konsisten dengan audit:

- H: **24.473** (49,0%);
- D: **11.341** (22,7%);
- A: **14.131** (28,3%).

Tabel dasar disimpan sebagai `data/processed/matches_base.csv`: **49.945 baris x 12 kolom**.

### 3.2 Merge shootouts

`matches_base` digabung dengan `shootouts.csv` memakai kunci `(date, home_team, away_team)`.

Karena di sisi kiri ada satu kunci ganda (Tahiti vs New Caledonia), merge memakai `validate="many_to_one"` secara eksplisit: satu baris shootout boleh cocok ke banyak baris di data dasar. Hasilnya:

- jumlah baris tetap **49.945**;
- `match_id` tetap unik;
- 699 baris shootout ter-join;
- tiga kolom baru: `has_shootout`, `shootout_winner`, `first_shooter`.

Tabel akhir `data/processed/matches_merged.csv` berukuran **49.945 x 15**.

Kolom `shootout_after_draw = has_shootout & (result == "D")` dibuat hanya sebagai diagnostik di memori dan **tidak disimpan** sebagai fitur model.

### 3.3 Rekonstruksi edisi turnamen

Data tidak punya kolom "edisi". Untuk memisahkan edisi, notebook memakai aturan sederhana: jika jarak antar-laga dalam satu turnamen **lebih dari 180 hari**, itu dianggap awal edisi baru.

Hasilnya:

- `AFF Championship` menjadi **14 edisi**;
- `ASEAN Championship` menjadi **2 edisi** (2024 dan 2026);
- masing-masing edisi ASEAN berisi **26 laga, 10 tim**.

Aturan ini adalah **rekonstruksi**, bukan kebenaran dari sumber resmi. Karena itu notebook menandainya sebagai usulan yang perlu diverifikasi. Untuk project ini, rekonstruksi tersebut cukup konsisten dengan format 26 laga yang dipakai di simulasi.

### 3.4 Mengapa `FIFA ASEAN Cup` dikeluarkan?

Karena 14 laga itu:

- berisi tim yang tidak sama dengan peserta AFF/ASEAN Championship (ada Bangladesh dan Pakistan);
- status dan formatnya belum jelas dari data;
- berada di luar periode fokus.

Menjaga data tetap bersih lebih penting daripada menambah 14 baris yang tidak jelas asalnya.

---

## 4. EDA: Apa yang Data Katakan Sebelum Model Dibuat

EDA (Exploratory Data Analysis) adalah pemeriksaan pola sebelum membangun model. Notebook hanya memakai **48.093 laga dev** (`date < 2024-12-08`), bukan final test.

### 4.1 Tiga pola utama

**Pola 1 - kelas tidak seimbang.**

H lebih sering muncul (sekitar 49%), diikuti A (28,3%), lalu D (22,7%). Artinya, model yang selalu menebak H sudah mendapat akurasi sekitar 49%. Baseline prior dipakai untuk menunjukkan apakah model benar-benar belajar sesuatu.

**Pola 2 - gol menurun, seri meningkat.**

Rata-rata total gol per laga turun dari sekitar **5,58** pada 1880-an menjadi **2,67** pada 2020-an. Tingkat seri naik dari sekitar 9% pada 1880-an menjadi sekitar 23% pada 2020-an. Ini mengisyaratkan bahwa era modern berbeda dari era awal; model yang memakai seluruh sejarah perlu diuji stabilitasnya.

**Pola 3 - laga netral makin umum, keuntungan kandang mengecil.**

Proporsi laga netral meningkat dari 0% pada 1870-an menjadi sekitar 32,8% pada 2020-an. Pada laga netral modern, selisih H dan A relatif kecil. Karena itu `neutral`, `home_is_host`, dan interaksi keduanya masuk sebagai fitur.

### 4.2 Mengapa EDA penting untuk desain?

EDA bukan sekadar membuat grafik. Di project ini, EDA menghasilkan keputusan:

- split harus **temporal**, bukan acak, karena era berbeda;
- prior kelas harus dihitung dari data latih, bukan dari seluruh data;
- `neutral` dan status tuan rumah perlu fitur terpisah;
- metrik tidak boleh hanya akurasi, karena kelas H mendominasi;
- evaluasi ASEAN harus dilaporkan terpisah, karena hanya 52 laga di final test.

> **Istilah sederhana - distribusi kelas:** komposisi jumlah contoh per kelas. Kalau 49% data adalah H, akurasi 49% bisa dicapai hanya dengan selalu menebak H; itu sebabnya kita butuh metrik probabilitas seperti log loss.

---

## 5. Split: Mengunci Masa Depan

### 5.1 Batas waktu

Project memakai satu garis waktu yang keras:

```text
date < 2024-12-08   -> dev
date >= 2024-12-08  -> final_test
```

Tanggal 2024-12-08 adalah laga pertama `ASEAN Championship` di data. Dengan batas ini:

- `dev`: **48.093 baris**, berakhir 2024-11-19;
- `final_test`: **1.852 baris**, mulai 2024-12-08;
- jarak antara keduanya: **19 hari**.

`final_test` hanya **3,71%** dari seluruh data. Ukurannya kecil, sehingga hasilnya harus dibaca dengan interval ketidakpastian.

### 5.2 Dua lapis validasi

Sebelum menyentuh final test, model diuji dengan dua lapis:

| Lapis | Cara | Jumlah |
|---|---|---:|
| Tahunan | untuk Y=2010..2024, latih pada data sebelum 1 Januari Y, uji tahun Y (2024 hanya sampai 2024-11-19, sebelum cutoff) | 15 fold, 14.487 baris validasi |
| ASEAN | untuk tiap edisi AFF Championship mulai 2010, latih sebelum edisi, uji seluruh edisi | 7 fold, 150 laga |

Lapis tahunan mengukur stabilitas di banyak tahun. Lapis ASEAN mengukur performa pada satu edisi utuh, yang lebih dekat dengan target aplikasi. Keduanya memakai **expanding window**: data latih tumbuh seiring waktu, dan tidak ada data validasi yang masuk latih.

### 5.3 Aturan "final test hanya sekali"

`final_test` tidak boleh dipakai untuk:

- memilih fitur;
- memilih model;
- tuning hyperparameter;
- memilih threshold;
- memilih aturan kalibrasi.

Satu-satunya hal yang boleh dihitung sebelum Section 8 adalah **jumlah baris per kelompok**. Isi final test baru dibuka satu kali di Section 8, setelah konfigurasi final dibekukan.

Definisi split disimpan di `data/processed/split_definition.json` agar batas train/validasi tidak bergeser diam-diam.

> **Istilah sederhana - walk-forward:** cara menguji model seperti orang belajar dari masa lalu: saat memprediksi 2020, ia hanya boleh tahu sampai akhir 2019; saat memprediksi 2021, ia boleh tahu sampai akhir 2020; dan seterusnya. Tidak ada "melihat masa depan".

---

## 6. Feature Engineering: Mengubah Sejarah Menjadi Sinyal

Fitur adalah input yang dilihat model. Semua fitur di project ini dibangun dengan aturan yang sama:

> **Untuk laga tanggal t, hanya informasi dari tanggal < t yang boleh dipakai. Laga pada tanggal yang sama tidak saling memengaruhi.**

Aturan ini diterapkan pada Elo, form, dan head-to-head. Jika beberapa laga terjadi pada tanggal yang sama, semua laga itu memakai kondisi **sebelum tanggal tersebut**, lalu pembaruan dilakukan setelah kelompok tanggal selesai.

### 6.1 Elo: rating kekuatan tim

Elo adalah angka yang naik saat menang dan turun saat kalah. Tim yang menang atas lawan kuat mendapat kenaikan lebih besar daripada menang atas lawan lemah.

Rumus yang dipakai:

```text
dr = (R_home - R_away) + (100 jika tidak netral, 0 jika netral)
E_home = 1 / (1 + 10^(-dr/400))
S_home = 1 (menang), 0.5 (seri), 0 (kalah)
G = 1 jika selisih gol <= 1
    1.5 jika selisih gol = 2
    (11 + selisih gol) / 8 jika selisih gol >= 3
delta = 30 * G * (S_home - E_home)
R_home += delta
R_away -= delta
```

Penjelasan sederhana:

- `R_home` dan `R_away` adalah rating sebelum laga;
- `dr` adalah selisih kekuatan, ditambah bonus kandang 100 jika tidak netral;
- `E_home` adalah peluang menang yang "diharapkan" oleh Elo;
- `S_home` adalah hasil nyata (1/0,5/0);
- `G` membuat kemenangan besar sedikit lebih berbobot;
- `delta` adalah perubahan rating.

Contoh intuisi: jika rating home 1600 dan away 1500, dengan bonus kandang 100, `dr=200`, maka `E_home` sekitar 0,76. Artinya, Elo menganggap home cukup diunggulkan. Jika home menang, kenaikannya lebih kecil daripada jika home menang saat diprediksi kalah.

Fitur yang dihasilkan:

- `elo_home_pre`, `elo_away_pre`: rating sebelum laga;
- `elo_diff`: selisih rating;
- `n_prev_home`, `n_prev_away`: jumlah laga sebelumnya.

Catatan penting: `K=30`, `home_adv=100`, `init=1500`, dan pengali gol adalah **nilai default**, bukan hasil tuning. Ini keterbatasan yang harus disebut.

### 6.2 Form: bentuk lima laga terakhir

Untuk setiap tim, project menghitung:

- rata-rata poin dari 5 laga terakhir (menang 3, seri 1, kalah 0);
- rata-rata gol cetak;
- rata-rata gol kemasukan;
- jumlah laga yang tersedia (`n_form`);
- `rest_days`: hari sejak laga terakhir, dibatasi maksimal 365 hari.

Form adalah fitur "sedang naik atau turun". Tim yang menang 4 dari 5 laga terakhir punya `form_pts` tinggi.

### 6.3 Head-to-head: sejarah pertemuan

Untuk pasangan tim:

- `n_h2h`: berapa kali mereka pernah bertemu;
- `h2h_score_home`: skor dari sudut pandang tim home, dengan menang=1, seri=0,5, kalah=0.

Jika belum pernah bertemu, `n_h2h=0` dan `h2h_score_home` kosong (`NaN`). Nilai kosong ini **tidak diisi saat pembuatan fitur**; nanti model yang mengisi dengan median data latih.

### 6.4 Konteks: netral, tuan rumah, turnamen

Empat fitur konteks:

- `neutral`: 0/1;
- `home_is_host`: 1 jika `home_team` sama dengan `country`;
- `away_is_host`: 1 jika `away_team` sama dengan `country`;
- `tournament_group`: Friendly, Kualifikasi, FIFA World Cup, atau Lainnya.

`tournament_group` menyederhanakan ratusan nama turnamen menjadi empat kelompok. Tujuannya agar model tidak terlalu bergantung pada nama turnamen yang sangat spesifik.

### 6.5 Fitur interaksi

Model `full_interaksi` menambahkan 13 fitur turunan:

- selisih form (`form_pts_diff`, `form_gf_diff`, `form_ga_diff`);
- selisih jumlah laga form dan rest days;
- `elo_diff_abs` dan `elo_diff_sq` (selisih Elo absolut dan kuadrat);
- `elo_sum` (total kekuatan kedua tim);
- interaksi tuan rumah dengan Elo;
- interaksi netral dengan Elo;
- interaksi H2H dengan Elo.

Ide sederhananya: pengaruh selisih Elo bisa berbeda saat home benar-benar tuan rumah, saat netral, atau saat kedua tim punya sejarah pertemuan.

### 6.6 Total kolom

Tabel fitur punya **26 kolom**:

- 5 kolom identitas dan target: `match_id`, `date`, `home_team`, `away_team`, `result`;
- 21 fitur prediktif: Elo, form, H2H, dan konteks.

Angka 26 adalah jumlah kolom file `features_dev.csv`. Saat notebook memuat metadata untuk evaluasi, `tournament` dan `country` ikut ditambahkan sehingga tampilan notebook menunjukkan 28 kolom; keduanya bukan fitur yang masuk model.

Nilai kosong tidak diisi di tahap ini. Pengisian dilakukan **di dalam pipeline model**, hanya memakai statistik data latih fold. Ini penting agar tidak ada leakage dari data validasi.

> **Istilah sederhana - fitur:** informasi yang diberikan ke model untuk membuat keputusan. Ibarat dokter: tekanan darah, suhu, dan riwayat penyakit adalah fitur; diagnosis adalah target.
>
> **Istilah sederhana - imputasi:** mengisi nilai yang kosong. Project memakai median dari data latih untuk angka, dan nilai paling sering untuk kategori.

---

## 7. Model: Dari Fitur ke Tiga Probabilitas

### 7.1 Tiga baseline

Baseline adalah pembanding minimum. Tanpa baseline, angka log loss tidak berarti apa-apa.

**A. Prior kelas**

Model ini tidak melihat tim atau fitur. Ia hanya menghitung frekuensi H/D/A di data latih, lalu memakai frekuensi yang sama untuk semua laga. Jika model lain tidak mengalahkan prior, fitur yang dipakai belum memberi nilai tambah.

**B. Elo murni (Davidson)**

Model ini hanya memakai `elo_home_pre`, `elo_away_pre`, dan `neutral`. Probabilitas H/D/A dibentuk dengan model Davidson:

```text
p_H ∝ exp(beta * (elo_home + home_adv * (1 - neutral)))
p_A ∝ exp(beta * elo_away)
p_D ∝ nu * sqrt(p_H_tanpa_normalisasi * p_A_tanpa_normalisasi)
```

`beta` mengatur seberapa tajam perbedaan Elo memengaruhi probabilitas. `nu` mengatur kecenderungan seri. Keduanya diestimasi dengan maximum likelihood pada data latih setiap fold. `home_adv` tetap 100 agar baseline tetap sederhana.

**C. Logistic Regression baseline**

Model ini memakai fitur lengkap: Elo, form, H2H, dan konteks. Pipeline-nya:

1. imputasi median untuk angka;
2. standardisasi angka;
3. imputasi most-frequent dan one-hot encoding untuk `tournament_group`;
4. Logistic Regression dengan regularisasi L2, `C=1,0`, `max_iter=2000`.

Semua langkah di-fit **hanya pada data latih fold**, bukan pada data validasi.

### 7.2 Model kandidat

Section 7 menguji empat kelompok fitur:

| Kelompok | Isi | Tujuan |
|---|---|---|
| `elo` | Elo, netral, status tuan rumah | seberapa jauh Elo saja bisa dibawa |
| `elo_form` | Elo + form + rest | menguji nilai form |
| `full` | semua fitur Section 5 | kandidat utama |
| `full_interaksi` | `full` + 13 interaksi | menguji hubungan non-linear sederhana |

Dua keluarga model:

1. **Logistic Regression L2** dengan `C` 0,03; 0,1; 1,0;
2. **HistGradientBoosting (HGB)** dengan learning rate 0,05/0,1 dan 15/31 daun.

HGB adalah model pohon bertahap: ia membangun banyak pohon keputusan kecil, lalu menggabungkannya. HGB tidak membutuhkan standardisasi, tetapi tetap memakai imputasi dan one-hot.

Ensemble juga diuji: rata-rata probabilitas logistic dan HGB dengan bobot 0 sampai 1, langkah 0,05.

### 7.3 Cara memilih model

Penyetelan hyperparameter dan bobot ensemble hanya memakai **15 fold tahunan**:

- metrik utama: log loss rata-rata per fold;
- metrik sekunder: Brier;
- fold ASEAN **tidak** dipakai untuk menyetel hyperparameter atau bobot; setelah konfigurasi dibekukan, fold ASEAN dipakai sekali untuk memilih di antara kandidat yang sudah lolos.

Hasilnya:

| Kandidat | Log loss tahunan mean | Log loss pooled | Catatan |
|---|---:|---:|---|
| Logistic `full` | 0,8897 | 0,8830 | baseline kuat |
| Logistic `full_interaksi` | **0,8890** | **0,8822** | dipilih |
| HGB + interaksi | 0,8924 | 0,8852 | tidak dipilih |
| Ensemble | 0,8886 | 0,8817 | menang tipis di tahunan, tetapi tidak terbawa ke ASEAN |

Logistic `full_interaksi` juga unggul di 150 laga ASEAN: log loss **0,7278**, Brier **0,4170**, RPS **0,1330**, akurasi **68,67%**, macro-F1 **0,4865**, ECE top **0,0604**. HGB **0,7417** dan ensemble **0,7306** lebih buruk pada log loss ASEAN.

Karena itu model final adalah **Logistic Regression `full_interaksi`, C=1,0, max_iter=2000**.

> **Istilah sederhana - regularisasi:** rem agar model tidak terlalu menghafal data latih. `C` kecil berarti rem kuat; `C` besar berarti rem lemah.
>
> **Istilah sederhana - softmax:** fungsi yang mengubah skor mentah menjadi tiga probabilitas yang jumlahnya 1. Jika skor H paling tinggi, p_H menjadi paling besar, tetapi kelas lain tetap punya peluang.

### 7.4 Metrik: mengapa log loss jadi raja?

| Metrik | Apa yang diukur | Arah |
|---|---|---|
| **Log loss** | seberapa besar hukuman jika probabilitas untuk hasil yang benar kecil | semakin kecil semakin baik |
| Brier | rata-rata kuadrat selisih probabilitas dan hasil | semakin kecil |
| RPS | error kumulatif untuk kelas berurutan H < D < A | semakin kecil |
| Akurasi | persentase tebakan keras (argmax) benar | semakin besar |
| Macro-F1 | keseimbangan performa antar kelas | semakin besar |
| ECE | selisih antara keyakinan dan frekuensi benar | semakin kecil |

Log loss dipilih sebagai metrik utama karena project ini menjual **probabilitas**, bukan label keras. Log loss sangat menghukum model yang "sangat yakin tetapi salah". Akurasi saja bisa menyesatkan: model yang selalu menebak H sudah bisa 49%.

Kalibrasi diukur dengan **ECE** dan reliability diagram. ECE kecil berarti ketika model berkata "70%", hasil benar terjadi sekitar 70% dari waktu. Kalibrasi penting karena probabilitas ini nanti dipakai untuk simulasi.

> **Istilah sederhana - kalibrasi:** kesesuaian antara ramalan dan kenyataan. Model yang berkata "80% menang" tetapi hanya menang 50% dari kasus serupa tidak terkalibrasi, meskipun kadang tebakannya benar.

### 7.5 Interval kepercayaan

Semua perbandingan penting memakai **bootstrap 2.000 resample**:

- ambil sampel ulang dari data evaluasi;
- hitung metrik;
- ulangi 2.000 kali;
- ambil persentil 2,5% dan 97,5% sebagai batas 95%.

Pada validasi ASEAN Section 7, resampling dilakukan **per edisi** (cluster bootstrap), karena laga dalam satu edisi tidak independen. Pada final test Section 8, 52 laga ASEAN di-resample per laga, sedangkan evaluasi gabungan di-resample per turnamen; perbedaan ini adalah keterbatasan tambahan karena sampel ASEAN sangat kecil.

Jika interval selisih **melewati nol**, kita tidak bisa mengklaim satu model lebih baik secara stabil.

> **Istilah sederhana - interval kepercayaan:** rentang ketidakpastian. Daripada hanya bilang "0,82", kita bilang "0,82, kira-kira di antara 0,75 dan 0,89".

---

## 8. Final Test: Membuka Segel Sekali

### 8.1 Cakupan

| Cakupan | Jumlah |
|---|---:|
| Final test mentah | 1.852 |
| `FIFA ASEAN Cup` dikeluarkan | 14 |
| Final test dievaluasi | **1.838** |
| `ASEAN Championship` | **52** |
| Internasional lain | 1.786 |

Final test berisi 52 laga ASEAN (2 edisi x 26) dan 1.786 laga internasional lain. Karena sekitar 97,2% isinya bukan ASEAN (1.786 dari 1.838), metrik gabungan tidak boleh dipakai sebagai pengganti evaluasi ASEAN.

### 8.2 Hasil pada 52 laga ASEAN

| Model | Log loss | Brier | RPS | Akurasi | Macro-F1 | ECE top | ECE classwise |
|---|---:|---:|---:|---:|---:|---:|---:|
| Prior kelas | 1,0686 | 0,6502 | 0,2521 | 42,31% | 19,82% | 0,0673 | 0,0810 |
| Elo murni | 0,8340 | 0,4792 | 0,1686 | 67,31% | 48,79% | 0,0859 | 0,0725 |
| Logistic baseline | 0,8219 | 0,4708 | 0,1658 | 67,31% | 48,79% | 0,0661 | 0,0816 |
| **Logistic final** | **0,8198** | **0,4704** | **0,1655** | 67,31% | 48,79% | 0,0704 | 0,0927 |

### 8.3 Apa yang benar-benar terbukti?

**Terhadap prior:** model final jelas lebih baik.

- selisih log loss: **-0,2488**;
- 95% CI: **[-0,4315; -0,0667]**;
- seluruh interval di bawah nol.

**Terhadap Elo:** model final hanya sedikit lebih baik di titik estimasi.

- selisih: **-0,0142**;
- 95% CI: **[-0,0431; +0,0178]**;
- interval melewati nol, jadi belum terbukti lebih baik secara stabil.

**Terhadap logistic baseline:** hampir sama.

- selisih: **-0,0021**;
- 95% CI: **[-0,0171; +0,0155]**;
- interval melewati nol.

Pada 1.838 laga gabungan, polanya sama: final **0,8473**, logistic baseline **0,8481**, Elo **0,8510**, prior **1,0478**.

### 8.4 Kalibrasi dan per edisi

Model final tidak unggul dalam kalibrasi final test:

- ECE top-label final **0,0704**, sedikit lebih tinggi dari baseline **0,0661**;
- ECE classwise final **0,0927**, lebih tinggi dari baseline **0,0816**.

Per edisi juga bercampur:

- 2026: final **0,7442** vs baseline **0,7558** (final lebih baik);
- 2024: final **0,8955** vs baseline **0,8880** (final lebih buruk).

Jadi kesimpulan yang jujur adalah: **menang jelas atas prior, setara dengan Elo dan logistic baseline, tanpa bukti keunggulan yang stabil**. Model tetap dipakai di simulasi karena ia kandidat terpilih sebelum final test dibuka, bukan karena final test menunjukkan superioritas.

> **Istilah sederhana - "setara secara statistik":** perbedaannya bisa jadi hanya kebetulan sampel. Kita tidak boleh mengklaim model A lebih baik hanya karena angkanya sedikit lebih rendah.

---

## 9. Monte Carlo: Dari Probabilitas Laga ke Probabilitas Juara

### 9.1 Mengapa perlu simulasi?

Model hanya memberi:

```text
p_H, p_D, p_A untuk satu laga
```

Yang ingin dijawab adalah:

```text
p_juara untuk satu tim dalam satu turnamen
```

Untuk menjembatani keduanya, project mengundi setiap laga sesuai probabilitasnya, menyusun klasemen, memainkan semifinal dan final, lalu mencatat juaranya. Proses itu diulang **10.000 kali per edisi**.

### 9.2 Format dan edisi yang disimulasikan

Project memakai lima edisi yang formatnya lengkap:

| Edisi | Turnamen | Tanggal | Grup A | Grup B |
|---|---|---|---|---|
| 2018 | AFF Championship | 2018-11-08 s/d 2018-12-15 | Cambodia, Malaysia, Laos, Vietnam, Myanmar | Singapore, Indonesia, Thailand, Timor-Leste, Philippines |
| 2021 | AFF Championship | 2021-12-05 s/d 2022-01-01 | Timor-Leste, Thailand, Singapore, Myanmar, Philippines | Cambodia, Malaysia, Laos, Vietnam, Indonesia |
| 2022 | AFF Championship | 2022-12-20 s/d 2023-01-16 | Cambodia, Philippines, Brunei, Indonesia, Thailand | Myanmar, Malaysia, Laos, Vietnam, Singapore |
| 2024 | ASEAN Championship | 2024-12-08 s/d 2025-01-05 | Cambodia, Malaysia, Singapore, Timor-Leste, Thailand | Myanmar, Indonesia, Laos, Vietnam, Philippines |
| 2026 | ASEAN Championship | 2026-07-24 s/d 2026-08-26 | Cambodia, Singapore, Timor-Leste, Indonesia, Vietnam | Myanmar, Malaysia, Laos, Thailand, Philippines |

Setiap edisi:

- 10 tim;
- 2 grup berisi 5 tim;
- 20 laga grup (round-robin satu kali);
- 2 semifinal dan 1 final, masing-masing dua leg = 6 laga knockout;
- total 26 laga.

### 9.3 Model walk-forward per edisi

Untuk setiap edisi, model **dilatih ulang** hanya pada laga sebelum tanggal mulai edisi:

| Edisi | Jumlah laga latih |
|---|---:|
| 2018 | 42.061 |
| 2021 | 44.829 |
| 2022 | 45.827 |
| 2024 | 48.093 |
| 2026 | 49.580 |

Konfigurasi tetap sama: logistic `full_interaksi`, `C=1,0`, `max_iter=2000`. Tidak ada hyperparameter baru yang dicari di Section 9.

Fitur laga turnamen dibekukan pada kondisi **pra-turnamen**:

- Elo, form, dan H2H memakai kondisi sebelum edisi dimulai;
- `rest_days` memakai tanggal fixture aktual;
- hasil simulasi tidak dipakai untuk memperbarui Elo/form/H2H.

Mengapa tidak diperbarui? Karena model tidak menghasilkan skor, sehingga tidak ada cara yang konsisten untuk memperbarui form atau rating di tengah turnamen. Ini simplifikasi yang disengaja.

Untuk setiap edisi, model memprediksi:

- 20 laga grup;
- 540 kemungkinan laga knockout (6 tanggal x 10 tim x 9 lawan).

Jadi ada 560 prediksi probabilitas per edisi. Prediksi untuk semua kemungkinan pasangan diperlukan agar simulasi bisa memainkan bracket apa pun, bukan hanya bracket yang benar-benar terjadi.

### 9.4 Cara satu turnamen diundi

**Langkah 1 - undi hasil laga grup.**

Untuk laga dengan probabilitas misalnya:

```text
p_H = 0,5668
p_D = 0,2630
p_A = 0,1701
```

ambil bilangan acak `u` antara 0 dan 1:

- `u < 0,5668` -> H;
- `0,5668 <= u < 0,8298` -> D;
- `u >= 0,8298` -> A.

Angka 0,8298 adalah `p_H + p_D`. Ini yang disebut **sampling dari distribusi kategorikal**.

**Langkah 2 - hitung poin grup.**

- menang = 3 poin;
- seri = 1 poin;
- kalah = 0 poin.

**Langkah 3 - urutkan grup.**

Urutan memakai:

1. poin;
2. jika poin sama, poin head-to-head di antara tim yang seri;
3. jika masih sama, undian acak.

Tidak ada selisih gol, karena model tidak menghasilkan skor.

**Langkah 4 - knockout dua leg.**

Dua tim teratas tiap grup lolos:

- SF1: A2 vs B1;
- SF2: B2 vs A1;
- leg pertama di kandang A2/B2;
- leg kedua di kandang B1/A1.

Pemenang dua leg ditentukan dari **jumlah kemenangan leg**. Jika satu leg dimenangkan masing-masing tim (atau keduanya seri), pemenang ditentukan adu penalti 50/50.

Final juga dua leg:

- leg pertama di kandang pemenang SF1;
- leg kedua di kandang pemenang SF2.

**Langkah 5 - catat juara.**

Satu simulasi menghasilkan satu juara. Ulangi 10.000 kali. Jika Thailand menjadi juara 3.097 kali:

```text
p_juara(Thailand) = 3.097 / 10.000 = 0,3097 = 30,97%
```

> **Istilah sederhana - Monte Carlo:** metode "coba berkali-kali". Kita tidak menghitung semua kemungkinan turnamen secara matematis; kita mengundi 10.000 turnamen dan melihat frekuensinya.
>
> **Istilah sederhana - Wilson interval:** cara membuat interval kepercayaan untuk proporsi, misalnya 30,97% dengan rentang [30,07%; 31,88%]. Interval ini terutama mengukur **galat sampling** dari 10.000 undian, bukan ketidakpastian model.

### 9.5 Hasil 2026

| Rank | Tim | Juara (dari 10.000) | p_juara | 95% CI Wilson | Finalis | Semifinalis |
|---:|---|---:|---:|---|---:|---:|
| 1 | Thailand | 3.097 | **30,97%** | [30,07%; 31,88%] | 5.242 | 8.401 |
| 2 | Indonesia | 2.734 | **27,34%** | [26,48%; 28,22%] | 4.982 | 8.508 |
| 3 | Vietnam | 2.173 | **21,73%** | [20,93%; 22,55%] | 4.490 | 8.565 |
| 4 | Malaysia | 1.540 | **15,40%** | [14,71%; 16,12%] | 3.477 | 7.329 |
| 5 | Philippines | 271 | 2,71% | [2,41%; 3,05%] | 1.009 | 3.490 |
| 6 | Singapore | 174 | 1,74% | [1,50%; 2,02%] | 643 | 2.328 |
| 7 | Myanmar | 6 | 0,06% | [0,03%; 0,13%] | 82 | 729 |
| 8 | Cambodia | 5 | 0,05% | [0,02%; 0,12%] | 72 | 583 |
| 9 | Laos | 0 | 0,00% | [0,00%; 0,04%] | 1 | 51 |
| 10 | Timor-Leste | 0 | 0,00% | [0,00%; 0,04%] | 2 | 16 |

Vietnam adalah juara aktual 2026, tetapi simulasi menempatkannya di **peringkat tiga** dengan **21,73%**. Ini bukan "kesalahan fatal"; ini menunjukkan bahwa turnamen pendek memang sangat tidak pasti. Model memberi Vietnam peluang yang cukup besar, tetapi bukan yang terbesar.

### 9.6 Backtest lima edisi

| Edisi | Juara aktual | p untuk juara aktual | Rank aktual | Pilihan top simulasi | p top | Top-3 simulasi |
|---|---|---:|---:|---|---:|---|
| 2018 | Vietnam | 28,11% | 2 | Thailand | 44,90% | Thailand, Vietnam, Philippines |
| 2021 | Thailand | 27,00% | 2 | Vietnam | 33,95% | Vietnam, Thailand, Singapore |
| 2022 | Thailand | 38,32% | 1 | Thailand | 38,32% | Thailand, Vietnam, Indonesia |
| 2024 | Vietnam | 10,94% | 4 | Thailand | 38,33% | Thailand, Indonesia, Malaysia |
| 2026 | Vietnam | 21,73% | 3 | Thailand | 30,97% | Thailand, Indonesia, Vietnam |

Ringkasan:

- rata-rata peluang untuk juara aktual: **25,22%**;
- uniform untuk 10 tim: **10%**;
- pilihan teratas tepat: **1 dari 5** edisi;
- juara aktual masuk top-3: **4 dari 5** edisi.

**Cara membaca:** simulasi lebih baik dalam **memberi peluang kepada kandidat** daripada dalam **menunjuk satu juara**. Ia seperti prakiraan cuaca: "kemungkinan hujan 70%" tidak berarti "pasti hujan di rumah Anda", tetapi tetap informatif.

Kegagalan terbesar ada di 2024: Vietnam hanya diberi **10,94%** dan peringkat 4. Model pra-turnamen lebih menyukai Thailand, Indonesia, dan Malaysia. Satu hasil seperti ini cukup untuk membuat rata-rata lima edisi goyah.

### 9.7 Galat Monte Carlo bukan seluruh ketidakpastian

Interval Wilson di tabel hanya mengukur:

- variasi karena kita hanya mengundi 10.000 kali, bukan tak terhingga.

Interval itu **tidak** mengukur:

- ketidakpastian model;
- kesalahan karena fitur dibekukan;
- kesalahan karena tidak ada model skor;
- kesalahan karena format disederhanakan;
- pergeseran kekuatan tim di masa depan.

Karena itu, jangan membaca `[30,07%; 31,88%]` sebagai "kalau diulang di dunia nyata, Thailand pasti juara 30-32%". Itu hanya batas sampling dari simulasi.

---

## 10. Analisis Inti: Mengapa Project Ini Dirancang Seperti Ini

### 10.1 Tiga lapis yang saling mengunci

| Lapis | Keputusan kunci | Akibat jika salah |
|---|---|---|
| Data dan waktu | `match_id`, split temporal, final test dikunci | leakage; skor validasi terlihat bagus tetapi tidak bermakna |
| Model | Elo/form/H2H, baseline, log loss, kalibrasi | model terlihat akurat tetapi probabilitasnya menyesatkan |
| Simulasi | format, bracket, tiebreak, penalti | probabilitas juara tidak mencerminkan turnamen nyata |

Project ini tidak hanya "melatih model". Ia membangun **rantai bukti**: setiap angka harus bisa dilacak kembali ke data dan aturan yang jelas.

### 10.2 Apa yang sebenarnya memberi sinyal?

Dari hasil:

- **Elo** adalah sinyal terkuat yang sederhana. Elo murni sudah mencapai log loss 0,8340 pada 52 laga ASEAN, tidak jauh dari model final 0,8198.
- **Form, H2H, dan konteks** memberi perbaikan kecil di atas Elo. `full_interaksi` hanya sedikit lebih baik daripada baseline logistic (`full`), dan perbaikan itu tidak stabil pada final test.
- **HGB dan ensemble** tidak memberi perbaikan yang stabil pada log loss. Kompleksitas tambahan tidak dibenarkan.
- **Kelas seri** tetap sulit. Model bisa memberi p_D, tetapi tidak selalu tajam.

Kesimpulan teknisnya: **model final bukan lompatan besar; ia adalah versi yang sedikit lebih baik dan dipilih dengan protokol yang ketat.** Nilai project terletak pada kejujuran membandingkan model, bukan pada klaim superioritas.

### 10.3 Rantai lengkap dari data mentah ke 30,97%

```text
1. results.csv
   -> audit, match_id, label H/D/A
   -> 49.945 laga

2. fitur pra-laga
   -> Elo, form, H2H, konteks
   -> 26 kolom per laga

3. model logistic
   -> (p_H, p_D, p_A) untuk setiap laga
   -> contoh 2026: Thailand vs Malaysia = 0,5668 / 0,2630 / 0,1701

4. simulasi satu turnamen
   -> undi hasil grup
   -> hitung poin dan urutan
   -> semifinal dua leg
   -> final dua leg
   -> satu juara

5. ulangi 10.000 kali
   -> hitung berapa kali Thailand juara
   -> 3.097 / 10.000 = 30,97%
```

Itulah arti angka 30,97%: **bukan probabilitas "Thailand pasti juara", melainkan frekuensi Thailand menjadi juara dalam 10.000 turnamen yang diundi menurut model dan asumsi project.**

### 10.4 Bacaan hasil yang benar

1. **Untuk membandingkan kandidat juara**, simulasi berguna: rata-rata 25,22% untuk juara aktual jauh di atas 10% uniform.
2. **Untuk menunjuk satu juara**, simulasi belum andal: pilihan teratas hanya tepat 1 dari 5 edisi.
3. **Untuk klaim "model lebih baik dari Elo"**, belum ada bukti stabil: interval selisih melewati nol.
4. **Untuk klaim kalibrasi sempurna**, belum: ECE classwise final test justru lebih tinggi dari baseline.

### 10.5 Batasan paling penting

- **Label tidak membedakan 90 menit dan perpanjangan waktu.** Skor di data adalah skor akhir; hasil 90 menit tidak tersedia.
- **Adu penalti tidak menjadi label.** Laga yang berakhir seri lalu diselesaikan penalti tetap berlabel D.
- **Tidak ada model skor.** Agregat dua leg tidak dihitung; pemenang dua leg didekati dengan jumlah kemenangan leg dan penalti 50/50.
- **Tidak ada pembaruan di dalam turnamen.** Elo/form/H2H dibekukan sebelum turnamen.
- **Sampel ASEAN kecil.** 52 laga final test dan 26 laga per edisi simulasi; satu hasil bisa mengubah banyak hal.
- **Kalibrasi belum kuat.** Probabilitas juara mewarisi kalibrasi model H/D/A.
- **Interval Monte Carlo bukan interval model.** 10.000 simulasi hanya mengurangi galat sampling, bukan galat spesifikasi.
- **`FIFA ASEAN Cup` tidak dipakai.** Project dibatasi pada AFF/ASEAN Championship.
- **Elo memakai parameter default.** `K=30`, `home_adv=100`, dan pengali gol belum dituning.

### 10.6 Jika project dilanjutkan

1. **Kalibrasi ulang** dengan data validasi terpisah (Platt/isotonic), lalu ukur ECE lagi.
2. **Model skor** (Poisson/Dixon-Coles) agar agregat gol, selisih gol, dan tiebreak grup bisa dimodelkan.
3. **Propagasi ketidakpastian model** ke simulasi: ulangi dengan beberapa model/bootstrap, bukan satu model titik.
4. **Cluster bootstrap** per turnamen/tim dan validasi prospektif pada edisi berikutnya.
5. **Fitur tambahan**: kualitas skuad, cedera, travel, jeda istirahat, venue, motivasi.
6. **Jangan memakai final test yang sama** untuk memilih model dan mengklaim performa.

---

## 11. Cara Mereproduksi

### 11.1 Lingkungan

Project memakai Python 3.10.11 dan dependensi di `requirements.txt`:

```text
pandas==2.3.3
numpy==2.2.6
scipy==1.15.3
scikit-learn==1.7.2
matplotlib==3.10.9
pytest==9.1.1
jupyter==1.1.1
nbconvert==7.17.2
PyYAML==6.0.3
```

Di Windows PowerShell:

```powershell
.\myvenv\Scripts\Activate.ps1
$env:PYTHONIOENCODING="utf-8"
```

### 11.2 Menjalankan uji

```powershell
python -m pytest -q
```

Hasil yang diharapkan: **45 passed**.

### 11.3 Menjalankan notebook dari awal

```powershell
jupyter nbconvert --to notebook --execute --inplace notebooks/asean_cup_prediction.ipynb --ExecutePreprocessor.timeout=1800
```

Notebook akan membangun ulang fitur, tabel, gambar, dan `data/processed/simulation_results.csv`.

### 11.4 Artefak utama

| Artefak | Isi |
|---|---|
| `data/processed/matches_base.csv` | 49.945 x 12; data dasar dengan `match_id` dan label |
| `data/processed/matches_merged.csv` | 49.945 x 15; data dasar + shootout |
| `data/processed/features_dev.csv` | 48.093 x 26; fitur dev |
| `data/processed/split_definition.json` | batas dev/final, 15 fold tahunan, 7 fold ASEAN |
| `data/processed/simulation_results.csv` | 50 baris; 5 edisi x 10 tim |
| `reports/figures/fig_01` sampai `fig_20` | grafik EDA, evaluasi, kalibrasi, simulasi |
| `notebooks/asean_cup_prediction.ipynb` | narasi dan bukti langkah demi langkah |

---

## 12. Glosarium

| Istilah | Penjelasan sederhana |
|---|---|
| **H/D/A** | Home win, Draw, Away win |
| **`match_id`** | nomor identitas unik untuk satu laga |
| **Label** | jawaban yang ingin dipelajari model; di sini H/D/A |
| **Fitur** | informasi masukan untuk model, misalnya Elo dan form |
| **Target** | hal yang diprediksi; di sini hasil H/D/A |
| **Leakage** | informasi masa depan atau informasi terlarang masuk ke model |
| **Split temporal** | membagi data berdasarkan waktu, bukan acak |
| **Walk-forward** | validasi bergerak maju; latih pada masa lalu, uji pada masa depan |
| **Elo** | rating kekuatan tim yang naik/turun setelah tiap laga |
| **Form** | performa beberapa laga terakhir |
| **H2H** | head-to-head; sejarah pertemuan dua tim |
| **Softmax** | mengubah skor menjadi probabilitas yang berjumlah 1 |
| **Regularisasi (C)** | rem agar model tidak terlalu menghafal data latih |
| **Imputasi** | mengisi nilai kosong dengan statistik data latih |
| **One-hot encoding** | mengubah kategori menjadi kolom 0/1 |
| **Log loss** | metrik yang menghukum keyakinan salah; semakin kecil semakin baik |
| **Brier score** | rata-rata kuadrat selisih probabilitas dan hasil |
| **RPS** | metrik error untuk kelas berurutan H < D < A |
| **Akurasi** | persentase tebakan keras yang benar |
| **Macro-F1** | rata-rata F1 per kelas; menjaga kelas minoritas tetap terlihat |
| **Kalibrasi** | kesesuaian antara probabilitas dan frekuensi kenyataan |
| **ECE** | ukuran rata-rata kesalahan kalibrasi |
| **Bootstrap** | resampling untuk mengukur ketidakpastian |
| **Interval kepercayaan** | rentang nilai yang masuk akal untuk estimasi |
| **Monte Carlo** | simulasi berulang dengan angka acak |
| **Wilson interval** | interval kepercayaan untuk proporsi |
| **`p_juara`** | proporsi simulasi tempat tim menjadi juara |
| **Dua leg** | pertandingan kandang-tandang; total dua pertemuan |
| **Agregat** | jumlah skor dari dua leg |
| **Adu penalti** | penentu pemenang setelah skor imbang |
| **Prior** | tebakan berdasarkan frekuensi kelas di data latih |
| **Ensemble** | gabungan beberapa model |
| **HGB** | model pohon bertahap (HistGradientBoosting) |
| **Static features** | fitur yang dibekukan pada kondisi pra-turnamen |

---

## 13. Penutup

Project ini bisa dibaca sebagai tiga pertanyaan berlapis:

1. **Apakah datanya bisa dipercaya?** Jawabannya: sebagian besar ya, dengan satu duplikat yang ditangani secara transparan dan satu file shootout yang hanya dipakai sebagai konteks.
2. **Apakah modelnya lebih baik dari tebakan sederhana?** Jawabannya: jelas lebih baik dari prior, tetapi hanya setara dengan Elo dan logistic baseline; belum ada bukti superioritas yang stabil.
3. **Apakah simulasinya berguna?** Jawabannya: ya, untuk menyusun skenario dan membandingkan kandidat; belum untuk menunjuk juara tunggal dengan yakin.

Nilai utama project ini adalah **rantai metodologisnya**: data mentah -> fitur kausal -> probabilitas -> simulasi -> evaluasi yang jujur. Angka 30,97% bukan ramalan yang berdiri sendiri; ia adalah hasil akhir dari rantai asumsi yang harus dibaca bersama batasannya.
