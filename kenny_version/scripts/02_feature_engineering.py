"""
# ==============================================================================
# [MODULE GOAL & ROLE]
#   Anti-Leakage Temporal Feature Engineering Pipeline
#   Strictly enforces Slide 7 & Slide 10 of AI_Football_Prediction_Blueprint.pdf:
#   1. Rolling 5-game recent form (Points, Goals Scored, Goals Conceded)
#   2. Cumulative historical win rates & goal scoring/conceding averages
#   3. Prior Head-to-Head (H2H) record between the two teams
#   4. Strict chronological timeline barrier (Zero data leakage from future events)
#   5. Time-based chronological split (Train: 1960-2020, Test: 2021-2026)
#
# [INTENTIONAL DESIGN DECISIONS - DO NOT REMOVE]
#   - Features for match at index (i) are computed STRICTLY before updating team stats.
#   - Produces `latest_team_stats.json` capturing current team standings as of 2026
#     for live inferencing in the web app and simulation suite.
#
# [SOLVED PAST MISTAKES & ANTIDOTES - NEVER REPEAT]
#   - Avoided random train/test split which leaks future tactical knowledge into the past.
#   - Handled neutral venues explicitly in home advantage calculations.
#
# [SESSION REVISION & CHAT MILESTONE LEDGER]
#   - 2026-10-26: Initial implementation for Kenny's School ML Football Assignment.
#   - 2026-10-30: Milestone 2: Worker M2 integrated Dynamic Elo Rating Engine (R_new = R_old + K*(S-E)).
# ==============================================================================
"""

import os
import json
import pandas as pd
import numpy as np
from collections import defaultdict, deque
import sys

# Ensure parent directory is importable
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from scripts.elo_module import EloEngine

def extract_features(csv_path: str, output_dir: str):
    print("=" * 60)
    print("STARTING TEMPORAL FEATURE ENGINEERING (ZERO-LEAKAGE)")
    print("=" * 60)
    
    df = pd.read_csv(csv_path)
    df['date'] = pd.to_datetime(df['date'])
    # Strict chronological sorting
    df = df.sort_values(by='date').reset_index(drop=True)
    
    if df['neutral'].dtype == object:
        df['neutral'] = df['neutral'].astype(str).str.upper() == 'TRUE'
    else:
        df['neutral'] = df['neutral'].astype(bool)
        
    df['is_neutral'] = df['neutral'].astype(int)
    df['is_friendly'] = (df['tournament'] == 'Friendly').astype(int)
    
    # Target definition
    # 0: Away Win, 1: Draw, 2: Home Win
    conditions = [
        df['home_score'] > df['away_score'],
        df['home_score'] == df['away_score'],
        df['home_score'] < df['away_score']
    ]
    df['target_label'] = np.select(conditions, ['Home Win', 'Draw', 'Away Win'], default='Unknown')
    # Integer encoding for models: 2 for Home Win, 1 for Draw, 0 for Away Win
    df['target_code'] = np.select(conditions, [2, 1, 0], default=-1)

    # State stores for anti-leakage rolling tracking
    # For each team:
    #   'history': total_matches, wins, draws, losses, goals_for, goals_against
    #   'recent_5': deque of maxlen=5 containing (pts, scored, conceded)
    team_history = defaultdict(lambda: {
        'matches': 0, 'wins': 0, 'draws': 0, 'losses': 0,
        'goals_for': 0, 'goals_against': 0,
        'recent_5': deque(maxlen=5)
    })
    
    # H2H store: key = tuple(sorted([teamA, teamB])) -> {teamA_wins, teamB_wins, draws}
    h2h_history = defaultdict(lambda: {'teamA_wins': 0, 'teamB_wins': 0, 'draws': 0})
    
    # Dynamic Elo Engine (K=32, R0=1500, H=100)
    elo_engine = EloEngine(k_factor=32.0, base_rating=1500.0, home_advantage=100.0)
    
    feature_rows = []
    
    for idx, row in df.iterrows():
        h_team = row['home_team']
        a_team = row['away_team']
        h_score = row['home_score']
        a_score = row['away_score']
        is_neut = row['is_neutral']
        is_frie = row['is_friendly']
        date_val = row['date']
        
        # --- 1. EXTRACT PRE-MATCH FEATURES (Strictly before match is played!) ---
        h_stat = team_history[h_team]
        a_stat = team_history[a_team]
        
        # Historical win rates (prior to this match)
        h_hist_matches = h_stat['matches']
        a_hist_matches = a_stat['matches']
        
        h_hist_wr = (h_stat['wins'] / h_hist_matches) if h_hist_matches > 0 else 0.33
        a_hist_wr = (a_stat['wins'] / a_hist_matches) if a_hist_matches > 0 else 0.33
        
        h_hist_avg_gf = (h_stat['goals_for'] / h_hist_matches) if h_hist_matches > 0 else 1.5
        a_hist_avg_gf = (a_stat['goals_for'] / a_hist_matches) if a_hist_matches > 0 else 1.2
        
        h_hist_avg_ga = (h_stat['goals_against'] / h_hist_matches) if h_hist_matches > 0 else 1.2
        a_hist_avg_ga = (a_stat['goals_against'] / a_hist_matches) if a_hist_matches > 0 else 1.5
        
        # Recent 5 form
        h_rec = list(h_stat['recent_5'])
        a_rec = list(a_stat['recent_5'])
        
        h_rec_pts = sum(x[0] for x in h_rec) if len(h_rec) > 0 else 5 # default neutral baseline
        a_rec_pts = sum(x[0] for x in a_rec) if len(a_rec) > 0 else 5
        
        h_rec_gf = np.mean([x[1] for x in h_rec]) if len(h_rec) > 0 else 1.5
        a_rec_gf = np.mean([x[1] for x in a_rec]) if len(a_rec) > 0 else 1.2
        
        h_rec_ga = np.mean([x[2] for x in h_rec]) if len(h_rec) > 0 else 1.2
        a_rec_ga = np.mean([x[2] for x in a_rec]) if len(a_rec) > 0 else 1.5
        
        # Head to Head prior record
        h2h_key = tuple(sorted([h_team, a_team]))
        h2h_data = h2h_history[h2h_key]
        if h_team < a_team:
            h2h_h_wins = h2h_data['teamA_wins']
            h2h_a_wins = h2h_data['teamB_wins']
        else:
            h2h_h_wins = h2h_data['teamB_wins']
            h2h_a_wins = h2h_data['teamA_wins']
        h2h_draws = h2h_data['draws']
        h2h_total = h2h_h_wins + h2h_a_wins + h2h_draws
        h2h_h_win_rate = (h2h_h_wins / h2h_total) if h2h_total > 0 else 0.33
        
        # Comparative differential features
        diff_form_pts = h_rec_pts - a_rec_pts
        diff_hist_wr = h_hist_wr - a_hist_wr
        diff_goal_power = (h_hist_avg_gf - h_hist_avg_ga) - (a_hist_avg_gf - a_hist_avg_ga)
        diff_recent_gd = (h_rec_gf - h_rec_ga) - (a_rec_gf - a_rec_ga)
        
        # Dynamic Elo pre-match calculation (strict timeline barrier: zero future leakage)
        elo_feats = elo_engine.get_pre_match_features(h_team, a_team, is_neutral=bool(is_neut))
        
        feature_rows.append({
            'date': date_val,
            'year': date_val.year,
            'home_team': h_team,
            'away_team': a_team,
            'home_score': h_score,
            'away_score': a_score,
            'tournament': row['tournament'],
            'is_neutral': is_neut,
            'is_friendly': is_frie,
            'home_hist_matches': h_hist_matches,
            'away_hist_matches': a_hist_matches,
            'home_hist_wr': round(h_hist_wr, 4),
            'away_hist_wr': round(a_hist_wr, 4),
            'home_hist_avg_gf': round(h_hist_avg_gf, 4),
            'away_hist_avg_gf': round(a_hist_avg_gf, 4),
            'home_hist_avg_ga': round(h_hist_avg_ga, 4),
            'away_hist_avg_ga': round(a_hist_avg_ga, 4),
            'home_rec_pts_5': h_rec_pts,
            'away_rec_pts_5': a_rec_pts,
            'home_rec_avg_gf_5': round(float(h_rec_gf), 4),
            'away_rec_avg_gf_5': round(float(a_rec_gf), 4),
            'home_rec_avg_ga_5': round(float(h_rec_ga), 4),
            'away_rec_avg_ga_5': round(float(a_rec_ga), 4),
            'h2h_matches': h2h_total,
            'h2h_home_win_rate': round(h2h_h_win_rate, 4),
            'diff_form_pts': diff_form_pts,
            'diff_hist_wr': round(diff_hist_wr, 4),
            'diff_goal_power': round(diff_goal_power, 4),
            'diff_recent_gd': round(diff_recent_gd, 4),
            'home_elo': elo_feats['home_elo'],
            'away_elo': elo_feats['away_elo'],
            'diff_elo': elo_feats['diff_elo'],
            'elo_expected_home': elo_feats['elo_expected_home'],
            'elo_expected_away': elo_feats['elo_expected_away'],
            'target_label': row['target_label'],
            'target_code': row['target_code']
        })
        
        # --- 2. UPDATE HISTORICAL LEDGER (Now safe to register post-match) ---
        if h_score > a_score:
            h_pts, a_pts = 3, 0
            h_win, a_win = 1, 0
            h_draw, a_draw = 0, 0
            h_loss, a_loss = 0, 1
            if h_team < a_team:
                h2h_data['teamA_wins'] += 1
            else:
                h2h_data['teamB_wins'] += 1
        elif h_score == a_score:
            h_pts, a_pts = 1, 1
            h_win, a_win = 0, 0
            h_draw, a_draw = 1, 1
            h_loss, a_loss = 0, 0
            h2h_data['draws'] += 1
        else:
            h_pts, a_pts = 0, 3
            h_win, a_win = 0, 1
            h_draw, a_draw = 0, 0
            h_loss, a_loss = 1, 0
            if h_team < a_team:
                h2h_data['teamB_wins'] += 1
            else:
                h2h_data['teamA_wins'] += 1
                
        # Update home team record
        h_stat['matches'] += 1
        h_stat['wins'] += h_win
        h_stat['draws'] += h_draw
        h_stat['losses'] += h_loss
        h_stat['goals_for'] += h_score
        h_stat['goals_against'] += a_score
        h_stat['recent_5'].append((h_pts, h_score, a_score))
        
        # Update away team record
        a_stat['matches'] += 1
        a_stat['wins'] += a_win
        a_stat['draws'] += a_draw
        a_stat['losses'] += a_loss
        a_stat['goals_for'] += a_score
        a_stat['goals_against'] += h_score
        a_stat['recent_5'].append((a_pts, a_score, h_score))
        
        # Update dynamic Elo rating post-match
        elo_engine.update_ratings(h_team, a_team, h_score, a_score, is_neutral=bool(is_neut))

    feat_df = pd.DataFrame(feature_rows)
    print(f"Engineered {len(feat_df):,} chronological matches with zero leakage.")
    
    # Filter for mature era (1960 onwards) where both teams have sufficient established international data
    mature_df = feat_df[(feat_df['year'] >= 1960) & (feat_df['home_hist_matches'] >= 3) & (feat_df['away_hist_matches'] >= 3)].copy()
    print(f"Filtered modern football era (>=1960 & >=3 prior games): {len(mature_df):,} matches.")
    
    # Save full engineered dataset
    all_engineered_path = os.path.join(output_dir, "engineered_matches.csv")
    mature_df.to_csv(all_engineered_path, index=False)
    print(f"Saved: {all_engineered_path}")
    
    # Strict Time-Based Split (Slide 10)
    # Train: 1960 through 2020 (Historical Training Era)
    # Test: 2021 through 2026 (Recent Out-of-Time Validation Era)
    train_df = mature_df[mature_df['date'] < '2021-01-01'].copy()
    test_df = mature_df[mature_df['date'] >= '2021-01-01'].copy()
    
    train_path = os.path.join(output_dir, "train_temporal.csv")
    test_path = os.path.join(output_dir, "test_temporal.csv")
    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)
    
    print(f"Train matches (< 2021-01-01): {len(train_df):,} (from {train_df['date'].min().strftime('%Y-%m-%d')} to {train_df['date'].max().strftime('%Y-%m-%d')})")
    print(f"Test matches  (>= 2021-01-01): {len(test_df):,} (from {test_df['date'].min().strftime('%Y-%m-%d')} to {test_df['date'].max().strftime('%Y-%m-%d')})")

    # Serialize latest team states as of 2026 for live inference in Web App
    active_teams_dict = {}
    for team, stat in team_history.items():
        if stat['matches'] >= 10: # active international national team
            rec = list(stat['recent_5'])
            rec_pts = sum(x[0] for x in rec) if len(rec) > 0 else 5
            rec_gf = float(np.mean([x[1] for x in rec])) if len(rec) > 0 else 1.2
            rec_ga = float(np.mean([x[2] for x in rec])) if len(rec) > 0 else 1.2
            wr = round(stat['wins'] / stat['matches'], 4)
            avg_gf = round(stat['goals_for'] / stat['matches'], 4)
            avg_ga = round(stat['goals_against'] / stat['matches'], 4)
            team_elo = round(elo_engine.get_rating(team), 2)
            
            active_teams_dict[team] = {
                'matches': stat['matches'],
                'wins': stat['wins'],
                'draws': stat['draws'],
                'losses': stat['losses'],
                'win_rate': wr,
                'avg_goals_for': avg_gf,
                'avg_goals_against': avg_ga,
                'recent_pts_5': rec_pts,
                'recent_avg_gf_5': round(rec_gf, 2),
                'recent_avg_ga_5': round(rec_ga, 2),
                'elo': team_elo,
                'elo_rating': team_elo
            }
            
    artifacts_dir = os.path.join(os.path.dirname(output_dir), "artifacts")
    os.makedirs(artifacts_dir, exist_ok=True)
    latest_teams_path = os.path.join(artifacts_dir, "latest_team_stats.json")
    with open(latest_teams_path, 'w', encoding='utf-8') as f:
        json.dump(active_teams_dict, f, indent=2)
    print(f"Saved latest team states ({len(active_teams_dict)} teams) to: {latest_teams_path}")
    
    # Save H2H registry for quick lookups
    clean_h2h = {}
    for (t1, t2), record in h2h_history.items():
        if record['teamA_wins'] + record['teamB_wins'] + record['draws'] > 0:
            key_str = f"{t1} vs {t2}"
            clean_h2h[key_str] = {
                t1: record['teamA_wins'],
                t2: record['teamB_wins'],
                'draws': record['draws']
            }
    h2h_path = os.path.join(artifacts_dir, "h2h_registry.json")
    with open(h2h_path, 'w', encoding='utf-8') as f:
        json.dump(clean_h2h, f, indent=2)
    print(f"Saved H2H registry ({len(clean_h2h)} matchups) to: {h2h_path}")
    
    print("=" * 60)
    print("FEATURE ENGINEERING COMPLETE!")
    print("=" * 60)

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_file = os.path.join(base_dir, "data", "results.csv")
    data_out = os.path.join(base_dir, "data")
    extract_features(csv_file, data_out)
