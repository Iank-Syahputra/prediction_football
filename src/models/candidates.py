"""Kandidat model Section 7: logistic dengan variasi fitur dan gradient boosting."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.models.baselines import (
    LOGISTIC_CATEGORICAL_COLUMNS,
    LOGISTIC_NUMERIC_COLUMNS,
    OrderedProbaModel,
)
from src.models.features import INTERACTION_COLUMNS, FeatureAugmenter

ELO_NUMERIC = ("elo_diff", "neutral", "home_is_host", "away_is_host")
ELO_FORM_NUMERIC = ELO_NUMERIC + (
    "form_pts_home", "form_pts_away", "n_form_home", "n_form_away",
    "rest_days_home", "rest_days_away",
)
FULL_NUMERIC = tuple(LOGISTIC_NUMERIC_COLUMNS)
FULL_INTERACTION_NUMERIC = FULL_NUMERIC + INTERACTION_COLUMNS
CATEGORICAL = tuple(LOGISTIC_CATEGORICAL_COLUMNS)

FEATURE_SETS = {
    "elo": {"numeric": ELO_NUMERIC, "categorical": ()},
    "elo_form": {"numeric": ELO_FORM_NUMERIC, "categorical": ()},
    "full": {"numeric": FULL_NUMERIC, "categorical": CATEGORICAL},
    "full_interaksi": {"numeric": FULL_INTERACTION_NUMERIC, "categorical": CATEGORICAL},
}


def _praproses(numeric, categorical, scale_numeric: bool) -> ColumnTransformer:
    langkah_numerik = [("imputer", SimpleImputer(strategy="median"))]
    if scale_numeric:
        langkah_numerik.append(("scaler", StandardScaler()))
    transformasi = [("numerik", Pipeline(langkah_numerik), list(numeric))]
    if categorical:
        transformasi.append((
            "kategorikal",
            Pipeline([
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
            ]),
            list(categorical),
        ))
    return ColumnTransformer(transformasi, remainder="drop")


def build_logistic_candidate(
    feature_set: str = "full",
    C: float = 1.0,
    max_iter: int = 2000,
) -> OrderedProbaModel:
    """Logistic Regression dengan pilihan fitur dan regularisasi L2."""
    if feature_set not in FEATURE_SETS:
        raise ValueError(f"feature_set tidak dikenal: {feature_set}")
    if C <= 0:
        raise ValueError("C harus > 0")
    if max_iter <= 0:
        raise ValueError("max_iter harus > 0")

    spesifikasi = FEATURE_SETS[feature_set]
    tambah_interaksi = feature_set == "full_interaksi"
    pipeline = Pipeline([
        ("augment", FeatureAugmenter(add_interactions=tambah_interaksi)),
        ("praproses", _praproses(
            spesifikasi["numeric"], spesifikasi["categorical"], scale_numeric=True
        )),
        ("model", LogisticRegression(C=C, max_iter=max_iter, solver="lbfgs")),
    ])
    return OrderedProbaModel(pipeline)


def build_hgb_candidate(
    learning_rate: float = 0.05,
    max_leaf_nodes: int = 15,
    l2_regularization: float = 1.0,
    max_iter: int = 100,
    min_samples_leaf: int = 20,
    add_interactions: bool = False,
    random_state: int = 42,
) -> OrderedProbaModel:
    """HistGradientBoostingClassifier dengan fitur penuh dan one-hot konteks."""
    if learning_rate <= 0:
        raise ValueError("learning_rate harus > 0")
    if max_leaf_nodes < 2:
        raise ValueError("max_leaf_nodes harus >= 2")
    if l2_regularization < 0:
        raise ValueError("l2_regularization tidak boleh negatif")
    if max_iter <= 0:
        raise ValueError("max_iter harus > 0")
    if min_samples_leaf <= 0:
        raise ValueError("min_samples_leaf harus > 0")

    model = HistGradientBoostingClassifier(
        learning_rate=learning_rate,
        max_leaf_nodes=max_leaf_nodes,
        l2_regularization=l2_regularization,
        max_iter=max_iter,
        min_samples_leaf=min_samples_leaf,
        early_stopping=False,
        random_state=random_state,
    )
    numeric = FULL_INTERACTION_NUMERIC if add_interactions else FULL_NUMERIC
    pipeline = Pipeline([
        ("augment", FeatureAugmenter(add_interactions=add_interactions)),
        ("praproses", _praproses(numeric, CATEGORICAL, scale_numeric=False)),
        ("model", model),
    ])
    return OrderedProbaModel(pipeline)


class ProbabilityEnsemble:
    """Rata-rata probabilitas beberapa model dengan bobot tetap."""

    def __init__(self, models, weights=None) -> None:
        if len(models) < 2:
            raise ValueError("ensemble membutuhkan minimal dua model")
        if weights is None:
            weights = [1.0 / len(models)] * len(models)
        if len(weights) != len(models):
            raise ValueError("jumlah bobot harus sama dengan jumlah model")
        bobot = np.asarray(weights, dtype=float)
        if not np.isfinite(bobot).all() or (bobot < 0).any() or bobot.sum() <= 0:
            raise ValueError("bobot harus non-negatif dan berjumlah > 0")
        self.models = list(models)
        self.weights = bobot / bobot.sum()

    def fit(self, X, y) -> "ProbabilityEnsemble":
        for model in self.models:
            model.fit(X, y)
        return self

    def predict_proba(self, X) -> np.ndarray:
        proba = np.zeros((len(X), 3), dtype=float)
        for model, bobot in zip(self.models, self.weights):
            p = np.asarray(model.predict_proba(X), dtype=float)
            if p.shape != (len(X), 3):
                raise ValueError("model anggota menghasilkan probabilitas dengan ukuran salah")
            proba += bobot * p
        return proba / proba.sum(axis=1, keepdims=True)


def build_ensemble_candidate(
    feature_set: str = "full",
    C: float = 1.0,
    learning_rate: float = 0.05,
    max_leaf_nodes: int = 15,
    l2_regularization: float = 1.0,
    weight_hgb: float = 0.5,
) -> ProbabilityEnsemble:
    """Gabungkan kandidat logistic dan HGB dengan bobot HGB tertentu."""
    if not 0 <= weight_hgb <= 1:
        raise ValueError("weight_hgb harus di antara 0 dan 1")
    return ProbabilityEnsemble(
        [
            build_logistic_candidate(feature_set=feature_set, C=C),
            build_hgb_candidate(
                learning_rate=learning_rate,
                max_leaf_nodes=max_leaf_nodes,
                l2_regularization=l2_regularization,
            ),
        ],
        weights=[1.0 - weight_hgb, weight_hgb],
    )
