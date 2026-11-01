"""
# ==============================================================================
# [MODULE GOAL & ROLE]
#   School Football Prediction Project - Exploratory Data Analysis (EDA) Engine
#   Fulfills:
#     - Week 3 Assignment (Kelompok 1 AI: Prediksi Hasil & Probabilitas Juara ASEAN Cup)
#     - Slides 4, 5 of AI_Football_Prediction_Blueprint.pdf
#     - SDG 9 (Industry, Innovation, and Infrastructure)
#   Analyzes:
#     1. Target Distribution (Home Win / Draw / Away Win) & Home Advantage Bias
#     2. Actual Scale (Volume, Date Ranges 1872-Present, Zero Missing Values)
#     3. Goal Patterns (Historical Productivity, Era-by-Era Trends, Goal Difference)
#     4. Match Context (Tournament Type & Neutral Venue Impact)
#     5. ASEAN Football Deep-Dive (Indonesia, Thailand, Vietnam, Malaysia, etc.)
#
# [INTENTIONAL DESIGN DECISIONS - DO NOT REMOVE]
#   - Headless matplotlib backend ('Agg') for zero-crash execution.
#   - Generates high-res charts and comprehensive `eda_summary.json`.
#   - Detailed ASEAN team breakdowns for the tournament champion simulation.
#
# [SOLVED PAST MISTAKES & ANTIDOTES - NEVER REPEAT]
#   - Handles both global international matches and AFF Championship subsets cleanly.
#
# [SESSION REVISION & CHAT MILESTONE LEDGER]
#   - 2026-10-26: Initial implementation + ASEAN Cup specialization.
# ==============================================================================
"""

import os
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

ASEAN_TEAMS = [
    'Indonesia', 'Thailand', 'Vietnam', 'Malaysia', 
    'Singapore', 'Philippines', 'Myanmar', 'Cambodia', 
    'Laos', 'Brunei', 'Timor-Leste'
]

def run_eda(csv_path: str, output_dir: str):
    print("=" * 60)
    print("STARTING ADVANCED EDA PIPELINE (ASEAN CUP & GLOBAL FOOTBALL)")
    print("=" * 60)
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Load Data
    df = pd.read_csv(csv_path)
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['decade'] = (df['year'] // 10) * 10
    
    if df['neutral'].dtype == object:
        df['neutral'] = df['neutral'].astype(str).str.upper() == 'TRUE'
    else:
        df['neutral'] = df['neutral'].astype(bool)
        
    total_rows = len(df)
    missing_counts = df.isnull().sum().to_dict()
    min_date = df['date'].min().strftime('%Y-%m-%d')
    max_date = df['date'].max().strftime('%Y-%m-%d')
    all_teams = sorted(list(set(df['home_team'].unique()).union(set(df['away_team'].unique()))))
    unique_tournaments = df['tournament'].nunique()
    
    # 2. Target Formulation (W / D / L)
    conditions = [
        df['home_score'] > df['away_score'],
        df['home_score'] == df['away_score'],
        df['home_score'] < df['away_score']
    ]
    df['target'] = np.select(conditions, ['Home Win', 'Draw', 'Away Win'], default='Unknown')
    df['goal_diff'] = df['home_score'] - df['away_score']
    df['total_goals'] = df['home_score'] + df['away_score']
    
    target_counts = df['target'].value_counts()
    target_pct = (df['target'].value_counts(normalize=True) * 100).round(2)
    home_adv_ratio = target_pct.get('Home Win', 0) / max(0.001, target_pct.get('Away Win', 1))

    # 3. Goal Stats
    avg_home_goals = df['home_score'].mean()
    avg_away_goals = df['away_score'].mean()
    avg_total_goals = df['total_goals'].mean()
    
    # 4. Neutral Venue & Friendly
    neutral_grp = df.groupby('neutral')['target'].value_counts(normalize=True).unstack() * 100
    df['is_friendly'] = df['tournament'] == 'Friendly'
    friendly_grp = df.groupby('is_friendly')['target'].value_counts(normalize=True).unstack() * 100

    # 5. ASEAN Subset Analysis
    df_asean = df[(df['home_team'].isin(ASEAN_TEAMS)) | (df['away_team'].isin(ASEAN_TEAMS))].copy()
    print(f"Total ASEAN Matches in History: {len(df_asean):,}")
    
    asean_stats = {}
    for team in ASEAN_TEAMS:
        home_m = df[df['home_team'] == team]
        away_m = df[df['away_team'] == team]
        
        total_m = len(home_m) + len(away_m)
        if total_m == 0:
            continue
            
        wins = (home_m['home_score'] > home_m['away_score']).sum() + (away_m['away_score'] > away_m['home_score']).sum()
        draws = (home_m['home_score'] == home_m['away_score']).sum() + (away_m['away_score'] == away_m['home_score']).sum()
        losses = (home_m['home_score'] < home_m['away_score']).sum() + (away_m['away_score'] < away_m['home_score']).sum()
        gf = home_m['home_score'].sum() + away_m['away_score'].sum()
        ga = home_m['away_score'].sum() + away_m['home_score'].sum()
        
        asean_stats[team] = {
            'matches': int(total_m),
            'wins': int(wins),
            'draws': int(draws),
            'losses': int(losses),
            'win_rate': round(float(wins / total_m), 4),
            'goals_for': int(gf),
            'goals_against': int(ga),
            'avg_gf': round(float(gf / total_m), 2),
            'avg_ga': round(float(ga / total_m), 2)
        }

    # --- PLOT 1: Global Target Distribution ---
    plt.figure(figsize=(9, 5), dpi=150)
    palette = ['#10B981', '#F59E0B', '#EF4444']
    bars = plt.bar(['Home Win', 'Draw', 'Away Win'], 
                   [target_counts.get('Home Win', 0), target_counts.get('Draw', 0), target_counts.get('Away Win', 0)],
                   color=palette, width=0.55, edgecolor='#1E293B', linewidth=1.5)
    for bar in bars:
        yval = bar.get_height()
        pct = (yval / total_rows) * 100
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 500, f"{yval:,}\n({pct:.1f}%)", 
                 ha='center', va='bottom', fontsize=11, fontweight='bold', color='#1E293B')
    plt.title("Distribusi Hasil Pertandingan Internasional (1872 - 2026)", fontsize=13, fontweight='bold', pad=15)
    plt.xlabel("Hasil Laga (Target)", fontsize=11, fontweight='bold')
    plt.ylabel("Jumlah Laga", fontsize=11, fontweight='bold')
    plt.ylim(0, max(target_counts) * 1.15)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "eda_target_distribution.png"))
    plt.close()

    # --- PLOT 2: Goals & Era Trends ---
    era_stats = df.groupby('decade').agg(
        avg_goals=('total_goals', 'mean'),
        match_count=('total_goals', 'count')
    ).reset_index()
    era_stats = era_stats[era_stats['decade'] >= 1880]

    fig, ax1 = plt.subplots(figsize=(11, 5), dpi=150)
    ax2 = ax1.twinx()
    ax2.bar(era_stats['decade'], era_stats['match_count'], width=6, color='#94A3B8', alpha=0.35, label='Volume Laga')
    ax2.set_ylabel("Jumlah Laga per Dekade", fontsize=10, fontweight='bold', color='#64748B')
    ax1.plot(era_stats['decade'], era_stats['avg_goals'], color='#2563EB', marker='o', linewidth=2.5, markersize=5, label='Rata-rata Gol/Laga')
    ax1.set_ylabel("Rata-rata Gol/Laga", fontsize=10, fontweight='bold', color='#1D4ED8')
    ax1.set_xlabel("Dekade", fontsize=10, fontweight='bold')
    ax1.set_title("Evolusi Produktivitas Gol & Volume Pertandingan Berdasarkan Dekade", fontsize=13, fontweight='bold', pad=15)
    ax1.grid(True, linestyle='--', alpha=0.4)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right', frameon=True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "eda_goals_and_era_trends.png"))
    plt.close()

    # --- PLOT 3: Neutral Venue Impact ---
    neutral_compare = df.groupby('neutral')['target'].value_counts(normalize=True).unstack() * 100
    neutral_compare = neutral_compare[['Home Win', 'Draw', 'Away Win']]
    neutral_compare.index = ['Kandang Normal (False)', 'Venue Netral (True)']
    ax = neutral_compare.plot(kind='bar', figsize=(9, 5), color=['#10B981', '#F59E0B', '#EF4444'], 
                              edgecolor='#1E293B', linewidth=1, rot=0)
    plt.title("Pengaruh Status Venue Netral terhadap Distribusi Hasil Pertandingan", fontsize=13, fontweight='bold', pad=15)
    plt.xlabel("Status Venue Netral", fontsize=10, fontweight='bold')
    plt.ylabel("Persentase (%)", fontsize=10, fontweight='bold')
    plt.ylim(0, 60)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.legend(title="Hasil Laga", frameon=True)
    for p in ax.patches:
        height = p.get_height()
        if height > 0:
            ax.annotate(f"{height:.1f}%", (p.get_x() + p.get_width() / 2., height + 1),
                        ha='center', va='bottom', fontsize=9, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "eda_match_context_and_neutral.png"))
    plt.close()

    # --- PLOT 4: ASEAN Team Historical Win Rates ---
    sorted_asean = sorted(asean_stats.items(), key=lambda x: x[1]['win_rate'], reverse=True)
    teams_lbl = [x[0] for x in sorted_asean]
    wr_vals = [x[1]['win_rate'] * 100 for x in sorted_asean]
    matches_vals = [x[1]['matches'] for x in sorted_asean]

    plt.figure(figsize=(11, 5), dpi=150)
    colors = ['#10B981' if t == 'Indonesia' else '#3B82F6' for t in teams_lbl]
    bars = plt.bar(teams_lbl, wr_vals, color=colors, width=0.6, edgecolor='#1E293B', linewidth=1.2)
    plt.title("Rasio Kemenangan Historis Tim Nasional ASEAN (1872 - 2026)", fontsize=13, fontweight='bold', pad=15)
    plt.xlabel("Negara ASEAN", fontsize=10, fontweight='bold')
    plt.ylabel("Win Rate (%)", fontsize=10, fontweight='bold')
    plt.xticks(rotation=30, ha='right', fontsize=9)
    plt.ylim(0, max(wr_vals) * 1.2)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    
    for bar, m in zip(bars, matches_vals):
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 1, f"{yval:.1f}%\n({m} laga)", 
                 ha='center', va='bottom', fontsize=8, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "eda_asean_performance.png"))
    plt.close()

    # 6. Export Full JSON Summary
    summary_data = {
        "project_info": {
            "title": "Prediksi Hasil Pertandingan dan Probabilitas Juara ASEAN Cup",
            "group": "Kelompok 1 - Divisi Artificial Intelligence",
            "sdg_target": "SDG 9: Industri, Inovasi, dan Infrastruktur",
            "members": [
                {"name": "Kenny Helim", "major": "Information Systems & Management", "univ": "BINUS University"},
                {"name": "Arya Wicaksana", "major": "Teknik Informatika", "univ": "Universitas Esa Unggul"},
                {"name": "Muhammad Ihram Syahputra", "major": "Ilmu Komputer", "univ": "Universitas Halu Oleo"},
                {"name": "Gisela Venska Millennia", "major": "Information System", "univ": "President University"},
                {"name": "Christian", "major": "Information Systems", "univ": "BINUS University"}
            ],
            "dataset_source": "Kaggle (martj42) & Historical International Football"
        },
        "dataset_metadata": {
            "total_matches": int(total_rows),
            "date_range": [min_date, max_date],
            "unique_teams_count": len(all_teams),
            "unique_tournaments_count": int(unique_tournaments),
            "asean_matches_count": len(df_asean),
            "missing_values": missing_counts
        },
        "target_distribution": {
            "home_win": {"count": int(target_counts.get('Home Win', 0)), "pct": float(target_pct.get('Home Win', 0))},
            "draw": {"count": int(target_counts.get('Draw', 0)), "pct": float(target_pct.get('Draw', 0))},
            "away_win": {"count": int(target_counts.get('Away Win', 0)), "pct": float(target_pct.get('Away Win', 0))},
            "home_advantage_multiplier": round(home_adv_ratio, 2)
        },
        "goal_patterns": {
            "avg_home_goals": round(float(avg_home_goals), 2),
            "avg_away_goals": round(float(avg_away_goals), 2),
            "avg_total_goals": round(float(avg_total_goals), 2)
        },
        "neutral_venue_impact": {
            "normal_venue": {
                "home_win_pct": round(float(neutral_grp.loc[False, 'Home Win']), 2),
                "draw_pct": round(float(neutral_grp.loc[False, 'Draw']), 2),
                "away_win_pct": round(float(neutral_grp.loc[False, 'Away Win']), 2)
            },
            "neutral_venue": {
                "home_win_pct": round(float(neutral_grp.loc[True, 'Home Win']), 2),
                "draw_pct": round(float(neutral_grp.loc[True, 'Draw']), 2),
                "away_win_pct": round(float(neutral_grp.loc[True, 'Away Win']), 2)
            }
        },
        "asean_statistics": asean_stats,
        "all_teams_list": all_teams[:150]
    }
    
    json_path = os.path.join(output_dir, "eda_summary.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, indent=2)
    print(f"Saved upgraded EDA summary JSON: {json_path}")
    print("=" * 60)
    print("ADVANCED EDA PIPELINE COMPLETE!")
    print("=" * 60)

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_file = os.path.join(base_dir, "data", "results.csv")
    out_dir = os.path.join(base_dir, "artifacts")
    run_eda(csv_file, out_dir)
