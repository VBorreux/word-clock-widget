"""Portuguese locale."""

from .base import build_locale

HOURS = [
    ["É", "UMA"],
    ["SÃO", "DUAS"],
    ["SÃO", "TRÊS"],
    ["SÃO", "QUATRO"],
    ["SÃO", "CINCO"],
    ["SÃO", "SEIS"],
    ["SÃO", "SETE"],
    ["SÃO", "OITO"],
    ["SÃO", "NOVE"],
    ["SÃO", "DEZ"],
    ["SÃO", "ONZE"],
    ["SÃO", "DOZE"],
]

MINUTE_MAP = {
    5: (["E", "CINCO"], 0),
    10: (["E", "DEZ"], 0),
    15: (["E", "QUARTO"], 0),
    20: (["E", "VINTE"], 0),
    25: (["E", "VINTE", "E", "CINCO"], 0),
    30: (["E", "MEIA"], 0),
    35: (["MENOS", "VINTE", "E", "CINCO"], 1),
    40: (["MENOS", "VINTE"], 1),
    45: (["MENOS", "QUARTO"], 1),
    50: (["MENOS", "DEZ"], 1),
    55: (["MENOS", "CINCO"], 1),
}

LOCALE = build_locale(
    code="pt",
    name="Português",
    intro=[],
    hours=HOURS,
    minute_map=MINUTE_MAP,
    filler="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
)
