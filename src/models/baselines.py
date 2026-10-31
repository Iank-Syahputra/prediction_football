"""Baseline Section 6: prior kelas, Elo murni, dan logistic regression.

Semua model dilatih pada data latih satu fold dan mengembalikan probabilitas
dengan urutan kolom H, D, A. Tidak ada penyetelan hyperparameter di sini.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.special import logsumexp
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.evaluation.metrics import N_KELAS, encode_labels

ELO_COLUMNS = ("elo_home_pre", "elo_away_pre", "neutral")

LOGISTIC_NUMERIC_COLUMNS = (
    "elo_home_pre", "elo_away_pre", "elo_diff",
    "neutral", "home_is_host", "away_is_host",
    "form_pts_home", "form_gf_home", "form_ga_home", "n_form_home", "rest_days_home",
    "form_pts_away", "form_gf_away", "form_ga_away", "n_form_away", "rest_days_away",
    "n_h2h", "h2h_score_home",
)
LOGISTIC_CATEGORICAL_COLUMNS = ("tournament_group",)
LOGISTIC_COLUMNS = LOGISTIC_NUMERIC_COLUMNS + LOGISTIC_CATEGORICAL_COLUMNS


class PriorBaseline:
    """Baseline yang selalu memakai frekuensi kelas dari data latih."""

    def __init__(self) -> None:
        self.proba_: np.ndarray | None = None
        self.classes_ = np.arange(N_KELAS)

    def fit(self, X, y) -> "PriorBaseline":
        indeks = encode_labels(y)
        frekuensi = np.bincount(indeks, minlength=N_KELAS).astype(float)
        if frekuensi.sum() == 0:
            raise ValueError("data latih tidak memiliki label")
        self.proba_ = frekuensi / frekuensi.sum()
        return self

    def predict_proba(self, X) -> np.ndarray:
        if self.proba_ is None:
            raise RuntimeError("model belum dilatih")
        n = len(X)
        return np.tile(self.proba_, (n, 1))


class EloDavidson:
    """Model Davidson untuk H/D/A dengan kekuatan tim dari rating Elo.

    Probabilitas:
        p_H ∝ exp(beta * (elo_home + home_adv * (1 - neutral)))
        p_A ∝ exp(beta * elo_away)
        p_D ∝ nu * sqrt(p_H_tanpa_normalisasi * p_A_tanpa_normalisasi)

    ``beta`` dan ``nu`` diestimasi dengan maximum likelihood pada data latih.
    ``home_adv`` tetap memakai nilai dari config agar baseline tetap sederhana.
    """

    def __init__(
        self,
        home_adv: float = 100.0,
        beta_init: float = 0.005756,
        nu_init: float = 1.0,
        beta_bounds: tuple[float, float] = (1e-5, 0.05),
        nu_bounds: tuple[float, float] = (1e-3, 20.0),
    ) -> None:
        if home_adv < 0:
            raise ValueError("home_adv tidak boleh negatif")
        if not 0 < beta_init:
            raise ValueError("beta_init harus > 0")
        if not 0 < nu_init:
            raise ValueError("nu_init harus > 0")
        self.home_adv = float(home_adv)
        self.beta_init = float(beta_init)
        self.nu_init = float(nu_init)
        self.beta_bounds = tuple(float(v) for v in beta_bounds)
        self.nu_bounds = tuple(float(v) for v in nu_bounds)
        self.beta_: float | None = None
        self.nu_: float | None = None
        self.nll_: float | None = None
        self.n_iter_: int | None = None

    @staticmethod
    def _matriks(X) -> np.ndarray:
        if isinstance(X, pd.DataFrame):
            hilang = [kolom for kolom in ELO_COLUMNS if kolom not in X.columns]
            if hilang:
                raise KeyError(f"kolom Elo tidak ada: {hilang}")
            matriks = X.loc[:, list(ELO_COLUMNS)].to_numpy(dtype=float)
        else:
            matriks = np.asarray(X, dtype=float)
            if matriks.ndim != 2 or matriks.shape[1] != len(ELO_COLUMNS):
                raise ValueError(f"X harus berukuran (n, {len(ELO_COLUMNS)})")
        if not np.isfinite(matriks).all():
            raise ValueError("fitur Elo mengandung nilai non-finite")
        if not np.isin(matriks[:, 2], [0.0, 1.0]).all():
            raise ValueError("kolom neutral harus 0 atau 1")
        return matriks

    def _log_proba(self, beta: float, nu: float, matriks: np.ndarray) -> np.ndarray:
        elo_home = matriks[:, 0]
        elo_away = matriks[:, 1]
        neutral = matriks[:, 2]
        keuntungan_home = self.home_adv * (1.0 - neutral)
        log_home = beta * (elo_home + keuntungan_home)
        log_away = beta * elo_away
        log_draw = 0.5 * (log_home + log_away) + np.log(nu)
        logits = np.column_stack([log_home, log_draw, log_away])
        logits = logits - logsumexp(logits, axis=1, keepdims=True)
        return logits

    def fit(self, X, y) -> "EloDavidson":
        matriks = self._matriks(X)
        indeks = encode_labels(y)
        if len(matriks) != len(indeks):
            raise ValueError("jumlah X dan y berbeda")

        def neg_log_likelihood(params: np.ndarray) -> float:
            if not np.isfinite(params).all():
                return 1e12
            beta = float(np.exp(params[0]))
            nu = float(np.exp(params[1]))
            log_p = self._log_proba(beta, nu, matriks)
            return float(-np.mean(log_p[np.arange(len(indeks)), indeks]))

        batas_beta = tuple(np.log(v) for v in self.beta_bounds)
        batas_nu = tuple(np.log(v) for v in self.nu_bounds)
        hasil = minimize(
            neg_log_likelihood,
            x0=np.log([self.beta_init, self.nu_init]),
            method="L-BFGS-B",
            bounds=[batas_beta, batas_nu],
            options={"maxiter": 1000},
        )
        if not hasil.success or not np.isfinite(hasil.fun):
            raise RuntimeError(f"optimasi Elo gagal: {hasil.message}")

        self.beta_ = float(np.exp(hasil.x[0]))
        self.nu_ = float(np.exp(hasil.x[1]))
        self.nll_ = float(hasil.fun)
        self.n_iter_ = int(hasil.nit)
        return self

    def predict_proba(self, X) -> np.ndarray:
        if self.beta_ is None or self.nu_ is None:
            raise RuntimeError("model belum dilatih")
        matriks = self._matriks(X)
        proba = np.exp(self._log_proba(self.beta_, self.nu_, matriks))
        return proba / proba.sum(axis=1, keepdims=True)


class OrderedProbaModel:
    """Wrapper agar kolom probabilitas selalu berurutan H, D, A."""

    def __init__(self, estimator) -> None:
        self.estimator = estimator
        self.classes_: np.ndarray | None = None

    def fit(self, X, y) -> "OrderedProbaModel":
        self.estimator.fit(X, encode_labels(y))
        self.classes_ = np.asarray(self.estimator.classes_, dtype=int)
        if set(self.classes_.tolist()) != set(range(N_KELAS)):
            raise ValueError("data latih harus memuat ketiga kelas H, D, dan A")
        return self

    def predict_proba(self, X) -> np.ndarray:
        if self.classes_ is None:
            raise RuntimeError("model belum dilatih")
        proba = self.estimator.predict_proba(X)
        hasil = np.zeros((len(proba), N_KELAS), dtype=float)
        for kolom, kelas in enumerate(self.classes_):
            hasil[:, kelas] = proba[:, kolom]
        return hasil


def build_logistic_pipeline(C: float = 1.0, max_iter: int = 2000) -> Pipeline:
    """Pipeline imputasi, standardisasi, one-hot konteks, lalu logistic regression."""
    if C <= 0:
        raise ValueError("C harus > 0")
    if max_iter <= 0:
        raise ValueError("max_iter harus > 0")

    numerik = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])
    kategorikal = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])
    praproses = ColumnTransformer([
        ("numerik", numerik, list(LOGISTIC_NUMERIC_COLUMNS)),
        ("kategorikal", kategorikal, list(LOGISTIC_CATEGORICAL_COLUMNS)),
    ], remainder="drop")
    return Pipeline([
        ("praproses", praproses),
        ("model", LogisticRegression(C=C, max_iter=max_iter, solver="lbfgs")),
    ])


def build_logistic_baseline(C: float = 1.0, max_iter: int = 2000) -> OrderedProbaModel:
    """Logistic regression baseline dengan urutan probabilitas H, D, A."""
    return OrderedProbaModel(build_logistic_pipeline(C=C, max_iter=max_iter))
