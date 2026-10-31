"""Fitur bentuk tim (form) menjelang laga.

Form sebuah laga hanya memakai laga-laga yang **lebih awal** dari tanggal laga
itu; semua laga pada tanggal yang sama memakai kondisi sebelum tanggal tersebut.
Tidak ada pengisian nilai kosong: tim tanpa riwayat mendapat ``NaN`` dan
``n_form = 0``.
"""

from __future__ import annotations

from collections import deque

import pandas as pd

KOLOM_WAJIB = (
    "match_id",
    "date",
    "home_team",
    "away_team",
    "home_score",
    "away_score",
)

KOLOM_FITUR = (
    "match_id",
    "form_pts_home",
    "form_gf_home",
    "form_ga_home",
    "n_form_home",
    "rest_days_home",
    "form_pts_away",
    "form_gf_away",
    "form_ga_away",
    "n_form_away",
    "rest_days_away",
)


def _poin(gol_cetak: int, gol_kemasukan: int) -> int:
    """Poin satu laga: 3 menang, 1 seri, 0 kalah."""
    if gol_cetak > gol_kemasukan:
        return 3
    if gol_cetak == gol_kemasukan:
        return 1
    return 0


def _ringkas(riwayat: deque) -> tuple[float, float, float, int]:
    """Rata-rata poin, gol cetak, dan gol kemasukan dari riwayat terakhir."""
    n = len(riwayat)
    if n == 0:
        return float("nan"), float("nan"), float("nan"), 0
    total_poin = sum(baris[0] for baris in riwayat)
    total_gf = sum(baris[1] for baris in riwayat)
    total_ga = sum(baris[2] for baris in riwayat)
    return total_poin / n, total_gf / n, total_ga / n, n


def build_form(df: pd.DataFrame, n_form: int = 5, rest_cap: int = 365) -> pd.DataFrame:
    """Bangun fitur form untuk setiap baris ``df``.

    Parameters
    ----------
    df : pandas.DataFrame
        Harus memuat :data:`KOLOM_WAJIB`.
    n_form : int
        Jumlah laga terakhir yang dipakai (default 5).
    rest_cap : int
        Batas atas ``rest_days`` dalam hari (default 365).

    Returns
    -------
    pandas.DataFrame
        Satu baris per ``match_id`` dengan kolom :data:`KOLOM_FITUR`. Untuk tiap
        sisi (home/away): rata-rata poin per laga (3/1/0), rata-rata gol cetak,
        rata-rata gol kemasukan, jumlah laga yang dipakai (``n_form``), dan hari
        sejak laga sebelumnya (``rest_days``, dibatasi ``rest_cap``). Tim tanpa
        riwayat mendapat ``NaN`` pada tiga rata-rata dan ``rest_days``, dengan
        ``n_form = 0``.
    """
    hilang = [kolom for kolom in KOLOM_WAJIB if kolom not in df.columns]
    if hilang:
        raise KeyError(f"kolom wajib tidak ada: {hilang}")
    if int(n_form) < 1:
        raise ValueError(f"n_form harus >= 1, ditemukan {n_form}")
    if int(rest_cap) < 1:
        raise ValueError(f"rest_cap harus >= 1, ditemukan {rest_cap}")

    data = df.loc[:, list(KOLOM_WAJIB)].copy()
    data["date"] = pd.to_datetime(data["date"], errors="raise")
    kosong = [kolom for kolom in KOLOM_WAJIB if data[kolom].isna().any()]
    if kosong:
        raise ValueError(f"kolom berisi nilai kosong: {kosong}")
    if not data["match_id"].is_unique:
        raise ValueError("match_id harus unik")

    data = data.sort_values(["date", "match_id"], kind="mergesort").reset_index(drop=True)

    riwayat: dict[str, deque] = {}
    laga_terakhir: dict[str, pd.Timestamp] = {}
    baris: list[tuple] = []
    pembaruan: list[tuple[str, int, int, int]] = []

    for tanggal, kelompok in data.groupby("date", sort=True):
        pembaruan = []
        for laga in kelompok.itertuples(index=False):
            home, away = laga.home_team, laga.away_team
            if home not in riwayat:
                riwayat[home] = deque(maxlen=int(n_form))
            if away not in riwayat:
                riwayat[away] = deque(maxlen=int(n_form))

            pts_home, gf_home, ga_home, n_home = _ringkas(riwayat[home])
            pts_away, gf_away, ga_away, n_away = _ringkas(riwayat[away])

            rest_home = (
                float(min((tanggal - laga_terakhir[home]).days, int(rest_cap)))
                if home in laga_terakhir
                else float("nan")
            )
            rest_away = (
                float(min((tanggal - laga_terakhir[away]).days, int(rest_cap)))
                if away in laga_terakhir
                else float("nan")
            )

            baris.append(
                (laga.match_id,
                 pts_home, gf_home, ga_home, n_home, rest_home,
                 pts_away, gf_away, ga_away, n_away, rest_away)
            )
            pembaruan.append((home, laga.home_score, laga.away_score, tanggal))
            pembaruan.append((away, laga.away_score, laga.home_score, tanggal))

        # riwayat baru diperbarui setelah seluruh laga tanggal ini dihitung
        for tim, gol_cetak, gol_kemasukan, tanggal_laga in pembaruan:
            riwayat[tim].append((_poin(gol_cetak, gol_kemasukan), gol_cetak, gol_kemasukan))
            laga_terakhir[tim] = tanggal_laga

    fitur = pd.DataFrame(baris, columns=list(KOLOM_FITUR))
    fitur = fitur.astype({
        "form_pts_home": float, "form_gf_home": float, "form_ga_home": float,
        "form_pts_away": float, "form_gf_away": float, "form_ga_away": float,
        "n_form_home": "int64", "n_form_away": "int64",
        "rest_days_home": float, "rest_days_away": float,
    })
    if not fitur.empty:
        fitur["match_id"] = fitur["match_id"].astype(data["match_id"].dtype)
    return fitur
