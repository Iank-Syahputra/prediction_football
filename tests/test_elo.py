"""Test untuk :func:`src.features.elo.build_elo`.

Seluruh test memakai data sintetis kecil, kecuali test prefix-invariance yang
memakai `data/processed/matches_merged.csv` yang dipotong ke `date < 2024-12-08`
(dev). Tidak ada test yang membaca atau menghitung apa pun pada `final_test`.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from src.features.elo import KOLOM_FITUR, build_elo

AKAR = Path(__file__).resolve().parents[1]
CUTOFF_TEST = pd.Timestamp("2024-12-08")
KOLOM_INPUT = (
    "match_id",
    "date",
    "home_team",
    "away_team",
    "home_score",
    "away_score",
    "neutral",
)


def _df(baris: list[tuple]) -> pd.DataFrame:
    """Bangun DataFrame input dari daftar tuple sesuai urutan KOLOM_INPUT."""
    return pd.DataFrame(baris, columns=list(KOLOM_INPUT))


def test_a_laga_pertama_rating_dan_n_prev() -> None:
    """Laga pertama kedua tim: rating 1500, n_prev 0, dan delta sesuai rumus."""
    df = _df([[1, "2020-01-01", "A", "B", 2, 0, False]])
    fitur, akhir = build_elo(df, k=30, home_adv=100, init=1500, use_goal_mult=True)

    assert list(fitur.columns) == list(KOLOM_FITUR)
    assert len(fitur) == 1
    baris = fitur.iloc[0]
    assert baris["match_id"] == 1
    assert baris["elo_home_pre"] == pytest.approx(1500.0)
    assert baris["elo_away_pre"] == pytest.approx(1500.0)
    assert baris["elo_diff"] == pytest.approx(0.0)
    assert baris["n_prev_home"] == 0
    assert baris["n_prev_away"] == 0

    # satu laga tuan rumah, selisih gol 2 -> G = 1,5, S = 1
    e_home = 1.0 / (1.0 + 10.0 ** (-(0.0 + 100.0) / 400.0))
    delta = 30.0 * 1.5 * (1.0 - e_home)
    assert akhir.loc["A"] == pytest.approx(1500.0 + delta)
    assert akhir.loc["B"] == pytest.approx(1500.0 - delta)


def test_b_zero_sum() -> None:
    """Jumlah seluruh rating akhir = init x jumlah tim yang pernah muncul."""
    df = _df(
        [
            [1, "2019-03-01", "A", "B", 1, 0, False],
            [2, "2019-04-01", "C", "A", 2, 2, True],
            [3, "2019-05-01", "B", "C", 0, 5, False],
            [4, "2019-06-01", "D", "A", 3, 1, True],
            [5, "2019-07-01", "D", "B", 0, 0, False],
        ]
    )
    _, akhir = build_elo(df, k=40, home_adv=80, init=1500, use_goal_mult=True)

    assert len(akhir) == 4
    assert set(akhir.index) == {"A", "B", "C", "D"}
    assert akhir.sum() == pytest.approx(1500.0 * 4)


def test_c_aturan_tanggal_sama() -> None:
    """Laga pada tanggal sama memakai rating sebelum tanggal itu."""
    df = _df(
        [
            [1, "2020-06-01", "A", "B", 3, 0, False],
            [2, "2020-06-01", "A", "C", 0, 1, False],
            [3, "2020-06-02", "A", "B", 1, 1, False],
        ]
    )
    fitur, _ = build_elo(df)
    per_id = fitur.set_index("match_id")

    # laga 2 memakai rating A sebelum 2020-06-01, bukan setelah laga 1
    assert per_id.loc[2, "elo_home_pre"] == pytest.approx(1500.0)
    assert per_id.loc[2, "elo_away_pre"] == pytest.approx(1500.0)
    assert per_id.loc[1, "elo_home_pre"] == pytest.approx(1500.0)
    assert per_id.loc[1, "n_prev_home"] == 0
    assert per_id.loc[2, "n_prev_home"] == 0

    # laga 3 baru melihat rating setelah kedua laga tanggal 2020-06-01
    _, akhir_dua_laga = build_elo(df.iloc[[0, 1]])
    assert per_id.loc[3, "elo_home_pre"] == pytest.approx(akhir_dua_laga.loc["A"])
    # A sudah main 2 kali pada 2020-06-01 (keduanya sebelum tanggal laga 3), B 1 kali
    assert per_id.loc[3, "n_prev_home"] == 2
    assert per_id.loc[3, "n_prev_away"] == 1


def test_d_kausalitas_skor_masa_depan() -> None:
    """Mengubah skor laga date >= T tidak mengubah fitur laga date <= T."""
    df = _df(
        [
            [1, "2020-01-01", "A", "B", 1, 0, False],
            [2, "2020-03-01", "B", "C", 0, 2, True],
            [3, "2020-09-01", "C", "A", 1, 1, False],
            [4, "2021-01-01", "A", "C", 2, 0, True],
            [5, "2021-05-01", "B", "A", 3, 1, False],
            [6, "2021-09-01", "C", "B", 0, 0, True],
        ]
    )
    batas = pd.Timestamp("2021-01-01")
    ubah = df.copy()
    nanti = ubah["date"].map(pd.Timestamp) >= batas
    ubah.loc[nanti, "home_score"] = 7
    ubah.loc[nanti, "away_score"] = 0

    fitur_asli, _ = build_elo(df)
    fitur_ubah, _ = build_elo(ubah)

    ids_lampau = df.loc[df["date"].map(pd.Timestamp) <= batas, "match_id"]
    lampau_asli = (
        fitur_asli[fitur_asli["match_id"].isin(ids_lampau)]
        .sort_values("match_id")
        .reset_index(drop=True)
    )
    lampau_ubah = (
        fitur_ubah[fitur_ubah["match_id"].isin(ids_lampau)]
        .sort_values("match_id")
        .reset_index(drop=True)
    )
    pd.testing.assert_frame_equal(lampau_asli, lampau_ubah)

    # pastikan perubahan skor memang berpengaruh pada laga sesudahnya
    ids_nanti = df.loc[df["date"].map(pd.Timestamp) > batas, "match_id"]
    nanti_asli = fitur_asli[fitur_asli["match_id"].isin(ids_nanti)].reset_index(drop=True)
    nanti_ubah = fitur_ubah[fitur_ubah["match_id"].isin(ids_nanti)].reset_index(drop=True)
    assert not nanti_asli.equals(nanti_ubah)


def test_e_prefix_invariance_pada_dev() -> None:
    """Fitur dari prefix dev identik dengan baris yang sama pada dev penuh."""
    berkas = AKAR / "data" / "processed" / "matches_merged.csv"
    kolom = ["match_id", "date", "home_team", "away_team", "home_score", "away_score", "neutral"]
    lengkap = pd.read_csv(berkas, parse_dates=["date"])[kolom]

    dev = lengkap[lengkap["date"] < CUTOFF_TEST].copy()
    assert dev["date"].max() < CUTOFF_TEST
    assert len(dev) == 48093

    batas_prefix = pd.Timestamp("2015-01-01")
    prefix = dev[dev["date"] < batas_prefix].copy()
    assert 0 < len(prefix) < len(dev)

    fitur_dev, _ = build_elo(dev, k=30, home_adv=100, init=1500, use_goal_mult=True)
    fitur_prefix, _ = build_elo(prefix, k=30, home_adv=100, init=1500, use_goal_mult=True)

    dari_dev = (
        fitur_dev[fitur_dev["match_id"].isin(set(fitur_prefix["match_id"]))]
        .sort_values("match_id")
        .reset_index(drop=True)
    )
    pd.testing.assert_frame_equal(dari_dev, fitur_prefix.sort_values("match_id").reset_index(drop=True))
