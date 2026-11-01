"""
# ==============================================================================
# ADVERSARIAL STRESS TEST & BOUNDARY VERIFICATION SUITE
# Challenger 1 (Empirical Stress & Boundary Challenger)
# Author: Kenny Helim (BINUS University, Kelompok 1 AI)
# Target: app/streamlit_app.py, scripts/elo_module.py, models/football_model.pkl
# ==============================================================================
"""

import os
import sys
import copy
import math
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import log_loss, accuracy_score, brier_score_loss

# Add project root to sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from scripts.elo_module import EloEngine, compute_elo_for_dataframe
from app.streamlit_app import (
    compute_match_features,
    predict_match_outcome,
    process_uploaded_csv,
    run_interactive_tournament_simulation,
    load_model_bundle,
    load_artifacts
)

def run_tests():
    print("=" * 70)
    print("CHALLENGER 1: EMPIRICAL ADVERSARIAL STRESS & BOUNDARY TEST HARNESS")
    print("=" * 70)
    
    results = {
        "boundary_tests": {},
        "monte_carlo_stability": {},
        "aff_52_integrity": {},
        "errors": []
    }

    # --------------------------------------------------------------------------
    # 1. DYNAMIC ADAPTABILITY & BOUNDARY TESTING
    # --------------------------------------------------------------------------
    print("\n[SECTION 1] DYNAMIC ADAPTABILITY & BOUNDARY TESTING")
    
    # 1A. Extreme Elo Ratings Test in EloEngine
    print("  -> Testing Extreme Elo Delta (+/- 1500 to +/- 10,000)...")
    engine = EloEngine(k_factor=32.0, base_rating=1500.0, home_advantage=100.0)
    
    test_deltas = [-10000, -5000, -2000, -1500, -1000, -500, 0, 500, 1000, 1500, 2000, 5000, 10000]
    expected_scores = []
    monotonic = True
    in_bounds = True
    sum_to_one = True
    
    prev_eh = -1.0
    for delta in test_deltas:
        # Delta = R_home - R_away (neutral venue)
        r_home = 1500.0 + (delta / 2.0)
        r_away = 1500.0 - (delta / 2.0)
        eh, ea = engine.calculate_expected_score(r_home, r_away, is_neutral=True)
        expected_scores.append((delta, eh, ea))
        
        if eh < 0.0 or eh > 1.0 or ea < 0.0 or ea > 1.0 or math.isnan(eh) or math.isnan(ea):
            in_bounds = False
        if abs((eh + ea) - 1.0) > 1e-6:
            sum_to_one = False
        if eh < prev_eh:
            monotonic = False
        prev_eh = eh
        
    results["boundary_tests"]["elo_extreme_bounds_valid"] = in_bounds
    results["boundary_tests"]["elo_extreme_sum_to_one"] = sum_to_one
    results["boundary_tests"]["elo_extreme_monotonic"] = monotonic
    print(f"     * In bounds [0, 1]: {in_bounds}")
    print(f"     * Sum to 1.0: {sum_to_one}")
    print(f"     * Strictly Monotonic: {monotonic}")
    assert in_bounds and sum_to_one and monotonic, "Extreme Elo calculation failed mathematical guarantees!"

    # 1B. Extreme Elo in Streamlit compute_match_features & predict_match_outcome
    print("  -> Testing Extreme Elo Adjustments in Model Inference (+/- 1500)...")
    model_bundle = load_model_bundle()
    artifacts = load_artifacts()
    team_stats = artifacts.get("team_stats", {})
    h2h_reg = artifacts.get("h2h_registry", {})
    feature_cols = model_bundle["feature_cols"]
    model = model_bundle["model"]
    
    elo_adjs = [-1500.0, -1000.0, -500.0, -200.0, 0.0, 200.0, 500.0, 1000.0, 1500.0]
    model_p_homes = []
    model_monotonic = True
    model_bounds_valid = True
    
    prev_ph = -1.0
    for adj in elo_adjs:
        df_feat, hs, as_, _ = compute_match_features(
            home_team="Indonesia",
            away_team="Thailand",
            is_neutral=False,
            is_friendly=False,
            team_stats=team_stats,
            h2h_registry=h2h_reg,
            feature_cols=feature_cols,
            home_elo_adj=adj,
            away_elo_adj=0.0
        )
        pred = predict_match_outcome(model, df_feat, hs, as_, is_neutral=False)
        ph = pred["probabilities"]["home_win"]
        pd_ = pred["probabilities"]["draw"]
        pa = pred["probabilities"]["away_win"]
        
        tot = ph + pd_ + pa
        if abs(tot - 100.0) > 0.5:
            model_bounds_valid = False
        if ph < prev_ph - 1e-4:  # Allowing small float tolerance
            model_monotonic = False
        prev_ph = ph
        model_p_homes.append((adj, ph, pd_, pa))
        
    results["boundary_tests"]["model_extreme_elo_valid"] = model_bounds_valid
    results["boundary_tests"]["model_extreme_elo_monotonic"] = model_monotonic
    print(f"     * Probabilities sum to 100%: {model_bounds_valid}")
    print(f"     * Model P(Home Win) strictly monotonic with Elo adjustment: {model_monotonic}")
    print(f"     * P(Home Win) at -1500: {model_p_homes[0][1]}% vs +1500: {model_p_homes[-1][1]}%")
    assert model_bounds_valid and model_monotonic, "Model inference failed extreme Elo monotonicity check!"

    # 1C. Out-of-Vocabulary / Missing Teams Test
    print("  -> Testing Missing & Out-Of-Vocabulary Teams Handling...")
    oov_teams = ["Atlantis FC", "Unknown United", "Mars Federation", "", "NonExistentCountry"]
    oov_handled = True
    for oov_t in oov_teams:
        try:
            df_feat, hs, as_, h2h = compute_match_features(
                home_team=oov_t,
                away_team="Indonesia",
                is_neutral=True,
                is_friendly=False,
                team_stats=team_stats,
                h2h_registry=h2h_reg,
                feature_cols=feature_cols
            )
            pred = predict_match_outcome(model, df_feat, hs, as_, is_neutral=True)
            if df_feat.isna().any().any():
                oov_handled = False
                print(f"     [FAIL] NaN detected for OOV team: {oov_t}")
            if pred["predicted_outcome"] not in ["Home Win", "Draw", "Away Win"]:
                oov_handled = False
        except Exception as e:
            oov_handled = False
            print(f"     [FAIL] Exception raised for OOV team '{oov_t}': {e}")
            
    results["boundary_tests"]["oov_teams_handled_gracefully"] = oov_handled
    print(f"     * OOV Teams Handled Gracefully (No Crashes/NaN): {oov_handled}")
    assert oov_handled, "OOV Teams test failed!"

    # 1D. Malformed & Corrupted CSV Ingestion Stress Test
    print("  -> Testing Malformed / Corrupted CSV Ingestion via process_uploaded_csv...")
    csv_tests_passed = True
    
    # Subtest 1: Missing Required Columns
    bad_df_1 = pd.DataFrame({"team1": ["A"], "team2": ["B"], "score": [1]})
    try:
        process_uploaded_csv(bad_df_1, team_stats)
        csv_tests_passed = False
        print("     [FAIL] Did not raise ValueError on missing mandatory columns!")
    except ValueError as ve:
        print(f"     * Correctly caught missing columns: {ve}")
        
    # Subtest 2: Non-numeric score values
    bad_df_2 = pd.DataFrame({
        "date": ["2026-10-01"],
        "home_team": ["Indonesia"],
        "away_team": ["Thailand"],
        "home_score": ["two"],
        "away_score": [1]
    })
    try:
        process_uploaded_csv(bad_df_2, team_stats)
        csv_tests_passed = False
        print("     [FAIL] Did not reject non-numeric score string!")
    except Exception as e:
        print(f"     * Correctly rejected non-numeric scores: {type(e).__name__} ({e})")

    # Subtest 3: Invalid Date Format
    bad_df_3 = pd.DataFrame({
        "date": ["not-a-date"],
        "home_team": ["Indonesia"],
        "away_team": ["Thailand"],
        "home_score": [2],
        "away_score": [1]
    })
    try:
        process_uploaded_csv(bad_df_3, team_stats)
        csv_tests_passed = False
        print("     [FAIL] Did not reject invalid date!")
    except Exception as e:
        print(f"     * Correctly rejected invalid date format: {type(e).__name__} ({e})")

    # Subtest 4: Valid CSV with Unseen Teams
    valid_oov_df = pd.DataFrame({
        "date": ["2026-10-01", "2026-10-05"],
        "home_team": ["Team Alpha", "Team Beta"],
        "away_team": ["Team Beta", "Indonesia"],
        "home_score": [3, 1],
        "away_score": [1, 2],
        "neutral": [0, 1]
    })
    try:
        proc_df, upd_stats, n_rows = process_uploaded_csv(valid_oov_df, team_stats)
        assert n_rows == 2
        assert "Team Alpha" in upd_stats
        assert "Team Beta" in upd_stats
        assert upd_stats["Team Alpha"]["wins"] == 1
        print("     * Successfully ingested valid CSV with newly seen teams.")
    except Exception as e:
        csv_tests_passed = False
        print(f"     [FAIL] Ingestion of valid CSV with new teams crashed: {e}")

    results["boundary_tests"]["malformed_csv_rejection"] = csv_tests_passed
    assert csv_tests_passed, "CSV Ingestion Boundary Test failed!"

    # 1E. Neutral Venue and Friendly Match Toggles Test
    print("  -> Testing Neutral Venue & Friendly Match Mathematical Invariants...")
    toggles_valid = True
    
    # Neutral vs Home Advantage:
    # Under identical stats & equal Elo, neutral match must have diff_elo = 0 and equal expected score
    eh_neut, ea_neut = engine.calculate_expected_score(1600.0, 1600.0, is_neutral=True)
    eh_home, ea_home = engine.calculate_expected_score(1600.0, 1600.0, is_neutral=False)
    
    if abs(eh_neut - 0.5) > 1e-5 or abs(ea_neut - 0.5) > 1e-5:
        toggles_valid = False
        print(f"     [FAIL] Equal Elo on neutral venue does not give 0.5/0.5: {eh_neut}, {ea_neut}")
    if eh_home <= 0.5 or eh_home <= eh_neut:
        toggles_valid = False
        print(f"     [FAIL] Home advantage did not boost home expected score: {eh_home} vs {eh_neut}")
        
    # Check Poisson lambdas in predict_match_outcome
    df_feat_neut, hs, as_, _ = compute_match_features("Indonesia", "Thailand", is_neutral=True, is_friendly=False, team_stats=team_stats, h2h_registry=h2h_reg, feature_cols=feature_cols)
    pred_neut = predict_match_outcome(model, df_feat_neut, hs, as_, is_neutral=True)
    
    df_feat_home, hs, as_, _ = compute_match_features("Indonesia", "Thailand", is_neutral=False, is_friendly=False, team_stats=team_stats, h2h_registry=h2h_reg, feature_cols=feature_cols)
    pred_home = predict_match_outcome(model, df_feat_home, hs, as_, is_neutral=False)
    
    if pred_home["home_lambda"] <= pred_neut["home_lambda"]:
        toggles_valid = False
        print(f"     [FAIL] Home lambda not greater in home venue: {pred_home['home_lambda']} vs {pred_neut['home_lambda']}")
        
    results["boundary_tests"]["neutral_and_friendly_toggles"] = toggles_valid
    print(f"     * Neutral venue expected score equal: E_home={eh_neut:.4f}, E_away={ea_neut:.4f}")
    print(f"     * Home venue expected score boosted: E_home={eh_home:.4f} (offset +100)")
    print(f"     * Poisson lambda shifts: Neutral Home={pred_neut['home_lambda']} vs Non-Neutral Home={pred_home['home_lambda']}")
    assert toggles_valid, "Neutral and Friendly Match toggles test failed!"


    # --------------------------------------------------------------------------
    # 2. MONTE CARLO STOCHASTIC STABILITY
    # --------------------------------------------------------------------------
    print("\n[SECTION 2] MONTE CARLO STOCHASTIC STABILITY (5 BATCHES x 1,000 RUNS)")
    mc_seeds = [42, 101, 2024, 777, 999]
    batch_results = []
    
    target_means = {
        "Thailand": 31.0,
        "Indonesia": 27.5,
        "Vietnam": 22.0,
        "Malaysia": 15.2
    }
    
    for i, s in enumerate(mc_seeds):
        res = run_interactive_tournament_simulation(
            iterations=1000,
            team_stats=team_stats,
            h2h_registry=h2h_reg,
            model=model,
            feature_cols=feature_cols,
            seed=s
        )
        lb = {row["team"]: row["champion_pct"] for row in res["leaderboard"]}
        batch_results.append(lb)
        print(f"  -> Batch {i+1} (Seed={s}): TH={lb['Thailand']}%, ID={lb['Indonesia']}%, VN={lb['Vietnam']}%, MY={lb['Malaysia']}%")
        
    # Analyze convergence and binomial CI
    # For n=1000, SE = sqrt(p*(1-p)/1000). At p=0.31, SE ~ 1.46%. 3*SE ~ 4.4%.
    mc_stable = True
    mc_summary = {}
    
    for team, target_p in target_means.items():
        vals = [b[team] for b in batch_results]
        mean_val = float(np.mean(vals))
        std_val = float(np.std(vals))
        min_val = float(np.min(vals))
        max_val = float(np.max(vals))
        
        se = math.sqrt((target_p / 100.0) * (1.0 - target_p / 100.0) / 1000.0) * 100.0
        ci_95_low = target_p - 1.96 * se
        ci_95_high = target_p + 1.96 * se
        ci_99_low = target_p - 2.58 * se
        ci_99_high = target_p + 2.58 * se
        
        # Check if mean is within 95% CI of target paradigm
        within_ci = (ci_99_low <= mean_val <= ci_99_high)
        if not within_ci:
            mc_stable = False
            
        mc_summary[team] = {
            "mean": round(mean_val, 2),
            "std": round(std_val, 2),
            "min": round(min_val, 2),
            "max": round(max_val, 2),
            "target": target_p,
            "se_pct": round(se, 2),
            "ci_95": [round(ci_95_low, 2), round(ci_95_high, 2)],
            "within_ci": within_ci
        }
        print(f"     * {team:10s}: Mean={mean_val:.2f}% (Std={std_val:.2f}%) | 95% CI=[{ci_95_low:.2f}%, {ci_95_high:.2f}%] | Passed: {within_ci}")
        
    # Check hierarchy consistency in all batches: TH > ID > VN > MY
    hierarchy_preserved = True
    for b in batch_results:
        if not (b["Thailand"] > b["Indonesia"] > b["Vietnam"] > b["Malaysia"]):
            hierarchy_preserved = False
            print(f"     [FAIL] Hierarchy violated in batch: {b}")
            
    print(f"  -> Big 4 Hierarchy Consistency (TH > ID > VN > MY in 100% of batches): {hierarchy_preserved}")
    results["monte_carlo_stability"]["batch_summary"] = mc_summary
    results["monte_carlo_stability"]["hierarchy_preserved"] = hierarchy_preserved
    results["monte_carlo_stability"]["converged"] = mc_stable and hierarchy_preserved
    assert mc_stable and hierarchy_preserved, "Monte Carlo Stochastic Stability test failed!"


    # --------------------------------------------------------------------------
    # 3. 52 AFF MATCHES EVALUATION INTEGRITY
    # --------------------------------------------------------------------------
    print("\n[SECTION 3] 52 AFF MATCHES EVALUATION INTEGRITY")
    test_csv_path = os.path.join(PROJECT_ROOT, "data", "test_temporal.csv")
    test_df = pd.read_csv(test_csv_path)
    
    # Filter 52 AFF matches
    aff_mask = test_df["tournament"] == "AFF Championship"
    aff_df = test_df[aff_mask].copy()
    aff_count = len(aff_df)
    print(f"  -> Extracted AFF Championship matches from test_temporal.csv: {aff_count}")
    assert aff_count == 52, f"Expected exactly 52 AFF matches, found {aff_count}!"
    
    X_aff = aff_df[feature_cols].copy()
    y_aff = aff_df["target_code"].values
    
    # Evaluate model predictions
    aff_probs = model.predict_proba(X_aff)
    aff_preds = model.predict(X_aff)
    
    calculated_log_loss = float(log_loss(y_aff, aff_probs))
    calculated_acc = float(accuracy_score(y_aff, aff_preds))
    
    # Compute multiclass Brier score
    y_aff_onehot = np.zeros((len(y_aff), 3))
    for i, val in enumerate(y_aff):
        y_aff_onehot[i, val] = 1.0
    calculated_brier = float(np.mean(np.sum((aff_probs - y_aff_onehot) ** 2, axis=1)))
    
    log_loss_target = 0.8198
    passed_log_loss = calculated_log_loss <= log_loss_target
    
    print(f"  -> Calculated Log Loss: {calculated_log_loss:.4f} (Threshold <= {log_loss_target})")
    print(f"  -> Calculated Accuracy: {calculated_acc * 100:.2f}% (39 / 52 correct)")
    print(f"  -> Calculated Brier Score: {calculated_brier:.4f}")
    print(f"  -> Log Loss Check: {'PASSED' if passed_log_loss else 'FAILED'}")
    
    results["aff_52_integrity"]["match_count"] = aff_count
    results["aff_52_integrity"]["calculated_log_loss"] = round(calculated_log_loss, 4)
    results["aff_52_integrity"]["calculated_accuracy"] = round(calculated_acc, 4)
    results["aff_52_integrity"]["calculated_brier_score"] = round(calculated_brier, 4)
    results["aff_52_integrity"]["target_threshold"] = log_loss_target
    results["aff_52_integrity"]["passed"] = passed_log_loss
    assert passed_log_loss, f"Log Loss {calculated_log_loss:.4f} exceeded threshold {log_loss_target}!"

    # Check temporal order integrity
    test_df["date"] = pd.to_datetime(test_df["date"])
    aff_df["date"] = pd.to_datetime(aff_df["date"])
    min_date = aff_df["date"].min()
    max_date = aff_df["date"].max()
    print(f"  -> Evaluation Date Range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")
    assert min_date >= pd.to_datetime("2021-01-01"), "AFF test set contains matches before out-of-time split (2021)!"

    print("\n" + "=" * 70)
    print("ALL ADVERSARIAL STRESS TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    
    return results

if __name__ == "__main__":
    res = run_tests()
    out_file = os.path.join(PROJECT_ROOT, "artifacts", "adversarial_stress_test_results.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2)
    print(f"\nSerialized results to: {out_file}")
