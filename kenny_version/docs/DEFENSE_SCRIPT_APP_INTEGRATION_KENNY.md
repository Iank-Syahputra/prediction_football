# Naskah Ujian Sidang Resmi: Bagian II — Integrasi Aplikasi & Decision Support Studio

**Presenter**: Kenny Helim (`kenny.helim@binus.ac.id`)  
**Program Studi**: Information System & Management, BINUS University  
**Kelompok**: Kelompok 1 - Divisi Artificial Intelligence (MSIB Batch 10 / Fast Track)  
**Mitra Perusahaan**: PT Vinix Seven Aurum  
**Dosen Pembimbing & Dewan Penguji**: Bapak Aslan Alwi & Bapak Bimo Rizki Abdusshamad  
**Periode Magang**: **4 Bulan (MUTLAK)**  
**Target SDG**: **UN SDG 9 (Industri, Inovasi, dan Infrastruktur Digital)**  
**Berkas Presentasi Utama**: [`FINAL_COMBINED_PRESENTATION_IAN_AND_KENNY.pptx`](file:///C:/Users/Kenny/Desktop/FINAL_COMBINED_PRESENTATION_IAN_AND_KENNY.pptx)  

---

## 📌 Peta Pembagian Peran Presentasi Kelompok 1

| Sesi | Pembicara | Cakupan Materi | Rentang Slide |
| :--- | :--- | :--- | :--- |
| **Bagian I** | **Muhammad Ihram Syahputra** | Fondasi Data FIFA 49.945 Laga, EDA, Temporal Split, Feature Engineering (Elo, Form, H2H), Model Multinomial Logistic, Evaluasi Baseline, & Rantai Bukti Batasan ML | **Slide 1 – 12** |
| **Bagian II** | **Kenny Helim** | **Integrasi Aplikasi & Decision Support Studio (Streamlit 5 Tabs)**: Solusi Skor Poisson (Tab 1), Ingesti CSV Dinamis (Tab 2), Simulasi Monte Carlo Interaktif (Tab 3), Monograf Komparasi vs YOLO11 (Tab 4), Underdog Tactics Lab (Tab 5), Standar QA 42 Unittest, Video Walkthrough, & Kesimpulan SDG 9 | **Slide 13 – 20** |

---

## 🎙️ Momen Transisi / Handoff (Slide 12 ke Slide 13)

### Kalimat Penutup Rekan Tim (Ian):
> *"Demikian pemaparan dari saya mengenai fondasi data historis, rekayasa fitur kausal, hingga mekanika simulasi Monte Carlo. Seperti yang terlihat pada Slide 12, model ML murni kami masih memiliki 3 batasan struktural: belum memiliki tebakan skor akhir, fiturnya statis sebelum turnamen, dan belum menjadi sistem pendukung keputusan yang interaktif.*  
> *Untuk menjelaskan bagaimana seluruh batasan tersebut berhasil kami selesaikan melalui integrasi aplikasi produksi dan antarmuka interaktif, saya persilakan rekan saya, **Kenny Helim**."*

---

## 🗣️ Naskah Presentasi Lengkap Kenny Helim (Slide 13 – 20)

### SLIDE 13: Transisi & Arsitektur Integrasi Sistem Produksi
*(Klik beralih ke Slide 13)*

> *"Terima kasih banyak kepada rekan saya, Ian, atas pemaparan alur Machine Learning yang sangat mendalam dan terstruktur.*  
>  
> *Selamat pagi/siang yang terhormat Bapak Aslan Alwi dan Bapak Bimo Rizki Abdusshamad.*  
>  
> *Melanjutkan apa yang baru saja disampaikan Ian pada Slide 12, kami menyadari bahwa riset Machine Learning tidak boleh hanya berakhir sebagai file kode atau angka probabilitas di dalam Jupyter Notebook. Sebuah model baru memiliki nilai guna nyata apabila berhasil diintegrasikan menjadi **Sistem Pendukung Keputusan (Decision Support System - DSS)** yang mudah digunakan, adaptif terhadap situasi dinamis, dan menjawab kebutuhan pemangku kepentingan di lapangan.*  
>  
> *Pada Slide 13 ini, saya memetakan bagaimana saya membangun arsitektur produksi end-to-end yang secara langsung menuntaskan ketiga batasan yang dipaparkan Ian:*  
> *1. **Batasan 'Tanpa Model Skor'**: Kami tuntaskan dengan mengintegrasikan distribusi Poisson Expected Goals sehingga pengguna mendapatkan estimasi skor riil pertandingan.*  
> *2. **Batasan 'Fitur Statis'**: Kami tuntaskan dengan slider penyesuaian dinamis dan pipeline ingesti data CSV baru tanpa perlu melatih ulang model dari nol.*  
> *3. **Batasan 'Belum Berupa Sistem Keputusan'**: Kami tuntaskan dengan menghadirkan Laboratorium Kontra-Taktik Underdog untuk tim kuda hitam dan federasi nasional di bawah naungan **UN SDG 9**.*  
>  
> *Seluruh sistem ini kami rangkai dalam antarmuka interaktif responsif berbasis Streamlit dengan 5 tab fungsional yang akan saya bedah satu per satu."*

---

### SLIDE 14: Tab 1 — Match Predictor Real-Time & Solusi Model Skor Poisson
*(Klik beralih ke Slide 14)*

> *"Mari kita masuk ke **Tab 1: Match Predictor Real-Time**.*  
>  
> *Bapak Penguji, pada model regresi logistik murni, output yang dihasilkan hanyalah probabilitas diskrit tiga kelas: menang, seri, atau kalah. Namun di dunia nyata, pelatih dan komentator selalu bertanya: 'Berapa perkiraan skor akhirnya?'.*  
>  
> *Di sinilah letak rekayasa integrasi kami. Kami memadukan nilai probabilitas logistik dengan pemodelan **Distribusi Poisson Expected Goals ($\lambda$)**. Nilai lambda gol kandang dan tandang kami hitung secara deterministik dari rata-rata gol historis, diferensial Elo, serta status kandang-tandang.*  
>  
> *Di sisi antarmuka, pelatih dapat memilih tim manapun—misalnya **Indonesia melawan Thailand**—lalu menggeser slider penyesuaian Elo sebesar $\pm 200$ poin. Contohnya: jika Indonesia baru saja diperkuat pemain naturalisasi baru atau tim lawan kehilangan striker utama karena cedera, pelatih cukup menggeser slider tersebut. Sistem secara cerdas akan langsung menghitung ulang probabilitas dan ekspektasi skor (misal: 2-1 atau 1-1) dalam hitungan milidetik secara real-time.*  
>  
> *Pengguna juga dapat mencentang lokasi netral, yang secara matematis akan langsung mencabut bobot Home Advantage sebesar 100 poin Elo."*

---

### SLIDE 15: Tab 2 — Ingesti Data Dinamis & Rekalibrasi Elo Tanpa Retrain
*(Klik beralih ke Slide 15)*

> *"Selanjutnya, mari kita bedah solusi untuk batasan kedua pada **Tab 2: Ingesti Data Dinamis**.*  
>  
> *Di industri olahraga, turnamen seperti Piala AFF bergulir selama hampir satu bulan. Jika sebuah model hanya mengandalkan data statis pra-turnamen, maka model tersebut akan mengalami degradasi relevansi setiap kali sebuah pertandingan fase grup selesai.*  
>  
> *Masalahnya, melatih ulang (re-train) model machine learning berskala 49.000 data setiap selesai laga adalah proses yang mahal dan lambat. Oleh karena itu, saya merancang **Dynamic Ingestion Engine**.*  
>  
> *Analis federasi cukup mengunggah berkas CSV yang berisi hasil pertandingan terkini. Sistem kami memiliki 4 lapisan pengamanan:*  
> *1. Memvalidasi skema berkas secara otomatis untuk menolak data korup atau skor non-numerik.*  
> *2. Mengurutkan pertandingan secara kronologis ketat demi memastikan **zero data leakage**.*  
> *3. Mesin Elo Engine kami secara instan menghitung delta perolehan poin dan memperbarui ranking tim di memori sesi aktif.*  
> *4. Kami menyediakan template CSV standar yang dapat diunduh langsung hanya dengan satu klik.*  
>  
> *Hasilnya, seluruh prediksi di Tab 1 dan Tab 3 langsung terbarukan secara otomatis tanpa downtime dan tanpa biaya komputasi tambahan."*

---

### SLIDE 16: Tab 3 — Simulasi Turnamen Monte Carlo Interaktif (10.000 Iterasi)
*(Klik beralih ke Slide 16)*

> *"Pada **Tab 3: Simulasi Turnamen Monte Carlo Interaktif**, kami membawa simulasi 10.000 iterasi yang tadi dijelaskan oleh Ian dari lingkungan terminal langsung ke hadapan pengguna dalam bentuk antarmuka visual yang interaktif.*  
>  
> *Pengguna cukup menekan tombol 'Jalankan Simulasi Monte Carlo', dan sistem akan memproses 10.000 siklus turnamen penuh dalam waktu kurang dari 2 detik. Kecepatan ini dapat tercapai karena kami melakukan pre-computing dan caching terhadap 180 kombinasi probabilitas antar-tim ASEAN di memori.*  
>  
> *Sistem memodelkan aturan resmi Piala AFF secara presisi: babak penyisihan Grup A dan B, disusul semifinal dua leg, dan grand final dua leg dengan agregat gol. Jika terjadi skor agregat imbang, sistem mengeksekusi simulasi adu penalti deterministik.*  
>  
> *Sebagaimana terlihat pada bagan dan tabel aplikasi kami, probabilitas juara Big 4 terbukti sangat stabil pada interval kepercayaan 95%: **Thailand memimpin dengan 30.80%**, disusul **Indonesia 27.22%**, **Vietnam 23.88%**, dan **Malaysia 15.56%**, sedangkan kelompok tim kuda hitam memegang peluang kumulatif sekitar 2.54%. Pengguna bahkan dapat melihat rincian peluang lolos semifinal maupun partai puncak bagi seluruh peserta."*

---

### SLIDE 17: Tab 4 — Evaluasi 52 Laga AFF & Monograf Komparasi vs YOLO11
*(Klik beralih ke Slide 17)*

> *"Beralih ke **Tab 4: Evaluasi Model dan Komparasi Ilmiah vs YOLO11**.*  
>  
> *Pada tab ini kami menampilkan dua hal fundamental: integritas metrik evaluasi dan kajian paradigma ilmiah.*  
>  
> *Pertama, mengenai integritas pengujian. Model kami diuji secara ketat pada 52 pertandingan resmi AFF Championship periode 2021 hingga 2023 di masa depan (out-of-time test). Hasilnya sangat memuaskan: model kami mencatatkan **Log Loss 0.5966**, jauh melampaui target ambang batas kelayakan $\le 0.8198$ dan mengalahkan Naive Baseline di angka 1.0686. Akurasi klasifikasinya mencapai **75.00%** (39 dari 52 laga benar), dengan Brier Score terkalibrasi di 0.3331.*  
>  
> *Kedua, kami menyusun monograf ilmiah untuk menjawab pertanyaan yang sering diajukan penguji: 'Mengapa memilih Tabular Decision Support System dan bukan Computer Vision seperti YOLO11?'.*  
> *Di sini kami membuktikan secara akademik bahwa arsitektur YOLO11 ditujukan untuk pelacakan spasial pemain dan bola per frame selama 90 menit pertandingan berjalan. YOLO11 membutuhkan GPU berdaya tinggi dan data video eksklusif, namun secara fundamental **tidak dapat meramalkan hasil sebelum kickoff dimulai**.*  
> *Sebaliknya, Tabular DSS kami sangat efisien energi (cukup berjalan di laptop biasa), memodelkan kekuatan tim lintas dekade, dan secara langsung menghasilkan nilai probabilitas strategis yang dibutuhkan oleh pengambil keputusan olahraga."*

---

### SLIDE 18: Tab 5 — Target Penerima Manfaat & Playbook Kontra-Taktik (SDG 9)
*(Klik beralih ke Slide 18)*

> *"Bapak Penguji, inilah puncak dari seluruh rekayasa sistem kami pada **Tab 5: Target Penerima Manfaat dan Laboratorium Kontra-Taktik Underdog**, yang menjadi pilar perwujudan **UN SDG 9 (Inovasi dan Infrastruktur Digital Terbuka)**.*  
>  
> *Layanan analitik sepak bola papan atas dunia saat ini dimonopoli oleh vendor komersial berbiaya miliaran rupiah seperti Opta atau StatsBomb, sehingga hanya dapat dinikmati oleh klub-klub kaya di Eropa. Melalui sistem terbuka ini, kami memberikan dampak nyata bagi 3 penerima manfaat:*  
>  
> *1. **Tim Kuda Hitam (*Underdogs*) seperti Kamboja, Laos, Myanmar, dan Timor-Leste**: Pelatih mereka dapat menggunakan Laboratorium Taktik kami untuk menguji strategi pertahanan. Dengan menggeser slider 'Low Block Defense', sistem membuktikan secara matematis bahwa taktik pertahanan rapat mampu meningkatkan peluang mengamankan poin seri sebesar **+14.2%** saat menghadapi tim raksasa seperti Thailand.*  
> *2. **Federasi Nasional seperti PSSI**: Membantu staf kepelatihan dalam merencanakan rotasi pemain inti pada laga penyisihan grup berisiko rendah agar stamina pemain terjaga di semifinal, serta memilih lawan uji coba internasional resmi yang paling optimal mendongkrak ranking FIFA.*  
> *3. **Media dan Broadcaster Olahraga**: Memanfaatkan Upset Probability Index untuk merancang liputan pertandingan yang lebih menarik dan berbasis data ilmiah.*"

---

### SLIDE 19: Standar Rekayasa Perangkat Lunak, Pengujian Otomatis & Video Demo
*(Klik beralih ke Slide 19)*

> *"Sebagai mahasiswa Information System & Management di BINUS University, saya memastikan bahwa produk ini dibangun mengikuti standar rekayasa perangkat lunak profesional tertinggi:*  
>  
> *1. **42 Real Unittests Passing (100% Lulus)**: Seluruh modul dilindungi oleh rangkaian pengujian unit otomatis—mulai dari inferensi model, integritas mesin Elo, penanganan data out-of-vocabulary, hingga adversarial stress test dengan pergeseran Elo ekstrem $\pm 10.000$ poin. Seluruh pengujian lulus dalam waktu 3,2 detik tanpa kegagalan.*  
> *2. **Video Walkthrough Full HD (30 FPS)**: Kami telah merekam demonstrasi penelusuran kelima tab secara otomatis menggunakan robot browser Playwright Chromium dan FFmpeg (`DEMO_STREAMLIT_APP_FULL_WALKTHROUGH.mp4`, 3.0 MB) yang siap diputar secara offline saat dibutuhkan.*  
> *3. **Integritas Repositori GitHub**: Seluruh 112 berkas kode, model, naskah presentasi, dan batch runner telah terunggah resmi di GitHub pada branch `main` repositori `Iank-Syahputra/prediction_football` di dalam folder mandiri `kenny_version/` tanpa merusak berkas rekan tim."*

---

### SLIDE 20: Kesimpulan, Penutup & Sesi Tanya Jawab (Closing & Q&A)
*(Klik beralih ke Slide 20)*

> *"Sebagai kesimpulan akhir dari Kelompok 1 Divisi Artificial Intelligence:*  
>  
> *Proyek ini berhasil membuktikan bahwa riset Machine Learning dan pemodelan probabilitas dapat dijembatani secara elegan menjadi produk perangkat lunak nyata yang siap pakai, transparan, terkalibrasi ilmiah, dan inklusif di bawah naungan **UN SDG 9**.*  
>  
> *Saya, **Kenny Helim** dari BINUS University, bersama rekan saya **Muhammad Ihram Syahputra**, telah menyelesaikan seluruh tanggung jawab dan persyaratan Tugas Akhir Magang Bersertifikat Kampus Merdeka (MSIB Batch 10) dengan durasi **4 Bulan (MUTLAK)** di **PT Vinix Seven Aurum**.*  
>  
> *Kami mengucapkan terima kasih yang sebesar-besarnya kepada Bapak Dosen Pembimbing dan Dewan Penguji, **Bapak Aslan Alwi** dan **Bapak Bimo Rizki Abdusshamad**, atas seluruh bimbingan, arahan metodologis, dan masukan berharga yang telah diberikan selama masa magang.*  
>  
> *Demikian presentasi dari Kelompok 1. Kami membuka sesi tanya jawab dan dengan senang hati menyambut pertanyaan, tanggapan, serta diskusi mendalam dari Dewan Penguji. Terima kasih."*

---

## 🛡️ Panduan Menjawab Pertanyaan Dosen Penguji (Cheat Sheet)

### Pertanyaan 1: *"Mengapa menggunakan pemodelan Poisson untuk memprediksi skor di Tab 1, bukan Linear Regression?"*
> **Jawaban Kenny**:  
> *"Gol dalam sepak bola adalah data pencacahan diskrit non-negatif ($0, 1, 2, ...$) yang jarang terjadi (*rare discrete events*), bukan data kontinu. Regresi linear dapat menghasilkan nilai negatif (misal: $-0.5$ gol) atau desimal yang tidak bermakna di lapangan. Distribusi Poisson adalah standar baku pemodelan gol internasional (sebagaimana metode Dixon & Coles) karena memetakan laju kedatangan gol ($\lambda$) secara alami dengan varians yang sebanding dengan rata-ratanya."*

### Pertanyaan 2: *"Bagaimana Anda menjamin tidak terjadi kebocoran data (data leakage) saat pengguna mengunggah CSV baru di Tab 2?"*
> **Jawaban Kenny**:  
> *"Pada fungsi `process_uploaded_csv`, data yang diunggah terlebih dahulu disortir secara kronologis ketat berdasarkan tanggal (`df.sort_values(by='date')`). Perhitungan selisih Elo dan pembaruan statistik gol dilakukan secara iteratif baris demi baris hanya menggunakan data sebelum pertandingan tersebut dimainkan. Informasi pasca-pertandingan hanya dipakai untuk memperbarui rating bagi laga-laga berikutnya di masa depan, persis seperti aliran waktu di dunia nyata."*

### Pertanyaan 3: *"Mengapa simulasi Monte Carlo di Tab 3 dijalankan 10.000 kali? Apakah 1.000 kali tidak cukup?"*
> **Jawaban Kenny**:  
> *"Kami telah mengujinya dalam `adversarial_stress_test.py` dengan 5 seed acak berbeda. Pada 1.000 iterasi, margin of error untuk tim dengan peluang kecil (seperti Kamboja atau Laos yang memiliki peluang $\approx 0.5\%$) masih terlalu besar secara statistik. Pada 10.000 iterasi, Central Limit Theorem menjamin bahwa estimasi probabilitas stabil dengan simpangan baku di bawah $1.5\%$ dan hierarki Big 4 konsisten $100\%$ di setiap pengujian."*

### Pertanyaan 4: *"Apa keunggulan sistem Anda dibandingkan sistem komersial seperti Opta atau model Computer Vision YOLO11?"*
> **Jawaban Kenny**:  
> *"Pertama, sistem komersial Opta bersifat tertutup dan berbiaya sangat mahal, sementara sistem kami mendukung SDG 9 dengan akses terbuka dan demokratis. Kedua, YOLO11 hanya melacak koordinat spasial 22 pemain di layar selama 90 menit pertandingan, namun tidak bisa memberikan prediksi sebelum pertandingan dimulai. Sistem Tabular Decision Support kami memodelkan sejarah performa 49.945 pertandingan lintas dekade dengan komputasi sangat ringan di laptop standar."*
