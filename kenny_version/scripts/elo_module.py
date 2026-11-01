"""
# ==============================================================================
# [MODULE GOAL & ROLE]
#   Dynamic Elo Rating Engine for International Football
#   Fulfills:
#     - Requirement R2 of MSIB Fast Track Batch 10 (Kelompok 1 AI)
#     - Rule VQ-336: Standardized script architecture header & near-code ground truth
#     - Slide 5 of 11-Slide Defense Deck: Dynamic Elo Ratings & Form Modeling
#   Mathematical Foundation:
#     - Expected score: E_A = 1 / (1 + 10 ^ ((R_B - (R_A + H_eff)) / 400))
#     - Rating update: R_new = R_old + K * (S - E)
#     - K-factor = 32, Base R0 = 1500.0, Home Advantage offset H = 100.0
#
# [INTENTIONAL DESIGN DECISIONS - DO NOT REMOVE]
#   - Strict timeline barrier: Pre-match Elo features for match (i) are extracted
#     STRICTLY before calling update_ratings on that match. Zero future leakage.
#   - Home advantage H is applied exclusively to the expectation calculation E_A,
#     and is NEVER permanently added to a team's baseline rating ledger.
#   - Configurable K, R0, and H parameters to support Streamlit interactive sliders.
#   - Actual score S: Win = 1.0, Draw = 0.5, Loss = 0.0.
#
# [SOLVED PAST MISTAKES & ANTIDOTES - NEVER REPEAT]
#   - Neutral venues (is_neutral=True) must zero out the home advantage offset H.
#   - Handled unseen teams gracefully by initializing to base_rating (1500.0).
#   - Maintained symmetry: E_A + E_B == 1.0 and Delta_R_A + Delta_R_B == 0.0.
#
# [SESSION REVISION & CHAT MILESTONE LEDGER]
#   - 2026-10-30: Milestone 2: Worker M2 implementation for calibrated ASEAN Cup model.
# ==============================================================================
"""

import math
from typing import Dict, Tuple, Optional
import pandas as pd
import numpy as np


class EloEngine:
    """
    Dynamic Elo Rating Engine for International Football Teams.
    Tracks chronological team strength with home advantage offset and zero data leakage.
    """

    def __init__(
        self,
        k_factor: float = 32.0,
        base_rating: float = 1500.0,
        home_advantage: float = 100.0
    ):
        """
        Initialize the Elo Engine.

        Args:
            k_factor: Weight constant determining rating volatility (default: 32.0).
            base_rating: Starting Elo rating for unranked or newly seen teams (default: 1500.0).
            home_advantage: Elo points added to home team when playing non-neutral match (default: 100.0).
        """
        self.k_factor = float(k_factor)
        self.base_rating = float(base_rating)
        self.home_advantage = float(home_advantage)
        self.ratings: Dict[str, float] = {}

    def get_rating(self, team: str) -> float:
        """
        Get current Elo rating for a team. Initializes to base_rating if unseen.
        """
        if team not in self.ratings:
            self.ratings[team] = self.base_rating
        return self.ratings[team]

    def set_rating(self, team: str, rating: float) -> None:
        """Set rating for a specific team."""
        self.ratings[team] = float(rating)

    def calculate_expected_score(
        self,
        rating_home: float,
        rating_away: float,
        is_neutral: bool = False
    ) -> Tuple[float, float]:
        """
        Calculate expected match scores (E_home, E_away) using logistic Elo curve.

        Args:
            rating_home: Elo rating of home team.
            rating_away: Elo rating of away team.
            is_neutral: Whether match is played on neutral ground.

        Returns:
            Tuple (expected_home, expected_away) where sum equals 1.0.
        """
        h_offset = 0.0 if is_neutral else self.home_advantage
        effective_home = rating_home + h_offset
        
        # Logistic curve: E_A = 1 / (1 + 10^((R_B - R_A_eff) / 400))
        diff = rating_away - effective_home
        expected_home = 1.0 / (1.0 + math.pow(10.0, diff / 400.0))
        expected_away = 1.0 - expected_home
        return expected_home, expected_away

    def get_pre_match_features(
        self,
        home_team: str,
        away_team: str,
        is_neutral: bool = False
    ) -> Dict[str, float]:
        """
        Extract pre-match Elo features strictly BEFORE the match result is processed.
        Guarantees zero future data leakage.

        Returns:
            Dictionary with home_elo, away_elo, diff_elo, elo_expected_home, elo_expected_away.
        """
        r_home = self.get_rating(home_team)
        r_away = self.get_rating(away_team)
        e_home, e_away = self.calculate_expected_score(r_home, r_away, is_neutral=is_neutral)
        
        return {
            'home_elo': round(r_home, 2),
            'away_elo': round(r_away, 2),
            'diff_elo': round(r_home - r_away, 2),
            'elo_expected_home': round(e_home, 4),
            'elo_expected_away': round(e_away, 4)
        }

    def update_ratings(
        self,
        home_team: str,
        away_team: str,
        home_score: int,
        away_score: int,
        is_neutral: bool = False
    ) -> Tuple[float, float]:
        """
        Update team ratings after match completion.

        Args:
            home_team: Name of home team.
            away_team: Name of away team.
            home_score: Goals scored by home team.
            away_score: Goals scored by away team.
            is_neutral: Whether match was played on neutral ground.

        Returns:
            Tuple of updated (new_home_rating, new_away_rating).
        """
        r_home = self.get_rating(home_team)
        r_away = self.get_rating(away_team)
        
        e_home, e_away = self.calculate_expected_score(r_home, r_away, is_neutral=is_neutral)
        
        # Actual outcome score S
        if home_score > away_score:
            s_home, s_away = 1.0, 0.0
        elif home_score == away_score:
            s_home, s_away = 0.5, 0.5
        else:
            s_home, s_away = 0.0, 1.0
            
        # Update formula: R_new = R_old + K * (S - E)
        delta_home = self.k_factor * (s_home - e_home)
        delta_away = self.k_factor * (s_away - e_away)
        
        new_home = r_home + delta_home
        new_away = r_away + delta_away
        
        self.ratings[home_team] = new_home
        self.ratings[away_team] = new_away
        
        return new_home, new_away

    def reset(self) -> None:
        """Reset all ratings."""
        self.ratings.clear()

    def get_ratings_dict(self) -> Dict[str, float]:
        """Return a copy of all current ratings."""
        return {team: round(rating, 2) for team, rating in self.ratings.items()}


def compute_elo_for_dataframe(
    df: pd.DataFrame,
    k_factor: float = 32.0,
    base_rating: float = 1500.0,
    home_advantage: float = 100.0
) -> Tuple[pd.DataFrame, EloEngine]:
    """
    Compute chronological Elo ratings across a DataFrame of historical matches.
    Enforces strict zero-leakage timeline barrier: pre-match features are assigned
    prior to updating ratings.

    Args:
        df: DataFrame containing ['date', 'home_team', 'away_team', 'home_score', 'away_score', 'neutral']
        k_factor: Weight constant (default: 32.0)
        base_rating: Starting rating (default: 1500.0)
        home_advantage: Home offset (default: 100.0)

    Returns:
        Tuple of (enhanced_df_with_elo_cols, fitted_elo_engine)
    """
    engine = EloEngine(k_factor=k_factor, base_rating=base_rating, home_advantage=home_advantage)
    
    # Ensure chronological order
    df_sorted = df.copy()
    if not pd.api.types.is_datetime64_any_dtype(df_sorted['date']):
        df_sorted['date'] = pd.to_datetime(df_sorted['date'])
    df_sorted = df_sorted.sort_values(by='date').reset_index(drop=True)
    
    home_elos = []
    away_elos = []
    diff_elos = []
    e_homes = []
    e_aways = []
    
    for _, row in df_sorted.iterrows():
        h_team = str(row['home_team'])
        a_team = str(row['away_team'])
        h_score = int(row['home_score'])
        a_score = int(row['away_score'])
        is_neut = bool(row['neutral']) if 'neutral' in row else bool(row.get('is_neutral', 0))
        
        # 1. Extract PRE-MATCH Elo (Zero future knowledge!)
        feats = engine.get_pre_match_features(h_team, a_team, is_neutral=is_neut)
        home_elos.append(feats['home_elo'])
        away_elos.append(feats['away_elo'])
        diff_elos.append(feats['diff_elo'])
        e_homes.append(feats['elo_expected_home'])
        e_aways.append(feats['elo_expected_away'])
        
        # 2. Update Elo POST-MATCH
        engine.update_ratings(h_team, a_team, h_score, a_score, is_neutral=is_neut)
        
    df_sorted['home_elo'] = home_elos
    df_sorted['away_elo'] = away_elos
    df_sorted['diff_elo'] = diff_elos
    df_sorted['elo_expected_home'] = e_homes
    df_sorted['elo_expected_away'] = e_aways
    
    return df_sorted, engine
