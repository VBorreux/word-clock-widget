"""Entry point for the Qlocktwo desktop widget."""

from __future__ import annotations

import sys

from PyQt6.QtWidgets import QApplication

from locales import DEFAULT_LANGUAGE, get_locale, validate_all
from settings import Settings
from widget import ClockWidget


def main() -> int:
    validate_all()
    open_settings = "--settings" in sys.argv
    app = QApplication([arg for arg in sys.argv if arg != "--settings"])
    app.setApplicationName("Qlocktwo")
    app.setApplicationDisplayName("Qlocktwo")
    app.setQuitOnLastWindowClosed(True)

    settings = Settings.load()
    try:
        locale = get_locale(str(settings.get("language")))
    except Exception:
        locale = get_locale(DEFAULT_LANGUAGE)

    widget = ClockWidget(settings, locale)
    widget.show()
    if open_settings:
        widget._open_settings()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
