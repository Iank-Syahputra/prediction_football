"""Test metrik probabilistik dan bootstrap pada data sintetis kecil."""

from __future__ import annotations

import numpy as np
import pytest

from src.evaluation.metrics import (
    accuracy_score,
    bootstrap_ci,
    brier_score,
    classwise_ece,
    expected_calibration_error,
    log_loss,
    macro_f1_score,
    paired_bootstrap_delta,
    ranked_probability_score,
    reliability_table,
    summary_metrics,
)


def test_metrik_sempurna() -> None:
    y = ["H", "D", "A"]
    p = np.eye(3)
    assert log_loss(y, p) == pytest.approx(0.0)
    assert brier_score(y, p) == pytest.approx(0.0)
    assert ranked_probability_score(y, p) == pytest.approx(0.0)
    assert accuracy_score(y, p) == pytest.approx(1.0)
    assert macro_f1_score(y, p) == pytest.approx(1.0)
    assert expected_calibration_error(y, p) == pytest.approx(0.0)
    assert classwise_ece(y, p) == pytest.approx(0.0)


def test_metrik_uniform() -> None:
    y = ["H", "D", "A"]
    p = np.full((3, 3), 1.0 / 3.0)
    assert log_loss(y, p) == pytest.approx(np.log(3.0))
    assert brier_score(y, p) == pytest.approx(2.0 / 3.0)
    assert ranked_probability_score(y, p) == pytest.approx(2.0 / 9.0)
    assert accuracy_score(y, p) == pytest.approx(1.0 / 3.0)
    assert macro_f1_score(y, p) == pytest.approx(1.0 / 6.0)


def test_ece_top_label_dan_classwise() -> None:
    y = ["H", "H", "D", "D"]
    p = np.tile([0.7, 0.2, 0.1], (4, 1))
    assert expected_calibration_error(y, p) == pytest.approx(0.2)
    assert classwise_ece(y, p) == pytest.approx(0.2)

    tabel = reliability_table(y, p, n_bins=10)
    assert list(tabel.columns) == [
        "kelompok", "bin", "batas_bawah", "batas_atas", "n", "prediksi_rata", "observasi",
    ]
    assert tabel["n"].sum() == 4
    assert tabel.loc[0, "prediksi_rata"] == pytest.approx(0.7)
    assert tabel.loc[0, "observasi"] == pytest.approx(0.5)


def test_summary_metrics_lengkap() -> None:
    y = np.array([0, 1, 2])
    p = np.eye(3)
    hasil = summary_metrics(y, p)
    assert set(hasil) == {
        "log_loss", "brier", "rps", "accuracy", "macro_f1", "ece_top", "ece_classwise",
    }
    assert all(np.isfinite(list(hasil.values())))


def test_bootstrap_ci_dan_paired_delta() -> None:
    y = np.array([0, 1, 2] * 10)
    p = np.eye(3)[y]
    hasil = bootstrap_ci(y, p, log_loss, n_boot=100, seed=7)
    assert hasil["estimate"] == pytest.approx(0.0)
    assert hasil["ci_low"] == pytest.approx(0.0)
    assert hasil["ci_high"] == pytest.approx(0.0)

    delta = paired_bootstrap_delta(y, p, p, log_loss, n_boot=100, seed=7)
    assert delta["estimate"] == pytest.approx(0.0)
    assert delta["ci_low"] == pytest.approx(0.0)
    assert delta["ci_high"] == pytest.approx(0.0)
    assert delta["proporsi_positif"] == pytest.approx(0.0)

    p_noisy = np.tile([0.6, 0.2, 0.2], (len(y), 1))
    hasil_noisy = bootstrap_ci(y, p_noisy, log_loss, n_boot=100, seed=7)
    assert hasil_noisy["ci_low"] <= hasil_noisy["estimate"] <= hasil_noisy["ci_high"]

    cluster = np.repeat([10, 20, 30], 10)
    hasil_cluster = bootstrap_ci(y, p_noisy, log_loss, n_boot=100, seed=7, cluster=cluster)
    assert hasil_cluster["ci_low"] <= hasil_cluster["estimate"] <= hasil_cluster["ci_high"]


def test_validasi_input() -> None:
    y = ["H", "D", "A"]
    with pytest.raises(ValueError, match="berukuran"):
        log_loss(y, np.ones((3, 2)))
    with pytest.raises(ValueError, match="berjumlah 1"):
        log_loss(y, np.full((3, 3), 0.5))
    with pytest.raises(ValueError, match="negatif"):
        log_loss(y, np.array([[1.1, -0.1, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]))
    with pytest.raises(ValueError, match="label"):
        log_loss(["H", "X", "A"], np.eye(3))
    with pytest.raises(ValueError, match="n_boot"):
        bootstrap_ci(y, np.eye(3), log_loss, n_boot=0)
    with pytest.raises(ValueError, match="alpha"):
        bootstrap_ci(y, np.eye(3), log_loss, n_boot=10, alpha=1.5)
    with pytest.raises(ValueError, match="cluster"):
        bootstrap_ci(y, np.eye(3), log_loss, n_boot=10, cluster=[1, 2])
