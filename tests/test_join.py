"""Join-module tests. Tricky cases from notebooks 03-04, locked in.

Synthetic frames only -- no data dependency, runs in milliseconds.
Run with: pytest tests/ -q (requires pytest; see requirements.txt)
"""

import pandas as pd

from src.join.clubs import CLUB_MAP, clubs_agree, map_club
from src.join.match import (
    FUZZY_THRESHOLD,
    candidate_pairs,
    disambiguate,
    fuzzy_matches,
    fuzzy_score,
    resolve_sample,
    token_subset,
)
from src.join.nicknames import NICKNAMES
from src.join.normalize import normalize_name


def make_sb(rows):
    return pd.DataFrame(rows, columns=["sb_player", "sb_team"]).assign(
        sb_key=lambda d: d["sb_player"].apply(normalize_name)
    )


def make_tm(rows):
    return pd.DataFrame(rows, columns=["player_id", "player_name", "tm_club"]).assign(
        tm_key=lambda d: d["player_name"].apply(normalize_name)
    )


# ---- normalization ----

def test_normalize_strips_accents_case_punct():
    assert normalize_name("Ousmane Dembélé") == "ousmane dembele"
    assert normalize_name("  Sergio Busquets i Burgos! ") == "sergio busquets i burgos"


def test_normalize_splits_hyphenated_surnames():
    # Fellaini-Bakkioui glued into one token was unmatchable (notebook 05).
    assert normalize_name("Marouane Fellaini-Bakkioui") == "marouane fellaini bakkioui"
    assert normalize_name("Alexandre Dimitri Song-Billong") == "alexandre dimitri song billong"
    assert token_subset("marouane fellaini bakkioui", "marouane fellaini")


# ---- club map + gate ----

def test_club_map_covers_grounded_entries():
    assert CLUB_MAP["RC Deportivo La Coruña"] == "Deportivo de La Coruña"
    assert CLUB_MAP["Athletic Club"] == "Athletic Bilbao"
    assert CLUB_MAP["Celta Vigo"] == "Celta de Vigo"
    assert CLUB_MAP["Atlético Madrid"] == "Atlético de Madrid"
    assert CLUB_MAP["Hertha Berlin"] == "Hertha BSC"
    # Bayer needs no entry: whitespace collapsing makes containment hold.
    assert clubs_agree("Bayer Leverkusen", "Bayer 04 Leverkusen")


def test_map_club_passes_unknown_through():
    assert map_club("Sevilla FC") == "Sevilla FC"


def test_clubs_agree_both_directions_and_map():
    assert clubs_agree("Barcelona", "FC Barcelona")
    assert clubs_agree("FC Barcelona", "Barcelona")
    assert clubs_agree("RC Deportivo La Coruña", "Deportivo de La Coruña")
    assert clubs_agree("Athletic Club", "Athletic Bilbao")


def test_clubs_agree_rejects_real_mismatches():
    # Llorente (Sevilla) vs Torres (Atletico): the gate must hold.
    assert not clubs_agree("Sevilla", "Atlético de Madrid")
    assert not clubs_agree("Sporting Gijón", "Celta de Vigo")
    # Notebook 06 audit: shared "Borussia" prefix, distinct clubs.
    # Prefix matching must never replace the containment gate.
    assert not clubs_agree("Borussia Dortmund", "Borussia Mönchengladbach")
    assert not clubs_agree("Borussia Mönchengladbach", "Borussia Dortmund")


# ---- token subset ----

def test_token_subset_common_vs_legal_name():
    assert token_subset("lionel andres messi cuccittini", "lionel messi")


def test_token_subset_documents_nesting_hazard():
    # Fernando Llorente Torres CONTAINS Fernando Torres' tokens.
    # True here is correct -- and exactly why the club gate must follow.
    assert token_subset("fernando llorente torres", "fernando torres")


def test_token_subset_rejects_unrelated():
    assert not token_subset("lionel andres messi cuccittini", "cristiano ronaldo")


# ---- fuzzy ----

def test_fuzzy_catches_spelling_variant():
    assert fuzzy_score("carlos henrique casimiro", "casemiro") >= FUZZY_THRESHOLD


def test_fuzzy_rejects_nickname_class():
    assert fuzzy_score("francisco roman alarcon suarez", "isco") < FUZZY_THRESHOLD
    assert fuzzy_score("kleper laveran lima ferreira", "pepe") < FUZZY_THRESHOLD


def test_fuzzy_requires_club_gate():
    sb = make_sb([("Fernando Llorente Torres", "Sevilla")])
    tm = make_tm([(7767, "Fernando Torres", "Atlético de Madrid")])
    out = fuzzy_matches(sb, tm)
    assert len(out) == 0


# ---- nicknames ----

def test_nickname_dict_has_verified_entries():
    assert NICKNAMES["Francisco Román Alarcón Suárez"] == "Isco"
    assert NICKNAMES["Kléper Laveran Lima Ferreira"] == "Pepe"
    assert NICKNAMES["Francisco Casilla Cortés"] == "Kiko Casilla"
    # Premier League supplement: 15 entries, all verified both sides.
    assert len(NICKNAMES) == 18
    assert NICKNAMES["Francesc Fàbregas i Soler"] == "Cesc Fàbregas"
    assert NICKNAMES["Bamidele Alli"] == "Dele Alli"
    assert NICKNAMES["John Michael Nchekwube Obinna"] == "Mikel John Obi"
    assert NICKNAMES["Jonathan Grant Evans"] == "Jonny Evans"


def test_nickname_keys_are_full_legal_names():
    # Keys must carry surnames (never bare common names) so same-name
    # collisions elsewhere (e.g. other Evanses) cannot match through the dict.
    assert len(normalize_name("Jonathan Grant Evans").split()) > 2


# ---- disambiguation cascade ----

def test_disambiguate_club_unique_wins():
    sb = make_sb([("Fernando Llorente Torres", "Sevilla")])
    tm = make_tm([
        (7767, "Fernando Torres", "Atlético de Madrid"),
        (35564, "Fernando Llorente", "Sevilla FC"),
    ])
    resolved, still = disambiguate(candidate_pairs(sb, tm))
    assert len(resolved) == 1
    assert resolved.iloc[0]["player_id"] == 35564
    assert len(still) == 0


def test_disambiguate_prefers_more_tokens_matched():
    sb = make_sb([("Rodrigo Javier De Paul", "Valencia")])
    tm = make_tm([
        (131505, "Rodrigo", "Valencia CF"),
        (255901, "Rodrigo De Paul", "Valencia CF"),
    ])
    resolved, still = disambiguate(candidate_pairs(sb, tm))
    assert resolved.iloc[0]["player_id"] == 255901
    # Both candidates survive the gate: flagged for human review, not dropped.
    assert "Rodrigo Javier De Paul" in set(still)


# ---- end-to-end on synthetic sample ----

def test_resolve_sample_methods_and_review():
    sb = make_sb([
        ("Lionel Andrés Messi Cuccittini", "Barcelona"),
        ("Fernando Llorente Torres", "Sevilla"),
        ("Francisco Román Alarcón Suárez", "Real Madrid"),
        ("Carlos Henrique Casimiro", "Real Madrid"),
    ])
    tm = make_tm([
        (28003, "Lionel Messi", "FC Barcelona"),
        (7767, "Fernando Torres", "Atlético de Madrid"),
        (35564, "Fernando Llorente", "Sevilla FC"),
        (85288, "Isco", "Real Madrid"),
        (23, "Casemiro", "Real Madrid"),
    ])
    final, still = resolve_sample(sb, tm)
    by_sb = dict(zip(final["sb_player"], final["method"]))
    assert by_sb["Lionel Andrés Messi Cuccittini"] == "token"
    assert by_sb["Fernando Llorente Torres"] == "token"
    assert final.loc[final["sb_player"] == "Fernando Llorente Torres", "player_id"].iloc[0] == 35564
    assert by_sb["Francisco Román Alarcón Suárez"] == "nickname"
    assert by_sb["Carlos Henrique Casimiro"] == "fuzzy"
