"""Gabungan seluruh fitur pra-laga: Elo, form, head-to-head, dan konteks.

Fungsi :func:`build_all` mengembalikan satu tabel per laga yang siap dipakai
tahap berikutnya (split dan model). Tidak ada pengisian nilai kosong di sini;
imputasi dilakukan nanti di pipeline, memakai statistik dari data latih saja.
"""

from __future__ import annotations

import pandas as pd

from src.features.context import KOLOM_FITUR as KOLOM_KONTEKS
from src.features.context import build_context
from src.features.elo import KOLOM_FITUR as KOLOM_ELO
from src.features.elo import build_elo
from src.features.form import KOLOM_FITUR as KOLOM_FORM
from src.features.form import build_form
from src.features.h2h import KOLOM_FITUR as KOLOM_H2H
from src.features.h2h import build_h2h

KOLOM_DASAR = ("match_id", "date", "home_team", "away_team", "result")

ELO_DEFAULT = {"k": 30, "home_adv": 100, "init": 1500, "use_goal_mult": True}

KOLOM_FITUR = (
    KOLOM_DASAR
    + tuple(kolom for kolom in KOLOM_ELO if kolom != "match_id")
    + tuple(kolom for kolom in KOLOM_FORM if kolom != "match_id")
    + tuple(kolom for kolom in KOLOM_H2H if kolom != "match_id")
    + tuple(kolom for kolom in KOLOM_KONTEKS if kolom != "match_id")
)


def build_all(
    df: pd.DataFrame,
    elo_params: dict | None = None,
    n_form: int = 5,
    rest_cap: int = 365,
) -> pd.DataFrame:
    """Gabungkan fitur Elo, form, head-to-head, dan konteks menjadi satu tabel.

    Parameters
    ----------
    df : pandas.DataFrame
        Data laga. Harus memuat kolom untuk Elo (``match_id``, ``date``,
        ``home_team``, ``away_team``, ``home_score``, ``away_score``,
        ``neutral``), form/h2h (kolom skor), konteks (``country``,
        ``tournament``), dan ``result`` sebagai target.
    elo_params : dict, optional
        Parameter Elo (``k``, ``home_adv``, ``init``, ``use_goal_mult``).
        Nilai yang tidak disebut memakai :data:`ELO_DEFAULT`.
    n_form : int
        Jumlah laga terakhir untuk fitur form (default 5).
    rest_cap : int
        Batas atas ``rest_days`` dalam hari (default 365).

    Returns
    -------
    pandas.DataFrame
        Satu baris per ``match_id``, terurut menurut ``date`` lalu ``match_id``,
        dengan kolom :data:`KOLOM_FITUR`: identitas laga, ``result`` sebagai
        target, lalu fitur Elo, form, head-to-head, dan konteks.
    """
    hilang = [kolom for kolom in KOLOM_DASAR if kolom not in df.columns]
    if hilang:
        raise KeyError(f"kolom wajib tidak ada: {hilang}")
    if df["match_id"].duplicated().any():
        raise ValueError("match_id harus unik")

    params = dict(ELO_DEFAULT)
    if elo_params:
        params.update(elo_params)

    fitur_elo, _ = build_elo(df, **params)
    fitur_form = build_form(df, n_form=n_form, rest_cap=rest_cap)
    fitur_h2h = build_h2h(df)
    fitur_konteks = build_context(df)

    tabel = df.loc[:, list(KOLOM_DASAR)].copy()
    tabel["date"] = pd.to_datetime(tabel["date"], errors="raise")
    for bagian in (fitur_elo, fitur_form, fitur_h2h, fitur_konteks):
        tabel = tabel.merge(bagian, on="match_id", how="left", validate="one_to_one")

    tabel = tabel.sort_values(["date", "match_id"], kind="mergesort").reset_index(drop=True)
    if len(tabel) != len(df):
        raise ValueError(f"jumlah baris berubah: {len(df)} -> {len(tabel)}")
    return tabel.loc[:, list(KOLOM_FITUR)]
