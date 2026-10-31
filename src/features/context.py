"""Fitur konteks laga: status netral, tuan rumah sebenarnya, dan jenis turnamen.

Aturan pengelompokan turnamen sama dengan subbagian 4.3: ``Friendly`` (persis),
nama yang memuat ``qualification``, ``FIFA World Cup`` (persis), dan sisanya
``Lainnya``.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

KOLOM_WAJIB = ("match_id", "home_team", "away_team", "country", "neutral", "tournament")

KOLOM_FITUR = ("match_id", "neutral", "home_is_host", "away_is_host", "tournament_group")

URUTAN_KELOMPOK = ("Friendly", "Kualifikasi", "FIFA World Cup", "Lainnya")


def kelompok_turnamen(tournament: pd.Series) -> pd.Series:
    """Petakan nama turnamen ke empat kelompok dengan aturan eksplisit 4.3."""
    return pd.Series(
        np.select(
            [
                tournament == "Friendly",
                tournament.str.contains("qualification", regex=False),
                tournament == "FIFA World Cup",
            ],
            ["Friendly", "Kualifikasi", "FIFA World Cup"],
            default="Lainnya",
        ),
        index=tournament.index,
    )


def build_context(df: pd.DataFrame, urutan_kelompok: tuple[str, ...] = URUTAN_KELOMPOK) -> pd.DataFrame:
    """Bangun fitur konteks untuk setiap baris ``df``.

    Returns
    -------
    pandas.DataFrame
        Satu baris per ``match_id``:

        - ``neutral``: 0/1 dari kolom ``neutral``.
        - ``home_is_host``: 1 bila ``home_team`` sama persis dengan ``country``.
        - ``away_is_host``: 1 bila ``away_team`` sama persis dengan ``country``.
        - ``tournament_group``: salah satu dari ``Friendly``, ``Kualifikasi``,
          ``FIFA World Cup``, ``Lainnya``.

        Perbandingan nama memakai kecocokan string persis, sehingga tim yang
        berganti nama antar-era tidak terhitung sebagai tuan rumah.
    """
    hilang = [kolom for kolom in KOLOM_WAJIB if kolom not in df.columns]
    if hilang:
        raise KeyError(f"kolom wajib tidak ada: {hilang}")

    data = df.loc[:, list(KOLOM_WAJIB)].copy()
    if data["match_id"].duplicated().any():
        raise ValueError("match_id harus unik")
    if data["match_id"].isna().any():
        raise ValueError("match_id tidak boleh kosong")

    konteks = pd.DataFrame({
        "match_id": data["match_id"].to_numpy(),
        "neutral": data["neutral"].astype(int).to_numpy(),
        "home_is_host": (data["home_team"] == data["country"]).astype(int).to_numpy(),
        "away_is_host": (data["away_team"] == data["country"]).astype(int).to_numpy(),
        "tournament_group": kelompok_turnamen(data["tournament"]).to_numpy(),
    })
    tak_dikenal = set(konteks["tournament_group"].unique()) - set(urutan_kelompok)
    if tak_dikenal:
        raise ValueError(f"kelompok turnamen tidak dikenal: {sorted(tak_dikenal)}")
    return konteks
