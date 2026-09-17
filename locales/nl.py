"""Dutch locale: "HET IS VIJF OVER TIEN"."""

from .base import build_locale, make_standard_build

TOKENS = {
    "HET": "HET",
    "IS": "IS",
    "VIJF_M": "VIJF",
    "TIEN_M": "TIEN",
    "KWART": "KWART",
    "TWINTIG": "TWINTIG",
    "OVER": "OVER",
    "VOOR": "VOOR",
    "HALF": "HALF",
    "TWAALF": "TWAALF",
    "ZEVEN": "ZEVEN",
    "NEGEN": "NEGEN",
    "TWEE": "TWEE",
    "VIER": "VIER",
    "VIJF_H": "VIJF",
    "DRIE": "DRIE",
    "ACHT": "ACHT",
    "TIEN_H": "TIEN",
    "ZES": "ZES",
    "EEN": "EEN",
    "ELF": "ELF",
    "UUR": "UUR",
}

INTRO = ["HET", "IS"]
MINUTE_WORDS = ["VIJF_M", "TIEN_M", "KWART", "TWINTIG", "OVER", "VOOR", "HALF"]
HOUR_WORDS = [
    "TWAALF",
    "ZEVEN",
    "NEGEN",
    "TWEE",
    "VIER",
    "VIJF_H",
    "DRIE",
    "ACHT",
    "TIEN_H",
    "ZES",
    "EEN",
    "ELF",
]
OCLOCK = ["UUR"]
ORDER = INTRO + MINUTE_WORDS + HOUR_WORDS + OCLOCK

HOURS = [
    ["EEN"],
    ["TWEE"],
    ["DRIE"],
    ["VIER"],
    ["VIJF_H"],
    ["ZES"],
    ["ZEVEN"],
    ["ACHT"],
    ["NEGEN"],
    ["TIEN_H"],
    ["ELF"],
    ["TWAALF"],
]

MINUTE_MAP = {
    5: (["VIJF_M", "OVER"], 0),
    10: (["TIEN_M", "OVER"], 0),
    15: (["KWART", "OVER"], 0),
    20: (["TWINTIG", "OVER"], 0),
    25: (["VIJF_M", "VOOR", "HALF"], 1),
    30: (["HALF"], 1),
    35: (["VIJF_M", "OVER", "HALF"], 1),
    40: (["TWINTIG", "VOOR"], 1),
    45: (["KWART", "VOOR"], 1),
    50: (["TIEN_M", "VOOR"], 1),
    55: (["VIJF_M", "VOOR"], 1),
}

BUILD = make_standard_build(INTRO, HOURS, MINUTE_MAP, OCLOCK, minute_first=True)

LOCALE = build_locale(
    code="nl",
    name="Nederlands",
    tokens=TOKENS,
    order=ORDER,
    build=BUILD,
    filler="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
)
