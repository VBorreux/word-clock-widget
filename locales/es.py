"""Spanish locale: "SON LAS DIEZ Y CUARTO"."""

from .base import build_locale, make_standard_build

TOKENS = {
    "SON": "SON",
    "LAS": "LAS",
    "ES": "ES",
    "LA": "LA",
    "CUATRO": "CUATRO",
    "CINCO_H": "CINCO",
    "SIETE": "SIETE",
    "NUEVE": "NUEVE",
    "DIEZ_H": "DIEZ",
    "DOCE": "DOCE",
    "ONCE": "ONCE",
    "OCHO": "OCHO",
    "TRES": "TRES",
    "SEIS": "SEIS",
    "DOS": "DOS",
    "UNA": "UNA",
    "MENOS": "MENOS",
    "Y": "Y",
    "CUARTO": "CUARTO",
    "MEDIA": "MEDIA",
    "VEINTE": "VEINTE",
    "CINCO_M": "CINCO",
    "DIEZ_M": "DIEZ",
}

PREFIXES = ["SON", "LAS", "ES", "LA"]
HOUR_WORDS = [
    "CUATRO",
    "CINCO_H",
    "SIETE",
    "NUEVE",
    "DIEZ_H",
    "DOCE",
    "ONCE",
    "OCHO",
    "TRES",
    "SEIS",
    "DOS",
    "UNA",
]
MINUTE_WORDS = ["MENOS", "Y", "CUARTO", "MEDIA", "VEINTE", "CINCO_M", "DIEZ_M"]
ORDER = PREFIXES + HOUR_WORDS + MINUTE_WORDS

HOURS = [
    ["ES", "LA", "UNA"],
    ["SON", "LAS", "DOS"],
    ["SON", "LAS", "TRES"],
    ["SON", "LAS", "CUATRO"],
    ["SON", "LAS", "CINCO_H"],
    ["SON", "LAS", "SEIS"],
    ["SON", "LAS", "SIETE"],
    ["SON", "LAS", "OCHO"],
    ["SON", "LAS", "NUEVE"],
    ["SON", "LAS", "DIEZ_H"],
    ["SON", "LAS", "ONCE"],
    ["SON", "LAS", "DOCE"],
]

MINUTE_MAP = {
    5: (["Y", "CINCO_M"], 0),
    10: (["Y", "DIEZ_M"], 0),
    15: (["Y", "CUARTO"], 0),
    20: (["Y", "VEINTE"], 0),
    25: (["Y", "VEINTE", "CINCO_M"], 0),
    30: (["Y", "MEDIA"], 0),
    35: (["MENOS", "VEINTE", "CINCO_M"], 1),
    40: (["MENOS", "VEINTE"], 1),
    45: (["MENOS", "CUARTO"], 1),
    50: (["MENOS", "DIEZ_M"], 1),
    55: (["MENOS", "CINCO_M"], 1),
}

BUILD = make_standard_build([], HOURS, MINUTE_MAP)

LOCALE = build_locale(
    code="es",
    name="Español",
    tokens=TOKENS,
    order=ORDER,
    build=BUILD,
    filler="ABCDEFGHIJKLMNOPQRSTUVWXYZÑ",
)
