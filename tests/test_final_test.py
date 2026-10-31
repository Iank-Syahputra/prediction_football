"""Test loader final test Section 8."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.evaluation.final_test import (
    N_ASEAN_FINAL,
    N_FINAL_EVAL,
    N_FINAL_TEST,
    TURNAMEN_ASEAN,
    TURNAMEN_FIFA,
    load_final_test,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_load_final_test_memisahkan_fifa_dan_menjaga_cutoff() -> None:
    mentah, fitur = load_final_test(PROJECT_ROOT)

    assert len(mentah) == N_FINAL_TEST
    assert len(fitur) == N_FINAL_EVAL
    assert len(mentah) - len(fitur) == int((mentah["tournament"] == TURNAMEN_FIFA).sum())
    assert (mentah["tournament"] == TURNAMEN_FIFA).sum() == 14
    assert (fitur["tournament"] == TURNAMEN_ASEAN).sum() == N_ASEAN_FINAL
    assert fitur["date"].min() >= pd.Timestamp("2024-12-08")
    assert fitur["match_id"].is_unique
    assert not (fitur["tournament"] == TURNAMEN_FIFA).any()
    assert {"elo_diff", "form_pts_home", "h2h_score_home", "tournament_group"} <= set(fitur.columns)
