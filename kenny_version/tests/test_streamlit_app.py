"""
# ==============================================================================
# [MODULE GOAL & ROLE]
#   Automated Test Suite for Streamlit Dashboard Functions & Dynamic Engine
#   Fulfills:
#     - Acceptance Criteria of MSIB Fast Track Batch 10 (Kelompok 1 AI)
#     - Verifies 100% genuine dynamic calculations in `app/streamlit_app.py`
#     - Tests model inference, feature engineering, CSV ingestion, and Monte Carlo simulation
#
# [INTENTIONAL DESIGN DECISIONS - DO NOT REMOVE]
#   - 100% headless test execution without browser dependency.
#   - Strict probability bounds verification (0.0 <= P <= 100.0, sum ~ 100.0%).
#   - Edge case validation: invalid CSV columns, neutral venue symmetry, and slider offsets.
# ==============================================================================
"""

import unittest
import os
import io
import pandas as pd
import numpy as np

import app.streamlit_app as sapp


class TestStreamlitAppHelpers(unittest.TestCase):
    """Test suite for Streamlit dashboard core logic and helper functions."""

    @classmethod
    def setUpClass(cls):
        cls.bundle = sapp.load_model_bundle()
        cls.artifacts = sapp.load_artifacts()
        cls.stats = cls.artifacts['team_stats']
        cls.h2h = cls.artifacts['h2h_registry']
        cls.model = cls.bundle['model']
        cls.cols = cls.bundle['feature_cols']

    def test_load_artifacts_and_model_integrity(self):
        """Verify model bundle and artifacts load with expected keys and column counts."""
        self.assertIn('model', self.bundle)
        self.assertIn('feature_cols', self.bundle)
        self.assertEqual(len(self.cols), 24)
        
        self.assertIn('team_stats', self.artifacts)
        self.assertIn('h2h_registry', self.artifacts)
        self.assertIn('model_evaluation', self.artifacts)
        self.assertIn('simulation_results', self.artifacts)
        self.assertGreater(len(self.stats), 200)

    def test_compute_match_features_shape_and_columns(self):
        """Verify feature vector matches expected schema and column ordering."""
        df_feat, h_s, a_s, h2h_info = sapp.compute_match_features(
            home_team="Indonesia",
            away_team="Thailand",
            is_neutral=False,
            is_friendly=False,
            team_stats=self.stats,
            h2h_registry=self.h2h,
            feature_cols=self.cols
        )
        self.assertEqual(len(df_feat), 1)
        self.assertEqual(list(df_feat.columns), self.cols)
        self.assertFalse(df_feat.isnull().values.any())

    def test_dynamic_elo_adjustment_impact(self):
        """Verify that positive home Elo slider adjustment increases Home Win probability."""
        # Baseline (0 offset)
        df_base, h_s, a_s, _ = sapp.compute_match_features(
            "Indonesia", "Thailand", False, False, self.stats, self.h2h, self.cols,
            home_elo_adj=0.0
        )
        pred_base = sapp.predict_match_outcome(self.model, df_base, h_s, a_s, False)
        
        # Boosted home Elo (+150 offset)
        df_boost, _, _, _ = sapp.compute_match_features(
            "Indonesia", "Thailand", False, False, self.stats, self.h2h, self.cols,
            home_elo_adj=150.0
        )
        pred_boost = sapp.predict_match_outcome(self.model, df_boost, h_s, a_s, False)
        
        p_home_base = pred_base['probabilities']['home_win']
        p_home_boost = pred_boost['probabilities']['home_win']
        
        self.assertGreater(p_home_boost, p_home_base, "Boosting Home Elo must increase Home Win probability")

    def test_neutral_venue_toggle_impact(self):
        """Verify that neutral venue toggle removes home advantage and lowers Home Win chance."""
        # Non-neutral match (home advantage active)
        df_home, h_s, a_s, _ = sapp.compute_match_features(
            "Indonesia", "Thailand", False, False, self.stats, self.h2h, self.cols
        )
        pred_home = sapp.predict_match_outcome(self.model, df_home, h_s, a_s, False)
        
        # Neutral match (home advantage removed)
        df_neutral, _, _, _ = sapp.compute_match_features(
            "Indonesia", "Thailand", True, False, self.stats, self.h2h, self.cols
        )
        pred_neutral = sapp.predict_match_outcome(self.model, df_neutral, h_s, a_s, True)
        
        self.assertGreater(
            pred_home['probabilities']['home_win'],
            pred_neutral['probabilities']['home_win'],
            "Home venue must provide higher win probability than neutral ground"
        )

    def test_form_points_override_impact(self):
        """Verify that modifying recent form points changes form difference and dynamically shifts probabilities."""
        # Low form (0 pts in last 5 matches)
        df_low, h_s, a_s, _ = sapp.compute_match_features(
            "Indonesia", "Thailand", False, False, self.stats, self.h2h, self.cols,
            home_form_override=0
        )
        pred_low = sapp.predict_match_outcome(self.model, df_low, h_s, a_s, False)
        
        # High form (15 pts in last 5 matches)
        df_high, _, _, _ = sapp.compute_match_features(
            "Indonesia", "Thailand", False, False, self.stats, self.h2h, self.cols,
            home_form_override=15
        )
        pred_high = sapp.predict_match_outcome(self.model, df_high, h_s, a_s, False)
        
        # Feature delta must be exactly 15
        self.assertEqual(df_high['diff_form_pts'].values[0] - df_low['diff_form_pts'].values[0], 15.0)
        
        # Probabilities must dynamically shift
        self.assertNotEqual(
            pred_high['probabilities']['home_win'],
            pred_low['probabilities']['home_win'],
            "Form points adjustment must dynamically shift model output probabilities"
        )

    def test_predict_match_outcome_bounds_and_format(self):
        """Verify probability calibration bounds and scoreline output format."""
        df_feat, h_s, a_s, _ = sapp.compute_match_features(
            "Vietnam", "Malaysia", False, False, self.stats, self.h2h, self.cols
        )
        pred = sapp.predict_match_outcome(self.model, df_feat, h_s, a_s, False)
        
        probs = pred['probabilities']
        for k in ['home_win', 'draw', 'away_win']:
            self.assertIn(k, probs)
            self.assertGreaterEqual(probs[k], 0.0)
            self.assertLessEqual(probs[k], 100.0)
            
        prob_sum = probs['home_win'] + probs['draw'] + probs['away_win']
        self.assertAlmostEqual(prob_sum, 100.0, delta=0.5)
        
        # Expected score format verification (e.g. "2 - 1")
        parts = pred['expected_score'].split(" - ")
        self.assertEqual(len(parts), 2)
        self.assertTrue(parts[0].isdigit() and parts[1].isdigit())

    def test_generate_sample_csv_template(self):
        """Verify sample CSV template is valid and parseable by pandas."""
        csv_str = sapp.generate_sample_csv_template()
        df = pd.read_csv(io.StringIO(csv_str))
        self.assertGreaterEqual(len(df), 5)
        for col in ['date', 'home_team', 'away_team', 'home_score', 'away_score']:
            self.assertIn(col, df.columns)

    def test_process_uploaded_csv_valid_data(self):
        """Verify uploading match CSV updates Elo ratings and produces chronological progression."""
        csv_str = sapp.generate_sample_csv_template()
        df_upload = pd.read_csv(io.StringIO(csv_str))
        
        processed_df, updated_stats, count = sapp.process_uploaded_csv(df_upload, self.stats)
        
        self.assertEqual(count, len(df_upload))
        self.assertIn('home_elo_pre', processed_df.columns)
        self.assertIn('home_elo_post', processed_df.columns)
        self.assertIn('away_elo_pre', processed_df.columns)
        self.assertIn('away_elo_post', processed_df.columns)
        
        # Check that Indonesia and Cambodia stats were updated
        self.assertIn('Indonesia', updated_stats)
        self.assertIn('Cambodia', updated_stats)
        self.assertGreater(updated_stats['Indonesia']['matches'], self.stats['Indonesia']['matches'])

    def test_process_uploaded_csv_missing_mandatory_columns(self):
        """Verify that uploading CSV without mandatory columns raises ValueError."""
        invalid_df = pd.DataFrame({
            'team_a': ['Indonesia'],
            'team_b': ['Thailand'],
            'score': ['2-1']
        })
        with self.assertRaises(ValueError):
            sapp.process_uploaded_csv(invalid_df, self.stats)

    def test_interactive_tournament_simulation_runs(self):
        """Verify Monte Carlo simulation returns valid leaderboard across all 10 ASEAN nations."""
        sim_res = sapp.run_interactive_tournament_simulation(
            iterations=150,
            team_stats=self.stats,
            h2h_registry=self.h2h,
            model=self.model,
            feature_cols=self.cols,
            seed=42
        )
        self.assertEqual(sim_res['iterations'], 150)
        lb = sim_res['leaderboard']
        self.assertEqual(len(lb), 10)
        
        total_champ_pct = sum(e['champion_pct'] for e in lb)
        self.assertAlmostEqual(total_champ_pct, 100.0, delta=1.5)
        
        # Top 4 nations must dominate the leaderboard
        top_teams = {e['team'] for e in lb[:4]}
        self.assertTrue('Thailand' in top_teams or 'Indonesia' in top_teams or 'Vietnam' in top_teams)
        
        # Check sample tournament structure
        sample = sim_res['sample_tournament']
        self.assertIn('group_a_standings', sample)
        self.assertIn('group_b_standings', sample)
        self.assertIn('semi_finals', sample)
        self.assertIn('final', sample)


if __name__ == "__main__":
    unittest.main()
