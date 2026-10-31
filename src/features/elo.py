"""Rating Elo kronologis untuk laga internasional.

Modul ini hanya membangun **fitur pra-laga** dari hasil laga sebelumnya. Tidak ada
model prediksi di sini. Seluruh perhitungan bersifat kausal: fitur sebuah laga
hanya bergantung pada laga-laga yang lebih awal, sehingga menjalankan fungsi ini
pada prefix data menghasilkan baris yang sama seperti menjalankannya pada data
penuh.

Aturan yang dipakai (sesuai protokol Section 5.2):

- Laga diurutkan menurut ``date`` lalu ``match_id``.
- Diproses **per kelompok tanggal**: semua laga pada tanggal yang sama memakai
  rating sebelum tanggal itu, lalu semua pembaruan diterapkan setelah kelompok
  selesai. Laga pada tanggal yang sama karena itu tidak saling memengaruhi.
- ``dr = (R_home - R_away) + (home_adv bila neutral == False, selain itu 0)``
- ``E_home = 1 / (1 + 10 ** (-dr / 400))``
- ``S_home`` = 1 (menang), 0,5 (seri), 0 (kalah)
- ``G`` = 1 bila selisih gol <= 1; 1,5 bila 2; ``(11 + n) / 8`` bila n >= 3;
  ``G = 1`` bila ``use_goal_mult=False``
- ``delta = k * G * (S_home - E_home)``; ``R_home += delta``; ``R_away -= delta``

Karena setiap pembaruan menambah ``delta`` ke satu tim dan mengurangkannya dari
tim lain, jumlah seluruh rating selalu sama dengan ``init`` dikali jumlah tim
yang pernah muncul.
"""

from __future__ import annotations

import pandas as pd

KOLOM_WAJIB = (
    "match_id",
    "date",
    "home_team",
    "away_team",
    "home_score",
    "away_score",
    "neutral",
)

KOLOM_FITUR = (
    "match_id",
    "elo_home_pre",
    "elo_away_pre",
    "elo_diff",
    "n_prev_home",
    "n_prev_away",
)


def _multiplier_gol(selisih: int, use_goal_mult: bool) -> float:
    """Faktor G pada selisih gol ``selisih`` (sudah dalam nilai absolut)."""
    if not use_goal_mult or selisih <= 1:
        return 1.0
    if selisih == 2:
        return 1.5
    return (11.0 + selisih) / 8.0


def build_elo(
    df: pd.DataFrame,
    k: float = 30.0,
    home_adv: float = 100.0,
    init: float = 1500.0,
    use_goal_mult: bool = True,
) -> tuple[pd.DataFrame, pd.Series]:
    """Hitung rating Elo dan fitur pra-laga untuk setiap baris ``df``.

    Parameters
    ----------
    df : pandas.DataFrame
        Harus memuat kolom :data:`KOLOM_WAJIB`. ``date`` boleh berupa string atau
        ``datetime``; ``neutral`` harus boolean; skor harus bilangan bulat dan
        tidak boleh kosong.
    k : float
        Faktor pembaruan (default 30).
    home_adv : float
        Bonus rating untuk tuan rumah pada laga ``neutral == False`` (default 100).
    init : float
        Rating awal setiap tim yang belum pernah bermain (default 1500).
    use_goal_mult : bool
        Bila ``False``, faktor ``G`` selalu 1 (default ``True``).

    Returns
    -------
    (features_df, final_ratings)
        ``features_df`` berurutan seperti data yang sudah diurutkan (``date`` lalu
        ``match_id``) dengan kolom :data:`KOLOM_FITUR`:

        - ``elo_home_pre``, ``elo_away_pre``: rating sebelum tanggal laga,
        - ``elo_diff``: ``elo_home_pre - elo_away_pre`` (tanpa ``home_adv``),
        - ``n_prev_home``, ``n_prev_away``: jumlah laga sebelumnya tim tersebut,
          dihitung sebelum tanggal laga (laga lain di tanggal yang sama tidak
          ikut dihitung).

        ``final_ratings`` adalah ``pandas.Series`` berisi rating akhir per nama tim
        (``index.name == "team"``, ``name == "elo"``), terurut menurun; bila
        ratingnya sama, diurutkan menurut nama tim agar hasil deterministik.
    """
    hilang = [kolom for kolom in KOLOM_WAJIB if kolom not in df.columns]
    if hilang:
        raise KeyError(f"kolom wajib tidak ada: {hilang}")
    if k <= 0:
        raise ValueError(f"k harus > 0, ditemukan {k}")
    if init <= 0:
        raise ValueError(f"init harus > 0, ditemukan {init}")

    data = df.loc[:, list(KOLOM_WAJIB)].copy()
    data["date"] = pd.to_datetime(data["date"], errors="raise")

    kosong = [kolom for kolom in KOLOM_WAJIB if data[kolom].isna().any()]
    if kosong:
        raise ValueError(f"kolom berisi nilai kosong: {kosong}")

    data["neutral"] = data["neutral"].astype(bool)
    for kolom in ("home_score", "away_score"):
        data[kolom] = data[kolom].astype(int)

    if not data["match_id"].is_unique:
        duplikat = data.loc[data["match_id"].duplicated(), "match_id"].head(5).tolist()
        raise ValueError(f"match_id harus unik, contoh duplikat: {duplikat}")

    data = data.sort_values(["date", "match_id"], kind="mergesort").reset_index(drop=True)

    rating: dict[str, float] = {}
    jumlah_laga: dict[str, int] = {}
    baris: list[tuple] = []

    for _, kelompok in data.groupby("date", sort=True):
        pembaruan: list[tuple[str, str, float]] = []
        for laga in kelompok.itertuples(index=False):
            r_home = rating.get(laga.home_team, float(init))
            r_away = rating.get(laga.away_team, float(init))
            n_home = jumlah_laga.get(laga.home_team, 0)
            n_away = jumlah_laga.get(laga.away_team, 0)

            dr = (r_home - r_away) + (0.0 if laga.neutral else float(home_adv))
            e_home = 1.0 / (1.0 + 10.0 ** (-dr / 400.0))
            if laga.home_score > laga.away_score:
                s_home = 1.0
            elif laga.home_score == laga.away_score:
                s_home = 0.5
            else:
                s_home = 0.0
            g = _multiplier_gol(abs(laga.home_score - laga.away_score), bool(use_goal_mult))
            delta = float(k) * g * (s_home - e_home)

            baris.append(
                (laga.match_id, r_home, r_away, r_home - r_away, n_home, n_away)
            )
            pembaruan.append((laga.home_team, laga.away_team, delta))

        # seluruh pembaruan tanggal ini baru diterapkan setelah kelompok selesai
        for tim_home, tim_away, delta in pembaruan:
            rating[tim_home] = rating.get(tim_home, float(init)) + delta
            rating[tim_away] = rating.get(tim_away, float(init)) - delta
            jumlah_laga[tim_home] = jumlah_laga.get(tim_home, 0) + 1
            jumlah_laga[tim_away] = jumlah_laga.get(tim_away, 0) + 1

    fitur = pd.DataFrame(baris, columns=list(KOLOM_FITUR))
    fitur = fitur.astype(
        {
            "elo_home_pre": float,
            "elo_away_pre": float,
            "elo_diff": float,
            "n_prev_home": "int64",
            "n_prev_away": "int64",
        }
    )
    if not fitur.empty:
        fitur["match_id"] = fitur["match_id"].astype(data["match_id"].dtype)

    akhir = (
        pd.Series(rating, name="elo", dtype=float)
        .rename_axis("team")
        .reset_index()
        .sort_values(["elo", "team"], ascending=[False, True], kind="mergesort")
        .set_index("team")["elo"]
    )
    return fitur, akhir
