"""Modeling-frame prep. Pure functions: DataFrame in, (X, y, meta) out.

Expected input columns (as loaded from the `player_season` table):
league_season, sb_player, sb_team, position, minutes, matches, starts,
shots_p90, goals_p90, xg_p90, passes_p90, pass_pct, drib_ok_p90, carries_p90,
pressures_p90, duels_w_p90, interceptions_p90, recoveries_p90,
market_value_in_eur, value_date, date_of_birth.
"""

import re

import numpy as np
import pandas as pd

# Notebook 08's confirmed shortlist (rates) plus volume/age/context terms.
SHORTLIST = [
    "minutes", "matches", "starts", "shots_p90", "goals_p90", "xg_p90",
    "passes_p90", "pass_pct", "drib_ok_p90", "carries_p90", "pressures_p90",
    "duels_w_p90", "interceptions_p90", "recoveries_p90", "age", "age2",
]

MIN_MINUTES = 500
TEST_START_YEAR = 2019  # seasons starting this year or later are the test set


def position_group(position: str) -> str:
    """Bucket 20+ StatsBomb position names into four model groups."""
    p = str(position)
    if "Goalkeeper" in p:
        return "GK"
    if any(k in p for k in ("Forward", "Wing", "Striker")):
        return "Attack"
    if "Midfield" in p:
        return "Midfield"
    if "Back" in p:
        return "Defence"
    return "Other"


def season_start_year(league_season: str) -> int:
    """'La Liga 2015/2016' -> 2015. Tournament labels ('Euro 2020') -> 2020."""
    m = re.search(r"(\d{4})", str(league_season))
    if m is None:
        raise ValueError(f"no year in league_season: {league_season!r}")
    return int(m.group(1))


def prepare_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Filter, engineer, and encode. Returns modeling-ready frame (with target `ln_v`).

    Drops rows below MIN_MINUTES, without values, or without birth dates
    (counted by the caller via the shape delta, as in notebook 09 Cell 1).
    """
    out = df[(df["minutes"] >= MIN_MINUTES) & (df["market_value_in_eur"] > 0)].copy()
    out["ln_v"] = np.log(out["market_value_in_eur"].astype(float))
    out["age"] = (
        pd.to_datetime(out["value_date"]).dt.year
        - pd.to_datetime(out["date_of_birth"]).dt.year
    )
    out = out[out["age"].notna()].reset_index(drop=True)
    out["age2"] = out["age"] ** 2
    out["pos_grp"] = out["position"].apply(position_group)
    out["league"] = out["league_season"].apply(lambda s: s.rsplit(" ", 1)[0])
    out["start_yr"] = out["league_season"].apply(season_start_year)
    return pd.get_dummies(out, columns=["pos_grp", "league"], drop_first=True)


def time_split(frame: pd.DataFrame):
    """Forward split: seasons before TEST_START_YEAR train, rest test.

    Returns (Xtr, Xte, ytr, yte, frame) with identifier/target columns
    excluded from X. Deterministic (no shuffling involved).
    """
    drop = {"league_season", "sb_player", "sb_team", "position", "ln_v",
            "market_value_in_eur", "euros", "value_date", "date_of_birth", "start_yr"}
    X = frame.drop(columns=[c for c in drop if c in frame.columns])
    train = frame["start_yr"] < TEST_START_YEAR
    return (X[train], X[~train],
            frame.loc[train, "ln_v"], frame.loc[~train, "ln_v"], frame)
