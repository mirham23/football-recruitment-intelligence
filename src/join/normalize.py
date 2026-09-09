"""Name normalization. Everything downstream matches on keys, never raw names."""

import re
import unicodedata


def normalize_name(name: str) -> str:
    """Lowercase, strip accents (NFKD), drop punctuation. Stdlib only."""
    folded = unicodedata.normalize("NFKD", str(name)).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z ]", "", folded.lower()).strip()


def tokens(key: str) -> list[str]:
    """Whitespace-split a normalized key into tokens."""
    return key.split()
