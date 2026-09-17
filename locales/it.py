"""Italian locale: "SONO LE DIECI E UN QUARTO"."""

from .base import build_locale, make_standard_build

TOKENS = {
    "SONO": "SONO",
    "LE": "LE",
    "È": "È",
    "QUATTRO": "QUATTRO",
    "DODICI": "DODICI",
    "CINQUE_H": "CINQUE",
    "UNDICI": "UNDICI",
    "DIECI_H": "DIECI",
    "SETTE": "SETTE",
    "NOVE": "NOVE",
    "OTTO": "OTTO",
    "TRE": "TRE",
    "SEI": "SEI",
    "DUE": "DUE",
    "UNA": "UNA",
    "MENO": "MENO",
    "E": "E",
    "UN": "UN",
    "QUARTO": "QUARTO",
    "MEZZA": "MEZZA",
    "VENTI": "VENTI",
    "CINQUE_M": "CINQUE",
    "DIECI_M": "DIECI",
}

PREFIXES = ["SONO", "LE", "È"]
HOUR_WORDS = [
    "QUATTRO",
    "DODICI",
    "CINQUE_H",
    "UNDICI",
    "DIECI_H",
    "SETTE",
    "NOVE",
    "OTTO",
    "TRE",
    "SEI",
    "DUE",
    "UNA",
]
MINUTE_WORDS = ["MENO", "E", "UN", "QUARTO", "MEZZA", "VENTI", "CINQUE_M", "DIECI_M"]
ORDER = PREFIXES + HOUR_WORDS + MINUTE_WORDS

HOURS = [
    ["È", "UNA"],
    ["SONO", "LE", "DUE"],
    ["SONO", "LE", "TRE"],
    ["SONO", "LE", "QUATTRO"],
    ["SONO", "LE", "CINQUE_H"],
    ["SONO", "LE", "SEI"],
    ["SONO", "LE", "SETTE"],
    ["SONO", "LE", "OTTO"],
    ["SONO", "LE", "NOVE"],
    ["SONO", "LE", "DIECI_H"],
    ["SONO", "LE", "UNDICI"],
    ["SONO", "LE", "DODICI"],
]

MINUTE_MAP = {
    5: (["E", "CINQUE_M"], 0),
    10: (["E", "DIECI_M"], 0),
    15: (["E", "UN", "QUARTO"], 0),
    20: (["E", "VENTI"], 0),
    25: (["E", "VENTI", "CINQUE_M"], 0),
    30: (["E", "MEZZA"], 0),
    35: (["MENO", "VENTI", "CINQUE_M"], 1),
    40: (["MENO", "VENTI"], 1),
    45: (["MENO", "UN", "QUARTO"], 1),
    50: (["MENO", "DIECI_M"], 1),
    55: (["MENO", "CINQUE_M"], 1),
}

BUILD = make_standard_build([], HOURS, MINUTE_MAP)

LOCALE = build_locale(
    code="it",
    name="Italiano",
    tokens=TOKENS,
    order=ORDER,
    build=BUILD,
    filler="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
)
