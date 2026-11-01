"""
# ==============================================================================
# Unit tests for Feature Engineering & Dataset Integrity
# Governed by Rule VQ-338 & Rule VQ-94
# ==============================================================================
"""

import os
import json
import unittest
import pandas as pd


class TestFeatureEngineering(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cls.train_path = os.path.join(cls.base_dir, "data", "train_temporal.csv")
        cls.test_path = os.path.join(cls.base_dir, "data", "test_temporal.csv")
        cls.stats_path = os.path.join(cls.base_dir, "artifacts", "latest_team_stats.json")

    def test_datasets_exist_and_non_empty(self):
        self.assertTrue(os.path.exists(self.train_path))
        self.assertTrue(os.path.exists(self.test_path))
        self.assertTrue(os.path.exists(self.stats_path))

    def test_elo_columns_present_in_datasets(self):
        train_df = pd.read_csv(self.train_path, nrows=50)
        test_df = pd.read_csv(self.test_path, nrows=50)
        
        expected_cols = [
            'home_elo', 'away_elo', 'diff_elo',
            'elo_expected_home', 'elo_expected_away'
        ]
        for col in expected_cols:
            self.assertIn(col, train_df.columns, f"Missing {col} in train_temporal.csv")
            self.assertIn(col, test_df.columns, f"Missing {col} in test_temporal.csv")

    def test_exact_52_aff_championship_matches(self):
        test_df = pd.read_csv(self.test_path)
        aff_52 = test_df[test_df['tournament'] == 'AFF Championship']
        self.assertEqual(len(aff_52), 52, f"Expected exactly 52 AFF Championship matches, got {len(aff_52)}")

    def test_latest_team_stats_contains_elo(self):
        with open(self.stats_path, 'r', encoding='utf-8') as f:
            stats = json.load(f)
        self.assertIn("Indonesia", stats)
        self.assertIn("Thailand", stats)
        self.assertIn("Vietnam", stats)
        self.assertIn("Malaysia", stats)
        self.assertIn("elo", stats["Indonesia"])
        self.assertIn("elo_rating", stats["Indonesia"])
        self.assertGreater(stats["Indonesia"]["elo"], 1000)


if __name__ == '__main__':
    unittest.main()
