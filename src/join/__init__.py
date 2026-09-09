"""StatsBomb <-> Transfermarkt entity resolution.

Decided logic graduated from notebooks 03-04. Scope is name/club matching
only; valuation attachment lives notebook-side until the scale-up.
"""

from src.join.clubs import CLUB_MAP, clubs_agree
from src.join.match import (
    candidate_pairs,
    disambiguate,
    fuzzy_matches,
    resolve_sample,
    token_subset,
)
from src.join.nicknames import NICKNAMES
from src.join.normalize import normalize_name

__all__ = [
    "CLUB_MAP",
    "NICKNAMES",
    "candidate_pairs",
    "clubs_agree",
    "disambiguate",
    "fuzzy_matches",
    "normalize_name",
    "resolve_sample",
    "token_subset",
]
