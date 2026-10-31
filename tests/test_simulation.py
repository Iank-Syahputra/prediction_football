from __future__ import annotations

from itertools import combinations

import numpy as np
import pandas as pd
import pytest

from src.simulation.monte_carlo import (
    EDITIONS,
    EditionSpec,
    actual_champion,
    build_edition_fixtures,
    rank_group,
    simulate_edition,
    two_legged_winner,
    wilson_interval,
)


@pytest.fixture(scope="module")
def matches() -> pd.DataFrame:
    return pd.read_csv("data/processed/matches_merged.csv", parse_dates=["date"])


@pytest.mark.parametrize("tahun", [2018, 2021, 2022, 2024, 2026])
def test_fixture_edisi_lengkap(matches, tahun):
    spec = EDITIONS[tahun]
    grup, knockout = build_edition_fixtures(matches, spec)

    assert len(grup) == 20
    assert len(knockout) == 6
    assert knockout["date"].nunique() == 6

    for nama, anggota in spec.groups.items():
        bagian = grup.loc[
            grup["home_team"].isin(anggota) & grup["away_team"].isin(anggota)
        ]
        assert len(bagian) == 10
        pasangan = {frozenset((h, a)) for h, a in zip(bagian["home_team"], bagian["away_team"])}
        assert pasangan == {frozenset(p) for p in combinations(anggota, 2)}


@pytest.mark.parametrize(
    ("tahun", "juara"),
    [(2018, "Vietnam"), (2021, "Thailand"), (2022, "Thailand"), (2024, "Vietnam"), (2026, "Vietnam")],
)
def test_juara_aktual(matches, tahun, juara):
    assert actual_champion(matches, EDITIONS[tahun]) == juara


def test_rank_group_poin_dan_h2h():
    tim = ["A", "B", "C", "D"]
    home = np.array(["A", "A", "B", "B", "D"])
    away = np.array(["B", "C", "C", "D", "A"])
    hasil = np.array([0, 0, 0, 0, 0])
    rng = np.random.default_rng(0)

    urutan = rank_group(tim, np.arange(len(home)), home, away, hasil, rng)

    assert urutan[:2] == ["A", "B"]
    assert urutan[2] == "D"
    assert urutan[3] == "C"


def test_rank_group_tie_h2h():
    tim = ["A", "B", "C", "D"]
    home = np.array(["A", "A", "B", "B", "D"])
    away = np.array(["B", "C", "C", "D", "A"])
    hasil = np.array([0, 0, 0, 0, 2])
    rng = np.random.default_rng(0)

    urutan = rank_group(tim, np.arange(len(home)), home, away, hasil, rng)

    assert urutan[0] == "A"
    assert urutan[1] == "B"


def test_two_legged_winner_agregat_dan_penalti():
    assert two_legged_winner("A", "B", 0, 2, penalty_first_wins=False) == "A"
    assert two_legged_winner("A", "B", 2, 0, penalty_first_wins=True) == "B"
    assert two_legged_winner("A", "B", 0, 1, penalty_first_wins=False) == "A"
    assert two_legged_winner("A", "B", 1, 0, penalty_first_wins=True) == "B"
    assert two_legged_winner("A", "B", 1, 1, penalty_first_wins=True) == "A"
    assert two_legged_winner("A", "B", 1, 1, penalty_first_wins=False) == "B"


def test_wilson_interval():
    lo, hi = wilson_interval(50, 100)
    assert lo < 0.5 < hi
    assert 0.0 <= lo <= hi <= 1.0
    assert wilson_interval(0, 10)[0] == 0.0
    assert wilson_interval(10, 10)[1] == pytest.approx(1.0)


def test_simulate_edition_sintetis():
    spec = EditionSpec(
        year=2099,
        tournament="Uji",
        start="2099-01-01",
        end="2099-01-20",
        groups={
            "A": ("A1", "A2", "A3", "A4", "A5"),
            "B": ("B1", "B2", "B3", "B4", "B5"),
        },
    )
    grup = []
    for nama, anggota in spec.groups.items():
        for home, away in combinations(anggota, 2):
            grup.append({
                "grup": nama, "home_team": home, "away_team": away,
                "p_H": 0.5, "p_D": 0.25, "p_A": 0.25,
            })
    group = pd.DataFrame(grup)

    knockout = []
    tim = [t for anggota in spec.groups.values() for t in anggota]
    for ronde in range(6):
        for home in tim:
            for away in tim:
                if home != away:
                    knockout.append({
                        "tanggal_knockout": ronde,
                        "home_team": home,
                        "away_team": away,
                        "p_H": 0.5, "p_D": 0.25, "p_A": 0.25,
                    })
    knockout = pd.DataFrame(knockout)

    tabel = simulate_edition(spec, group, knockout, n_sims=500, seed=1)

    assert len(tabel) == 10
    assert tabel["juara"].sum() == 500
    assert tabel["finalis"].sum() == 1000
    assert tabel["semifinalis"].sum() == 2000
    assert np.isclose(tabel["p_juara"].sum(), 1.0)
    assert tabel["p_juara"].between(0, 1).all()
