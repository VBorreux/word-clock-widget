#!/usr/bin/env python3
"""Render the application icon to a PNG file (used by the packaging scripts).

Prefers the canonical SVG asset; falls back to the Qt-drawn icon.
"""

from __future__ import annotations

import os
import sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

from PyQt6.QtGui import QImage, QPainter  # noqa: E402
from PyQt6.QtWidgets import QApplication  # noqa: E402

from tray import make_icon  # noqa: E402

SVG_PATH = os.path.join(ROOT, "assets", "qlocktwo.svg")


def _render_svg(path: str, output: str, size: int) -> bool:
    from PyQt6.QtSvg import QSvgRenderer

    renderer = QSvgRenderer(path)
    if not renderer.isValid():
        return False
    image = QImage(size, size, QImage.Format.Format_ARGB32)
    image.fill(0)
    painter = QPainter(image)
    renderer.render(painter)
    painter.end()
    return image.save(output)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: make_icon.py OUTPUT.png", file=sys.stderr)
        return 2
    output = sys.argv[1]
    QApplication.instance() or QApplication([])

    if os.path.exists(SVG_PATH) and _render_svg(SVG_PATH, output, 256):
        print(output)
        return 0

    if not make_icon(256).pixmap(256, 256).save(output):
        print("failed to write icon", file=sys.stderr)
        return 1
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
