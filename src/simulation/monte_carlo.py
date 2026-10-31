"""Simulasi Monte Carlo ASEAN Championship berbasis probabilitas H/D/A.

Modul ini memakai model logistic yang sudah dibekukan konfigurasinya. Untuk
setiap edisi, model dilatih ulang hanya pada laga sebelum tanggal mulai edisi
(walk-forward). Fitur laga turnamen dihitung dari kondisi pra-turnamen; hasil
simulasi tidak dipakai untuk memperbarui fitur di tengah turnamen karena model
tidak menghasilkan skor.

Format yang disimulasikan: 10 tim, dua grup berisi lima tim, round-robin satu
kali, dua tim teratas lolos, semifinal dan final dua leg. Pemenang dua leg
ditentukan dari jumlah kemenangan leg; bila imbang, adu penalti adil 50/50.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Sequence

import numpy as np
import pandas as pd

from src.features.build_features import build_all
from src.models.candidates import build_logistic_candidate

N_SIM_DEFAULT = 10_000
PENALTI_ADIL = 0.5
KOLOM_PROBA = ("p_H", "p_D", "p_A")
FIFA_ASEAN_CUP = "FIFA ASEAN Cup"


@dataclass(frozen=True)
class EditionSpec:
    """Definisi satu edisi turnamen yang disimulasikan."""

    year: int
    tournament: str
    start: str
    end: str
    groups: dict[str, tuple[str, ...]]
    knockout_host: str | None = None


EDITIONS = {
    2018: EditionSpec(
        year=2018,
        tournament="AFF Championship",
        start="2018-11-08",
        end="2018-12-15",
        groups={
            "A": ("Cambodia", "Malaysia", "Laos", "Vietnam", "Myanmar"),
            "B": ("Singapore", "Indonesia", "Thailand", "Timor-Leste", "Philippines"),
        },
    ),
    2021: EditionSpec(
        year=2021,
        tournament="AFF Championship",
        start="2021-12-05",
        end="2022-01-01",
        groups={
            "A": ("Timor-Leste", "Thailand", "Singapore", "Myanmar", "Philippines"),
            "B": ("Cambodia", "Malaysia", "Laos", "Vietnam", "Indonesia"),
        },
        knockout_host="Singapore",
    ),
    2022: EditionSpec(
        year=2022,
        tournament="AFF Championship",
        start="2022-12-20",
        end="2023-01-16",
        groups={
            "A": ("Cambodia", "Philippines", "Brunei", "Indonesia", "Thailand"),
            "B": ("Myanmar", "Malaysia", "Laos", "Vietnam", "Singapore"),
        },
    ),
    2024: EditionSpec(
        year=2024,
        tournament="ASEAN Championship",
        start="2024-12-08",
        end="2025-01-05",
        groups={
            "A": ("Cambodia", "Malaysia", "Singapore", "Timor-Leste", "Thailand"),
            "B": ("Myanmar", "Indonesia", "Laos", "Vietnam", "Philippines"),
        },
    ),
    2026: EditionSpec(
        year=2026,
        tournament="ASEAN Championship",
        start="2026-07-24",
        end="2026-08-26",
        groups={
            "A": ("Cambodia", "Singapore", "Timor-Leste", "Indonesia", "Vietnam"),
            "B": ("Myanmar", "Malaysia", "Laos", "Thailand", "Philippines"),
        },
    ),
}


def _team_groups(spec: EditionSpec) -> dict[str, str]:
    return {tim: grup for grup, anggota in spec.groups.items() for tim in anggota}


def _edition_rows(matches: pd.DataFrame, spec: EditionSpec) -> pd.DataFrame:
    data = matches.copy()
    data["date"] = pd.to_datetime(data["date"], errors="raise")
    mask = (
        (data["tournament"] == spec.tournament)
        & data["date"].between(pd.Timestamp(spec.start), pd.Timestamp(spec.end))
    )
    edisi = data.loc[mask].sort_values(["date", "match_id"], kind="mergesort").reset_index(drop=True)
    if len(edisi) != 26:
        raise ValueError(f"edisi {spec.year} harus 26 laga, ditemukan {len(edisi)}")
    return edisi


def build_edition_fixtures(
    matches: pd.DataFrame,
    spec: EditionSpec,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Kembalikan fixture grup dan knockout aktual untuk satu edisi."""
    edisi = _edition_rows(matches, spec)
    grup = edisi.iloc[:20].copy()
    knockout = edisi.iloc[20:].copy()

    tim_edisi = set(grup["home_team"]) | set(grup["away_team"])
    if tim_edisi != set(_team_groups(spec)):
        raise ValueError(f"daftar tim edisi {spec.year} tidak cocok dengan spesifikasi")

    for nama, anggota in spec.groups.items():
        if len(anggota) != 5 or len(set(anggota)) != 5:
            raise ValueError(f"grup {nama} harus berisi lima tim unik")
        bagian = grup.loc[
            grup["home_team"].isin(anggota) & grup["away_team"].isin(anggota)
        ]
        if len(bagian) != 10:
            raise ValueError(f"grup {nama} edisi {spec.year} harus 10 laga, ditemukan {len(bagian)}")
        pasangan = {frozenset((h, a)) for h, a in zip(bagian["home_team"], bagian["away_team"])}
        pasangan_harap = {frozenset(p) for p in combinations(anggota, 2)}
        if pasangan != pasangan_harap:
            raise ValueError(f"pasangan laga grup {nama} edisi {spec.year} tidak lengkap")

    if len(knockout) != 6:
        raise ValueError(f"knockout edisi {spec.year} harus 6 laga, ditemukan {len(knockout)}")
    if knockout["date"].nunique() != 6:
        raise ValueError(f"enam tanggal knockout edisi {spec.year} harus unik")
    return grup, knockout


def actual_champion(matches: pd.DataFrame, spec: EditionSpec) -> str:
    """Juara aktual dari agregat dua leg final; error bila agregat imbang."""
    _, knockout = build_edition_fixtures(matches, spec)
    final = knockout.tail(2)
    tim = list(dict.fromkeys(final["home_team"].tolist() + final["away_team"].tolist()))
    if len(tim) != 2:
        raise ValueError(f"final edisi {spec.year} tidak memuat tepat dua tim")
    skor = {t: 0 for t in tim}
    for laga in final.itertuples(index=False):
        skor[laga.home_team] += int(laga.home_score)
        skor[laga.away_team] += int(laga.away_score)
    if skor[tim[0]] == skor[tim[1]]:
        pemenang = final["shootout_winner"].dropna()
        if pemenang.empty:
            raise ValueError(f"final edisi {spec.year} imbang tanpa data adu penalti")
        return str(pemenang.iloc[-1])
    return max(tim, key=lambda t: skor[t])


def _last_match_dates(history: pd.DataFrame) -> pd.Series:
    home = history.loc[:, ["date", "home_team"]].rename(columns={"home_team": "team"})
    away = history.loc[:, ["date", "away_team"]].rename(columns={"away_team": "team"})
    return pd.concat([home, away], ignore_index=True).groupby("team")["date"].max()


def _rest_days(tanggal: pd.Timestamp, tim: str, terakhir: pd.Series, cap: int = 365) -> float:
    if tim not in terakhir.index:
        return float("nan")
    return float(min((pd.Timestamp(tanggal) - terakhir.loc[tim]).days, cap))


def _konteks_knockout(spec: EditionSpec, home_team: str) -> tuple[str, bool]:
    if spec.knockout_host is None:
        return home_team, False
    return spec.knockout_host, home_team != spec.knockout_host


def build_static_features(
    matches: pd.DataFrame,
    spec: EditionSpec,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Bangun fitur latih dan fitur pra-turnamen untuk grup serta knockout.

    Seluruh fitur fixture dihitung dari riwayat sebelum tanggal mulai edisi.
    ``rest_days`` kemudian diganti memakai tanggal fixture aktual, tetapi Elo,
    form, dan head-to-head tetap dibekukan pada kondisi pra-turnamen.
    """
    grup, knockout = build_edition_fixtures(matches, spec)
    data = matches.copy()
    data["date"] = pd.to_datetime(data["date"], errors="raise")
    history = data.loc[
        (data["date"] < pd.Timestamp(spec.start)) & (data["tournament"] != FIFA_ASEAN_CUP)
    ].copy()
    if history.empty:
        raise ValueError(f"riwayat sebelum edisi {spec.year} kosong")

    terakhir = _last_match_dates(history)
    grup_tim = _team_groups(spec)
    tim = sorted(grup_tim)
    tanggal_knockout = sorted(knockout["date"].unique())
    if len(tanggal_knockout) != 6:
        raise ValueError("tanggal knockout tidak lengkap")

    baris = []
    meta = []
    nomor = -1_000_000

    def tambah(meta_baru, tanggal_aktual, home, away, country, neutral):
        nonlocal nomor
        sim_id = nomor
        nomor -= 1
        baris.append({
            "match_id": sim_id,
            "date": pd.Timestamp(spec.start),
            "home_team": home,
            "away_team": away,
            "result": "H",
            "home_score": 0,
            "away_score": 0,
            "neutral": bool(neutral),
            "country": country,
            "tournament": spec.tournament,
        })
        meta.append({"match_id": sim_id, "date_aktual": pd.Timestamp(tanggal_aktual), **meta_baru})

    for laga in grup.itertuples(index=False):
        tambah(
            {"jenis": "grup", "grup": grup_tim[laga.home_team]},
            laga.date,
            laga.home_team,
            laga.away_team,
            laga.country,
            bool(laga.neutral),
        )

    for indeks_tanggal, tanggal in enumerate(tanggal_knockout):
        for home in tim:
            for away in tim:
                if home == away:
                    continue
                country, neutral = _konteks_knockout(spec, home)
                tambah(
                    {"jenis": "knockout", "tanggal_knockout": indeks_tanggal},
                    tanggal,
                    home,
                    away,
                    country,
                    neutral,
                )

    kolom_history = list(history.columns)
    tambahan = pd.DataFrame(baris).reindex(columns=kolom_history)
    gabungan = pd.concat([history, tambahan], ignore_index=True)
    semua_fitur = build_all(gabungan)

    id_history = set(history["match_id"])
    fitur_history = semua_fitur.loc[semua_fitur["match_id"].isin(id_history)].copy()
    fitur_fixture = semua_fitur.loc[~semua_fitur["match_id"].isin(id_history)].copy()
    fitur_fixture = fitur_fixture.merge(
        pd.DataFrame(meta), on="match_id", how="left", validate="one_to_one"
    )

    fitur_fixture["date"] = pd.to_datetime(fitur_fixture["date_aktual"], errors="raise")
    for sisi in ("home", "away"):
        fitur_fixture[f"rest_days_{sisi}"] = [
            _rest_days(tgl, tim_, terakhir)
            for tgl, tim_ in zip(fitur_fixture["date"], fitur_fixture[f"{sisi}_team"])
        ]

    fitur_grup = fitur_fixture.loc[fitur_fixture["jenis"] == "grup"].copy()
    fitur_knockout = fitur_fixture.loc[fitur_fixture["jenis"] == "knockout"].copy()
    if len(fitur_grup) != 20 or len(fitur_knockout) != 6 * len(tim) * (len(tim) - 1):
        raise ValueError("jumlah fitur fixture tidak sesuai")
    return fitur_history, fitur_grup, fitur_knockout


def _pair_h2h(history: pd.DataFrame) -> dict[tuple[str, str], list[int]]:
    rekap: dict[tuple[str, str], list[int]] = {}
    for laga in history.itertuples(index=False):
        kunci = tuple(sorted((laga.home_team, laga.away_team)))
        rekap.setdefault(kunci, [0, 0, 0])
        if laga.home_score > laga.away_score:
            rekap[kunci][0 if laga.home_team == kunci[0] else 1] += 1
        elif laga.home_score < laga.away_score:
            rekap[kunci][1 if laga.home_team == kunci[0] else 0] += 1
        else:
            rekap[kunci][2] += 1
    return rekap


def _team_state_from_features(
    features_all: pd.DataFrame,
    grup: pd.DataFrame,
    tim: Sequence[str],
) -> dict[str, dict[str, float]]:
    fitur = features_all.set_index("match_id", drop=False)
    state = {}
    for t in tim:
        pertama = grup.loc[(grup["home_team"] == t) | (grup["away_team"] == t)].iloc[0]
        baris = fitur.loc[pertama["match_id"]]
        sisi = "home" if pertama["home_team"] == t else "away"
        state[t] = {
            "elo": float(baris[f"elo_{sisi}_pre"]),
            "n_prev": int(baris[f"n_prev_{sisi}"]),
            "form_pts": float(baris[f"form_pts_{sisi}"]),
            "form_gf": float(baris[f"form_gf_{sisi}"]),
            "form_ga": float(baris[f"form_ga_{sisi}"]),
            "n_form": int(baris[f"n_form_{sisi}"]),
        }
    return state


def build_static_features_from_features(
    matches: pd.DataFrame,
    features_all: pd.DataFrame,
    spec: EditionSpec,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Versi cepat: pakai fitur kausal yang sudah dihitung untuk semua laga.

    ``features_all`` harus memuat seluruh laga non-FIFA yang pernah dimainkan.
    Fitur fixture tetap dibekukan pada kondisi pra-turnamen.
    """
    grup, knockout = build_edition_fixtures(matches, spec)
    data = matches.copy()
    data["date"] = pd.to_datetime(data["date"], errors="raise")
    history = data.loc[
        (data["date"] < pd.Timestamp(spec.start)) & (data["tournament"] != FIFA_ASEAN_CUP)
    ].copy()
    if history.empty:
        raise ValueError(f"riwayat sebelum edisi {spec.year} kosong")

    fitur_history = features_all.loc[
        features_all["match_id"].isin(set(history["match_id"]))
    ].copy()
    if len(fitur_history) != len(history):
        raise ValueError(
            f"fitur history edisi {spec.year} tidak lengkap: "
            f"{len(fitur_history)} vs {len(history)}"
        )
    fitur_history = fitur_history.sort_values(
        ["date", "match_id"], kind="mergesort"
    ).reset_index(drop=True)

    grup_tim = _team_groups(spec)
    tim = sorted(grup_tim)
    state = _team_state_from_features(features_all, grup, tim)
    terakhir = _last_match_dates(history)
    rekap_h2h = _pair_h2h(history)
    tanggal_knockout = sorted(knockout["date"].unique())
    if len(tanggal_knockout) != 6:
        raise ValueError("tanggal knockout tidak lengkap")

    def h2h(home: str, away: str) -> tuple[int, float]:
        kunci = tuple(sorted((home, away)))
        menang1, menang2, seri = rekap_h2h.get(kunci, [0, 0, 0])
        n = menang1 + menang2 + seri
        if n == 0:
            return 0, float("nan")
        menang_home = menang1 if home == kunci[0] else menang2
        return n, (menang_home + 0.5 * seri) / n

    def baris_fitur(
        match_id: int,
        tanggal: pd.Timestamp,
        home: str,
        away: str,
        country: str,
        neutral: bool,
    ) -> dict:
        sh, sa = state[home], state[away]
        n_h2h, skor_h2h = h2h(home, away)
        return {
            "match_id": match_id,
            "date": pd.Timestamp(tanggal),
            "home_team": home,
            "away_team": away,
            "result": "H",
            "elo_home_pre": sh["elo"],
            "elo_away_pre": sa["elo"],
            "elo_diff": sh["elo"] - sa["elo"],
            "n_prev_home": sh["n_prev"],
            "n_prev_away": sa["n_prev"],
            "form_pts_home": sh["form_pts"],
            "form_gf_home": sh["form_gf"],
            "form_ga_home": sh["form_ga"],
            "n_form_home": sh["n_form"],
            "rest_days_home": _rest_days(tanggal, home, terakhir),
            "form_pts_away": sa["form_pts"],
            "form_gf_away": sa["form_gf"],
            "form_ga_away": sa["form_ga"],
            "n_form_away": sa["n_form"],
            "rest_days_away": _rest_days(tanggal, away, terakhir),
            "n_h2h": n_h2h,
            "h2h_score_home": skor_h2h,
            "neutral": int(bool(neutral)),
            "home_is_host": int(home == country),
            "away_is_host": int(away == country),
            "tournament_group": "Lainnya",
        }

    baris_grup = []
    meta_grup = []
    baris_knockout = []
    meta_knockout = []
    nomor = -1_000_000
    for laga in grup.itertuples(index=False):
        baris_grup.append(
            baris_fitur(nomor, laga.date, laga.home_team, laga.away_team, laga.country, laga.neutral)
        )
        meta_grup.append({"match_id": nomor, "jenis": "grup", "grup": grup_tim[laga.home_team]})
        nomor -= 1

    for indeks_tanggal, tanggal in enumerate(tanggal_knockout):
        for home in tim:
            for away in tim:
                if home == away:
                    continue
                country, neutral = _konteks_knockout(spec, home)
                baris_knockout.append(
                    baris_fitur(nomor, tanggal, home, away, country, neutral)
                )
                meta_knockout.append({
                    "match_id": nomor,
                    "jenis": "knockout",
                    "tanggal_knockout": indeks_tanggal,
                })
                nomor -= 1

    fitur_grup = pd.DataFrame(baris_grup).merge(
        pd.DataFrame(meta_grup), on="match_id", how="left", validate="one_to_one"
    )
    fitur_knockout = pd.DataFrame(baris_knockout).merge(
        pd.DataFrame(meta_knockout), on="match_id", how="left", validate="one_to_one"
    )
    return fitur_history, fitur_grup, fitur_knockout


def prepare_edition(
    matches: pd.DataFrame,
    spec: EditionSpec,
    C: float = 1.0,
    max_iter: int = 2000,
    features_all: pd.DataFrame | None = None,
) -> dict:
    """Latih model walk-forward dan prediksi seluruh fixture edisi."""
    if features_all is None:
        history, grup, knockout = build_static_features(matches, spec)
    else:
        history, grup, knockout = build_static_features_from_features(
            matches, features_all, spec
        )
    model = build_logistic_candidate(
        feature_set="full_interaksi", C=C, max_iter=max_iter
    ).fit(history, history["result"])

    grup = grup.copy()
    knockout = knockout.copy()
    knockout["tanggal_knockout"] = knockout["tanggal_knockout"].astype(int)
    grup.loc[:, list(KOLOM_PROBA)] = model.predict_proba(grup)
    knockout.loc[:, list(KOLOM_PROBA)] = model.predict_proba(knockout)
    for tabel, nama in ((grup, "grup"), (knockout, "knockout")):
        proba = tabel.loc[:, KOLOM_PROBA].to_numpy(dtype=float)
        if not np.isfinite(proba).all():
            raise ValueError(f"probabilitas {nama} edisi {spec.year} mengandung nilai non-finite")
        if not np.allclose(proba.sum(axis=1), 1.0, atol=1e-8):
            raise ValueError(f"probabilitas {nama} edisi {spec.year} tidak berjumlah 1")

    return {
        "spec": spec,
        "model": model,
        "n_train": int(len(history)),
        "group": grup,
        "knockout": knockout,
        "actual_champion": actual_champion(matches, spec),
    }


def _sample_outcome(proba: np.ndarray, rng: np.random.Generator) -> int:
    u = float(rng.random())
    if u < proba[0]:
        return 0
    if u < proba[0] + proba[1]:
        return 1
    return 2


def _update_poin(poin: dict[str, int], home: str, away: str, hasil: int) -> None:
    if hasil == 0:
        poin[home] += 3
    elif hasil == 1:
        poin[home] += 1
        poin[away] += 1
    else:
        poin[away] += 3


def rank_group(
    tim: Sequence[str],
    indeks: np.ndarray,
    home: np.ndarray,
    away: np.ndarray,
    hasil: np.ndarray,
    rng: np.random.Generator,
) -> list[str]:
    """Urutkan grup: poin, lalu poin head-to-head, lalu undian acak."""
    poin = {t: 0 for t in tim}
    for i in indeks:
        _update_poin(poin, str(home[i]), str(away[i]), int(hasil[i]))

    urutan: list[str] = []
    for nilai in sorted(set(poin.values()), reverse=True):
        seri = [t for t in tim if poin[t] == nilai]
        if len(seri) > 1:
            poin_h2h = {t: 0 for t in seri}
            for i in indeks:
                h, a = str(home[i]), str(away[i])
                if h in poin_h2h and a in poin_h2h:
                    _update_poin(poin_h2h, h, a, int(hasil[i]))
            kunci_acak = {t: float(rng.random()) for t in seri}
            seri = sorted(seri, key=lambda t: (-poin_h2h[t], kunci_acak[t]))
        urutan.extend(seri)
    return urutan


def two_legged_winner(
    first_home: str,
    first_away: str,
    leg1: int,
    leg2: int,
    penalty_first_wins: bool,
) -> str:
    """Pemenang dua leg dari outcome relatif terhadap tuan rumah tiap leg."""
    kemenangan = 0
    kemenangan += 1 if leg1 == 0 else (-1 if leg1 == 2 else 0)
    kemenangan += 1 if leg2 == 2 else (-1 if leg2 == 0 else 0)
    if kemenangan > 0:
        return first_home
    if kemenangan < 0:
        return first_away
    return first_home if penalty_first_wins else first_away


def wilson_interval(k: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    """Interval kepercayaan Wilson untuk proporsi binomial."""
    if n <= 0:
        raise ValueError("n harus > 0")
    if not 0 <= k <= n:
        raise ValueError("k harus di antara 0 dan n")
    p = k / n
    penyebut = 1.0 + z * z / n
    tengah = (p + z * z / (2.0 * n)) / penyebut
    lebar = z * np.sqrt(p * (1.0 - p) / n + z * z / (4.0 * n * n)) / penyebut
    return float(max(0.0, tengah - lebar)), float(min(1.0, tengah + lebar))


def simulate_edition(
    spec: EditionSpec,
    group: pd.DataFrame,
    knockout: pd.DataFrame,
    n_sims: int = N_SIM_DEFAULT,
    seed: int = 42,
) -> pd.DataFrame:
    """Jalankan Monte Carlo dan kembalikan tabel probabilitas per tim."""
    if n_sims <= 0:
        raise ValueError("n_sims harus > 0")

    tim = sorted(_team_groups(spec))
    indeks_tim = {t: i for i, t in enumerate(tim)}
    g_home = group["home_team"].to_numpy()
    g_away = group["away_team"].to_numpy()
    g_grup = group["grup"].to_numpy()
    g_proba = group.loc[:, KOLOM_PROBA].to_numpy(dtype=float)
    indeks_grup = {nama: np.where(g_grup == nama)[0] for nama in spec.groups}

    n_ronde = int(knockout["tanggal_knockout"].max()) + 1
    proba_knockout = np.zeros((n_ronde, len(tim), len(tim), 3), dtype=float)
    for laga in knockout.itertuples(index=False):
        h = indeks_tim[laga.home_team]
        a = indeks_tim[laga.away_team]
        proba_knockout[int(laga.tanggal_knockout), h, a] = (
            float(laga.p_H), float(laga.p_D), float(laga.p_A)
        )

    def main_dua_leg(
        first_home: str,
        first_away: str,
        ronde: tuple[int, int],
        rng: np.random.Generator,
    ) -> str:
        h = indeks_tim[first_home]
        a = indeks_tim[first_away]
        leg1 = _sample_outcome(proba_knockout[ronde[0], h, a], rng)
        leg2 = _sample_outcome(proba_knockout[ronde[1], a, h], rng)
        return two_legged_winner(
            first_home, first_away, leg1, leg2, bool(rng.random() < PENALTI_ADIL)
        )

    rng = np.random.default_rng(seed)
    juara = {t: 0 for t in tim}
    finalis = {t: 0 for t in tim}
    semifinalis = {t: 0 for t in tim}

    for _ in range(n_sims):
        u = rng.random(len(g_proba))
        hasil = (u[:, None] > np.cumsum(g_proba, axis=1)).sum(axis=1)
        kualifikasi = {}
        for nama, anggota in spec.groups.items():
            urutan = rank_group(
                anggota, indeks_grup[nama], g_home, g_away, hasil, rng
            )
            kualifikasi[nama] = urutan[:2]
            for t in urutan[:2]:
                semifinalis[t] += 1

        a1, a2 = kualifikasi["A"]
        b1, b2 = kualifikasi["B"]
        pemenang1 = main_dua_leg(a2, b1, (0, 2), rng)
        pemenang2 = main_dua_leg(b2, a1, (1, 3), rng)
        finalis[pemenang1] += 1
        finalis[pemenang2] += 1
        champion = main_dua_leg(pemenang1, pemenang2, (4, 5), rng)
        juara[champion] += 1

    baris = []
    for t in tim:
        p_juara = juara[t] / n_sims
        p_final = finalis[t] / n_sims
        p_semi = semifinalis[t] / n_sims
        lo, hi = wilson_interval(juara[t], n_sims)
        baris.append({
            "tim": t,
            "grup": _team_groups(spec)[t],
            "juara": juara[t],
            "p_juara": p_juara,
            "se_juara": float(np.sqrt(p_juara * (1.0 - p_juara) / n_sims)),
            "ci_low": lo,
            "ci_high": hi,
            "finalis": finalis[t],
            "p_finalis": p_final,
            "semifinalis": semifinalis[t],
            "p_semifinalis": p_semi,
        })
    tabel = pd.DataFrame(baris)
    return tabel.sort_values(["p_juara", "tim"], ascending=[False, True], kind="mergesort").reset_index(drop=True)


def run_editions(
    matches: pd.DataFrame,
    editions: dict[int, EditionSpec] | None = None,
    n_sims: int = N_SIM_DEFAULT,
    seed: int = 42,
    C: float = 1.0,
    features_all: pd.DataFrame | None = None,
) -> dict[int, dict]:
    """Siapkan dan simulasikan semua edisi; hasil disimpan per tahun."""
    editions = EDITIONS if editions is None else editions
    if features_all is None:
        features_all = build_all(matches)
    hasil = {}
    for i, (tahun, spec) in enumerate(sorted(editions.items())):
        siap = prepare_edition(matches, spec, C=C, features_all=features_all)
        tabel = simulate_edition(spec, siap["group"], siap["knockout"], n_sims=n_sims, seed=seed + i)
        hasil[tahun] = {**siap, "tabel": tabel, "n_sims": n_sims}
    return hasil
