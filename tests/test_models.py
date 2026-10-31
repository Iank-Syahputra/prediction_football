"""Test kandidat model, feature augmenter, ensemble, dan helper tuning."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.models.baselines import LOGISTIC_NUMERIC_COLUMNS
from src.models.candidates import (
    ProbabilityEnsemble,
    build_hgb_candidate,
    build_logistic_candidate,
)
from src.models.features import FeatureAugmenter
from src.models.tuning import blend_predictions, tune_blend_weights, tune_grid


def _fitur(n: int = 36) -> pd.DataFrame:
    rng = np.random.default_rng(7)
    data = {kolom: rng.normal(size=n) for kolom in LOGISTIC_NUMERIC_COLUMNS}
    data["tournament_group"] = rng.choice(["Friendly", "Kualifikasi", "Lainnya"], size=n)
    X = pd.DataFrame(data)
    for kolom in ("form_pts_home", "form_pts_away", "rest_days_home", "rest_days_away"):
        X.loc[X.index % 6 == 0, kolom] = np.nan
    return X


def test_feature_augmenter_menambah_kolom_turunan() -> None:
    X = pd.DataFrame({
        "form_pts_home": [2.0], "form_pts_away": [1.0],
        "form_gf_home": [3.0], "form_gf_away": [1.0],
        "form_ga_home": [1.0], "form_ga_away": [2.0],
        "n_form_home": [5.0], "n_form_away": [4.0],
        "rest_days_home": [10.0], "rest_days_away": [15.0],
        "elo_diff": [120.0], "elo_home_pre": [1600.0], "elo_away_pre": [1480.0],
        "home_is_host": [1.0], "away_is_host": [0.0], "neutral": [0.0],
        "h2h_score_home": [np.nan],
    })
    hasil = FeatureAugmenter(add_interactions=True).fit_transform(X)
    assert len(hasil) == 1
    assert hasil.loc[0, "form_pts_diff"] == pytest.approx(1.0)
    assert hasil.loc[0, "elo_diff_abs"] == pytest.approx(120.0)
    assert hasil.loc[0, "elo_diff_sq"] == pytest.approx(14400.0)
    assert hasil.loc[0, "elo_sum"] == pytest.approx(3080.0)
    assert hasil.loc[0, "host_advantage"] == pytest.approx(1.0)
    assert hasil.loc[0, "host_x_elo_diff"] == pytest.approx(120.0)
    assert np.isnan(hasil.loc[0, "h2h_x_elo_diff"])

    tanpa = FeatureAugmenter(add_interactions=False).fit_transform(X)
    assert list(tanpa.columns) == list(X.columns)

    with pytest.raises(KeyError, match="fitur turunan"):
        FeatureAugmenter(add_interactions=True).fit_transform(X.drop(columns="elo_diff"))


def test_logistic_candidate_bisa_dilatih_dengan_interaksi() -> None:
    X = _fitur()
    y = np.tile([0, 1, 2], len(X) // 3)
    model = build_logistic_candidate(feature_set="full_interaksi", C=1.0, max_iter=1000)
    model.fit(X, y)
    p = model.predict_proba(X)
    assert p.shape == (len(X), 3)
    np.testing.assert_allclose(p.sum(axis=1), 1.0, atol=1e-10)
    assert model.classes_.tolist() == [0, 1, 2]


@pytest.mark.parametrize("add_interactions", [False, True])
def test_hgb_candidate_bisa_dilatih_dan_memprediksi(add_interactions) -> None:
    X = _fitur()
    y = np.tile([0, 1, 2], len(X) // 3)
    model = build_hgb_candidate(
        learning_rate=0.1, max_leaf_nodes=5, l2_regularization=0.1,
        max_iter=10, min_samples_leaf=5, add_interactions=add_interactions,
    )
    model.fit(X, y)
    p = model.predict_proba(X)
    assert p.shape == (len(X), 3)
    np.testing.assert_allclose(p.sum(axis=1), 1.0, atol=1e-10)
    assert model.classes_.tolist() == [0, 1, 2]


class _ModelTetap:
    def __init__(self, proba):
        self.proba = np.asarray(proba, dtype=float)

    def fit(self, X, y):
        return self

    def predict_proba(self, X):
        return np.tile(self.proba, (len(X), 1))


def test_probability_ensemble_rata_rata_berbobot() -> None:
    ensemble = ProbabilityEnsemble(
        [_ModelTetap([1.0, 0.0, 0.0]), _ModelTetap([0.0, 0.0, 1.0])],
        weights=[0.25, 0.75],
    )
    X = pd.DataFrame({"x": [1.0, 2.0]})
    p = ensemble.fit(X, [0, 2]).predict_proba(X)
    np.testing.assert_allclose(p, [[0.25, 0.0, 0.75], [0.25, 0.0, 0.75]])
    np.testing.assert_allclose(p.sum(axis=1), 1.0)

    with pytest.raises(ValueError, match="bobot"):
        ProbabilityEnsemble([_ModelTetap([1, 0, 0]), _ModelTetap([0, 1, 0])], weights=[-1, 2])
    with pytest.raises(ValueError, match="minimal dua"):
        ProbabilityEnsemble([_ModelTetap([1, 0, 0])])


def _prediksi(proba_h, proba_d, proba_a) -> pd.DataFrame:
    n = len(proba_h)
    return pd.DataFrame({
        "fold": ["F"] * n,
        "match_id": list(range(n)),
        "date": pd.date_range("2020-01-01", periods=n),
        "home_team": ["A"] * n,
        "away_team": ["B"] * n,
        "tournament": ["Friendly"] * n,
        "edition": [np.nan] * n,
        "y": ["H", "D"][:n] if n <= 2 else (["H", "D"] * (n // 2 + 1))[:n],
        "p_H": proba_h,
        "p_D": proba_d,
        "p_A": proba_a,
    })


def test_blend_predictions_dan_tune_bobot() -> None:
    pred_a = _prediksi([0.8, 0.2], [0.1, 0.2], [0.1, 0.6])
    pred_b = _prediksi([0.2, 0.6], [0.2, 0.2], [0.6, 0.2])

    p0 = blend_predictions(pred_a, pred_b, 0.0)
    p1 = blend_predictions(pred_a, pred_b, 1.0)
    np.testing.assert_allclose(p0[["p_H", "p_D", "p_A"]], pred_a[["p_H", "p_D", "p_A"]])
    np.testing.assert_allclose(p1[["p_H", "p_D", "p_A"]], pred_b[["p_H", "p_D", "p_A"]])

    p50 = blend_predictions(pred_a, pred_b, 0.5)
    np.testing.assert_allclose(
        p50.loc[0, ["p_H", "p_D", "p_A"]].to_numpy(dtype=float),
        [0.5, 0.15, 0.35],
    )

    tabel = tune_blend_weights(pred_a, pred_b, [0.0, 0.5, 1.0], n_bins=2)
    assert set(tabel["weight_b"]) == {0.0, 0.5, 1.0}
    assert "log_loss_mean" in tabel.columns

    with pytest.raises(ValueError, match="weight_b"):
        blend_predictions(pred_a, pred_b, 1.5)


def test_tune_grid_menjalankan_semua_kombinasi() -> None:
    features = pd.DataFrame({
        "match_id": [1, 2, 3, 4],
        "date": pd.date_range("2020-01-01", periods=4),
        "home_team": ["A", "B", "C", "D"],
        "away_team": ["B", "C", "D", "A"],
        "tournament": ["Friendly"] * 4,
        "result": ["H", "D", "A", "H"],
    })
    folds = [{
        "name": "F",
        "edition": np.nan,
        "train_idx": np.array([True, True, False, False]),
        "val_idx": np.array([False, False, True, True]),
    }]

    def build_model(alpha):
        return _ModelTetap([0.5, 0.25, 0.25])

    tabel = tune_grid(features, folds, build_model, {"alpha": [1, 2]}, n_bins=2)
    assert len(tabel) == 2
    assert set(tabel["alpha"]) == {1, 2}
    assert (tabel["log_loss_mean"] >= 0).all()
