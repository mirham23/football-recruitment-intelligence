"""Club-name mapping + agreement gate.

The gate is load-bearing (notebook 03): token matching alone merges distinct
players (Llorente/Torres, the two Sergio Alvarezes). Never bypass it.
"""

from src.join.normalize import normalize_name

# SB team name -> TM club name. Grounded in notebook 03's mismatch table.
# One entry fixes every player at that club (Deportivo alone unblocked 5+).
CLUB_MAP: dict[str, str] = {
    "RC Deportivo La Coruña": "Deportivo de La Coruña",
    "Athletic Club": "Athletic Bilbao",
    "Celta Vigo": "Celta de Vigo",
    "Atlético Madrid": "Atlético de Madrid",
    # Bundesliga (notebook 06 audit): Berlin and BSC share no containment.
    "Hertha Berlin": "Hertha BSC",
}


def map_club(sb_team: str, club_map: dict[str, str] = CLUB_MAP) -> str:
    """Translate an SB team name to TM naming. Unknown names pass through."""
    return club_map.get(sb_team, sb_team)


def clubs_agree(sb_team: str, tm_club: str, club_map: dict[str, str] = CLUB_MAP) -> bool:
    """Normalized containment, either direction, after map translation."""
    sb, tm = normalize_name(map_club(sb_team, club_map)), normalize_name(tm_club)
    return sb in tm or tm in sb
