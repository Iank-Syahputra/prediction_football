"""
# ==============================================================================
# Unit tests for Dynamic Elo Rating Engine (scripts/elo_module.py)
# Governed by Rule VQ-338 & Rule VQ-94
# ==============================================================================
"""

import os
import sys
import unittest
import pandas as pd

# Add project root to sys.path so tests can be run from any working directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.elo_module import EloEngine, compute_elo_for_dataframe


class TestEloEngine(unittest.TestCase):
    def setUp(self):
        self.engine = EloEngine(k_factor=32.0, base_rating=1500.0, home_advantage=100.0)

    def test_initial_rating_for_unseen_team(self):
        self.assertEqual(self.engine.get_rating("Indonesia"), 1500.0)
        self.assertEqual(self.engine.get_rating("Thailand"), 1500.0)

    def test_expected_score_neutral_equal_teams(self):
        e_home, e_away = self.engine.calculate_expected_score(1500.0, 1500.0, is_neutral=True)
        self.assertAlmostEqual(e_home, 0.5, places=4)
        self.assertAlmostEqual(e_away, 0.5, places=4)
        self.assertAlmostEqual(e_home + e_away, 1.0, places=6)

    def test_expected_score_home_advantage(self):
        # With home advantage = 100, effective home is 1600 vs 1500
        # Expected score: 1 / (1 + 10^(-100/400)) = 1 / (1 + 10^(-0.25)) ≈ 0.6401
        e_home, e_away = self.engine.calculate_expected_score(1500.0, 1500.0, is_neutral=False)
        self.assertGreater(e_home, 0.60)
        self.assertLess(e_home, 0.65)
        self.assertAlmostEqual(e_home + e_away, 1.0, places=6)

    def test_update_ratings_win_zero_sum(self):
        # Both start at 1500, neutral venue
        r_home_new, r_away_new = self.engine.update_ratings(
            "TeamA", "TeamB", home_score=2, away_score=0, is_neutral=True
        )
        # Expected was 0.5, K=32 -> delta = 32 * (1.0 - 0.5) = +16.0
        self.assertAlmostEqual(r_home_new, 1516.0, places=2)
        self.assertAlmostEqual(r_away_new, 1484.0, places=2)
        # Check symmetry: delta_A + delta_B == 0
        self.assertAlmostEqual((r_home_new - 1500.0) + (r_away_new - 1500.0), 0.0, places=6)

    def test_draw_equal_neutral_produces_no_change(self):
        r_home_new, r_away_new = self.engine.update_ratings(
            "TeamX", "TeamY", home_score=1, away_score=1, is_neutral=True
        )
        self.assertAlmostEqual(r_home_new, 1500.0, places=2)
        self.assertAlmostEqual(r_away_new, 1500.0, places=2)

    def test_underdog_win_yields_larger_gain(self):
        engine1 = EloEngine(k_factor=32.0, base_rating=1500.0, home_advantage=0.0)
        # Favorite (1800) vs Underdog (1400) on neutral ground
        engine1.set_rating("Favorite", 1800.0)
        engine1.set_rating("Underdog", 1400.0)
        
        # Underdog wins
        new_fav, new_und = engine1.update_ratings(
            "Favorite", "Underdog", home_score=0, away_score=1, is_neutral=True
        )
        gain_underdog = new_und - 1400.0
        
        # In contrast, if favorite wins:
        engine2 = EloEngine(k_factor=32.0, base_rating=1500.0, home_advantage=0.0)
        engine2.set_rating("Favorite", 1800.0)
        engine2.set_rating("Underdog", 1400.0)
        new_fav2, new_und2 = engine2.update_ratings(
            "Favorite", "Underdog", home_score=1, away_score=0, is_neutral=True
        )
        gain_favorite = new_fav2 - 1800.0
        
        # Underdog win gain must be much greater than favorite win gain
        self.assertGreater(gain_underdog, gain_favorite * 5)

    def test_chronological_dataframe_zero_leakage(self):
        # 3 sequential matches:
        # Match 1: Alpha vs Beta (Alpha wins 1-0)
        # Match 2: Alpha vs Gamma (pre-match Alpha should reflect Match 1 rating!)
        # Match 3: Beta vs Gamma
        df_raw = pd.DataFrame([
            {'date': '2023-01-01', 'home_team': 'Alpha', 'away_team': 'Beta', 'home_score': 1, 'away_score': 0, 'neutral': True},
            {'date': '2023-01-05', 'home_team': 'Alpha', 'away_team': 'Gamma', 'home_score': 0, 'away_score': 0, 'neutral': True},
            {'date': '2023-01-10', 'home_team': 'Beta', 'away_team': 'Gamma', 'home_score': 2, 'away_score': 1, 'neutral': True},
        ])
        df_res, engine = compute_elo_for_dataframe(df_raw, k_factor=32.0, base_rating=1500.0, home_advantage=0.0)
        
        # Match 1 pre-match rating for Alpha must be strictly 1500.0
        self.assertEqual(df_res.iloc[0]['home_elo'], 1500.0)
        self.assertEqual(df_res.iloc[0]['away_elo'], 1500.0)
        
        # Match 2 pre-match rating for Alpha must be 1516.0 (reflects Match 1, but NOT Match 2)
        self.assertEqual(df_res.iloc[1]['home_elo'], 1516.0)
        self.assertEqual(df_res.iloc[1]['away_elo'], 1500.0)


if __name__ == '__main__':
    unittest.main()
