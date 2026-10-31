"""Pemuatan data dev, definisi fold, dan orkestrasi evaluasi baseline.

Modul ini hanya memakai baris dev (``date < 2024-12-08``). Data ``final_test``
tidak pernah dipakai atau dievaluasi di sini.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.evaluation.metrics import (
    accuracy_score,
    brier_score,
    log_loss,
    macro_f1_score,
    ranked_probability_score,
    summary_metrics,
)

CUTOFF_TEST = pd.Timestamp("2024-12-08")
TURNAMEN_ASEAN = "AFF Championship"
N_DEV = 48093

METRICS_BOOTSTRAP = {
    "log_loss": log_loss,
    "brier": brier_score,
    "rps": ranked_probability_score,
    "accuracy": accuracy_score,
    "macro_f1": macro_f1_score,
}


def load_split_definition(root: str | Path) -> dict:
    """Baca ``data/processed/split_definition.json``."""
    path = Path(root) / "data" / "processed" / "split_definition.json"
    with path.open(encoding="utf-8") as berkas:
        return json.load(berkas)


def load_dev_features(root: str | Path) -> pd.DataFrame:
    """Gabungkan fitur dev dengan metadata turnamen; hanya baris dev yang dipakai."""
    root = Path(root)
    fitur = pd.read_csv(
        root / "data" / "processed" / "features_dev.csv",
        parse_dates=["date"],
    )
    if len(fitur) != N_DEV:
        raise ValueError(f"features_dev.csv harus {N_DEV} baris, ditemukan {len(fitur)}")

    metadata = pd.read_csv(
        root / "data" / "processed" / "matches_merged.csv",
        usecols=["match_id", "date", "tournament", "country"],
        parse_dates=["date"],
    )
    metadata = metadata.loc[metadata["date"] < CUTOFF_TEST, ["match_id", "tournament", "country"]]
    if len(metadata) != N_DEV:
        raise ValueError(f"metadata dev harus {N_DEV} baris, ditemukan {len(metadata)}")

    tabel = fitur.merge(metadata, on="match_id", how="left", validate="one_to_one")
    if len(tabel) != N_DEV:
        raise ValueError("merge fitur dan metadata mengubah jumlah baris")
    if tabel["tournament"].isna().any():
        raise ValueError("ada laga dev tanpa nama turnamen")
    if tabel["date"].max() >= CUTOFF_TEST:
        raise ValueError("load_dev_features tidak boleh memuat final_test")

    return tabel.sort_values(["date", "match_id"], kind="mergesort").reset_index(drop=True)


def annual_folds(features: pd.DataFrame, split_def: dict) -> list[dict]:
    """Fold walk-forward tahunan Y=2010..2024 sesuai split_definition.json."""
    folds = []
    for entri in split_def["fold_validasi_tahunan"]:
        tahun = int(entri["Y"])
        train_mask = (features["date"] < pd.Timestamp(f"{tahun}-01-01")).to_numpy()
        val_mask = (features["date"].dt.year == tahun).to_numpy()
        if int(train_mask.sum()) != int(entri["n_train"]):
            raise ValueError(f"n_train fold {tahun} tidak cocok")
        if int(val_mask.sum()) != int(entri["n_val"]):
            raise ValueError(f"n_val fold {tahun} tidak cocok")
        folds.append({
            "name": f"Y{tahun}",
            "edition": np.nan,
            "train_idx": train_mask,
            "val_idx": val_mask,
        })
    return folds


def asean_folds(features: pd.DataFrame, split_def: dict) -> list[dict]:
    """Fold edisi AFF Championship mulai 2010 sesuai split_definition.json."""
    folds = []
    for entri in split_def["fold_validasi_asean"]:
        awal = pd.Timestamp(entri["val_tanggal_awal"])
        akhir = pd.Timestamp(entri["val_tanggal_akhir"])
        train_mask = (features["date"] < awal).to_numpy()
        val_mask = (
            (features["tournament"] == TURNAMEN_ASEAN)
            & features["date"].between(awal, akhir)
        ).to_numpy()
        if int(train_mask.sum()) != int(entri["n_train"]):
            raise ValueError(f"n_train edisi {entri['edisi']} tidak cocok")
        if int(val_mask.sum()) != int(entri["n_val"]):
            raise ValueError(f"n_val edisi {entri['edisi']} tidak cocok")
        folds.append({
            "name": f"ASEAN-{entri['edisi']}",
            "edition": int(entri["edisi"]),
            "train_idx": train_mask,
            "val_idx": val_mask,
        })
    return folds


def run_folds(
    features: pd.DataFrame,
    folds: list[dict],
    fit_predict,
    n_bins: int = 10,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Jalankan satu baseline pada setiap fold dan kumpulkan prediksi + metrik."""
    if not folds:
        raise ValueError("daftar fold kosong")

    semua_prediksi = []
    baris_metrik = []
    for fold in folds:
        train = features.loc[fold["train_idx"]]
        val = features.loc[fold["val_idx"]]
        if train.empty or val.empty:
            raise ValueError(f"fold {fold['name']} memiliki data latih/validasi kosong")

        proba = np.asarray(fit_predict(train, val), dtype=float)
        if proba.shape != (len(val), 3):
            raise ValueError(f"proba fold {fold['name']} berukuran {proba.shape}, bukan {(len(val), 3)}")
        if not np.isfinite(proba).all():
            raise ValueError(f"proba fold {fold['name']} mengandung nilai non-finite")
        if not np.allclose(proba.sum(axis=1), 1.0, atol=1e-8):
            raise ValueError(f"proba fold {fold['name']} tidak berjumlah 1")

        prediksi = pd.DataFrame({
            "fold": fold["name"],
            "edition": fold.get("edition", np.nan),
            "match_id": val["match_id"].to_numpy(),
            "date": val["date"].to_numpy(),
            "home_team": val["home_team"].to_numpy(),
            "away_team": val["away_team"].to_numpy(),
            "tournament": val["tournament"].to_numpy(),
            "y": val["result"].to_numpy(),
            "p_H": proba[:, 0],
            "p_D": proba[:, 1],
            "p_A": proba[:, 2],
        })
        semua_prediksi.append(prediksi)

        metrik = summary_metrics(val["result"], proba, n_bins=n_bins)
        baris_metrik.append({
            "fold": fold["name"],
            "edition": fold.get("edition", np.nan),
            "n_train": int(len(train)),
            "n_val": int(len(val)),
            "val_start": val["date"].min(),
            "val_end": val["date"].max(),
            **metrik,
        })

    return pd.concat(semua_prediksi, ignore_index=True), pd.DataFrame(baris_metrik)


def pooled_metrics(predictions: pd.DataFrame, n_bins: int = 10) -> dict[str, float]:
    """Metrik pada seluruh baris prediksi yang digabung."""
    return summary_metrics(
        predictions["y"],
        predictions.loc[:, ["p_H", "p_D", "p_A"]].to_numpy(),
        n_bins=n_bins,
    )


def fold_metrics_from_predictions(
    predictions: pd.DataFrame,
    n_bins: int = 10,
) -> pd.DataFrame:
    """Hitung metrik per fold dari tabel prediksi yang sudah digabung."""
    if "fold" not in predictions.columns:
        raise KeyError("kolom fold tidak ada")
    baris = []
    for fold, bagian in predictions.groupby("fold", sort=False):
        metrik = pooled_metrics(bagian, n_bins=n_bins)
        baris.append({
            "fold": fold,
            "edition": bagian["edition"].iloc[0] if "edition" in bagian.columns else np.nan,
            "n_val": int(len(bagian)),
            "val_start": bagian["date"].min(),
            "val_end": bagian["date"].max(),
            **metrik,
        })
    return pd.DataFrame(baris)


def metrics_by_group(
    predictions: pd.DataFrame,
    group_col: str = "edition",
    n_bins: int = 10,
) -> pd.DataFrame:
    """Hitung metrik per kelompok (mis. edisi ASEAN)."""
    if group_col not in predictions.columns:
        raise KeyError(f"kolom {group_col} tidak ada")
    baris = []
    for nilai, bagian in predictions.groupby(group_col, sort=True, dropna=False):
        metrik = pooled_metrics(bagian, n_bins=n_bins)
        baris.append({group_col: nilai, "n": int(len(bagian)), **metrik})
    return pd.DataFrame(baris)


def bootstrap_metrics_table(
    predictions: pd.DataFrame,
    n_boot: int = 2000,
    seed: int = 42,
    alpha: float = 0.05,
    cluster_col: str | None = None,
) -> pd.DataFrame:
    """Tabel estimasi dan CI bootstrap untuk metrik utama."""
    from src.evaluation.metrics import bootstrap_ci

    y = predictions["y"].to_numpy()
    proba = predictions.loc[:, ["p_H", "p_D", "p_A"]].to_numpy()
    cluster = predictions[cluster_col].to_numpy() if cluster_col else None

    baris = []
    for nama, fungsi in METRICS_BOOTSTRAP.items():
        hasil = bootstrap_ci(
            y, proba, fungsi,
            n_boot=n_boot, seed=seed, alpha=alpha, cluster=cluster,
        )
        baris.append({"metrik": nama, **hasil})
    return pd.DataFrame(baris)


def paired_delta_table(
    prediksi_a: pd.DataFrame,
    prediksi_b: pd.DataFrame,
    n_boot: int = 2000,
    seed: int = 42,
    alpha: float = 0.05,
    cluster_col: str | None = None,
) -> pd.DataFrame:
    """Bandingkan dua baseline dengan pasangan laga yang sama."""
    from src.evaluation.metrics import paired_bootstrap_delta

    kunci = ["fold", "match_id"]
    kiri = prediksi_a.set_index(kunci).sort_index()
    kanan = prediksi_b.set_index(kunci).sort_index()
    if not kiri.index.equals(kanan.index):
        raise ValueError("pasangan prediksi tidak identik")
    if not kiri["y"].equals(kanan["y"]):
        raise ValueError("label target tidak identik")

    y = kiri["y"].to_numpy()
    p_a = kiri.loc[:, ["p_H", "p_D", "p_A"]].to_numpy()
    p_b = kanan.loc[:, ["p_H", "p_D", "p_A"]].to_numpy()
    if cluster_col is None:
        cluster = None
    elif cluster_col in kiri.columns:
        cluster = kiri[cluster_col].to_numpy()
    elif cluster_col in kiri.index.names:
        cluster = kiri.index.get_level_values(cluster_col).to_numpy()
    else:
        raise KeyError(f"kolom cluster {cluster_col} tidak ada")

    baris = []
    for nama, fungsi in METRICS_BOOTSTRAP.items():
        hasil = paired_bootstrap_delta(
            y, p_a, p_b, fungsi,
            n_boot=n_boot, seed=seed, alpha=alpha, cluster=cluster,
        )
        baris.append({"metrik": nama, **hasil})
    return pd.DataFrame(baris)
