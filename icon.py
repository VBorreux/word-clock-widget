"""Application icon.

The canonical icon is the SVG in ``assets/``; a Qt-drawn icon is used as a
fallback if the SVG cannot be loaded (e.g. missing SVG image plugin).
"""

from __future__ import annotations

from pathlib import Path

from PyQt6.QtGui import QIcon

from tray import make_icon

ASSET_PATH = Path(__file__).resolve().with_name("assets") / "qlocktwo.svg"


def app_icon() -> QIcon:
    if ASSET_PATH.exists():
        icon = QIcon(str(ASSET_PATH))
        if not icon.isNull() and not icon.pixmap(64, 64).isNull():
            return icon
    return make_icon(256)
