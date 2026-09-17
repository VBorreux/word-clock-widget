"""Dutch locale."""

from .base import build_locale

HOURS = [
    ["EEN"],
    ["TWEE"],
    ["DRIE"],
    ["VIER"],
    ["VIJF"],
    ["ZES"],
    ["ZEVEN"],
    ["ACHT"],
    ["NEGEN"],
    ["TIEN"],
    ["ELF"],
    ["TWAALF"],
]

MINUTE_MAP = {
    5: (["VIJF", "OVER"], 0),
    10: (["TIEN", "OVER"], 0),
    15: (["KWART", "OVER"], 0),
    20: (["TWINTIG", "OVER"], 0),
    25: (["VIJF", "VOOR", "HALF"], 1),
    30: (["HALF"], 1),
    35: (["VIJF", "OVER", "HALF"], 1),
    40: (["TWINTIG", "VOOR"], 1),
    45: (["KWART", "VOOR"], 1),
    50: (["TIEN", "VOOR"], 1),
    55: (["VIJF", "VOOR"], 1),
}

LOCALE = build_locale(
    code="nl",
    name="Nederlands",
    intro=["HET", "IS"],
    hours=HOURS,
    minute_map=MINUTE_MAP,
    oclock=["UUR"],
    filler="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
)
