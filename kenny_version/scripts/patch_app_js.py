import os

app_js_path = r"C:\Users\Kenny\.gemini\antigravity-ide\scratch\school_football_prediction\app\static\app.js"

with open(app_js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# Revised 11 Slides Array
revised_slides = '''const SLIDES = [
    {
        num: "01 / 11",
        title: "Panduan Metodologi: Dari Data Mentah ke Probabilitas Juara",
        subtitle: "Membedah Mesin Prediksi ASEAN Cup: Menghitung Peluang Secara Transparan Tanpa Ilusi Kepastian",
        body: `
            <div style="background:rgba(2,132,199,0.1); border-left:4px solid #0284c7; padding:16px; border-radius:6px; margin-bottom:16px;">
                <strong>FAST TRACK MSIB BATCH 10 (DIVISI ARTIFICIAL INTELLIGENCE)</strong><br/>
                PT Vinix Seven Aurum • SDG 9: Industri, Inovasi, dan Infrastruktur Digital
            </div>
            <p><strong>Kelompok 1 (AI Football Prediction):</strong></p>
            <ul>
                <li>Kenny Helim (BINUS University - Information System and Management)</li>
                <li>Arya Wicaksana (Universitas Esa Unggul - Teknik Informatika)</li>
                <li>Muhammad Ihram Syahputra (Universitas Halu Oleo - Ilmu Komputer)</li>
                <li>Gisela Venska Millennia (President University - Information System)</li>
                <li>Christian (BINUS University - Information Systems)</li>
            </ul>
            <p style="margin-top:12px; color:#94a3b8;"><strong>Dosen & Mentor Pembimbing:</strong> Pak Aslan Alwi & Bimo Rizki Abdusshamad</p>
        `,
        notes: "Slide pembuka: Menegaskan identitas kelompok 1, pembimbing, dan SDG 9."
    },
    {
        num: "02 / 11",
        title: "Rantai Probabilitas: Mengubah Sejarah Menjadi Peluang",
        subtitle: "Inti Proyek: Bukan Sekadar Menebak Siapa Juara, Melainkan Membangun Rantai Logika Virtual",
        body: `
            <p>Analisis olahraga konvensional seringkali bias opini subjektif fans. Sistem kami membangun 5 rantai logika objektif:</p>
            <div style="display:grid; grid-template-columns:repeat(5, 1fr); gap:10px; margin:20px 0; text-align:center;">
                <div style="background:rgba(2,132,199,0.15); border:1px solid #0284c7; border-radius:8px; padding:12px;">
                    <div style="font-size:1.4rem;">📜</div>
                    <strong style="font-size:0.85rem; color:#38bdf8;">1. Sejarah Laga</strong>
                    <p style="font-size:0.75rem; color:#cbd5e1;">49.945 Laga Masa Lalu</p>
                </div>
                <div style="background:rgba(6,182,212,0.15); border:1px solid #06b6d4; border-radius:8px; padding:12px;">
                    <div style="font-size:1.4rem;">⚙️</div>
                    <strong style="font-size:0.85rem; color:#22d3ee;">2. Fitur Pra-Laga</strong>
                    <p style="font-size:0.75rem; color:#cbd5e1;">Elo, Form, & H2H</p>
                </div>
                <div style="background:rgba(16,185,129,0.15); border:1px solid #10b981; border-radius:8px; padding:12px;">
                    <div style="font-size:1.4rem;">📈</div>
                    <strong style="font-size:0.85rem; color:#34d399;">3. Probabilitas Laga</strong>
                    <p style="font-size:0.75rem; color:#cbd5e1;">P(Win), P(Draw), P(Loss)</p>
                </div>
                <div style="background:rgba(249,115,22,0.15); border:1px solid #f97316; border-radius:8px; padding:12px;">
                    <div style="font-size:1.4rem;">🎲</div>
                    <strong style="font-size:0.85rem; color:#fb923c;">4. 10.000 Simulasi</strong>
                    <p style="font-size:0.75rem; color:#cbd5e1;">Mesin Monte Carlo</p>
                </div>
                <div style="background:rgba(168,85,247,0.15); border:1px solid #a855f7; border-radius:8px; padding:12px;">
                    <div style="font-size:1.4rem;">🏆</div>
                    <strong style="font-size:0.85rem; color:#c084fc;">5. Probabilitas Juara</strong>
                    <p style="font-size:0.75rem; color:#cbd5e1;">Frekuensi Angkat Trofi</p>
                </div>
            </div>
        `,
        notes: "Menjelaskan rantai logika probabilistik dari data mentah hingga proyeksi turnamen."
    },
    {
        num: "03 / 11",
        title: "Langkah 1: Bahan Baku & Aturan Besi 'Tanpa Mesin Waktu'",
        subtitle: "Disiplin Ketat Pencegahan Data Leakage dengan Batas Waktu 2024-12-08",
        body: `
            <div style="background:rgba(239,68,68,0.1); border-left:4px solid #ef4444; padding:14px; border-radius:6px; margin-bottom:16px;">
                <strong>🔒 Aturan Besi Anti Data Leakage:</strong> Model dilarang keras melihat masa depan.
            </div>
            <ul>
                <li><strong>Cut-Off Waktu Kunci (2024-12-08):</strong> 48.093 pertandingan resmi sebelum 8 Desember 2024 dialokasikan murni untuk kalibrasi masa lalu.</li>
                <li><strong>Kunci Adu Penalti:</strong> Data adu penalti (shootouts) dikunci dan tidak dijadikan fitur agar model tidak 'menyontek' hasil akhir sebelum laga berjalan.</li>
                <li><strong>Final Test Set:</strong> 52 pertandingan kompetisi ASEAN Championship aktual dievaluasi secara out-of-time murni.</li>
            </ul>
        `,
        notes: "Menjawab kaidah validasi ilmiah: model tidak boleh mengalami kebocoran data."
    },
    {
        num: "04 / 11",
        title: "Langkah 2: Meracik Sinyal Pra-Laga (Anatomy of a Match)",
        subtitle: "Empat Pilar Informasi Murni yang Dikunci Sebelum Peluit Pertandingan Dimulai",
        body: `
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px; margin:16px 0;">
                <div style="background:rgba(15,23,42,0.8); border:1px solid #38bdf8; border-radius:8px; padding:14px;">
                    <strong style="color:#38bdf8;">1. Kekuatan (Elo Dynamic Rating):</strong>
                    <p style="font-size:0.82rem; color:#cbd5e1; margin-top:6px;">Rating dinamis yang naik saat menang melawan tim berbobot tinggi dan turun saat kalah. Menjadi jangkar utama kekuatan tim.</p>
                </div>
                <div style="background:rgba(15,23,42,0.8); border:1px solid #34d399; border-radius:8px; padding:14px;">
                    <strong style="color:#34d399;">2. Momentum (Rolling Form 5 Laga):</strong>
                    <p style="font-size:0.82rem; color:#cbd5e1; margin-top:6px;">Rata-rata poin per laga dan rata-rata selisih gol (GD) dari 5 pertandingan terakhir menjelang turnamen.</p>
                </div>
                <div style="background:rgba(15,23,42,0.8); border:1px solid #fb923c; border-radius:8px; padding:14px;">
                    <strong style="color:#fb923c;">3. Sejarah (Head-to-Head):</strong>
                    <p style="font-size:0.82rem; color:#cbd5e1; margin-top:6px;">Rekor pertemuan langsung spesifik kedua negara dan rasio kemenangan pertemuan sebelumnya.</p>
                </div>
                <div style="background:rgba(15,23,42,0.8); border:1px solid #a855f7; border-radius:8px; padding:14px;">
                    <strong style="color:#a855f7;">4. Konteks Laga:</strong>
                    <p style="font-size:0.82rem; color:#cbd5e1; margin-top:6px;">Apakah laga dimainkan di kandang asli atau venue netral (runtuhnya home advantage pada lapangan netral).</p>
                </div>
            </div>
        `,
        notes: "Menjelaskan 4 pilar fitur pra-laga yang tidak diperbarui di tengah laga."
    },
    {
        num: "05 / 11",
        title: "Langkah 3: Uji Kejujuran Model di Laga Final",
        subtitle: "Metrik Multi-Class Log Loss pada 52 Laga Kompetisi ASEAN",
        body: `
            <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:16px; margin:20px 0; text-align:center;">
                <div style="background:rgba(239,68,68,0.15); border:2px solid #ef4444; border-radius:10px; padding:20px;">
                    <div style="color:#ef4444; font-size:0.85rem; font-weight:700;">Tebakan Buta (Prior)</div>
                    <div style="font-size:2rem; font-weight:800; color:#fff; margin:10px 0;">1.0686 ❌</div>
                    <p style="font-size:0.75rem; color:#fca5a5;">Hanya menebak frekuensi tanpa mengenal lawan.</p>
                </div>
                <div style="background:rgba(245,158,11,0.15); border:2px solid #f59e0b; border-radius:10px; padding:20px;">
                    <div style="color:#f59e0b; font-size:0.85rem; font-weight:700;">Faktor Tunggal (Elo Murni)</div>
                    <div style="font-size:2rem; font-weight:800; color:#fff; margin:10px 0;">0.8340 ➖</div>
                    <p style="font-size:0.75rem; color:#fde68a;">Memangkas log loss secara drastis.</p>
                </div>
                <div style="background:rgba(16,185,129,0.15); border:2px solid #10b981; border-radius:10px; padding:20px;">
                    <div style="color:#10b981; font-size:0.85rem; font-weight:700;">Model Final (Logistic Full Interaksi)</div>
                    <div style="font-size:2rem; font-weight:800; color:#10b981; margin:10px 0;">0.8198 ✔️</div>
                    <p style="font-size:0.75rem; color:#a7f3d0;">Skor terbaik, solid, dan terkalibrasi.</p>
                </div>
            </div>
            <p style="font-size:0.85rem; color:#cbd5e1;"><strong>Kesimpulan Jujur:</strong> Fitur tambahan memberi keunggulan tipis, namun sinyal terkuat tetap berasal dari kekuatan murni (Elo). Model akhir terbukti mengalahkan tebakan buta secara signifikan.</p>
        `,
        notes: "Menunjukkan pembuktian kuantitatif Log Loss 0.8198."
    },
    {
        num: "06 / 11",
        title: "Mengapa Menjual Probabilitas, Bukan Kepastian?",
        subtitle: "Menolak Akurasi Biner Semu Demi Proyeksi Risiko yang Ilmiah",
        body: `
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px; margin:20px 0;">
                <div style="background:rgba(239,68,68,0.1); border:1px solid #ef4444; border-radius:8px; padding:16px;">
                    <strong style="color:#ef4444;">❌ Akurasi Semu: 'Tim A Pasti Menang!'</strong>
                    <p style="font-size:0.82rem; color:#cbd5e1; margin-top:8px;">Sepak bola modern penuh dengan hasil seri (22.7%) dan laga netral. Model deterministik yang sangat yakin tapi salah akan menuai kerugian fatal dalam dunia nyata.</p>
                </div>
                <div style="background:rgba(16,185,129,0.1); border:1px solid #10b981; border-radius:8px; padding:16px;">
                    <strong style="color:#10b981;">✔️ Probabilitas: 'Menang 70%, Seri 20%, Kalah 10%'</strong>
                    <p style="font-size:0.82rem; color:#cbd5e1; margin-top:8px;">Metrik Log Loss menghukum keras model yang overconfident. Angka 0.30 berarti skenario terjadi 30 kali dari 100, bukan kekalahan mutlak. Ini adalah dasar sains keputusan manajemen risiko.</p>
                </div>
            </div>
        `,
        notes: "Menjelaskan filosofi probabilitas vs kepastian palsu."
    },
    {
        num: "07 / 11",
        title: "Langkah 4: Mesin Monte Carlo (10.000 Putaran)",
        subtitle: "Mengundi Jalannya Turnamen Virtual Lengkap Termasuk Fase Grup & Babak Gugur",
        body: `
            <p>Model dasar memprediksi satu laga. Untuk mencari probabilitas juara, kami mengundi hasil laga, menyusun klasemen grup, dan menjalankan turnamen sebanyak 10.000 kali per edisi.</p>
            <div style="background:rgba(15,23,42,0.8); border:1px solid #f97316; border-radius:8px; padding:16px; margin:16px 0;">
                <strong style="color:#fb923c;">Mekanisme Undian Turnamen (Dice Roll):</strong>
                <p style="font-size:0.85rem; color:#cbd5e1; margin-top:6px;">Contoh Laga: <strong>Thailand vs Malaysia</strong> (Win 56.68% | Draw 26.30% | Lose 17.01%). Pemenang undian melaju ke semifinal dan final. Total frekuensi juara dari 10.000 simulasi menjadi estimasi peluang juara nyata.</p>
            </div>
        `,
        notes: "Menerangkan mekanisme stochastic simulation 10.000 run."
    },
    {
        num: "08 / 11",
        title: "Hasil Simulasi ASEAN Championship 2026",
        subtitle: "Peta Kekuatan Probabilitas Juara Berdasarkan Kondisi Pra-Turnamen",
        body: `
            <div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:14px; margin:20px 0; text-align:center;">
                <div style="background:rgba(249,115,22,0.15); border:2px solid #f97316; border-radius:10px; padding:16px;">
                    <div style="font-weight:700; color:#fff;">1. Thailand</div>
                    <div style="font-size:1.8rem; font-weight:800; color:#f97316; margin:8px 0;">30.97%</div>
                    <div style="font-size:0.75rem; color:#94a3b8;">[30.07% - 31.88%]</div>
                    <div style="font-size:0.8rem; color:#cbd5e1; margin-top:6px;">Juara 3.097 Kali</div>
                </div>
                <div style="background:rgba(16,185,129,0.15); border:2px solid #10b981; border-radius:10px; padding:16px;">
                    <div style="font-weight:700; color:#fff;">2. Indonesia</div>
                    <div style="font-size:1.8rem; font-weight:800; color:#10b981; margin:8px 0;">27.34%</div>
                    <div style="font-size:0.75rem; color:#94a3b8;">[26.48% - 28.22%]</div>
                    <div style="font-size:0.8rem; color:#cbd5e1; margin-top:6px;">Juara 2.734 Kali</div>
                </div>
                <div style="background:rgba(6,182,212,0.15); border:2px solid #06b6d4; border-radius:10px; padding:16px;">
                    <div style="font-weight:700; color:#fff;">3. Vietnam</div>
                    <div style="font-size:1.8rem; font-weight:800; color:#06b6d4; margin:8px 0;">21.73%</div>
                    <div style="font-size:0.75rem; color:#94a3b8;">[20.93% - 22.55%]</div>
                    <div style="font-size:0.8rem; color:#cbd5e1; margin-top:6px;">Juara 2.173 Kali</div>
                </div>
                <div style="background:rgba(59,130,246,0.15); border:2px solid #3b82f6; border-radius:10px; padding:16px;">
                    <div style="font-weight:700; color:#fff;">4. Malaysia</div>
                    <div style="font-size:1.8rem; font-weight:800; color:#3b82f6; margin:8px 0;">15.40%</div>
                    <div style="font-size:0.75rem; color:#94a3b8;">[14.71% - 16.12%]</div>
                    <div style="font-size:0.8rem; color:#cbd5e1; margin-top:6px;">Juara 1.540 Kali</div>
                </div>
            </div>
        `,
        notes: "Menyajikan hasil simulasi Monte Carlo turnamen 2026."
    },
    {
        num: "09 / 11",
        title: "Uji Coba Masa Lalu (Backtest Validasi)",
        subtitle: "Membuktikan Akurasi Model pada 5 Edisi Turnamen ASEAN Masa Lalu",
        body: `
            <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:16px; margin:20px 0; text-align:center;">
                <div style="background:rgba(2,132,199,0.1); border:1px solid #0284c7; border-radius:8px; padding:16px;">
                    <h3 style="color:#38bdf8; font-size:1.6rem; margin-bottom:4px;">1 dari 5</h3>
                    <p style="font-size:0.8rem; color:#cbd5e1;">Pilihan simulasi nomor 1 benar-benar keluar sebagai juara aktual.</p>
                </div>
                <div style="background:rgba(16,185,129,0.1); border:1px solid #10b981; border-radius:8px; padding:16px;">
                    <h3 style="color:#34d399; font-size:1.6rem; margin-bottom:4px;">4 dari 5</h3>
                    <p style="font-size:0.8rem; color:#cbd5e1;">Juara aktual selalu berada di Top-3 simulasi (kecuali anomali 2024).</p>
                </div>
                <div style="background:rgba(249,115,22,0.1); border:1px solid #f97316; border-radius:8px; padding:16px;">
                    <h3 style="color:#fb923c; font-size:1.6rem; margin-bottom:4px;">25.22%</h3>
                    <p style="font-size:0.8rem; color:#cbd5e1;">Rata-rata peluang yang diberikan simulasi kepada tim juara nyata (jauh di atas tebakan acak 10%).</p>
                </div>
            </div>
        `,
        notes: "Membuktikan validasi empiris masa lalu."
    },
    {
        num: "10 / 11",
        title: "Tiga Lapis Kepercayaan & Arsitektur AI (vs YOLO11)",
        subtitle: "Integritas Metodologi & Komparasi Pendekatan Artificial Intelligence",
        body: `
            <div style="background:rgba(15,23,42,0.8); border:1px solid #10b981; border-radius:8px; padding:14px; margin-bottom:14px;">
                <strong style="color:#10b981;">🛡️ The Trust Triad (Tiga Lapis Kepercayaan):</strong>
                <p style="font-size:0.8rem; color:#cbd5e1; margin-top:4px;">1. Data & Waktu (Zero Leakage, cutoff 2024-12-08) • 2. Model (Terkalibrasi Log Loss 0.8198) • 3. Simulasi (Monte Carlo 10.000 iterasi dengan regulasi tiebreak resmi).</p>
            </div>
            <div style="background:rgba(15,23,42,0.8); border:1px solid #0284c7; border-radius:8px; padding:14px;">
                <strong style="color:#38bdf8;">🧠 Komparasi Arsitektur AI (Sepak Bola vs YOLO11):</strong>
                <p style="font-size:0.8rem; color:#cbd5e1; margin-top:4px;">Jika kelompok aspal jalanan menggunakan <strong>YOLO11 Computer Vision</strong> untuk mencari koordinat piksel bounding box cacat jalan, kelompok kami menggunakan <strong>Logistic Full Interaction + Stochastic Monte Carlo</strong> untuk memetakan koordinat probabilitas dan variansi olahraga non-linear.</p>
            </div>
        `,
        notes: "Membahas Trust Triad dan perbandingan dengan model computer vision YOLO11."
    },
    {
        num: "11 / 11",
        title: "Pihak Terbantu, Batasan Transparan, & Sidang Akhir",
        subtitle: "Memenuhi Mandat Mentoring Week 4 Pak Aslan Menuju Sidang 2 - 6 November 2026",
        body: `
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px; margin:16px 0;">
                <div style="background:rgba(245,158,11,0.1); border:1px solid #f59e0b; border-radius:8px; padding:14px;">
                    <strong style="color:#fbbf24;">🎯 Pihak yang Paling Terbantu (Mandat Week 4):</strong>
                    <ul style="font-size:0.8rem; color:#cbd5e1; margin-top:6px;">
                        <li><strong>Tim Liga & Timnas Underdogs:</strong> Mengetahui celah riil kekuatan lawan dan merancang taktik perlawanan baru sebelum turnamen.</li>
                        <li><strong>Federasi Nasional:</strong> Alokasi pemusatan latihan & jadwal uji coba berbasis Elo.</li>
                    </ul>
                </div>
                <div style="background:rgba(2,132,199,0.1); border:1px solid #0284c7; border-radius:8px; padding:14px;">
                    <strong style="color:#38bdf8;">🚀 Batasan & Evolusi Berikutnya:</strong>
                    <ul style="font-size:0.8rem; color:#cbd5e1; margin-top:6px;">
                        <li>Prediksi skor spesifik (Poisson Distribution).</li>
                        <li>Penyertaan data cedera pemain dan rotasi kedalaman skuad.</li>
                        <li><strong>Jadwal Sidang Akhir:</strong> Siap dipresentasikan pada 2 - 6 November 2026.</li>
                    </ul>
                </div>
            </div>
        `,
        notes: "Slide penutup: Menjawab pihak terbantu, limitasi, dan kesiapan sidang akhir."
    }
];'''

# Replace SLIDES array
start_marker = "const SLIDES = ["
end_marker = "];\n\nfunction showSlide("

idx_start = js.find(start_marker)
idx_end = js.find(end_marker)

if idx_start != -1 and idx_end != -1:
    js = js[:idx_start] + revised_slides + js[idx_end + 2:]
    print("Replaced SLIDES array with revised 11 slides!")

# Add dynamic adaptation functions to app.js
dynamic_js = '''
// ==============================================================================
// DYNAMIC ADAPTABILITY FUNCTIONS
// ==============================================================================

async function loadDynamicAdaptTeams() {
    try {
        const res = await fetch("/api/teams");
        const data = await res.json();
        
        const hSelect = document.getElementById("adaptHomeTeam");
        const aSelect = document.getElementById("adaptAwayTeam");
        const pSelect = document.getElementById("paramTeamSelect");
        
        if (!hSelect || !aSelect || !pSelect) return;
        
        hSelect.innerHTML = "";
        aSelect.innerHTML = "";
        pSelect.innerHTML = "";
        
        data.all_teams.forEach(t => {
            hSelect.appendChild(new Option(t, t));
            aSelect.appendChild(new Option(t, t));
            pSelect.appendChild(new Option(t, t));
        });
        
        if (data.all_teams.includes("Indonesia")) hSelect.value = "Indonesia";
        if (data.all_teams.includes("Thailand")) aSelect.value = "Thailand";
        if (data.all_teams.includes("Indonesia")) pSelect.value = "Indonesia";
        
        loadTeamParamsToEdit();
    } catch(e) {
        console.error("Error loading dynamic adapt teams:", e);
    }
}

async function loadTeamParamsToEdit() {
    const pSelect = document.getElementById("paramTeamSelect");
    if (!pSelect) return;
    const team = pSelect.value;
    
    try {
        const res = await fetch("/api/teams");
        const data = await res.json();
        const stats = data.team_stats[team] || {
            win_rate: 0.35, recent_pts_5: 6, avg_goals_for: 1.4, avg_goals_against: 1.3
        };
        
        document.getElementById("editWinRate").value = stats.win_rate;
        document.getElementById("editRecentPts").value = stats.recent_pts_5;
        document.getElementById("editAvgGF").value = stats.avg_goals_for;
        document.getElementById("editAvgGA").value = stats.avg_goals_against;
    } catch(e) {
        console.error("Error loading team params:", e);
    }
}

async function submitNewMatch() {
    const homeTeam = document.getElementById("adaptHomeTeam").value;
    const awayTeam = document.getElementById("adaptAwayTeam").value;
    const homeScore = document.getElementById("adaptHomeScore").value;
    const awayScore = document.getElementById("adaptAwayScore").value;
    const feedback = document.getElementById("ingestFeedback");
    
    if (homeTeam === awayTeam) {
        alert("Tim kandang dan tim tandang tidak boleh sama!");
        return;
    }
    
    try {
        feedback.innerText = "Mengirim data laga...";
        const res = await fetch("/api/add-match-data", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                home_team: homeTeam,
                away_team: awayTeam,
                home_score: parseInt(homeScore),
                away_score: parseInt(awayScore)
            })
        });
        const data = await res.json();
        feedback.innerText = `✔️ Sukses! Form & H2H diperbarui: ${homeTeam} ${homeScore} - ${awayScore} ${awayTeam}`;
        loadTeamParamsToEdit();
    } catch(e) {
        feedback.innerText = "❌ Gagal mengunggah data laga: " + e.message;
    }
}

async function applyTeamParams() {
    const team = document.getElementById("paramTeamSelect").value;
    const winRate = document.getElementById("editWinRate").value;
    const recentPts = document.getElementById("editRecentPts").value;
    const avgGF = document.getElementById("editAvgGF").value;
    const avgGA = document.getElementById("editAvgGA").value;
    const feedback = document.getElementById("paramFeedback");
    
    try {
        feedback.innerText = "Menyimpan parameter...";
        const res = await fetch("/api/adjust-team-params", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                team: team,
                win_rate: parseFloat(winRate),
                recent_pts_5: parseFloat(recentPts),
                avg_goals_for: parseFloat(avgGF),
                avg_goals_against: parseFloat(avgGA)
            })
        });
        const data = await res.json();
        feedback.innerText = `✔️ Parameter untuk ${team} berhasil disimpan!`;
    } catch(e) {
        feedback.innerText = "❌ Gagal menyimpan parameter: " + e.message;
    }
}

async function recalculateMonteCarlo() {
    const feedback = document.getElementById("paramFeedback");
    try {
        feedback.innerText = "🔄 Menjalankan 10.000 simulasi Monte Carlo dengan data teradaptasi...";
        const res = await fetch("/api/recalculate-sim", {
            method: "POST",
            headers: { "Content-Type": "application/json" }
        });
        const data = await res.json();
        feedback.innerText = "✔️ Sukses! 10.000 simulasi turnamen selesai dihitung ulang.";
        
        // Refresh Tab 1 leaderboard
        loadAseanSimulation();
        alert("Simulasi Monte Carlo 10.000 iterasi berhasil diperbarui dengan data statistik terkini! Buka tab '🏆 Simulasi Juara ASEAN Cup' untuk melihat leaderboard terbaru.");
    } catch(e) {
        feedback.innerText = "❌ Gagal kalkulasi ulang simulasi: " + e.message;
    }
}

async function resetToBaselineData() {
    if (!confirm("Apakah Anda yakin ingin mereset seluruh parameter kembali ke data asli Kaggle?")) return;
    try {
        const res = await fetch("/api/reset-data", { method: "POST" });
        const data = await res.json();
        alert(data.message);
        loadTeamParamsToEdit();
        loadAseanSimulation();
    } catch(e) {
        alert("Gagal mereset data: " + e.message);
    }
}

// Hook dynamic adapt into DOMContentLoaded
document.addEventListener("DOMContentLoaded", () => {
    loadDynamicAdaptTeams();
});
'''

if 'loadDynamicAdaptTeams' not in js:
    js += '\n' + dynamic_js

with open(app_js_path, 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated app.js successfully!")

