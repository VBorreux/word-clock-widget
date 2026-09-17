"""English locale: "IT IS QUARTER PAST TEN"."""

from .base import build_locale, make_standard_build

TOKENS = {
    "IT": "IT",
    "IS": "IS",
    "TWENTY": "TWENTY",
    "FIVE_M": "FIVE",
    "TEN_M": "TEN",
    "QUARTER": "QUARTER",
    "HALF": "HALF",
    "PAST": "PAST",
    "TO": "TO",
    "ONE": "ONE",
    "TWO": "TWO",
    "THREE": "THREE",
    "FOUR": "FOUR",
    "FIVE_H": "FIVE",
    "SIX": "SIX",
    "SEVEN": "SEVEN",
    "EIGHT": "EIGHT",
    "NINE": "NINE",
    "TEN_H": "TEN",
    "ELEVEN": "ELEVEN",
    "TWELVE": "TWELVE",
    "OCLOCK": "OCLOCK",
}

INTRO = ["IT", "IS"]
MINUTE_WORDS = ["TWENTY", "FIVE_M", "TEN_M", "QUARTER", "HALF", "PAST", "TO"]
HOUR_WORDS = [
    "ELEVEN",
    "TWELVE",
    "THREE",
    "SEVEN",
    "EIGHT",
    "FOUR",
    "FIVE_H",
    "NINE",
    "ONE",
    "TWO",
    "SIX",
    "TEN_H",
]
OCLOCK = ["OCLOCK"]
ORDER = INTRO + MINUTE_WORDS + HOUR_WORDS + OCLOCK

HOURS = [
    ["ONE"],
    ["TWO"],
    ["THREE"],
    ["FOUR"],
    ["FIVE_H"],
    ["SIX"],
    ["SEVEN"],
    ["EIGHT"],
    ["NINE"],
    ["TEN_H"],
    ["ELEVEN"],
    ["TWELVE"],
]

MINUTE_MAP = {
    5: (["FIVE_M", "PAST"], 0),
    10: (["TEN_M", "PAST"], 0),
    15: (["QUARTER", "PAST"], 0),
    20: (["TWENTY", "PAST"], 0),
    25: (["TWENTY", "FIVE_M", "PAST"], 0),
    30: (["HALF", "PAST"], 0),
    35: (["TWENTY", "FIVE_M", "TO"], 1),
    40: (["TWENTY", "TO"], 1),
    45: (["QUARTER", "TO"], 1),
    50: (["TEN_M", "TO"], 1),
    55: (["FIVE_M", "TO"], 1),
}

BUILD = make_standard_build(INTRO, HOURS, MINUTE_MAP, OCLOCK, minute_first=True)

LOCALE = build_locale(
    code="en",
    name="English",
    tokens=TOKENS,
    order=ORDER,
    build=BUILD,
    filler="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
)
