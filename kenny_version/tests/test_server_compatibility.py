"""
# ==============================================================================
# Unit tests for app/server.py compatibility with calibrated production model
# Governed by Rule VQ-94 & Rule VQ-338
# ==============================================================================
"""

import unittest
import json
import sys
import os

# Add root directory to sys.path
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from app.server import app, compute_features


class TestServerCompatibility(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_compute_features_has_all_model_features(self):
        df_feat, h_stat, a_stat, h2h_info, raw_feat = compute_features("Indonesia", "Thailand", 0, 0)
        self.assertIn("home_elo", raw_feat)
        self.assertIn("away_elo", raw_feat)
        self.assertIn("diff_elo", raw_feat)
        self.assertIn("elo_expected_home", raw_feat)
        self.assertIn("elo_expected_away", raw_feat)
        self.assertEqual(len(df_feat.columns), 24)

    def test_api_predict_endpoint(self):
        payload = {
            "home_team": "Indonesia",
            "away_team": "Thailand",
            "is_neutral": 0,
            "is_friendly": 0
        }
        response = self.client.post("/api/predict", data=json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("probabilities", data)
        self.assertIn("predicted_outcome", data)
        probs = data["probabilities"]
        self.assertIn("home_win", probs)
        self.assertIn("draw", probs)
        self.assertIn("away_win", probs)
        total_p = probs["home_win"] + probs["draw"] + probs["away_win"]
        self.assertAlmostEqual(total_p, 100.0, delta=0.5)

    def test_api_models_endpoint(self):
        response = self.client.get("/api/models")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("aff_52_evaluation", data)
        self.assertEqual(data["aff_52_evaluation"]["match_count"], 52)


if __name__ == '__main__':
    unittest.main()
