"""German locale: "ES IST FÜNF VOR HALB ZEHN"."""

from .base import build_locale, make_standard_build

TOKENS = {
    "ES": "ES",
    "IST": "IST",
    "FÜNF_M": "FÜNF",
    "ZEHN_M": "ZEHN",
    "VIERTEL": "VIERTEL",
    "ZWANZIG": "ZWANZIG",
    "NACH": "NACH",
    "VOR": "VOR",
    "HALB": "HALB",
    "SIEBEN": "SIEBEN",
    "ZWÖLF": "ZWÖLF",
    "SECHS": "SECHS",
    "DREI": "DREI",
    "VIER": "VIER",
    "FÜNF_H": "FÜNF",
    "NEUN": "NEUN",
    "ZWEI": "ZWEI",
    "EINS": "EINS",
    "ACHT": "ACHT",
    "ZEHN_H": "ZEHN",
    "ELF": "ELF",
    "UHR": "UHR",
}

INTRO = ["ES", "IST"]
MINUTE_WORDS = ["FÜNF_M", "ZEHN_M", "VIERTEL", "ZWANZIG", "NACH", "VOR", "HALB"]
HOUR_WORDS = [
    "SIEBEN",
    "ZWÖLF",
    "SECHS",
    "DREI",
    "VIER",
    "FÜNF_H",
    "NEUN",
    "ZWEI",
    "EINS",
    "ACHT",
    "ZEHN_H",
    "ELF",
]
OCLOCK = ["UHR"]
ORDER = INTRO + MINUTE_WORDS + HOUR_WORDS + OCLOCK

HOURS = [
    ["EINS"],
    ["ZWEI"],
    ["DREI"],
    ["VIER"],
    ["FÜNF_H"],
    ["SECHS"],
    ["SIEBEN"],
    ["ACHT"],
    ["NEUN"],
    ["ZEHN_H"],
    ["ELF"],
    ["ZWÖLF"],
]

MINUTE_MAP = {
    5: (["FÜNF_M", "NACH"], 0),
    10: (["ZEHN_M", "NACH"], 0),
    15: (["VIERTEL", "NACH"], 0),
    20: (["ZWANZIG", "NACH"], 0),
    25: (["FÜNF_M", "VOR", "HALB"], 1),
    30: (["HALB"], 1),
    35: (["FÜNF_M", "NACH", "HALB"], 1),
    40: (["ZWANZIG", "VOR"], 1),
    45: (["VIERTEL", "VOR"], 1),
    50: (["ZEHN_M", "VOR"], 1),
    55: (["FÜNF_M", "VOR"], 1),
}

BUILD = make_standard_build(INTRO, HOURS, MINUTE_MAP, OCLOCK, minute_first=True)

LOCALE = build_locale(
    code="de",
    name="Deutsch",
    tokens=TOKENS,
    order=ORDER,
    build=BUILD,
    filler="ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ",
)
