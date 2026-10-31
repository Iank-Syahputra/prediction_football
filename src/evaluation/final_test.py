"""Pemuatan final test dan pembangunan fitur pra-laga untuk evaluasi Section 8."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.evaluation.validation import CUTOFF_TEST
from src.features.build_features import build_all

N_FINAL_TEST = 1852
N_FINAL_EVAL = 1838
N_ASEAN_FINAL = 52
TURNAMEN_ASEAN = "ASEAN Championship"
TURNAMEN_FIFA = "FIFA ASEAN Cup"


def load_final_test(root: str | Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Muat final test sekali dan bangun fiturnya secara kausal.

    ``FIFA ASEAN Cup`` dikeluarkan dari feature history dan dari tabel fitur,
    sesuai keputusan Section 5. Tabel mentah final test tetap dikembalikan agar
    komposisi baris dapat dilaporkan tanpa menghitung metriknya.
    """
    root = Path(root)
    path = root / "data" / "processed" / "matches_merged.csv"
    mentah = pd.read_csv(path, parse_dates=["date"])

    final_mentah = mentah.loc[mentah["date"] >= CUTOFF_TEST].copy()
    if len(final_mentah) != N_FINAL_TEST:
        raise ValueError(f"final test harus {N_FINAL_TEST} baris, ditemukan {len(final_mentah)}")
    if final_mentah["date"].min() < CUTOFF_TEST:
        raise ValueError("final test memuat tanggal sebelum cutoff")

    dasar = mentah.loc[mentah["tournament"] != TURNAMEN_FIFA].copy()
    fitur = build_all(dasar)
    fitur = fitur.loc[fitur["date"] >= CUTOFF_TEST].copy()

    metadata = dasar.loc[
        dasar["date"] >= CUTOFF_TEST, ["match_id", "tournament"]
    ]
    fitur = fitur.merge(metadata, on="match_id", how="left", validate="one_to_one")
    if len(fitur) != N_FINAL_EVAL:
        raise ValueError(f"fitur final test harus {N_FINAL_EVAL} baris, ditemukan {len(fitur)}")
    if fitur["tournament"].isna().any():
        raise ValueError("ada baris final test tanpa nama turnamen")
    if (fitur["tournament"] == TURNAMEN_FIFA).any():
        raise ValueError("FIFA ASEAN Cup tidak boleh masuk tabel fitur final test")

    asean = fitur.loc[fitur["tournament"] == TURNAMEN_ASEAN]
    if len(asean) != N_ASEAN_FINAL:
        raise ValueError(f"ASEAN Championship final test harus {N_ASEAN_FINAL} baris, ditemukan {len(asean)}")

    fitur = fitur.sort_values(["date", "match_id"], kind="mergesort").reset_index(drop=True)
    return final_mentah, fitur
