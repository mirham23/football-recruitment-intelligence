"""SB full legal name -> TM common name, for players invisible to tokens.

Entries are structural (TM's single token appears nowhere in the legal name)
and each was verified present in the same league-season window on both sides:
ES1 2015/16 (notebook 04) and GB1 2015/16 (notebook 05 follow-up).
Keys are exact SB legal names; values are exact TM common names. Club
agreement is re-verified at application time, so same-name collisions
(e.g. the three SB Evanses vs TM's Jonny Evans) cannot cross-contaminate.
Keep this short and manual; fuzzy matching must NOT absorb these cases.
"""

NICKNAMES: dict[str, str] = {
    # La Liga 2015/16 (notebook 04)
    "Francisco Román Alarcón Suárez": "Isco",
    "Kléper Laveran Lima Ferreira": "Pepe",
    "Francisco Casilla Cortés": "Kiko Casilla",
    # Premier League 2015/16 (verified both sides, clubs agree)
    "Francesc Fàbregas i Soler": "Cesc Fàbregas",
    "Ignacio Monreal Eraso": "Nacho Monreal",
    "Wilfredo Daniel Caballero": "Willy Caballero",
    "José Luis Sanmartín Mato": "Joselu",
    "Bamidele Alli": "Dele Alli",
    "Jonathan Grant Evans": "Jonny Evans",
    "Rhu-endly Martina": "Cuco Martina",
    "Juan Miguel Jiménez López": "Juanmi",
    "Andrew Philip King": "Andy King",
    "Robert Brady": "Robbie Brady",
    "John Michael Nchekwube Obinna": "Mikel John Obi",
    "Gabriel Armando de Abreu": "Gabriel Paulista",
    "Glyn Oliver Myhill": "Boaz Myhill",
    "Santiago Cazorla González": "Santi Cazorla",
    "Bradley Guzan": "Brad Guzan",
}
