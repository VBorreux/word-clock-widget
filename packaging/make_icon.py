#!/usr/bin/env python3
"""Render the application icon to a PNG file (used by the packaging scripts)."""

from __future__ import annotations

import os
import sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from PyQt6.QtWidgets import QApplication  # noqa: E402

from tray import make_icon  # noqa: E402


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: make_icon.py OUTPUT.png", file=sys.stderr)
        return 2
    app = QApplication.instance() or QApplication([])
    icon = make_icon(256)
    if not icon.pixmap(256, 256).save(sys.argv[1]):
        print("failed to write icon", file=sys.stderr)
        return 1
    print(sys.argv[1])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
