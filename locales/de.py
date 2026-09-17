"""German locale."""

from .base import build_locale

HOURS = [
    ["EINS"],
    ["ZWEI"],
    ["DREI"],
    ["VIER"],
    ["FÜNF"],
    ["SECHS"],
    ["SIEBEN"],
    ["ACHT"],
    ["NEUN"],
    ["ZEHN"],
    ["ELF"],
    ["ZWÖLF"],
]

MINUTE_MAP = {
    5: (["FÜNF", "NACH"], 0),
    10: (["ZEHN", "NACH"], 0),
    15: (["VIERTEL", "NACH"], 0),
    20: (["ZWANZIG", "NACH"], 0),
    25: (["FÜNF", "VOR", "HALB"], 1),
    30: (["HALB"], 1),
    35: (["FÜNF", "NACH", "HALB"], 1),
    40: (["ZWANZIG", "VOR"], 1),
    45: (["VIERTEL", "VOR"], 1),
    50: (["ZEHN", "VOR"], 1),
    55: (["FÜNF", "VOR"], 1),
}

LOCALE = build_locale(
    code="de",
    name="Deutsch",
    intro=["ES", "IST"],
    hours=HOURS,
    minute_map=MINUTE_MAP,
    oclock=["UHR"],
    filler="ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ",
)
