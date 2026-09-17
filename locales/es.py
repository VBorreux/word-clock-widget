"""Spanish locale."""

from .base import build_locale

HOURS = [
    ["ES", "LA", "UNA"],
    ["SON", "LAS", "DOS"],
    ["SON", "LAS", "TRES"],
    ["SON", "LAS", "CUATRO"],
    ["SON", "LAS", "CINCO"],
    ["SON", "LAS", "SEIS"],
    ["SON", "LAS", "SIETE"],
    ["SON", "LAS", "OCHO"],
    ["SON", "LAS", "NUEVE"],
    ["SON", "LAS", "DIEZ"],
    ["SON", "LAS", "ONCE"],
    ["SON", "LAS", "DOCE"],
]

MINUTE_MAP = {
    5: (["Y", "CINCO"], 0),
    10: (["Y", "DIEZ"], 0),
    15: (["Y", "CUARTO"], 0),
    20: (["Y", "VEINTE"], 0),
    25: (["Y", "VEINTE", "CINCO"], 0),
    30: (["Y", "MEDIA"], 0),
    35: (["MENOS", "VEINTE", "CINCO"], 1),
    40: (["MENOS", "VEINTE"], 1),
    45: (["MENOS", "CUARTO"], 1),
    50: (["MENOS", "DIEZ"], 1),
    55: (["MENOS", "CINCO"], 1),
}

LOCALE = build_locale(
    code="es",
    name="Español",
    intro=[],
    hours=HOURS,
    minute_map=MINUTE_MAP,
    filler="ABCDEFGHIJKLMNOPQRSTUVWXYZÑ",
)
