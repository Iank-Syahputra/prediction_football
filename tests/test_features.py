"""Test untuk fitur tambahan 5.3: form, head-to-head, konteks, dan build_all.

Seluruh test memakai data sintetis kecil, kecuali test prefix-invariance yang
memakai `data/processed/matches_merged.csv` yang dipotong ke `date < 2024-12-08`
(dev). Tidak ada test yang membaca atau menghitung apa pun pada `final_test`.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src.features.build_features import build_all
from src.features.context import build_context, kelompok_turnamen
from src.features.form import build_form
from src.features.h2h import build_h2h

AKAR = Path(__file__).resolve().parents[1]
CUTOFF_TEST = pd.Timestamp("2024-12-08")

KOLOM = (
    "match_id", "date", "home_team", "away_team", "home_score", "away_score",
    "neutral", "country", "tournament",
)


def _df(baris: list[tuple]) -> pd.DataFrame:
    """Bangun DataFrame lengkap (termasuk ``result``) dari daftar tuple KOLOM."""
    df = pd.DataFrame(baris, columns=list(KOLOM))
    df["result"] = np.where(
        df["home_score"] > df["away_score"], "H",
        np.where(df["home_score"] == df["away_score"], "D", "A"),
    )
    return df


def _isi_hasil(df: pd.DataFrame) -> pd.DataFrame:
    """Hitung ulang ``result`` dari skor (dipakai setelah skor diubah)."""
    df = df.copy()
    df["result"] = np.where(
        df["home_score"] > df["away_score"], "H",
        np.where(df["home_score"] == df["away_score"], "D", "A"),
    )
    return df


def test_a_kausalitas_skor_masa_depan() -> None:
    """Mengubah skor laga date >= T tidak mengubah fitur laga date <= T."""
    df = _df([
        [1, "2019-03-01", "A", "B", 1, 0, False, "A", "Friendly"],
        [2, "2019-06-01", "B", "C", 2, 2, True, "C", "FIFA World Cup"],
        [3, "2019-09-01", "C", "A", 0, 3, False, "C", "Friendly"],
        [4, "2020-02-01", "A", "C", 1, 1, True, "C", "Friendly"],
        [5, "2020-08-01", "B", "A", 2, 0, False, "B", "Friendly"],
        [6, "2021-01-01", "C", "B", 1, 2, True, "C", "Friendly"],
        [7, "2021-06-01", "A", "B", 3, 0, False, "A", "Friendly"],
        [8, "2021-09-01", "B", "C", 0, 0, True, "C", "Friendly"],
    ])
    batas = pd.Timestamp("2021-01-01")
    ubah = df.copy()
    nanti = ubah["date"].map(pd.Timestamp) >= batas
    ubah.loc[nanti, "home_score"] = 9
    ubah.loc[nanti, "away_score"] = 0
    ubah = _isi_hasil(ubah)

    asli = build_all(df)
    diubah = build_all(ubah)
    assert list(asli.columns) == list(diubah.columns)

    ids_lampau = df.loc[df["date"].map(pd.Timestamp) <= batas, "match_id"]
    a = asli[asli["match_id"].isin(ids_lampau)].sort_values("match_id").reset_index(drop=True)
    b = diubah[diubah["match_id"].isin(ids_lampau)].sort_values("match_id").reset_index(drop=True)
    # `result` adalah target, bukan fitur, sehingga tidak dibandingkan:
    # laga pada tanggal T sendiri memang ikut berubah hasilnya.
    pd.testing.assert_frame_equal(a.drop(columns="result"), b.drop(columns="result"))

    # pastikan perubahan skor memang berpengaruh pada laga sesudahnya
    ids_nanti = df.loc[df["date"].map(pd.Timestamp) > batas, "match_id"]
    c = asli[asli["match_id"].isin(ids_nanti)].reset_index(drop=True)
    d = diubah[diubah["match_id"].isin(ids_nanti)].reset_index(drop=True)
    assert not c.equals(d)


def test_b_aturan_tanggal_sama() -> None:
    """Dua laga tim yang sama di tanggal sama tidak saling memengaruhi."""
    df = _df([
        [1, "2020-01-01", "A", "B", 2, 0, False, "A", "Friendly"],
        [2, "2020-01-01", "A", "B", 3, 1, False, "A", "Friendly"],
        [3, "2020-02-01", "A", "B", 1, 1, False, "A", "Friendly"],
    ])
    tabel = build_all(df)
    per_id = tabel.set_index("match_id")

    for mid in (1, 2):
        assert per_id.loc[mid, "n_form_home"] == 0
        assert per_id.loc[mid, "n_form_away"] == 0
        assert np.isnan(per_id.loc[mid, "form_pts_home"])
        assert np.isnan(per_id.loc[mid, "rest_days_home"])
        assert per_id.loc[mid, "n_h2h"] == 0
        assert np.isnan(per_id.loc[mid, "h2h_score_home"])
        # rating Elo juga memakai kondisi sebelum tanggal
        assert per_id.loc[mid, "elo_home_pre"] == pytest.approx(1500.0)

    assert per_id.loc[3, "n_form_home"] == 2
    assert per_id.loc[3, "n_form_away"] == 2
    assert per_id.loc[3, "form_pts_home"] == pytest.approx(3.0)
    assert per_id.loc[3, "rest_days_home"] == pytest.approx(31.0)
    assert per_id.loc[3, "n_h2h"] == 2
    assert per_id.loc[3, "h2h_score_home"] == pytest.approx(1.0)


def test_c_n_form_dan_tim_baru() -> None:
    """n_form tidak pernah > 5; tim tanpa riwayat mendapat NaN dan n_form = 0."""
    baris = [[100 + i, f"2021-{i + 1:02d}-01", "A", f"Lawan{i}", 2, i % 3, False, "A", "Friendly"]
             for i in range(7)]
    baris.append([200, "2021-09-01", "TimBaru", "A", 0, 1, True, "Netral", "Friendly"])
    form = build_form(_df(baris))

    per_id = form.set_index("match_id")
    assert per_id["n_form_home"].max() <= 5
    assert per_id["n_form_away"].max() <= 5
    assert per_id.loc[100, "n_form_home"] == 0
    assert np.isnan(per_id.loc[100, "form_gf_home"])
    assert per_id.loc[200, "n_form_home"] == 0 and np.isnan(per_id.loc[200, "form_pts_home"])
    assert per_id.loc[200, "n_form_away"] == 5
    assert per_id.loc[106, "n_form_home"] == 5
    assert per_id["rest_days_home"].max() <= 365


def test_d_h2h_simetris() -> None:
    """Menukar home/away membuat h2h_score_home saling melengkapi (jumlah = 1)."""
    df = _df([
        [1, "2018-01-01", "A", "B", 2, 0, False, "A", "Friendly"],
        [2, "2018-06-01", "B", "A", 1, 1, True, "C", "Friendly"],
        [3, "2019-01-01", "A", "B", 0, 1, False, "A", "Friendly"],
        [4, "2019-06-01", "B", "A", 3, 2, False, "B", "Friendly"],
        [5, "2019-09-01", "A", "C", 1, 0, False, "A", "Friendly"],
    ])
    tukar = df.copy()
    tukar[["home_team", "away_team"]] = df[["away_team", "home_team"]].to_numpy()
    tukar[["home_score", "away_score"]] = df[["away_score", "home_score"]].to_numpy()
    tukar = _isi_hasil(tukar)

    asli = build_h2h(df).set_index("match_id")
    balik = build_h2h(tukar).set_index("match_id")

    pd.testing.assert_series_equal(asli["n_h2h"], balik["n_h2h"])
    ada = asli["n_h2h"] > 0
    assert ada.sum() == 3
    jumlah = asli.loc[ada, "h2h_score_home"] + balik.loc[ada, "h2h_score_home"]
    assert np.allclose(jumlah.to_numpy(), 1.0)


def test_konteks_aturan_turnamen_dan_host() -> None:
    """Aturan kelompok turnamen sama dengan 4.3; host memakai kecocokan persis."""
    nama = pd.Series(["Friendly", "FIFA World Cup", "FIFA World Cup qualification",
                      "AFC Asian Cup qualification", "AFC Asian Cup", "Friendly"])
    assert list(kelompok_turnamen(nama)) == [
        "Friendly", "FIFA World Cup", "Kualifikasi", "Kualifikasi", "Lainnya", "Friendly"]

    df = _df([
        [1, "2020-01-01", "Indonesia", "Thailand", 2, 0, False, "Indonesia", "Friendly"],
        [2, "2020-02-01", "Thailand", "Vietnam", 1, 1, True, "Malaysia", "Friendly"],
        [3, "2020-03-01", "Vietnam", "Indonesia", 0, 1, False, "Vietnam", "Friendly"],
    ])
    konteks = build_context(df).set_index("match_id")
    assert list(konteks.columns) == ["neutral", "home_is_host", "away_is_host", "tournament_group"]
    assert konteks.loc[1, "home_is_host"] == 1 and konteks.loc[1, "away_is_host"] == 0
    assert konteks.loc[2, "neutral"] == 1
    assert konteks.loc[2, "home_is_host"] == 0 and konteks.loc[2, "away_is_host"] == 0
    assert konteks.loc[3, "home_is_host"] == 1 and konteks.loc[3, "away_is_host"] == 0
    assert set(konteks["neutral"].unique()) <= {0, 1}


def test_e_prefix_invariance_pada_dev() -> None:
    """Fitur dari prefix dev identik dengan baris yang sama pada dev penuh."""
    berkas = AKAR / "data" / "processed" / "matches_merged.csv"
    kolom = ["match_id", "date", "home_team", "away_team", "home_score", "away_score",
             "neutral", "country", "tournament", "result"]
    lengkap = pd.read_csv(berkas, parse_dates=["date"])[kolom]

    dev = lengkap[lengkap["date"] < CUTOFF_TEST].copy()
    assert dev["date"].max() < CUTOFF_TEST
    assert len(dev) == 48093

    batas_prefix = pd.Timestamp("2015-01-01")
    prefix = dev[dev["date"] < batas_prefix].copy()
    assert 0 < len(prefix) < len(dev)

    tabel_dev = build_all(dev, {"k": 30, "home_adv": 100, "init": 1500, "use_goal_mult": True})
    tabel_prefix = build_all(prefix, {"k": 30, "home_adv": 100, "init": 1500, "use_goal_mult": True})

    dari_dev = (tabel_dev[tabel_dev["match_id"].isin(set(tabel_prefix["match_id"]))]
                .sort_values("match_id").reset_index(drop=True))
    pd.testing.assert_frame_equal(
        dari_dev, tabel_prefix.sort_values("match_id").reset_index(drop=True))
