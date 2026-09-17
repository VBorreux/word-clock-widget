"""French locale."""

from .base import build_locale

HOURS = [
    ["UNE", "HEURE"],
    ["DEUX", "HEURES"],
    ["TROIS", "HEURES"],
    ["QUATRE", "HEURES"],
    ["CINQ", "HEURES"],
    ["SIX", "HEURES"],
    ["SEPT", "HEURES"],
    ["HUIT", "HEURES"],
    ["NEUF", "HEURES"],
    ["DIX", "HEURES"],
    ["ONZE", "HEURES"],
    ["DOUZE", "HEURES"],
]

MINUTE_MAP = {
    5: (["CINQ"], 0),
    10: (["DIX"], 0),
    15: (["ET", "QUART"], 0),
    20: (["VINGT"], 0),
    25: (["VINGT", "CINQ"], 0),
    30: (["ET", "DEMIE"], 0),
    35: (["MOINS", "VINGT", "CINQ"], 1),
    40: (["MOINS", "VINGT"], 1),
    45: (["MOINS", "LE", "QUART"], 1),
    50: (["MOINS", "DIX"], 1),
    55: (["MOINS", "CINQ"], 1),
}

LOCALE = build_locale(
    code="fr",
    name="Français",
    intro=["IL", "EST"],
    hours=HOURS,
    minute_map=MINUTE_MAP,
    filler="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
)
