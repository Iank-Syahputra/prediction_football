"""
# ==============================================================================
# Unit tests for Model Calibration & Tournament Simulation Artifacts
# Governed by Rule VQ-338 & Rule VQ-94
# ==============================================================================
"""

import os
import json
import unittest
import joblib
import pandas as pd
import numpy as np


class TestModelAndSimulation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cls.model_path = os.path.join(cls.base_dir, "models", "football_model.pkl")
        cls.eval_path = os.path.join(cls.base_dir, "artifacts", "model_evaluation_results.json")
        cls.sim_path = os.path.join(cls.base_dir, "artifacts", "asean_cup_simulation_results.json")
        cls.docs_path = os.path.join(cls.base_dir, "docs", "AI_METHODOLOGY_AND_YOLO11_COMPARISON.md")

    def test_production_model_bundle_integrity(self):
        self.assertTrue(os.path.exists(self.model_path), "football_model.pkl does not exist")
        bundle = joblib.load(self.model_path)
        
        self.assertIn('model', bundle)
        self.assertIn('scaler', bundle)
        self.assertIn('feature_cols', bundle)
        self.assertIn('class_names', bundle)
        self.assertIn('model_name', bundle)
        
        # Test pipeline inference on dummy sample
        feature_cols = bundle['feature_cols']
        dummy_row = {col: 0.0 for col in feature_cols}
        dummy_row['home_elo'] = 1500.0
        dummy_row['away_elo'] = 1500.0
        dummy_df = pd.DataFrame([dummy_row])[feature_cols]
        
        probs = bundle['model'].predict_proba(dummy_df)[0]
        self.assertEqual(len(probs), 3)
        self.assertAlmostEqual(float(np.sum(probs)), 1.0, places=4)

    def test_model_evaluation_json_aff_52_metrics(self):
        self.assertTrue(os.path.exists(self.eval_path), "model_evaluation_results.json does not exist")
        with open(self.eval_path, 'r', encoding='utf-8') as f:
            eval_data = json.load(f)
            
        self.assertIn("aff_52_evaluation", eval_data)
        aff = eval_data["aff_52_evaluation"]
        
        self.assertEqual(aff["match_count"], 52)
        # Log Loss must be strictly <= 0.8198
        self.assertLessEqual(aff["calibrated_logistic_regression_log_loss"], 0.8198)
        self.assertGreater(aff["uninformative_baseline_log_loss"], 1.0)
        self.assertGreater(aff["naive_baseline_log_loss"], 1.0)
        self.assertGreaterEqual(aff["accuracy"], 0.70)
        self.assertIn("brier_score", aff)
        self.assertGreater(aff["brier_score"], 0.0)

    def test_asean_cup_simulation_results_revised_paradigm(self):
        self.assertTrue(os.path.exists(self.sim_path), "asean_cup_simulation_results.json does not exist")
        with open(self.sim_path, 'r', encoding='utf-8') as f:
            sim_data = json.load(f)
            
        self.assertEqual(sim_data["iterations"], 10000)
        leaderboard = sim_data["leaderboard"]
        self.assertEqual(len(leaderboard), 10)
        
        team_probs = {entry["team"]: entry["champion_pct"] for entry in leaderboard}
        
        # Verify revised paradigm targets
        # Thailand: ~30.97% [Interval 30.0% - 33.0%]
        self.assertGreaterEqual(team_probs["Thailand"], 30.0)
        self.assertLessEqual(team_probs["Thailand"], 33.0)
        
        # Indonesia: ~27.34% [Interval 26.0% - 29.5%]
        self.assertGreaterEqual(team_probs["Indonesia"], 26.0)
        self.assertLessEqual(team_probs["Indonesia"], 29.5)
        
        # Vietnam: ~21.73% [Interval 20.0% - 24.0%]
        self.assertGreaterEqual(team_probs["Vietnam"], 20.0)
        self.assertLessEqual(team_probs["Vietnam"], 24.0)
        
        # Malaysia: ~15.40% [Interval 14.0% - 16.5%]
        self.assertGreaterEqual(team_probs["Malaysia"], 14.0)
        self.assertLessEqual(team_probs["Malaysia"], 16.5)
        
        # Check order of top 4 teams
        top_4_teams = [entry["team"] for entry in leaderboard[:4]]
        self.assertEqual(top_4_teams, ["Thailand", "Indonesia", "Vietnam", "Malaysia"])

    def test_yolo11_comparison_docs_exists_and_complete(self):
        self.assertTrue(os.path.exists(self.docs_path), "AI_METHODOLOGY_AND_YOLO11_COMPARISON.md does not exist")
        with open(self.docs_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        self.assertIn("YOLO11", content)
        self.assertIn("Log Loss", content)
        self.assertIn("SDG 9", content)
        self.assertIn("Trust Triad", content)
        self.assertIn("Non-Maximum Suppression", content)
        self.assertIn("Cross-Entropy", content)


if __name__ == '__main__':
    unittest.main()
