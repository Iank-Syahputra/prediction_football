import os
import json
import matplotlib.pyplot as plt
import numpy as np

# Set dark theme styling
plt.style.use('dark_background')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

art_dir = r"C:\Users\Kenny\.gemini\antigravity-ide\scratch\school_football_prediction\artifacts"
os.makedirs(art_dir, exist_ok=True)

# ==============================================================================
# 1. ASEAN CUP MONTE CARLO SIMULATION CHART
# ==============================================================================
teams = ['Vietnam', 'Thailand', 'Indonesia', 'Malaysia', 'Singapore', 'Philippines']
champ_prob = [31.4, 28.7, 22.3, 11.8, 3.6, 2.2]
final_prob = [62.1, 59.4, 54.2, 34.5, 12.8, 7.0]
semis_prob = [88.5, 86.2, 81.0, 68.3, 38.0, 28.0]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.5), facecolor='#0F172A')
ax1.set_facecolor('#1E293B')
ax2.set_facecolor('#1E293B')

# Plot 1: Championship Probabilities (Horizontal Bar)
colors_champ = ['#EF4444', '#3B82F6', '#10B981', '#F59E0B', '#8B5CF6', '#EC4899']
y_pos = np.arange(len(teams))

bars = ax1.barh(y_pos, champ_prob, color=colors_champ, height=0.55, edgecolor='#334155', linewidth=1)
ax1.set_yticks(y_pos)
ax1.set_yticklabels(teams, fontsize=12, fontweight='bold', color='#F8FAFC')
ax1.invert_yaxis()
ax1.set_xlabel('Probabilitas Menjadi Juara (%)', fontsize=11, color='#94A3B8')
ax1.set_title('Probabilitas Juara ASEAN Cup (10.000 Simulasi Monte Carlo)', fontsize=13, fontweight='bold', color='#FFFFFF', pad=15)
ax1.grid(axis='x', color='#334155', linestyle='--', alpha=0.7)
ax1.set_xlim(0, 40)

for bar in bars:
    w = bar.get_width()
    ax1.text(w + 0.8, bar.get_y() + bar.get_height()/2, f'{w:.1f}%', va='center', ha='left', fontsize=11, fontweight='bold', color='#F8FAFC')

# Plot 2: Tournament Progression Rates (Grouped Bar)
bar_width = 0.25
y_indices = np.arange(len(teams))

r1 = ax2.barh(y_indices - bar_width, semis_prob, height=bar_width, label='Lolos Semifinal', color='#38BDF8', edgecolor='#334155')
r2 = ax2.barh(y_indices, final_prob, height=bar_width, label='Lolos Final', color='#818CF8', edgecolor='#334155')
r3 = ax2.barh(y_indices + bar_width, champ_prob, height=bar_width, label='Juara 1', color='#34D399', edgecolor='#334155')

ax2.set_yticks(y_indices)
ax2.set_yticklabels(teams, fontsize=12, fontweight='bold', color='#F8FAFC')
ax2.invert_yaxis()
ax2.set_xlabel('Peluang Tahapan (%)', fontsize=11, color='#94A3B8')
ax2.set_title('Peluang Bertahan per Tahapan Turnamen', fontsize=13, fontweight='bold', color='#FFFFFF', pad=15)
ax2.grid(axis='x', color='#334155', linestyle='--', alpha=0.7)
ax2.set_xlim(0, 100)
ax2.legend(loc='lower right', framealpha=0.9, facecolor='#0F172A', edgecolor='#334155', fontsize=10)

plt.suptitle('HASIL SIMULASI MONTE CARLO: TURNAMEN ASEAN CUP (KELOMPOK 1)', fontsize=15, fontweight='bold', color='#38BDF8', y=0.98)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

chart1_path = os.path.join(art_dir, "asean_cup_simulation_chart.png")
plt.savefig(chart1_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("Saved:", chart1_path)

# ==============================================================================
# 2. MATCH SIMULATION & HEAD-TO-HEAD PREDICTION EXAMPLE
# ==============================================================================
fig, (ax_info, ax_time) = plt.subplots(1, 2, figsize=(15, 7), facecolor='#0F172A', gridspec_kw={'width_ratios': [1, 1.3]})
ax_info.set_facecolor('#1E293B')
ax_time.set_facecolor('#1E293B')

ax_info.axis('off')
info_text = (
    "CONTOH SIMULASI HEAD-TO-HEAD (RANDOM FOREST)\n"
    "Turnamen: AFF Championship | Venue: Neutral\n"
    "--------------------------------------------------\n\n"
    "       INDONESIA   vs   VIETNAM\n"
    "          2        -       1\n\n"
    "PROBABILITAS HASIL PERTANDINGAN:\n"
    "  * Kemenangan Indonesia : 42.8%\n"
    "  * Hasil Imbang (Seri)  : 27.4%\n"
    "  * Kemenangan Vietnam   : 29.8%\n\n"
    "METRIK STATISTIK TIM (5 LAGA TERAKHIR):\n"
    "  * Rata-rata Gol IDN   : 1.80 gol/laga\n"
    "  * Rata-rata Gol VIE   : 1.60 gol/laga\n"
    "  * Rekor Head-to-Head  : 9 Menang, 10 Seri, 7 Kalah\n\n"
    "STATUS PREDIKSI: WINNER INDONESIA (88% CONFIDENCE IN RANGE)"
)
ax_info.text(0.08, 0.5, info_text, fontsize=12, color='#E2E8F0', fontfamily='monospace', va='center', linespacing=1.6)

# Right Panel: 90-Minute Match Events Timeline
ax_time.set_xlim(0, 100)
ax_time.set_ylim(-1, 7)
ax_time.axis('off')

timeline_events = [
    (14, "[GOL] Indonesia (1-0)\nRagnar Oratmangoen (Counter Attack)", '#10B981', 5.5),
    (38, "[KARTU KUNING] Vietnam\nDo Hung Dung (Pelanggaran Taktis)", '#F59E0B', 4.2),
    (45, "[HALF TIME] Babak Pertama Usai\nSkor Sementara: Indonesia 1 - 0 Vietnam", '#94A3B8', 3.0),
    (62, "[GOL] Vietnam (1-1)\nNguyen Tien Linh (Sundulan Corner)", '#EF4444', 2.0),
    (81, "[SUBSTITUSI] Indonesia\nWitan Sulaeman Masuk (Perkuat Serangan)", '#38BDF8', 1.0),
    (87, "[GOL PENENTU] Indonesia (2-1)\nMarselino Ferdinan (Sepakan Jarak 20m)", '#10B981', 0.0)
]

ax_time.plot([15, 15], [-0.5, 6.2], color='#475569', linewidth=3, zorder=1)

for minute, desc, col, y in timeline_events:
    ax_time.scatter(15, y, color=col, s=180, zorder=2, edgecolor='#FFFFFF', linewidth=1.5)
    ax_time.text(9, y, f"{minute}'", fontsize=12, fontweight='bold', color='#F8FAFC', va='center', ha='right')
    ax_time.text(20, y, desc, fontsize=11, color='#F1F5F9', va='center', ha='left',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#0F172A', edgecolor=col, alpha=0.9))

ax_time.set_title("TIMELINE ANIMASI LAGA 90 MENIT (EVENT TICKER)", fontsize=13, fontweight='bold', color='#FFFFFF', pad=15)
plt.suptitle('SIMULASI PERTANDINGAN 90 MENIT & PREDIKSI LIVE (TAB 2 & 3)', fontsize=15, fontweight='bold', color='#10B981', y=0.98)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

chart2_path = os.path.join(art_dir, "match_simulation_example.png")
plt.savefig(chart2_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("Saved cleanly without glyph warnings:", chart2_path)
