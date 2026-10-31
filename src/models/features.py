"""Transformasi fitur turunan untuk kandidat model Section 7.

Semua fitur turunan dihitung dari fitur pra-laga yang sudah ada. Tidak ada
statistik yang diestimasi dari data validasi, sehingga transformasi ini aman
dipakai di dalam pipeline per fold.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

INTERACTION_COLUMNS = (
    "form_pts_diff",
    "form_gf_diff",
    "form_ga_diff",
    "n_form_diff",
    "rest_days_diff",
    "elo_diff_abs",
    "elo_diff_sq",
    "elo_sum",
    "host_advantage",
    "host_x_elo_diff",
    "away_host_x_elo_diff",
    "neutral_x_elo_diff",
    "h2h_x_elo_diff",
)

_KOLOM_WAJIB = (
    "form_pts_home", "form_pts_away",
    "form_gf_home", "form_gf_away",
    "form_ga_home", "form_ga_away",
    "n_form_home", "n_form_away",
    "rest_days_home", "rest_days_away",
    "elo_diff", "elo_home_pre", "elo_away_pre",
    "home_is_host", "away_is_host", "neutral",
    "h2h_score_home",
)


class FeatureAugmenter(BaseEstimator, TransformerMixin):
    """Tambahkan interaksi dan selisih fitur tanpa mengubah baris data."""

    def __init__(self, add_interactions: bool = True) -> None:
        self.add_interactions = add_interactions

    def fit(self, X, y=None) -> "FeatureAugmenter":
        if not isinstance(X, pd.DataFrame):
            raise TypeError("FeatureAugmenter membutuhkan pandas.DataFrame")
        self.feature_names_in_ = np.asarray(X.columns, dtype=object)
        self.n_features_in_ = X.shape[1]
        return self

    def transform(self, X) -> pd.DataFrame:
        if not isinstance(X, pd.DataFrame):
            raise TypeError("FeatureAugmenter membutuhkan pandas.DataFrame")
        if not self.add_interactions:
            return X.copy()

        hilang = [kolom for kolom in _KOLOM_WAJIB if kolom not in X.columns]
        if hilang:
            raise KeyError(f"kolom untuk fitur turunan tidak ada: {hilang}")

        hasil = X.copy()
        hasil["form_pts_diff"] = hasil["form_pts_home"] - hasil["form_pts_away"]
        hasil["form_gf_diff"] = hasil["form_gf_home"] - hasil["form_gf_away"]
        hasil["form_ga_diff"] = hasil["form_ga_home"] - hasil["form_ga_away"]
        hasil["n_form_diff"] = hasil["n_form_home"] - hasil["n_form_away"]
        hasil["rest_days_diff"] = hasil["rest_days_home"] - hasil["rest_days_away"]
        hasil["elo_diff_abs"] = hasil["elo_diff"].abs()
        hasil["elo_diff_sq"] = hasil["elo_diff"] ** 2
        hasil["elo_sum"] = hasil["elo_home_pre"] + hasil["elo_away_pre"]
        hasil["host_advantage"] = hasil["home_is_host"] - hasil["away_is_host"]
        hasil["host_x_elo_diff"] = hasil["home_is_host"] * hasil["elo_diff"]
        hasil["away_host_x_elo_diff"] = hasil["away_is_host"] * hasil["elo_diff"]
        hasil["neutral_x_elo_diff"] = hasil["neutral"] * hasil["elo_diff"]
        hasil["h2h_x_elo_diff"] = hasil["h2h_score_home"] * hasil["elo_diff"]
        return hasil

    def get_feature_names_out(self, input_features=None) -> np.ndarray:
        if input_features is None:
            input_features = getattr(self, "feature_names_in_", None)
        if input_features is None:
            raise ValueError("input_features belum tersedia; panggil fit terlebih dahulu")
        if not self.add_interactions:
            return np.asarray(input_features, dtype=object)
        return np.concatenate([np.asarray(input_features, dtype=object), np.asarray(INTERACTION_COLUMNS, dtype=object)])
