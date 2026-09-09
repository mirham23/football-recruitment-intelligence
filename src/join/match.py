"""Match cascade: token-subset -> club gate -> disambiguation -> fuzzy.

Column contracts:
  df_sb: sb_player, sb_team, sb_key
  df_tm: player_id, player_name, tm_club, tm_key
  pairs:  above + tok_sb, tok_tm, club_ok, n_tok
  final:  sb_player, sb_team, player_id, player_name, tm_club, method
        method in {"exact", "token", "nickname", "fuzzy"}
"""

import difflib

import pandas as pd

from src.join.clubs import CLUB_MAP, clubs_agree
from src.join.nicknames import NICKNAMES
from src.join.normalize import tokens

FUZZY_THRESHOLD = 0.85


def token_subset(sb_key: str, tm_key: str) -> bool:
    """Every TM token appears in the SB tokens.

    High recall, unsafe alone: also matches distinct players whose names
    nest (Llorente Torres / Fernando Torres). The club gate must follow.
    """
    return set(tokens(tm_key)).issubset(set(tokens(sb_key)))


def candidate_pairs(
    df_sb: pd.DataFrame,
    df_tm: pd.DataFrame,
    club_map: dict[str, str] = CLUB_MAP,
) -> pd.DataFrame:
    """Cross-join filtered to token-subset pairs, with club agreement flag."""
    sb = df_sb.assign(tok=df_sb["sb_key"].str.split())
    tm = df_tm.assign(tok=df_tm["tm_key"].str.split())
    pairs = sb.merge(tm, how="cross", suffixes=("_sb", "_tm"))
    pairs = pairs[
        pairs.apply(lambda r: set(r["tok_tm"]).issubset(set(r["tok_sb"])), axis=1)
    ].copy()
    pairs["club_ok"] = pairs.apply(
        lambda r: clubs_agree(r["sb_team"], r["tm_club"], club_map), axis=1
    )
    pairs["n_tok"] = pairs["tok_tm"].apply(len)
    return pairs


def disambiguate(pairs: pd.DataFrame) -> tuple[pd.DataFrame, pd.Index]:
    """Cascade over club-agreed pairs.

    Rule 1: exactly one club-agreed candidate wins.
    Rule 2: most TM tokens matched wins (Rodrigo De Paul 3 > Rodrigo 1).
    Returns (resolved, still_ambiguous_index) -- the latter is for manual
    DOB/position review, never silently dropped.
    """
    agreed = pairs[pairs["club_ok"]].copy()
    agreed = agreed.sort_values(["sb_player", "n_tok"], ascending=[True, False])
    resolved = agreed.drop_duplicates("sb_player")
    n_cand = agreed.groupby("sb_player")["player_id"].nunique()
    return resolved, n_cand[n_cand > 1].index


def fuzzy_score(sb_key: str, tm_key: str) -> float:
    """Min over TM tokens of best difflib ratio against SB tokens.

    Grounded: casemiro/casimiro scores 0.875 (match); isco/francisco 0.615,
    pepe/sebastian 0.15 (correctly below -- those need the nickname dict).
    """
    sb_toks = tokens(sb_key)
    return min(
        max(difflib.SequenceMatcher(None, tt, st).ratio() for st in sb_toks)
        for tt in tokens(tm_key)
    )


def fuzzy_matches(
    todo_sb: pd.DataFrame,
    todo_tm: pd.DataFrame,
    threshold: float = FUZZY_THRESHOLD,
    club_map: dict[str, str] = CLUB_MAP,
) -> pd.DataFrame:
    """Token-fuzzy for spelling variants. Club agreement is mandatory."""
    rows = []
    for _, s in todo_sb.iterrows():
        for _, t in todo_tm.iterrows():
            score = fuzzy_score(s["sb_key"], t["tm_key"])
            if score >= threshold and clubs_agree(s["sb_team"], t["tm_club"], club_map):
                rows.append(
                    (s["sb_player"], s["sb_team"], t["player_id"],
                     t["player_name"], t["tm_club"], round(score, 3))
                )
    return pd.DataFrame(
        rows,
        columns=["sb_player", "sb_team", "player_id", "player_name", "tm_club", "min_score"],
    )


def resolve_sample(
    df_sb: pd.DataFrame,
    df_tm: pd.DataFrame,
    nicknames: dict[str, str] = NICKNAMES,
    threshold: float = FUZZY_THRESHOLD,
    club_map: dict[str, str] = CLUB_MAP,
) -> tuple[pd.DataFrame, pd.Index]:
    """Full cascade -> (final with method, still_ambiguous for manual review)."""
    pairs = candidate_pairs(df_sb, df_tm, club_map)
    agreed = pairs[pairs["club_ok"]].copy()
    resolved, still_ambiguous = disambiguate(pairs)

    exact_ids = set(
        df_sb.merge(df_tm, left_on="sb_key", right_on="tm_key", how="inner")["sb_player"]
    ) & set(resolved["sb_player"])
    final = resolved[["sb_player", "sb_team", "player_id", "player_name", "tm_club"]].copy()
    final["method"] = final["sb_player"].apply(lambda s: "exact" if s in exact_ids else "token")

    nick_rows = []
    for sb_name, tm_name in nicknames.items():
        sb_hit = df_sb[df_sb["sb_player"] == sb_name]
        tm_hit = df_tm[df_tm["player_name"] == tm_name]
        if (
            len(sb_hit)
            and len(tm_hit)
            and clubs_agree(sb_hit.iloc[0]["sb_team"], tm_hit.iloc[0]["tm_club"], club_map)
        ):
            nick_rows.append(
                (sb_hit.iloc[0]["sb_player"], sb_hit.iloc[0]["sb_team"],
                 tm_hit.iloc[0]["player_id"], tm_hit.iloc[0]["player_name"],
                 tm_hit.iloc[0]["tm_club"], "nickname")
            )
    df_nick = pd.DataFrame(
        nick_rows,
        columns=["sb_player", "sb_team", "player_id", "player_name", "tm_club", "method"],
    )
    final = pd.concat([final, df_nick], ignore_index=True)

    done_sb = set(final["sb_player"])
    todo_sb = df_sb[~df_sb["sb_player"].isin(done_sb)]
    todo_tm = df_tm[~df_tm["player_id"].isin(final["player_id"])]
    df_fuzzy = fuzzy_matches(todo_sb, todo_tm, threshold, club_map)
    df_fuzzy = df_fuzzy.drop_duplicates("sb_player")
    df_fuzzy = df_fuzzy[~df_fuzzy["sb_player"].isin(final["sb_player"])]
    df_fuzzy["method"] = "fuzzy"
    final = pd.concat(
        [final, df_fuzzy[["sb_player", "sb_team", "player_id", "player_name", "tm_club", "method"]]],
        ignore_index=True,
    )
    return final, still_ambiguous
