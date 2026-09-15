"""Name normalization. Everything downstream matches on keys, never raw names."""

import re
import unicodedata


def normalize_name(name: str) -> str:
    """Lowercase, strip accents (NFKD), drop punctuation. Stdlib only.

    Hyphens (ASCII and Unicode variants) become spaces, not deletions:
    "Fellaini-Bakkioui" must tokenize as two tokens, otherwise the surname
    glues into an unmatchable single token.
    Collapsed whitespace handles digit-stripping gaps ("Bayer 04 Leverkusen"
    cleans to "bayer  leverkusen", which only contains "bayer leverkusen"
    after collapsing).
    """
    folded = unicodedata.normalize("NFKD", str(name)).encode("ascii", "ignore").decode("ascii")
    spaced = re.sub(r"[\-\u2010-\u2015\u2212]", " ", folded)
    cleaned = re.sub(r"[^a-z ]", "", spaced.lower())
    return re.sub(r"\s+", " ", cleaned).strip()


def tokens(key: str) -> list[str]:
    """Whitespace-split a normalized key into tokens."""
    return key.split()
