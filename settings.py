"""Persistent widget configuration.

The configuration lives in the user's XDG config directory
(``~/.config/qlocktwo/config.json``) so that several machines sharing the same
source checkout (e.g. over NFS) keep their own settings.  ``QLOCKTWO_CONFIG``
overrides the location and a legacy ``config.json`` next to the sources is
migrated automatically.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Mapping

APP_DIR_NAME = "qlocktwo"
CONFIG_NAME = "config.json"

DEFAULTS: dict[str, Any] = {
    "language": "en",
    "opacity": 0.85,
    "scale": 1.0,
    "always_on_top": False,
    "show_dots": True,
    "glow": True,
    "enable_optional_locales": False,
    "position": None,
    "active_color": "#FFFFFF",
    "inactive_color": "#222222",
    "background_color": "#101014",
    "refresh_ms": 1000,
    "show_digital": False,
    "clock_24h": True,
    "show_date": False,
    "font_family": "",
    "font_scale": 1.0,
    "glow_strength": 1.0,
    "corner_radius": 20,
}


def legacy_path() -> Path:
    """Old per-checkout config location (pre-XDG)."""
    return Path(__file__).resolve().with_name(CONFIG_NAME)


def default_path() -> Path:
    override = os.environ.get("QLOCKTWO_CONFIG")
    if override:
        return Path(override).expanduser()
    base = os.environ.get("XDG_CONFIG_HOME")
    root = Path(base).expanduser() if base else Path.home() / ".config"
    return root / APP_DIR_NAME / CONFIG_NAME


def _read_json(path: Path) -> dict[str, Any]:
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return loaded if isinstance(loaded, dict) else {}


class Settings:
    """Small dict-like wrapper that persists changes to a JSON file."""

    def __init__(self, path: Path | str, data: Mapping[str, Any] | None = None) -> None:
        self.path = Path(path)
        self._data: dict[str, Any] = dict(DEFAULTS)
        if data:
            self._data.update(data)

    @classmethod
    def load(cls, path: Path | str | None = None) -> "Settings":
        if path is not None:
            target = Path(path)
            return cls(target, _read_json(target))

        target = default_path()
        if not target.exists():
            legacy = legacy_path()
            if legacy.exists():
                settings = cls(target, _read_json(legacy))
                settings.save()
                return settings
        return cls(target, _read_json(target))

    def get(self, key: str, default: Any = None) -> Any:
        if key in self._data:
            return self._data[key]
        if default is not None:
            return default
        return DEFAULTS.get(key)

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value
        self.save()

    def update(self, **values: Any) -> None:
        self._data.update(values)
        self.save()

    def merge(self, values: Mapping[str, Any], save: bool = True) -> None:
        self._data.update(values)
        if save:
            self.save()

    @property
    def data(self) -> dict[str, Any]:
        return dict(self._data)

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(self._data, ensure_ascii=False, indent=2) + "\n"
        handle, tmp_name = tempfile.mkstemp(
            dir=str(self.path.parent), prefix=".config-", suffix=".tmp"
        )
        try:
            with os.fdopen(handle, "w", encoding="utf-8") as stream:
                stream.write(payload)
            os.replace(tmp_name, self.path)
        finally:
            if os.path.exists(tmp_name):
                os.unlink(tmp_name)
