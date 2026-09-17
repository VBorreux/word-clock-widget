"""English locale."""

from .base import build_locale

HOURS = [
    ["ONE"],
    ["TWO"],
    ["THREE"],
    ["FOUR"],
    ["FIVE"],
    ["SIX"],
    ["SEVEN"],
    ["EIGHT"],
    ["NINE"],
    ["TEN"],
    ["ELEVEN"],
    ["TWELVE"],
]

MINUTE_MAP = {
    5: (["FIVE", "PAST"], 0),
    10: (["TEN", "PAST"], 0),
    15: (["QUARTER", "PAST"], 0),
    20: (["TWENTY", "PAST"], 0),
    25: (["TWENTY", "FIVE", "PAST"], 0),
    30: (["HALF", "PAST"], 0),
    35: (["TWENTY", "FIVE", "TO"], 1),
    40: (["TWENTY", "TO"], 1),
    45: (["QUARTER", "TO"], 1),
    50: (["TEN", "TO"], 1),
    55: (["FIVE", "TO"], 1),
}

LOCALE = build_locale(
    code="en",
    name="English",
    intro=["IT", "IS"],
    hours=HOURS,
    minute_map=MINUTE_MAP,
    oclock=["OCLOCK"],
    filler="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
)
