"""Metrik evaluasi probabilitas dan interval bootstrap.

Semua fungsi menerima ``y_true`` berupa label ``"H"``/``"D"``/``"A"`` atau
integer ``0``/``1``/``2``, serta ``proba`` berukuran ``(n, 3)`` dengan urutan
kolom H, D, A. Probabilitas harus non-negatif dan berjumlah 1 per baris.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator

import numpy as np
import pandas as pd

LABELS = ("H", "D", "A")
N_KELAS = len(LABELS)
_LABEL_KE_INDEKS = {label: i for i, label in enumerate(LABELS)}


def encode_labels(y_true) -> np.ndarray:
    """Ubah label H/D/A (atau integer 0/1/2) menjadi array integer 0/1/2."""
    return _as_indeks(y_true)


def decode_labels(y_true) -> np.ndarray:
    """Ubah integer 0/1/2 menjadi label H/D/A."""
    indeks = _as_indeks(y_true)
    return np.asarray(LABELS, dtype=object)[indeks]


def _as_indeks(y_true) -> np.ndarray:
    """Validasi dan normalisasi label target."""
    y = np.asarray(y_true)
    if y.ndim != 1:
        raise ValueError(f"y_true harus 1 dimensi, ditemukan {y.shape}")
    if len(y) == 0:
        raise ValueError("y_true tidak boleh kosong")

    if y.dtype.kind in "OUS":
        hasil = np.full(len(y), -1, dtype=int)
        for i, nilai in enumerate(y):
            if isinstance(nilai, str) and nilai in _LABEL_KE_INDEKS:
                hasil[i] = _LABEL_KE_INDEKS[nilai]
        if (hasil < 0).any():
            raise ValueError("label tidak dikenal; gunakan H, D, A, atau 0/1/2")
        return hasil

    if y.dtype.kind not in "iu":
        if y.dtype.kind == "f" and np.isfinite(y).all() and np.all(y == np.floor(y)):
            y = y.astype(int)
        else:
            raise ValueError("label numerik harus berupa integer 0/1/2")

    indeks = y.astype(int)
    if ((indeks < 0) | (indeks >= N_KELAS)).any():
        raise ValueError("label numerik harus 0, 1, atau 2")
    return indeks


def _as_proba(proba) -> np.ndarray:
    """Validasi matriks probabilitas berukuran (n, 3)."""
    p = np.asarray(proba, dtype=float)
    if p.ndim != 2 or p.shape[1] != N_KELAS:
        raise ValueError(f"proba harus berukuran (n, 3), ditemukan {p.shape}")
    if len(p) == 0:
        raise ValueError("proba tidak boleh kosong")
    if not np.isfinite(p).all():
        raise ValueError("proba mengandung nilai non-finite")
    if (p < 0).any():
        raise ValueError("proba mengandung nilai negatif")
    jumlah = p.sum(axis=1)
    if not np.allclose(jumlah, 1.0, atol=1e-8):
        raise ValueError("setiap baris proba harus berjumlah 1")
    return p


def _pasangan_valid(y_true, proba) -> tuple[np.ndarray, np.ndarray]:
    y = _as_indeks(y_true)
    p = _as_proba(proba)
    if len(y) != len(p):
        raise ValueError(f"jumlah y_true ({len(y)}) dan proba ({len(p)}) berbeda")
    return y, p


def log_loss(y_true, proba, eps: float = 1e-15) -> float:
    """Multiclass log loss (semakin kecil semakin baik)."""
    y, p = _pasangan_valid(y_true, proba)
    p_benar = np.clip(p[np.arange(len(y)), y], eps, 1.0)
    return float(-np.mean(np.log(p_benar)))


def brier_score(y_true, proba) -> float:
    """Multiclass Brier score: rata-rata jumlah kuadrat selisih (semakin kecil)."""
    y, p = _pasangan_valid(y_true, proba)
    satu_panas = np.zeros_like(p)
    satu_panas[np.arange(len(y)), y] = 1.0
    return float(np.mean(np.sum((p - satu_panas) ** 2, axis=1)))


def ranked_probability_score(y_true, proba) -> float:
    """Ranked Probability Score untuk tiga kelas terurut H, D, A."""
    y, p = _pasangan_valid(y_true, proba)
    satu_panas = np.zeros_like(p)
    satu_panas[np.arange(len(y)), y] = 1.0
    kumulatif_p = np.cumsum(p, axis=1)[:, :-1]
    kumulatif_y = np.cumsum(satu_panas, axis=1)[:, :-1]
    return float(np.mean(np.sum((kumulatif_p - kumulatif_y) ** 2, axis=1) / (N_KELAS - 1)))


def accuracy_score(y_true, proba) -> float:
    """Akurasi kelas dengan probabilitas terbesar."""
    y, p = _pasangan_valid(y_true, proba)
    return float(np.mean(p.argmax(axis=1) == y))


def macro_f1_score(y_true, proba) -> float:
    """Macro F1 atas tiga kelas."""
    y, p = _pasangan_valid(y_true, proba)
    prediksi = p.argmax(axis=1)
    f1_per_kelas = []
    for kelas in range(N_KELAS):
        benar = prediksi == kelas
        aktual = y == kelas
        tp = int(np.sum(benar & aktual))
        fp = int(np.sum(benar & ~aktual))
        fn = int(np.sum(~benar & aktual))
        presisi = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * presisi * recall / (presisi + recall) if presisi + recall else 0.0
        f1_per_kelas.append(f1)
    return float(np.mean(f1_per_kelas))


def reliability_table(y_true, proba, n_bins: int = 10, class_idx: int | None = None) -> pd.DataFrame:
    """Tabel reliabilitas untuk plot kalibrasi.

    ``class_idx=None`` memakai top-label (kelas dengan probabilitas terbesar).
    ``class_idx=0/1/2`` memakai pendekatan one-vs-rest untuk kelas tersebut.
    """
    y, p = _pasangan_valid(y_true, proba)
    if n_bins < 2:
        raise ValueError("n_bins harus >= 2")

    if class_idx is None:
        keyakinan = p.max(axis=1)
        observasi = (p.argmax(axis=1) == y).astype(float)
        nama = "top-label"
    else:
        if class_idx not in range(N_KELAS):
            raise ValueError("class_idx harus 0, 1, 2, atau None")
        keyakinan = p[:, class_idx]
        observasi = (y == class_idx).astype(float)
        nama = f"kelas {LABELS[class_idx]}"

    batas = np.linspace(0.0, 1.0, n_bins + 1)
    bin_id = np.digitize(keyakinan, batas[1:-1], right=False)

    baris = []
    for b in range(n_bins):
        mask = bin_id == b
        n = int(mask.sum())
        if n == 0:
            continue
        baris.append({
            "kelompok": nama,
            "bin": b,
            "batas_bawah": float(batas[b]),
            "batas_atas": float(batas[b + 1]),
            "n": n,
            "prediksi_rata": float(keyakinan[mask].mean()),
            "observasi": float(observasi[mask].mean()),
        })
    return pd.DataFrame(baris)


def expected_calibration_error(
    y_true,
    proba,
    n_bins: int = 10,
    class_idx: int | None = None,
) -> float:
    """Expected Calibration Error (ECE) top-label atau one-vs-rest."""
    tabel = reliability_table(y_true, proba, n_bins=n_bins, class_idx=class_idx)
    if tabel.empty:
        raise ValueError("tidak ada bin yang terisi")
    total = tabel["n"].sum()
    return float(np.sum(tabel["n"] / total * np.abs(tabel["prediksi_rata"] - tabel["observasi"])))


def classwise_ece(y_true, proba, n_bins: int = 10) -> float:
    """Rata-rata ECE one-vs-rest untuk H, D, dan A."""
    return float(np.mean([
        expected_calibration_error(y_true, proba, n_bins=n_bins, class_idx=k)
        for k in range(N_KELAS)
    ]))


def summary_metrics(y_true, proba, n_bins: int = 10) -> dict[str, float]:
    """Kumpulan metrik utama untuk satu set prediksi."""
    return {
        "log_loss": log_loss(y_true, proba),
        "brier": brier_score(y_true, proba),
        "rps": ranked_probability_score(y_true, proba),
        "accuracy": accuracy_score(y_true, proba),
        "macro_f1": macro_f1_score(y_true, proba),
        "ece_top": expected_calibration_error(y_true, proba, n_bins=n_bins),
        "ece_classwise": classwise_ece(y_true, proba, n_bins=n_bins),
    }


def _bootstrap_indices(
    n: int,
    n_boot: int,
    seed: int,
    cluster=None,
) -> Iterator[np.ndarray]:
    """Hasilkan indeks bootstrap; opsional dengan resampling per cluster."""
    if n_boot <= 0:
        raise ValueError("n_boot harus > 0")
    rng = np.random.default_rng(seed)
    if cluster is None:
        for _ in range(n_boot):
            yield rng.integers(0, n, size=n)
        return

    kelompok = np.asarray(cluster)
    if kelompok.shape != (n,):
        raise ValueError("cluster harus 1 dimensi dan sepanjang y_true")
    if pd.isna(kelompok).any():
        raise ValueError("cluster mengandung nilai kosong")
    unik = np.unique(kelompok)
    indeks_per_kelompok = {nilai: np.flatnonzero(kelompok == nilai) for nilai in unik}
    for _ in range(n_boot):
        dipilih = rng.choice(unik, size=len(unik), replace=True)
        yield np.concatenate([indeks_per_kelompok[nilai] for nilai in dipilih])


def _validasi_alpha(alpha: float) -> None:
    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha harus di antara 0 dan 1")


def bootstrap_ci(
    y_true,
    proba,
    metric_fn: Callable[[np.ndarray, np.ndarray], float],
    n_boot: int = 2000,
    seed: int = 42,
    alpha: float = 0.05,
    cluster=None,
) -> dict[str, float]:
    """Interval kepercayaan bootstrap persentil untuk satu metrik."""
    y, p = _pasangan_valid(y_true, proba)
    _validasi_alpha(alpha)
    nilai = np.asarray([
        metric_fn(y[idx], p[idx])
        for idx in _bootstrap_indices(len(y), n_boot, seed, cluster)
    ])
    return {
        "estimate": float(metric_fn(y, p)),
        "ci_low": float(np.quantile(nilai, alpha / 2)),
        "ci_high": float(np.quantile(nilai, 1 - alpha / 2)),
        "n_boot": int(n_boot),
    }


def paired_bootstrap_delta(
    y_true,
    proba_a,
    proba_b,
    metric_fn: Callable[[np.ndarray, np.ndarray], float],
    n_boot: int = 2000,
    seed: int = 42,
    alpha: float = 0.05,
    cluster=None,
) -> dict[str, float]:
    """Bootstrap selisih metrik A - B dengan indeks resampling yang sama."""
    y, p_a = _pasangan_valid(y_true, proba_a)
    _, p_b = _pasangan_valid(y_true, proba_b)
    _validasi_alpha(alpha)
    delta = np.asarray([
        metric_fn(y[idx], p_a[idx]) - metric_fn(y[idx], p_b[idx])
        for idx in _bootstrap_indices(len(y), n_boot, seed, cluster)
    ])
    return {
        "estimate": float(metric_fn(y, p_a) - metric_fn(y, p_b)),
        "ci_low": float(np.quantile(delta, alpha / 2)),
        "ci_high": float(np.quantile(delta, 1 - alpha / 2)),
        "proporsi_positif": float(np.mean(delta > 0)),
        "n_boot": int(n_boot),
    }
