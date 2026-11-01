// ==============================================================================
// AI Football Prediction & ASEAN Cup Simulator - Frontend Logic
// Kelompok 1 - Divisi AI (SDG 9)
// Kenny Helim (BINUS), Arya Wicaksana, M. Ihram, Gisela Venska, Christian
// ==============================================================================

document.addEventListener("DOMContentLoaded", () => {
    initTabs();
    loadTeams();
    loadAseanSimulation();
    loadEdaData();
    loadModelData();
    initPresentationDeck();
});

// 1. Navigation Tabs
function initTabs() {
    const tabs = document.querySelectorAll(".nav-tab");
    tabs.forEach(tab => {
        tab.addEventListener("click", () => {
            tabs.forEach(t => t.classList.remove("active"));
            document.querySelectorAll(".tab-pane").forEach(p => p.classList.remove("active"));
            
            tab.classList.add("active");
            const target = document.getElementById(tab.dataset.target);
            if (target) target.classList.add("active");
        });
    });
}

// 2. Load Teams for Match Predictor
async function loadTeams() {
    try {
        const res = await fetch("/api/teams");
        const data = await res.json();
        
        const homeSelect = document.getElementById("homeTeamSelect");
        const awaySelect = document.getElementById("awayTeamSelect");
        
        if (!homeSelect || !awaySelect) return;
        
        homeSelect.innerHTML = "";
        awaySelect.innerHTML = "";
        
        // Optgroups
        const grpAseanH = document.createElement("optgroup");
        grpAseanH.label = "--- Tim ASEAN ---";
        const grpAllH = document.createElement("optgroup");
        grpAllH.label = "--- Tim Internasional Lainnya ---";
        
        const grpAseanA = document.createElement("optgroup");
        grpAseanA.label = "--- Tim ASEAN ---";
        const grpAllA = document.createElement("optgroup");
        grpAllA.label = "--- Tim Internasional Lainnya ---";
        
        data.asean_teams.forEach(t => {
            grpAseanH.appendChild(new Option(t, t));
            grpAseanA.appendChild(new Option(t, t));
        });
        
        data.all_teams.forEach(t => {
            if (!data.asean_teams.includes(t)) {
                grpAllH.appendChild(new Option(t, t));
                grpAllA.appendChild(new Option(t, t));
            }
        });
        
        homeSelect.appendChild(grpAseanH);
        homeSelect.appendChild(grpAllH);
        awaySelect.appendChild(grpAseanA);
        awaySelect.appendChild(grpAllA);
        
        // Default selection: Indonesia vs Thailand
        homeSelect.value = "Indonesia";
        awaySelect.value = "Thailand";
        
        // Trigger initial prediction
        executePrediction();
    } catch (err) {
        console.error("Failed to load teams:", err);
    }
}

// 3. Match Predictor Execution
async function executePrediction() {
    const homeTeam = document.getElementById("homeTeamSelect").value;
    const awayTeam = document.getElementById("awayTeamSelect").value;
    const isNeutral = document.getElementById("neutralVenueCheck").checked ? 1 : 0;
    const isFriendly = document.getElementById("friendlyCheck").checked ? 1 : 0;
    
    if (homeTeam === awayTeam) {
        alert("Pilih dua tim yang berbeda!");
        return;
    }
    
    const predResultCard = document.getElementById("predictionResultCard");
    predResultCard.style.opacity = "0.5";
    
    try {
        const res = await fetch("/api/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                home_team: homeTeam,
                away_team: awayTeam,
                is_neutral: isNeutral,
                is_friendly: isFriendly
            })
        });
        
        const data = await res.json();
        predResultCard.style.opacity = "1";
        
        // Render probabilities
        const pHome = data.probabilities.home_win;
        const pDraw = data.probabilities.draw;
        const pAway = data.probabilities.away_win;
        
        document.getElementById("probHomeLabel").textContent = `${homeTeam}: ${pHome}%`;
        document.getElementById("probDrawLabel").textContent = `Seri (Draw): ${pDraw}%`;
        document.getElementById("probAwayLabel").textContent = `${awayTeam}: ${pAway}%`;
        
        document.getElementById("probBarHome").style.width = `${pHome}%`;
        document.getElementById("probBarDraw").style.width = `${pDraw}%`;
        document.getElementById("probBarAway").style.width = `${pAway}%`;
        
        document.getElementById("probBarHome").textContent = pHome > 12 ? `${pHome}%` : '';
        document.getElementById("probBarDraw").textContent = pDraw > 12 ? `${pDraw}%` : '';
        document.getElementById("probBarAway").textContent = pAway > 12 ? `${pAway}%` : '';
        
        // Expected outcome & score
        document.getElementById("predOutcomeText").textContent = data.predicted_outcome === "Home Win" ? `${homeTeam} Menang` : (data.predicted_outcome === "Away Win" ? `${awayTeam} Menang` : "Hasil Imbang (Draw)");
        document.getElementById("predScoreText").textContent = data.expected_score;
        
        // Stats table
        document.getElementById("predStatsHomeMatches").textContent = data.home_stats.matches || '-';
        document.getElementById("predStatsAwayMatches").textContent = data.away_stats.matches || '-';
        document.getElementById("predStatsHomeWinRate").textContent = `${((data.home_stats.win_rate || 0) * 100).toFixed(1)}%`;
        document.getElementById("predStatsAwayWinRate").textContent = `${((data.away_stats.win_rate || 0) * 100).toFixed(1)}%`;
        document.getElementById("predStatsHomeAvgGf").textContent = data.home_stats.avg_goals_for || '-';
        document.getElementById("predStatsAwayAvgGf").textContent = data.away_stats.avg_goals_for || '-';
        document.getElementById("predStatsHomeForm").textContent = `${data.home_stats.recent_pts_5 || 0} pts`;
        document.getElementById("predStatsAwayForm").textContent = `${data.away_stats.recent_pts_5 || 0} pts`;
        
        // H2H
        const h2h = data.h2h_info;
        document.getElementById("h2hSummaryText").textContent = h2h.played > 0 
            ? `${h2h.played} pertemuan: ${data.home_team} menang ${h2h.home_wins}x, ${data.away_team} menang ${h2h.away_wins}x, Seri ${h2h.draws}x.`
            : "Belum pernah bertemu sebelumnya di dataset resmi.";
            
    } catch (err) {
        console.error("Prediction failed:", err);
        predResultCard.style.opacity = "1";
    }
}

// 4. Live 90-Minute Match Simulator
async function runLiveMatchSimulation() {
    const homeTeam = document.getElementById("homeTeamSelect").value;
    const awayTeam = document.getElementById("awayTeamSelect").value;
    const isNeutral = document.getElementById("neutralVenueCheck").checked ? 1 : 0;
    const isFriendly = document.getElementById("friendlyCheck").checked ? 1 : 0;
    
    const timelineEl = document.getElementById("matchTimeline");
    const scoreBadge = document.getElementById("liveScoreBadge");
    const btnSim = document.getElementById("btnRunLiveSim");
    
    btnSim.disabled = true;
    btnSim.textContent = "⏳ Mensimulasikan Laga...";
    timelineEl.innerHTML = "<div style='color:#94a3b8; text-align:center; padding:20px;'>Menghitung kalkulasi probabilistik lapangan...</div>";
    
    try {
        const res = await fetch("/api/simulate-match", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                home_team: homeTeam,
                away_team: awayTeam,
                is_neutral: isNeutral,
                is_friendly: isFriendly
            })
        });
        
        const data = await res.json();
        timelineEl.innerHTML = "";
        
        let delay = 0;
        data.events.forEach((evt, idx) => {
            setTimeout(() => {
                const item = document.createElement("div");
                item.className = `event-item ${evt.type === 'goal' ? 'event-goal' : (evt.type === 'whistle' || evt.type === 'halftime' || evt.type === 'fulltime' ? 'event-whistle' : '')}`;
                item.innerHTML = `
                    <span class="event-minute">${evt.minute}'</span>
                    <span>${evt.text}</span>
                `;
                timelineEl.prepend(item);
                
                if (evt.type === 'goal') {
                    scoreBadge.textContent = `${homeTeam} ${evt.score} ${awayTeam}`;
                } else if (idx === data.events.length - 1) {
                    scoreBadge.textContent = `${homeTeam} ${data.final_score} ${awayTeam} (Selesai)`;
                    btnSim.disabled = false;
                    btnSim.textContent = "🔁 Ulangi Simulasi Laga";
                }
            }, delay);
            delay += 180; // Fast animated playback
        });
        
    } catch (err) {
        console.error("Match simulation failed:", err);
        btnSim.disabled = false;
        btnSim.textContent = "▶️ Jalankan Simulasi 90 Menit";
    }
}

// 5. ASEAN Cup Monte Carlo Leaderboard
async function loadAseanSimulation() {
    try {
        const res = await fetch("/api/asean-sim");
        const data = await res.json();
        
        // Leaderboard table
        const tbody = document.getElementById("aseanLeaderboardBody");
        if (!tbody) return;
        tbody.innerHTML = "";
        
        data.leaderboard.forEach((row, idx) => {
            const tr = document.createElement("tr");
            const isTop3 = idx < 3;
            const medal = idx === 0 ? "🥇 " : (idx === 1 ? "🥈 " : (idx === 2 ? "🥉 " : ""));
            tr.innerHTML = `
                <td style="font-weight:700;">${idx + 1}</td>
                <td style="font-weight:700; color:${isTop3 ? '#38bdf8' : '#e2e8f0'}">${medal}${row.team}</td>
                <td style="font-weight:800; color:#34d399;">${row.champion_pct}%</td>
                <td>${row.finalist_pct}%</td>
                <td>${row.semi_finalist_pct}%</td>
                <td style="color:#94a3b8;">${row.group_exit_pct}%</td>
            `;
            tbody.appendChild(tr);
        });
        
        // Sample tournament bracket
        if (data.sample_tournament) {
            const st = data.sample_tournament;
            document.getElementById("sf1Text").textContent = `${st.semi_finals[0].match} ➔ Pemenang: ${st.semi_finals[0].winner}`;
            document.getElementById("sf2Text").textContent = `${st.semi_finals[1].match} ➔ Pemenang: ${st.semi_finals[1].winner}`;
            document.getElementById("finalText").textContent = `${st.final.match} ➔ JUARA: 🏆 ${st.final.winner} (Runner-up: ${st.final.runner_up})`;
        }
        
    } catch (err) {
        console.error("Failed to load ASEAN simulation:", err);
    }
}

// 6. Exploratory Data Analysis (EDA)
async function loadEdaData() {
    try {
        const res = await fetch("/api/eda");
        const data = await res.json();
        
        document.getElementById("edaTotalMatches").textContent = data.dataset_metadata.total_matches.toLocaleString();
        document.getElementById("edaDateRange").textContent = `${data.dataset_metadata.date_range[0].split('-')[0]} - ${data.dataset_metadata.date_range[1].split('-')[0]}`;
        document.getElementById("edaHomeWinPct").textContent = `${data.target_distribution.home_win.pct}%`;
        document.getElementById("edaAvgGoals").textContent = data.goal_patterns.avg_total_goals;
        document.getElementById("edaHomeAdv").textContent = `${data.target_distribution.home_advantage_multiplier}x`;
        document.getElementById("edaAseanMatches").textContent = data.dataset_metadata.asean_matches_count.toLocaleString();
    } catch (err) {
        console.error("Failed to load EDA data:", err);
    }
}

// 7. Machine Learning Model Lab
async function loadModelData() {
    try {
        const res = await fetch("/api/models");
        const data = await res.json();
        
        const tbody = document.getElementById("modelComparisonBody");
        if (!tbody) return;
        tbody.innerHTML = "";
        
        for (const [mname, mstats] of Object.entries(data)) {
            const tr = document.createElement("tr");
            const isBest = mname === "Random Forest";
            tr.innerHTML = `
                <td style="font-weight:700; color:${isBest ? '#34d399' : '#e2e8f0'}">${mname} ${isBest ? '⭐ (Terpilih)' : ''}</td>
                <td style="font-weight:800;">${(mstats.accuracy * 100).toFixed(2)}%</td>
                <td>${mstats.macro_f1.toFixed(4)}</td>
                <td>${mstats.weighted_f1.toFixed(4)}</td>
                <td>${mstats.per_class['Home Win'].f1.toFixed(2)}</td>
                <td>${mstats.per_class['Draw'].f1.toFixed(2)}</td>
                <td>${mstats.per_class['Away Win'].f1.toFixed(2)}</td>
            `;
            tbody.appendChild(tr);
        }
    } catch (err) {
        console.error("Failed to load model data:", err);
    }
}

// 8. 12-Slide Interactive Presentation Deck
const SLIDES = [
    {
        num: "01 / 12",
        title: "Prediksi Hasil Pertandingan Sepak Bola Internasional Berbasis AI",
        subtitle: "Pemetaan Masalah, Eksplorasi Data, dan Pendekatan Machine Learning (Kelompok 1 - SDG 9)",
        body: `
            <div style="background:rgba(59,130,246,0.1); border:1px solid rgba(59,130,246,0.3); padding:16px; border-radius:8px; margin-bottom:16px;">
                <strong>🎯 Judul Proyek Resmi:</strong><br>
                <em>"Prediksi Hasil Pertandingan dan Probabilitas Juara ASEAN Cup Menggunakan Algoritma Machine Learning Berdasarkan Statistik Historis Tim Nasional"</em>
            </div>
            <p><strong>Anggota Kelompok 1:</strong></p>
            <ul>
                <li>Kenny Helim - Information Systems & Management (Bina Nusantara University / BINUS)</li>
                <li>Arya Wicaksana - Teknik Informatika (Universitas Esa Unggul)</li>
                <li>Muhammad Ihram Syahputra - Ilmu Komputer (Universitas Halu Oleo)</li>
                <li>Gisela Venska Millennia - Information System (President University)</li>
                <li>Christian - Information Systems (Bina Nusantara University)</li>
            </ul>
        `,
        notes: "Slide pembuka memperkenalkan topik kelompok 1 di bawah bimbingan Pak Aslan, menyelaraskan dengan target SDG 9 (Inovasi & Infrastruktur Digital)."
    },
    {
        num: "02 / 12",
        title: "Keterbatasan Analisis Manual vs. Skalabilitas Otomasi",
        subtitle: "Mengapa Kita Memerlukan Machine Learning untuk Prediksi Sepak Bola?",
        body: `
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px;">
                <div style="background:rgba(239,68,68,0.1); border:1px solid rgba(239,68,68,0.3); padding:16px; border-radius:8px;">
                    <h3 style="color:#ef4444; margin-bottom:8px;">❌ Pendekatan Manual</h3>
                    <ul>
                        <li>Membuka CSV/Excel dan menghitung rekaman manual.</li>
                        <li>Sangat repetitif, memakan waktu, dan rawan salah hitung.</li>
                        <li>Terjebak bias kognitif dan intuisi subjektif penggemar.</li>
                    </ul>
                </div>
                <div style="background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.3); padding:16px; border-radius:8px;">
                    <h3 style="color:#10b981; margin-bottom:8px;">✅ Pendekatan Machine Learning</h3>
                    <ul>
                        <li>Otomasi ekstraksi fitur (form 5 laga, H2H, selisih gol).</li>
                        <li>Konsisten, terukur, dan mampu memproses 49.000+ pertandingan seketika.</li>
                        <li>Evaluasi berbasis probabilitas matematis yang dapat diuji ulang (reproducible).</li>
                    </ul>
                </div>
            </div>
        `,
        notes: "Menjelaskan urgensi otomasi analitik dibandingkan analisa manual manual spreadsheet."
    },
    {
        num: "03 / 12",
        title: "Mendefinisikan Ruang Lingkup dan Ekspektasi Sistem",
        subtitle: "Pertanyaan Inti, Batasan Realitas, dan Pihak Terdampak",
        body: `
            <ul>
                <li><strong>Pertanyaan Inti:</strong> Dapatkah data pertandingan masa lalu membantu memperkirakan hasil laga internasional dan probabilitas juara turnamen regional secara objektif?</li>
                <li><strong>Batasan Realitas (Scope):</strong> Berfungsi murni sebagai <em>baseline analitik</em> berbasis probabilitas historis, bukan bola kristal ramalan mutlak atau perjudian.</li>
                <li><strong>Pihak Terdampak (Audiens):</strong> Analis sepak bola, jurnalis olahraga, federasi sepak bola (PSSI / AFF), dan pengembang aplikasi digital.</li>
            </ul>
        `,
        notes: "Mendefinisikan batasan etis dan tujuan teknis dari model."
    },
    {
        num: "04 / 12",
        title: "Anatomi Dataset Historis Sebagai Bahan Bakar Model",
        subtitle: "Dataset Resmi Kaggle (martj42): 1872 hingga 2026",
        body: `
            <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:16px; text-align:center;">
                <div class="stat-box"><div class="stat-label">Total Pertandingan</div><div class="stat-value">49.945</div></div>
                <div class="stat-box"><div class="stat-label">Rentang Waktu</div><div class="stat-value">154 Tahun</div></div>
                <div class="stat-box"><div class="stat-label">Laga Tim ASEAN</div><div class="stat-value">3.782</div></div>
            </div>
            <p style="margin-top:16px;"><strong>Atribut Kunci yang Digunakan:</strong></p>
            <ul>
                <li><code>date</code>: Tanggal laga (fondasi aturan anti-leakage temporal)</li>
                <li><code>home_team</code> & <code>away_team</code>: Nama tim peserta</li>
                <li><code>home_score</code> & <code>away_score</code>: Skor akhir riil</li>
                <li><code>tournament</code>: Turnamen kompetitif (World Cup, AFF Cup, Asian Cup) vs Friendly</li>
                <li><code>neutral</code>: Status venue netral (mempengaruhi faktor kandang)</li>
            </ul>
        `,
        notes: "Memperlihatkan integritas dataset Kaggle martj42 dengan 0 missing values."
    },
    {
        num: "05 / 12",
        title: "Eksplorasi Data (EDA) Berbasis Hipotesis",
        subtitle: "Temuan Empiris: Distribusi Target, Gol, dan Pengaruh Kandang",
        body: `
            <ul>
                <li><strong>Distribusi Target:</strong> Home Win 49.00% (24.473 laga), Away Win 28.29% (14.131 laga), Draw 22.71% (11.341 laga).</li>
                <li><strong>Home Advantage:</strong> Tim tuan rumah 1.73x lebih berpeluang menang dibanding tim tamu di lapangan kandang.</li>
                <li><strong>Pengaruh Venue Netral:</strong> Pada venue netral, Home Win turun dari 50.73% menjadi 44.22%, sedangkan Away Win melonjak ke 33.40%!</li>
                <li><strong>Produktivitas Gol:</strong> Rata-rata 2.94 gol per pertandingan internasional (Kandang: 1.76 vs Tandang: 1.18).</li>
            </ul>
        `,
        notes: "Menjawab instruksi eksplorasi data di Canva: Distribusi Target, Skala Aktual, dan Pola Gol masa lalu."
    },
    {
        num: "06 / 12",
        title: "Formulasi Output: Multiclass Classification",
        subtitle: "Klasifikasi Kategorikal 3 Kelas (Home Win, Draw, Away Win)",
        body: `
            <p>Model diformulasikan bukan untuk memprediksi angka skor eksak (seperti 2-1 atau 3-2), melainkan mengklasifikasikan probabilitas hasil laga ke dalam 3 kelas absolut:</p>
            <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:16px; margin:20px 0; text-align:center;">
                <div style="background:rgba(16,185,129,0.15); border:2px solid #10b981; border-radius:10px; padding:20px;">
                    <h2 style="color:#10b981;">W (Home Win)</h2>
                    <p>Skor Tim Kandang > Skor Tim Tamu</p>
                </div>
                <div style="background:rgba(245,158,11,0.15); border:2px solid #f59e0b; border-radius:10px; padding:20px;">
                    <h2 style="color:#f59e0b;">D (Draw)</h2>
                    <p>Skor Tim Kandang == Skor Tim Tamu</p>
                </div>
                <div style="background:rgba(239,68,68,0.15); border:2px solid #ef4444; border-radius:10px; padding:20px;">
                    <h2 style="color:#ef4444;">L (Away Win)</h2>
                    <p>Skor Tim Kandang < Skor Tim Tamu</p>
                </div>
            </div>
        `,
        notes: "Menjelaskan formulasi target multiclass W-D-L."
    },
    {
        num: "07 / 12",
        title: "Rekayasa Fitur Temporal & Barrier Anti-Leakage",
        subtitle: "Hanya Menggunakan Informasi Pra-Laga Sebelum Waktu (T)",
        body: `
            <p><strong>Daftar 19 Fitur Prediktor yang Dibangun:</strong></p>
            <ul>
                <li><strong>Recent Form:</strong> Poin akumulasi 5 laga terakhir (W=3, D=1, L=0) serta rata-rata gol & kebobolan 5 laga terakhir.</li>
                <li><strong>Historical Strength:</strong> Rasio kemenangan kumulatif dan produktivitas gol sepanjang sejarah hingga T-1.</li>
                <li><strong>Head-to-Head (H2H):</strong> Rasio kemenangan pertemuan langsung antara kedua negara sebelum tanggal laga.</li>
                <li><strong>Differential Features:</strong> Selisih form poin, selisih win rate, dan selisih daya serang/kebobolan tim.</li>
                <li><strong>Konteks Laga:</strong> <code>is_neutral</code> (boolean) dan <code>is_friendly</code> (boolean).</li>
            </ul>
        `,
        notes: "Menegaskan prinsip anti-leakage: fitur laga hari ini dihitung murni dari data kemarin."
    },
    {
        num: "08 / 12",
        title: "Mitigasi Ancaman Data Leakage: Time-Based Split",
        subtitle: "Menolak Random Split Demi Keabsahan Real-World Model",
        body: `
            <div style="background:rgba(245,158,11,0.1); border-left:4px solid #f59e0b; padding:16px; border-radius:4px; margin-bottom:16px;">
                <strong>⚠️ Aturan Absolut Machine Learning Waktu:</strong> Random train_test_split dilarang keras karena membocorkan form masa depan ke masa lalu.
            </div>
            <ul>
                <li><strong>Training Set (Era Historis):</strong> Laga tahun 1960 s.d. 31 Desember 2020 (38.288 laga).</li>
                <li><strong>Testing Set (Out-of-Time Era Baru):</strong> Laga 1 Januari 2021 s.d. Oktober 2026 (6.162 laga riil termasuk Euro, World Cup 2022, AFF Cup).</li>
            </ul>
        `,
        notes: "Membuktikan model dievaluasi secara out-of-time untuk mencegah overfitting."
    },
    {
        num: "09 / 12",
        title: "Perbandingan Model Baseline vs Algoritma Terpilih",
        subtitle: "Naive Baseline vs Decision Tree vs Random Forest vs Gradient Boosting",
        body: `
            <table class="custom-table">
                <thead>
                    <tr><th>Algoritma</th><th>Akurasi</th><th>Macro F1</th><th>Weighted F1</th><th>Evaluasi</th></tr>
                </thead>
                <tbody>
                    <tr><td>Naive Majority Baseline</td><td>47.89%</td><td>0.2159</td><td>0.3102</td><td>Tebakan naif (selalu tebak Home)</td></tr>
                    <tr><td>Decision Tree (depth=6)</td><td>57.43%</td><td>0.4116</td><td>0.4925</td><td>Pohon keputusan interpretable</td></tr>
                    <tr><td>Logistic Regression</td><td>58.00%</td><td>0.4192</td><td>0.4990</td><td>Linear baseline terkalibrasi</td></tr>
                    <tr style="background:rgba(59,130,246,0.15); font-weight:700;"><td>Random Forest (150 trees) ⭐</td><td>58.05%</td><td>0.4153</td><td>0.4964</td><td>Ensemble paling stabil & presisi 60% Away</td></tr>
                    <tr><td>Gradient Boosting</td><td>57.85%</td><td>0.4312</td><td>0.5072</td><td>Macro F1 tertinggi untuk kelas Draw</td></tr>
                </tbody>
            </table>
            <p style="margin-top:14px; font-weight:600; color:#34d399;">Peningkatan (Lift): Model ML Random Forest mengungguli Naive Baseline sebesar +10.16% akurasi dan +0.20 F1-Score!</p>
        `,
        notes: "Menjawab sesi Pak Aslan di hari Jumat mengenai pembentukan dan pemilihan model machine learning terbaik."
    },
    {
        num: "10 / 12",
        title: "Confusion Matrix & Analisis Kesalahan Prediksi",
        subtitle: "Membedah Blind Spot: Mengapa Hasil 'Draw' Sulit Diprediksi?",
        body: `
            <ul>
                <li><strong>Performa Home Win:</strong> Precision 58%, Recall 91%, F1-Score 0.71. Model sangat efektif mengidentifikasi kemenangan tuan rumah.</li>
                <li><strong>Performa Away Win:</strong> Precision 60%, Recall 49%, F1-Score 0.54. Model sangat berhati-hati dan akurat ketika memprediksi kemenangan tim tamu.</li>
                <li><strong>Blind Spot (Draw):</strong> Hasil seri secara statistik merupakan anomali dengan variansi tertinggi di sepak bola (biasanya hanya terjadi saat kedua tim mengalami kebuntuan taktis di 15 menit akhir).</li>
            </ul>
        `,
        notes: "Menganalisis matriks kebingungan dan karakteristik alamiah olahraga sepak bola."
    },
    {
        num: "11 / 12",
        title: "Simulasi Probabilitas Juara ASEAN Cup (AFF Championship)",
        subtitle: "10.000 Iterasi Monte Carlo Berdasarkan Probabilitas Model ML",
        body: `
            <p>Mengintegrasikan model Random Forest ke dalam simulasi turnamen ASEAN Cup 10 tim (Babak Grup Home-Away, Semifinal 2 Leg, Final 2 Leg):</p>
            <div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:12px; margin:16px 0; text-align:center;">
                <div class="stat-box"><div class="stat-label">Vietnam 🇻🇳</div><div class="stat-value" style="color:#ef4444;">26.5%</div><div style="font-size:0.75rem;">Juara 1</div></div>
                <div class="stat-box"><div class="stat-label">Thailand 🇹🇭</div><div class="stat-value" style="color:#3b82f6;">24.5%</div><div style="font-size:0.75rem;">Juara 2</div></div>
                <div class="stat-box"><div class="stat-label">Indonesia 🇮🇩</div><div class="stat-value" style="color:#10b981;">21.2%</div><div style="font-size:0.75rem;">Juara 3</div></div>
                <div class="stat-box"><div class="stat-label">Malaysia 🇲🇾</div><div class="stat-value" style="color:#f59e0b;">21.0%</div><div style="font-size:0.75rem;">Juara 4</div></div>
            </div>
            <p style="font-size:0.9rem; color:#94a3b8;">Tim seperti Myanmar (4.0%), Singapura (2.2%), dan Filipina (0.5%) memiliki probabilitas lolos fase grup yang lebih kompetitif namun peluang juara lebih kecil.</p>
        `,
        notes: "Menjawab tuntas judul kelompok: Simulasi Probabilitas Juara ASEAN Cup berbasis Machine Learning."
    },
    {
        num: "12 / 12",
        title: "Kesimpulan, Relevansi SDG 9, dan Langkah Lanjutan",
        subtitle: "Ringkasan Hasil Karya Kelompok 1 - Artificial Intelligence",
        body: `
            <ul>
                <li><strong>Kesimpulan Metodologis:</strong> Pendekatan Machine Learning terbukti mampu menyaring sinyal objektif dari 49.000+ data historis dan mengungguli tebakan naif sebesar +10%.</li>
                <li><strong>Kontribusi SDG 9:</strong> Membangun infrastruktur analitik olahraga berbasis kecerdasan buatan yang terbuka, transparan, dan dapat digunakan sebagai baseline keputusan federasi/tim.</li>
                <li><strong>Pengembangan Berikutnya:</strong>
                    <ul>
                        <li>Menambahkan fitur cuaca, jarak tempuh perjalanan tim, dan status rotasi pemain inti.</li>
                        <li>Eksplorasi model deep learning sequence (LSTM/Transformer) untuk merekam momentum taktis pertandingan.</li>
                    </ul>
                </li>
            </ul>
        `,
        notes: "Slide penutup: sintesis proyek, relevansi SDG 9, dan rencana pengembangan masa depan."
    }
];

let currentSlideIndex = 0;

function initPresentationDeck() {
    renderSlide(currentSlideIndex);
    
    document.getElementById("btnPrevSlide").addEventListener("click", () => {
        if (currentSlideIndex > 0) {
            currentSlideIndex--;
            renderSlide(currentSlideIndex);
        }
    });
    
    document.getElementById("btnNextSlide").addEventListener("click", () => {
        if (currentSlideIndex < SLIDES.length - 1) {
            currentSlideIndex++;
            renderSlide(currentSlideIndex);
        }
    });
    
    // Keyboard navigation
    document.addEventListener("keydown", (e) => {
        const presTab = document.getElementById("tabPresentation");
        if (presTab && presTab.classList.contains("active")) {
            if (e.key === "ArrowRight" || e.key === " ") {
                if (currentSlideIndex < SLIDES.length - 1) {
                    currentSlideIndex++;
                    renderSlide(currentSlideIndex);
                }
            } else if (e.key === "ArrowLeft") {
                if (currentSlideIndex > 0) {
                    currentSlideIndex--;
                    renderSlide(currentSlideIndex);
                }
            }
        }
    });
}

function renderSlide(idx) {
    const s = SLIDES[idx];
    document.getElementById("slideNum").textContent = s.num;
    document.getElementById("slideTitle").textContent = s.title;
    document.getElementById("slideSubtitle").textContent = s.subtitle;
    document.getElementById("slideBody").innerHTML = s.body;
    document.getElementById("slideNotes").innerHTML = `<strong>💡 Catatan Presenter (Speaker Notes):</strong> ${s.notes}`;
    
    document.getElementById("btnPrevSlide").disabled = idx === 0;
    document.getElementById("btnNextSlide").disabled = idx === SLIDES.length - 1;
}

// Global button hookups
window.executePrediction = executePrediction;
window.runLiveMatchSimulation = runLiveMatchSimulation;


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
