import os

index_path = r"C:\Users\Kenny\.gemini\antigravity-ide\scratch\school_football_prediction\app\static\index.html"

with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Navigation Tabs to include Studio Adaptasi Dinamis
old_nav = '<button class="nav-tab" data-target="tabPresentation">📽️ Presentasi Slide (12 Slide)</button>'
new_nav = '''<button class="nav-tab" data-target="tabDynamicAdapt">⚡ Studio Adaptasi Dinamis</button>
      <button class="nav-tab" data-target="tabPresentation">📽️ Presentasi Slide (11 Slide Revisi)</button>'''
html = html.replace(old_nav, new_nav)

# 2. Add Problem Statement & Trust Triad Banner right before the main tabs
banner_html = '''
    <!-- PROBLEM STATEMENT & TRUST TRIAD BANNER (SDG 9 & WEEK 4 MANDATE) -->
    <div class="card" style="margin-bottom: 24px; border: 1.5px solid #0284c7; background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.9));">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:12px;">
        <div style="display:flex; align-items:center; gap:8px;">
          <span style="background:#0284c7; color:#fff; font-size:0.75rem; font-weight:700; padding:4px 8px; border-radius:4px;">SDG 9 INOVASI</span>
          <h2 style="font-size:1.15rem; color:#f8fafc; margin:0;">Problem Statement: Mengeliminasi Ilusi Kepastian Sepak Bola</h2>
        </div>
        <span style="color:#38bdf8; font-weight:600; font-size:0.85rem;">Metrik Validasi: Multi-Class Log Loss 0.8198 ✔️</span>
      </div>
      
      <p style="color:#cbd5e1; font-size:0.88rem; line-height:1.5; margin-bottom:14px;">
        <strong>Masalah Analisis Konvensional:</strong> Prediksi sepak bola seringkali terjebak pada bias opini dan ilusi kepastian semu (<em>"Tim A Pasti Menang"</em>). Sistem kami membangun <strong>Rantai Logika Probabilistik Murni</strong>: 49.945 Laga Historis &rarr; Fitur Pra-Laga Tanpa Leakage &rarr; Model Logistic Full Interaction &rarr; 10.000 Putaran Monte Carlo.
      </p>

      <div class="grid-3" style="gap:14px;">
        <div style="background:rgba(2, 132, 199, 0.1); border-left:3px solid #0284c7; padding:10px; border-radius:4px;">
          <div style="font-size:0.8rem; font-weight:700; color:#38bdf8; margin-bottom:4px;">🧠 Komparasi Arsitektur AI (vs YOLO11)</div>
          <div style="font-size:0.78rem; color:#94a3b8; line-height:1.4;">
            Jika tim deteksi aspal jalan menggunakan <strong>YOLO11 Computer Vision</strong> untuk mencari koordinat bounding box lubang jalan, model kami menggunakan <strong>Logistic Full Interaction + Stochastic Monte Carlo</strong> untuk memetakan koordinat probabilitas olahraga yang stokastik dan non-linear.
          </div>
        </div>

        <div style="background:rgba(16, 185, 129, 0.1); border-left:3px solid #10b981; padding:10px; border-radius:4px;">
          <div style="font-size:0.8rem; font-weight:700; color:#34d399; margin-bottom:4px;">🛡️ Tiga Lapis Kepercayaan (Trust Triad)</div>
          <div style="font-size:0.78rem; color:#94a3b8; line-height:1.4;">
            <strong>1. Data & Waktu:</strong> Cut-off 2024-12-08 (No Leakage, shootouts dikunci).<br/>
            <strong>2. Model:</strong> Terkalibrasi Log Loss 0.8198 vs Baseline 1.0686.<br/>
            <strong>3. Simulasi:</strong> 10.000 iterasi dengan aturan tiebreak resmi turnamen.
          </div>
        </div>

        <div style="background:rgba(245, 158, 11, 0.1); border-left:3px solid #f59e0b; padding:10px; border-radius:4px;">
          <div style="font-size:0.8rem; font-weight:700; color:#fbbf24; margin-bottom:4px;">🎯 Target Pihak Terbantu (Mandat Week 4)</div>
          <div style="font-size:0.78rem; color:#94a3b8; line-height:1.4;">
            <strong>Tim Liga & Timnas Underdogs:</strong> Tim dengan peluang rendah dapat melihat celah riil kekuatan lawan, menyiapkan kontra-taktik berbeda, dan mengoptimalkan strategi sebelum turnamen dimulai.
          </div>
        </div>
      </div>
    </div>
'''

if '<!-- PROBLEM STATEMENT & TRUST TRIAD BANNER' not in html:
    html = html.replace('<main>', '<main>\n' + banner_html)

# 3. Add Dynamic Adaptation Tab Section before tabPresentation
tab_adapt_html = '''
    <!-- TAB: Dynamic Adaptability Studio -->
    <section id="tabDynamicAdapt" class="tab-pane">
      <div class="card">
        <div class="card-title">⚡ Studio Adaptasi Data Dinamis & Real-Time Recalculation</div>
        <p style="color:var(--text-muted); font-size:0.88rem; margin-bottom:20px;">
          Fitur ini membuktikan kemampuan adaptasi AI secara interaktif: pengguna dapat menyuntikkan data pertandingan baru atau memodifikasi parameter tim, dan sistem langsung memperbarui Elo rating, form, serta menjalankan ulang 10.000 simulasi Monte Carlo secara real-time.
        </p>

        <div class="grid-2">
          <!-- Ingest Match -->
          <div style="background:rgba(15,23,42,0.6); padding:16px; border-radius:8px; border:1px solid #334155;">
            <h3 style="font-size:0.95rem; color:#38bdf8; margin-bottom:12px;">⚽ Suntikkan Hasil Laga Baru (Update H2H & Form)</h3>
            <div class="grid-2" style="gap:10px; margin-bottom:10px;">
              <div>
                <label style="font-size:0.75rem; color:#94a3b8;">Tim Kandang</label>
                <select id="adaptHomeTeam" style="width:100%; padding:8px; background:#1e293b; color:#fff; border:1px solid #475569; border-radius:6px;"></select>
              </div>
              <div>
                <label style="font-size:0.75rem; color:#94a3b8;">Skor Kandang</label>
                <input type="number" id="adaptHomeScore" value="2" min="0" max="20" style="width:100%; padding:8px; background:#1e293b; color:#fff; border:1px solid #475569; border-radius:6px;">
              </div>
            </div>

            <div class="grid-2" style="gap:10px; margin-bottom:14px;">
              <div>
                <label style="font-size:0.75rem; color:#94a3b8;">Tim Tandang</label>
                <select id="adaptAwayTeam" style="width:100%; padding:8px; background:#1e293b; color:#fff; border:1px solid #475569; border-radius:6px;"></select>
              </div>
              <div>
                <label style="font-size:0.75rem; color:#94a3b8;">Skor Tandang</label>
                <input type="number" id="adaptAwayScore" value="1" min="0" max="20" style="width:100%; padding:8px; background:#1e293b; color:#fff; border:1px solid #475569; border-radius:6px;">
              </div>
            </div>

            <button class="btn" style="width:100%;" onclick="submitNewMatch()">
              📥 Ingest Pertandingan & Perbarui Statistik Form
            </button>
            <div id="ingestFeedback" style="font-size:0.8rem; margin-top:8px; color:#34d399;"></div>
          </div>

          <!-- Adjust Team Parameters -->
          <div style="background:rgba(15,23,42,0.6); padding:16px; border-radius:8px; border:1px solid #334155;">
            <h3 style="font-size:0.95rem; color:#34d399; margin-bottom:12px;">⚙️ Modifikasi Parameter Kekuatan Tim</h3>
            <div style="margin-bottom:10px;">
              <label style="font-size:0.75rem; color:#94a3b8;">Pilih Tim untuk Dimodifikasi</label>
              <select id="paramTeamSelect" onchange="loadTeamParamsToEdit()" style="width:100%; padding:8px; background:#1e293b; color:#fff; border:1px solid #475569; border-radius:6px;"></select>
            </div>

            <div class="grid-2" style="gap:10px; margin-bottom:10px;">
              <div>
                <label style="font-size:0.75rem; color:#94a3b8;">Win Rate Historis (0.0 - 1.0)</label>
                <input type="number" step="0.01" id="editWinRate" style="width:100%; padding:8px; background:#1e293b; color:#fff; border:1px solid #475569; border-radius:6px;">
              </div>
              <div>
                <label style="font-size:0.75rem; color:#94a3b8;">Poin Form 5 Laga (0 - 15)</label>
                <input type="number" step="0.5" id="editRecentPts" style="width:100%; padding:8px; background:#1e293b; color:#fff; border:1px solid #475569; border-radius:6px;">
              </div>
            </div>

            <div class="grid-2" style="gap:10px; margin-bottom:14px;">
              <div>
                <label style="font-size:0.75rem; color:#94a3b8;">Rata-rata Gol Cetak (GF)</label>
                <input type="number" step="0.1" id="editAvgGF" style="width:100%; padding:8px; background:#1e293b; color:#fff; border:1px solid #475569; border-radius:6px;">
              </div>
              <div>
                <label style="font-size:0.75rem; color:#94a3b8;">Rata-rata Kebobolan (GA)</label>
                <input type="number" step="0.1" id="editAvgGA" style="width:100%; padding:8px; background:#1e293b; color:#fff; border:1px solid #475569; border-radius:6px;">
              </div>
            </div>

            <div style="display:flex; gap:10px;">
              <button class="btn btn-secondary" style="flex:1;" onclick="applyTeamParams()">
                💾 Simpan Parameter
              </button>
              <button class="btn" style="flex:1; background:#0284c7;" onclick="recalculateMonteCarlo()">
                🔄 Hitung Ulang 10k Monte Carlo
              </button>
            </div>
            <div id="paramFeedback" style="font-size:0.8rem; margin-top:8px; color:#38bdf8;"></div>
          </div>
        </div>

        <div style="margin-top:20px; display:flex; justify-content:flex-end;">
          <button class="btn btn-secondary" onclick="resetToBaselineData()" style="border-color:#ef4444; color:#f87171;">
            ↺ Reset ke Data Asli Kaggle
          </button>
        </div>
      </div>
    </section>
'''

if '<!-- TAB: Dynamic Adaptability Studio -->' not in html:
    html = html.replace('<section id="tabPresentation"', tab_adapt_html + '\n    <section id="tabPresentation"')

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html successfully!")

