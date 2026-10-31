"""Helper tuning walk-forward dan penggabungan probabilitas dua model."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.model_selection import ParameterGrid

from src.evaluation.metrics import encode_labels
from src.evaluation.validation import (
    fold_metrics_from_predictions,
    pooled_metrics,
    run_folds,
)


def evaluate_candidate(
    features: pd.DataFrame,
    folds: list[dict],
    build_model,
    params: dict,
    n_bins: int = 10,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Latih satu konfigurasi pada setiap fold, lalu kembalikan prediksi + metrik."""
    def fit_predict(train, val):
        model = build_model(**params)
        model.fit(train, encode_labels(train["result"]))
        return model.predict_proba(val)

    return run_folds(features, folds, fit_predict, n_bins=n_bins)


def tune_grid(
    features: pd.DataFrame,
    folds: list[dict],
    build_model,
    param_grid: dict,
    n_bins: int = 10,
    verbose: bool = False,
) -> pd.DataFrame:
    """Evaluasi seluruh kombinasi parameter pada fold yang diberikan."""
    baris = []
    for params in ParameterGrid(param_grid):
        pred, met = evaluate_candidate(
            features, folds, build_model, params, n_bins=n_bins
        )
        pool = pooled_metrics(pred, n_bins=n_bins)
        baris.append({
            **params,
            "log_loss_mean": float(met["log_loss"].mean()),
            "log_loss_sd": float(met["log_loss"].std()),
            "log_loss_pooled": float(pool["log_loss"]),
            "brier_mean": float(met["brier"].mean()),
            "brier_pooled": float(pool["brier"]),
            "rps_mean": float(met["rps"].mean()),
            "accuracy_mean": float(met["accuracy"].mean()),
            "macro_f1_mean": float(met["macro_f1"].mean()),
            "ece_top_mean": float(met["ece_top"].mean()),
        })
        if verbose:
            print(
                f"{params} -> log_loss_mean={baris[-1]['log_loss_mean']:.4f} "
                f"(pooled {baris[-1]['log_loss_pooled']:.4f})"
            )

    hasil = pd.DataFrame(baris)
    return hasil.sort_values(
        ["log_loss_mean", "brier_mean"], ascending=True
    ).reset_index(drop=True)


def blend_predictions(
    pred_a: pd.DataFrame,
    pred_b: pd.DataFrame,
    weight_b: float,
) -> pd.DataFrame:
    """Gabungkan dua tabel prediksi dengan bobot ``weight_b`` untuk model B."""
    if not 0 <= weight_b <= 1:
        raise ValueError("weight_b harus di antara 0 dan 1")

    kunci = ["fold", "match_id"]
    kiri = pred_a.set_index(kunci).sort_index()
    kanan = pred_b.set_index(kunci).sort_index()
    if not kiri.index.equals(kanan.index):
        raise ValueError("pasangan prediksi tidak identik")
    if not kiri["y"].equals(kanan["y"]):
        raise ValueError("label target tidak identik")

    kolom_meta = ["date", "home_team", "away_team", "tournament", "edition", "y"]
    hasil = kiri.loc[:, kolom_meta].copy()
    proba = (
        (1.0 - weight_b) * kiri.loc[:, ["p_H", "p_D", "p_A"]].to_numpy()
        + weight_b * kanan.loc[:, ["p_H", "p_D", "p_A"]].to_numpy()
    )
    hasil["p_H"] = proba[:, 0]
    hasil["p_D"] = proba[:, 1]
    hasil["p_A"] = proba[:, 2]
    return hasil.reset_index()


def tune_blend_weights(
    pred_a: pd.DataFrame,
    pred_b: pd.DataFrame,
    weights,
    n_bins: int = 10,
) -> pd.DataFrame:
    """Cari bobot model B yang meminimalkan rata-rata log loss antar fold."""
    baris = []
    for bobot in weights:
        bobot = float(bobot)
        if not 0 <= bobot <= 1:
            raise ValueError("setiap bobot harus di antara 0 dan 1")
        gabungan = blend_predictions(pred_a, pred_b, bobot)
        met = fold_metrics_from_predictions(gabungan, n_bins=n_bins)
        pool = pooled_metrics(gabungan, n_bins=n_bins)
        baris.append({
            "weight_b": bobot,
            "log_loss_mean": float(met["log_loss"].mean()),
            "log_loss_sd": float(met["log_loss"].std()),
            "log_loss_pooled": float(pool["log_loss"]),
            "brier_mean": float(met["brier"].mean()),
            "brier_pooled": float(pool["brier"]),
            "accuracy_pooled": float(pool["accuracy"]),
            "macro_f1_pooled": float(pool["macro_f1"]),
        })

    hasil = pd.DataFrame(baris)
    return hasil.sort_values(
        ["log_loss_mean", "brier_mean"], ascending=True
    ).reset_index(drop=True)
