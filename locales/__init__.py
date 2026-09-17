"""Language registry.

Every locale module exposes a ``LOCALE`` object.  The registry keeps insertion
order stable so menus list languages in a predictable order.
"""

from __future__ import annotations

from typing import Mapping

from . import ar, de, en, es, fr, it, nl, pt, ru, zh
from .base import Locale, LocaleError, minute_dots

DEFAULT_LANGUAGE = "en"

_ORDER = (en, fr, de, es, it, nl, pt, ru, zh, ar)

LANGUAGES: dict[str, Locale] = {module.LOCALE.code: module.LOCALE for module in _ORDER}


def get_locale(code: str) -> Locale:
    try:
        return LANGUAGES[code]
    except KeyError as exc:
        raise LocaleError(f"unknown language code: {code!r}") from exc


def get_available_locales(config: Mapping[str, object] | None = None) -> list[Locale]:
    """Return locales available for the given configuration.

    Optional locales (currently Arabic) are hidden unless explicitly enabled.
    """
    enabled = bool((config or {}).get("enable_optional_locales", False))
    return [locale for locale in LANGUAGES.values() if enabled or not locale.optional]


def validate_all() -> None:
    for locale in LANGUAGES.values():
        locale.validate()


__all__ = [
    "DEFAULT_LANGUAGE",
    "LANGUAGES",
    "Locale",
    "LocaleError",
    "get_available_locales",
    "get_locale",
    "minute_dots",
    "validate_all",
]
