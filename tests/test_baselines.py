"""Test baseline Section 6 pada data sintetis kecil."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.evaluation.metrics import encode_labels
from src.models.baselines import (
    EloDavidson,
    LOGISTIC_NUMERIC_COLUMNS,
    PriorBaseline,
    build_logistic_baseline,
)


def test_prior_memakai_frekuensi_latih() -> None:
    y = encode_labels(["H", "H", "D", "A", "A", "A"])
    model = PriorBaseline().fit(None, y)
    proba = model.predict_proba(np.zeros((4, 1)))
    assert proba.shape == (4, 3)
    np.testing.assert_allclose(proba[0], [2 / 6, 1 / 6, 3 / 6])
    np.testing.assert_allclose(proba.sum(axis=1), 1.0)


def test_elo_davidson_terfit_dan_menghormati_home_advantage() -> None:
    rng = np.random.default_rng(0)
    n = 80
    elo_home = rng.normal(1500, 150, n)
    elo_away = rng.normal(1500, 150, n)
    neutral = rng.integers(0, 2, n).astype(float)
    X = pd.DataFrame({
        "elo_home_pre": elo_home,
        "elo_away_pre": elo_away,
        "neutral": neutral,
    })
    selisih = (elo_home + 100 * (1 - neutral)) - elo_away
    y = np.where(selisih > 75, 0, np.where(selisih < -75, 2, 1))

    model = EloDavidson(home_adv=100).fit(X, y)
    assert model.beta_ is not None and model.beta_ > 0
    assert model.nu_ is not None and model.nu_ > 0
    assert model.n_iter_ is not None and model.n_iter_ > 0

    p = model.predict_proba(X)
    assert p.shape == (n, 3)
    np.testing.assert_allclose(p.sum(axis=1), 1.0, atol=1e-10)

    X_test = pd.DataFrame({
        "elo_home_pre": [1600.0, 1500.0],
        "elo_away_pre": [1500.0, 1500.0],
        "neutral": [0.0, 1.0],
    })
    p_test = model.predict_proba(X_test)
    assert p_test[0, 0] > p_test[0, 2]
    assert p_test[1, 0] == pytest.approx(p_test[1, 2])


def test_elo_davidson_validasi_kolom() -> None:
    X = pd.DataFrame({
        "elo_home_pre": [1500.0],
        "elo_away_pre": [1500.0],
        "neutral": [2.0],
    })
    with pytest.raises(ValueError, match="neutral"):
        EloDavidson().fit(X, [1])
    with pytest.raises(KeyError, match="kolom Elo"):
        EloDavidson().fit(pd.DataFrame({"elo_home_pre": [1500.0]}), [1])


def test_logistic_baseline_shape_dan_kategori_baru() -> None:
    rng = np.random.default_rng(1)
    n = 60
    data = {kolom: rng.normal(size=n) for kolom in LOGISTIC_NUMERIC_COLUMNS}
    data["tournament_group"] = rng.choice(["Friendly", "Kualifikasi", "Lainnya"], size=n)
    X = pd.DataFrame(data)
    for kolom in ("form_pts_home", "form_pts_away", "rest_days_home", "rest_days_away"):
        X.loc[X.index % 7 == 0, kolom] = np.nan
    y = np.tile([0, 1, 2], n // 3)

    model = build_logistic_baseline(C=1.0, max_iter=1000).fit(X, y)
    assert model.classes_.tolist() == [0, 1, 2]
    p = model.predict_proba(X)
    assert p.shape == (n, 3)
    np.testing.assert_allclose(p.sum(axis=1), 1.0, atol=1e-10)

    X_baru = X.copy()
    X_baru.loc[0, "tournament_group"] = "TurnamenBaru"
    p_baru = model.predict_proba(X_baru)
    assert p_baru.shape == (n, 3)
    assert np.isfinite(p_baru).all()


def test_logistic_baseline_membutuhkan_semua_kelas() -> None:
    X = pd.DataFrame({kolom: [0.0, 1.0] for kolom in LOGISTIC_NUMERIC_COLUMNS})
    X["tournament_group"] = ["Friendly", "Friendly"]
    with pytest.raises(ValueError, match="ketiga kelas"):
        build_logistic_baseline(max_iter=100).fit(X, [0, 1])
