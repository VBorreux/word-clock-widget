"""Italian locale."""

from .base import build_locale

HOURS = [
    ["È", "UNA"],
    ["SONO", "LE", "DUE"],
    ["SONO", "LE", "TRE"],
    ["SONO", "LE", "QUATTRO"],
    ["SONO", "LE", "CINQUE"],
    ["SONO", "LE", "SEI"],
    ["SONO", "LE", "SETTE"],
    ["SONO", "LE", "OTTO"],
    ["SONO", "LE", "NOVE"],
    ["SONO", "LE", "DIECI"],
    ["SONO", "LE", "UNDICI"],
    ["SONO", "LE", "DODICI"],
]

MINUTE_MAP = {
    5: (["E", "CINQUE"], 0),
    10: (["E", "DIECI"], 0),
    15: (["E", "UN", "QUARTO"], 0),
    20: (["E", "VENTI"], 0),
    25: (["E", "VENTI", "CINQUE"], 0),
    30: (["E", "MEZZA"], 0),
    35: (["MENO", "VENTI", "CINQUE"], 1),
    40: (["MENO", "VENTI"], 1),
    45: (["MENO", "UN", "QUARTO"], 1),
    50: (["MENO", "DIECI"], 1),
    55: (["MENO", "CINQUE"], 1),
}

LOCALE = build_locale(
    code="it",
    name="Italiano",
    intro=[],
    hours=HOURS,
    minute_map=MINUTE_MAP,
    filler="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
)
