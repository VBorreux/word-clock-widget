"""French locale: "IL EST DEUX HEURES MOINS LE QUART"."""

from .base import build_locale, make_standard_build

TOKENS = {
    "IL": "IL",
    "EST": "EST",
    "QUATRE": "QUATRE",
    "DOUZE": "DOUZE",
    "TROIS": "TROIS",
    "ONZE": "ONZE",
    "CINQ_H": "CINQ",
    "SEPT": "SEPT",
    "HUIT": "HUIT",
    "NEUF": "NEUF",
    "DEUX": "DEUX",
    "UNE": "UNE",
    "SIX": "SIX",
    "DIX_H": "DIX",
    "HEURES": "HEURES",
    "HEURE": "HEURE",
    "MOINS": "MOINS",
    "ET": "ET",
    "LE": "LE",
    "QUART": "QUART",
    "DEMIE": "DEMIE",
    "VINGT": "VINGT",
    "CINQ_M": "CINQ",
    "DIX_M": "DIX",
}

INTRO = ["IL", "EST"]
HOUR_WORDS = [
    "QUATRE",
    "DOUZE",
    "TROIS",
    "ONZE",
    "CINQ_H",
    "SEPT",
    "HUIT",
    "NEUF",
    "DEUX",
    "UNE",
    "SIX",
    "DIX_H",
]
HOUR_UNITS = ["HEURES", "HEURE"]
MINUTE_WORDS = ["MOINS", "ET", "LE", "QUART", "DEMIE", "VINGT", "CINQ_M", "DIX_M"]
ORDER = INTRO + HOUR_WORDS + HOUR_UNITS + MINUTE_WORDS

HOURS = [
    ["UNE", "HEURE"],
    ["DEUX", "HEURES"],
    ["TROIS", "HEURES"],
    ["QUATRE", "HEURES"],
    ["CINQ_H", "HEURES"],
    ["SIX", "HEURES"],
    ["SEPT", "HEURES"],
    ["HUIT", "HEURES"],
    ["NEUF", "HEURES"],
    ["DIX_H", "HEURES"],
    ["ONZE", "HEURES"],
    ["DOUZE", "HEURES"],
]

MINUTE_MAP = {
    5: (["CINQ_M"], 0),
    10: (["DIX_M"], 0),
    15: (["ET", "QUART"], 0),
    20: (["VINGT"], 0),
    25: (["VINGT", "CINQ_M"], 0),
    30: (["ET", "DEMIE"], 0),
    35: (["MOINS", "VINGT", "CINQ_M"], 1),
    40: (["MOINS", "VINGT"], 1),
    45: (["MOINS", "LE", "QUART"], 1),
    50: (["MOINS", "DIX_M"], 1),
    55: (["MOINS", "CINQ_M"], 1),
}

BUILD = make_standard_build(INTRO, HOURS, MINUTE_MAP)

LOCALE = build_locale(
    code="fr",
    name="Français",
    tokens=TOKENS,
    order=ORDER,
    build=BUILD,
    filler="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
)
