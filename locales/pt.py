"""Portuguese locale: "SÃO DEZ E QUARTO"."""

from .base import build_locale, make_standard_build

TOKENS = {
    "SÃO": "SÃO",
    "É": "É",
    "QUATRO": "QUATRO",
    "CINCO_H": "CINCO",
    "SETE": "SETE",
    "OITO": "OITO",
    "NOVE": "NOVE",
    "ONZE": "ONZE",
    "DOZE": "DOZE",
    "TRÊS": "TRÊS",
    "DUAS": "DUAS",
    "SEIS": "SEIS",
    "DEZ_H": "DEZ",
    "UMA": "UMA",
    "MENOS": "MENOS",
    "E": "E",
    "QUARTO": "QUARTO",
    "MEIA": "MEIA",
    "VINTE": "VINTE",
    "E2": "E",
    "CINCO_M": "CINCO",
    "DEZ_M": "DEZ",
}

PREFIXES = ["SÃO", "É"]
HOUR_WORDS = [
    "QUATRO",
    "CINCO_H",
    "SETE",
    "OITO",
    "NOVE",
    "ONZE",
    "DOZE",
    "TRÊS",
    "DUAS",
    "SEIS",
    "DEZ_H",
    "UMA",
]
MINUTE_WORDS = ["MENOS", "E", "QUARTO", "MEIA", "VINTE", "E2", "CINCO_M", "DEZ_M"]
ORDER = PREFIXES + HOUR_WORDS + MINUTE_WORDS

HOURS = [
    ["É", "UMA"],
    ["SÃO", "DUAS"],
    ["SÃO", "TRÊS"],
    ["SÃO", "QUATRO"],
    ["SÃO", "CINCO_H"],
    ["SÃO", "SEIS"],
    ["SÃO", "SETE"],
    ["SÃO", "OITO"],
    ["SÃO", "NOVE"],
    ["SÃO", "DEZ_H"],
    ["SÃO", "ONZE"],
    ["SÃO", "DOZE"],
]

MINUTE_MAP = {
    5: (["E", "CINCO_M"], 0),
    10: (["E", "DEZ_M"], 0),
    15: (["E", "QUARTO"], 0),
    20: (["E", "VINTE"], 0),
    25: (["E", "VINTE", "E2", "CINCO_M"], 0),
    30: (["E", "MEIA"], 0),
    35: (["MENOS", "VINTE", "E2", "CINCO_M"], 1),
    40: (["MENOS", "VINTE"], 1),
    45: (["MENOS", "QUARTO"], 1),
    50: (["MENOS", "DEZ_M"], 1),
    55: (["MENOS", "CINCO_M"], 1),
}

BUILD = make_standard_build([], HOURS, MINUTE_MAP)

LOCALE = build_locale(
    code="pt",
    name="Português",
    tokens=TOKENS,
    order=ORDER,
    build=BUILD,
    filler="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
)
