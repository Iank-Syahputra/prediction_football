"""Fitur riwayat pertemuan dua tim (head-to-head).

Hanya laga dengan tanggal **lebih awal** yang dihitung; pertemuan pada tanggal
yang sama tidak saling memengaruhi. Tidak ada pengisian nilai kosong: pasangan
yang belum pernah bertemu mendapat ``n_h2h = 0`` dan ``h2h_score_home = NaN``.
"""

from __future__ import annotations

import pandas as pd

KOLOM_WAJIB = ("match_id", "date", "home_team", "away_team", "home_score", "away_score")

KOLOM_FITUR = ("match_id", "n_h2h", "h2h_score_home")


def build_h2h(df: pd.DataFrame) -> pd.DataFrame:
    """Bangun fitur head-to-head untuk setiap baris ``df``.

    Returns
    -------
    pandas.DataFrame
        Satu baris per ``match_id``:

        - ``n_h2h``: jumlah pertemuan sebelumnya antara kedua tim, tanpa
          membedakan siapa tuan rumah.
        - ``h2h_score_home``: ``(menang_home + 0,5 * seri) / n_h2h`` dari sudut
          pandang ``home_team`` pada laga ini; ``NaN`` bila ``n_h2h = 0``.
    """
    hilang = [kolom for kolom in KOLOM_WAJIB if kolom not in df.columns]
    if hilang:
        raise KeyError(f"kolom wajib tidak ada: {hilang}")

    data = df.loc[:, list(KOLOM_WAJIB)].copy()
    data["date"] = pd.to_datetime(data["date"], errors="raise")
    kosong = [kolom for kolom in KOLOM_WAJIB if data[kolom].isna().any()]
    if kosong:
        raise ValueError(f"kolom berisi nilai kosong: {kosong}")
    if not data["match_id"].is_unique:
        raise ValueError("match_id harus unik")

    data = data.sort_values(["date", "match_id"], kind="mergesort").reset_index(drop=True)

    # kunci pasangan selalu terurut alfabetis -> [menang_kunci1, menang_kunci2, seri]
    rekap: dict[tuple[str, str], list[int]] = {}
    baris: list[tuple] = []

    for _, kelompok in data.groupby("date", sort=True):
        for laga in kelompok.itertuples(index=False):
            kunci = tuple(sorted((laga.home_team, laga.away_team)))
            menang_1, menang_2, seri = rekap.get(kunci, [0, 0, 0])
            n = menang_1 + menang_2 + seri
            if n:
                menang_home = menang_1 if laga.home_team == kunci[0] else menang_2
                skor = (menang_home + 0.5 * seri) / n
            else:
                skor = float("nan")
            baris.append((laga.match_id, n, skor))

        # pembaruan dilakukan setelah seluruh laga tanggal ini dihitung
        for laga in kelompok.itertuples(index=False):
            kunci = tuple(sorted((laga.home_team, laga.away_team)))
            rekap.setdefault(kunci, [0, 0, 0])
            if laga.home_score > laga.away_score:
                rekap[kunci][0 if laga.home_team == kunci[0] else 1] += 1
            elif laga.home_score < laga.away_score:
                rekap[kunci][1 if laga.home_team == kunci[0] else 0] += 1
            else:
                rekap[kunci][2] += 1

    fitur = pd.DataFrame(baris, columns=list(KOLOM_FITUR))
    fitur = fitur.astype({"n_h2h": "int64", "h2h_score_home": float})
    if not fitur.empty:
        fitur["match_id"] = fitur["match_id"].astype(data["match_id"].dtype)
    return fitur
