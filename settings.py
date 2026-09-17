"""Persistent widget configuration stored as JSON next to the sources."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Mapping

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
}


def default_path() -> Path:
    return Path(__file__).resolve().with_name(CONFIG_NAME)


class Settings:
    """Small dict-like wrapper that persists changes to ``config.json``."""

    def __init__(self, path: Path | str, data: Mapping[str, Any] | None = None) -> None:
        self.path = Path(path)
        self._data: dict[str, Any] = dict(DEFAULTS)
        if data:
            self._data.update(data)

    @classmethod
    def load(cls, path: Path | str | None = None) -> "Settings":
        target = Path(path) if path is not None else default_path()
        data: dict[str, Any] = {}
        if target.exists():
            try:
                loaded = json.loads(target.read_text(encoding="utf-8"))
                if isinstance(loaded, dict):
                    data = loaded
            except (OSError, ValueError):
                data = {}
        return cls(target, data)

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
