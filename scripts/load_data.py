"""Load CSVs into Postgres. Idempotent: re-runs skip existing rows.

Usage (from repo root):
    pip install psycopg2-binary
    python scripts/load_data.py            # prompts for the postgres password
"""

import getpass
import os

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED = os.path.join(ROOT, "data", "processed")
TM = os.path.join(ROOT, "data", "transfermarkt")


def clean(value):
    """NaN/NaT -> None, numpy scalars -> native Python types."""
    # pd.NaT is its own type (not a Timestamp): catch it explicitly,
    # otherwise it reaches Postgres as the literal string 'NaT'.
    if value is None or value is pd.NaT:
        return None
    if isinstance(value, float) and pd.isna(value):
        return None
    if isinstance(value, pd.Timestamp):
        return value.date()
    if hasattr(value, "item"):
        return value.item()
    return value


def main():
    import psycopg2  # deferred: pure logic above stays importable without the driver

    password = getpass.getpass("postgres password: ")
    conn = psycopg2.connect(host="localhost", dbname="fri", user="postgres", password=password)
    conn.autocommit = True
    cur = conn.cursor()

    features = pd.read_csv(os.path.join(PROCESSED, "player_season_features.csv"))
    wanted_ids = set(features["player_id"].dropna().astype(int))

    players = pd.read_csv(
        os.path.join(TM, "players.csv"),
        usecols=["player_id", "name", "date_of_birth", "position",
                 "foot", "height_in_cm", "current_club_name"],
        parse_dates=["date_of_birth"],
    )
    players = players[players["player_id"].isin(wanted_ids)]
    cur.executemany(
        """INSERT INTO players
           (player_id, player_name, date_of_birth, position, foot, height_in_cm, current_club_name)
           VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING""",
        [[clean(v) for v in row] for row in players.itertuples(index=False)],
    )
    print(f"players: {cur.rowcount} new rows ({len(players)} in file slice)")

    cols = ["league_season", "sb_player", "sb_team", "minutes", "matches", "starts",
            "position", "shots", "goals", "xg", "passes", "pass_ok", "drib_att",
            "drib_ok", "carries", "pressures", "duels_w", "duels_l", "interceptions",
            "recoveries", "blocks", "clearances", "fouls_w", "fouls_c", "shots_p90",
            "goals_p90", "xg_p90", "passes_p90", "drib_att_p90", "drib_ok_p90",
            "carries_p90", "pressures_p90", "duels_w_p90", "interceptions_p90",
            "recoveries_p90", "blocks_p90", "clearances_p90", "pass_pct", "player_id",
            "player_name", "tm_club", "method", "value_date", "market_value_in_eur"]
    feats = features.rename(columns={"date": "value_date"})
    feats["value_date"] = pd.to_datetime(feats["value_date"], errors="coerce")
    placeholders = ", ".join(["%s"] * len(cols))
    cur.executemany(
        f"INSERT INTO player_season ({', '.join(cols)}) VALUES ({placeholders})"
        " ON CONFLICT DO NOTHING",
        [[clean(v) for v in row] for row in feats[cols].itertuples(index=False)],
    )
    print(f"player_season: {cur.rowcount} new rows ({len(feats)} in file)")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
