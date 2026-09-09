"""SB full legal name -> TM common name, for players invisible to tokens.

Entries are structural (TM's single token appears nowhere in the legal name)
and each was verified present in TM ES1 2015/16 appearances (notebook 04).
Keep this short and manual; fuzzy matching must NOT absorb these cases.
"""

NICKNAMES: dict[str, str] = {
    "Francisco Román Alarcón Suárez": "Isco",
    "Kléper Laveran Lima Ferreira": "Pepe",
    "Francisco Casilla Cortés": "Kiko Casilla",
}
