"""Smoke tests for the Qt widget (skipped when PyQt6 is unavailable)."""

import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

try:
    from PyQt6.QtWidgets import QApplication

    HAVE_QT = True
except Exception:  # pragma: no cover - depends on the environment
    HAVE_QT = False

from locales import LANGUAGES
from settings import Settings


@unittest.skipUnless(HAVE_QT, "PyQt6 is not installed")
class WidgetSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = QApplication.instance() or QApplication([])

    def _make_widget(self, settings: Settings, code: str):
        from widget import ClockWidget

        widget = ClockWidget(settings, LANGUAGES[code])
        widget.show()
        self.app.processEvents()
        return widget

    def test_construct_and_render_every_script(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            settings = Settings.load(Path(directory) / "config.json")
            for code in ("en", "fr", "ru", "zh", "ar"):
                with self.subTest(code=code):
                    widget = self._make_widget(settings, code)
                    try:
                        image = widget.grab()
                        self.assertFalse(image.isNull())
                        self.assertGreater(image.width(), 0)
                        self.assertGreater(image.height(), 0)
                    finally:
                        widget.close()

    def test_language_switch_resizes_board(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            settings = Settings.load(Path(directory) / "config.json")
            widget = self._make_widget(settings, "en")
            try:
                small = widget.size()
                widget._set_language("ru")
                self.app.processEvents()
                self.assertGreater(widget.size().width(), small.width())
                self.assertEqual(settings.get("language"), "ru")
            finally:
                widget.close()

    def test_offscreen_saved_position_is_recentered(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            settings = Settings.load(Path(directory) / "config.json")
            settings.set("position", [10_000_000, 10_000_000])
            widget = self._make_widget(settings, "en")
            try:
                geometry = widget.geometry()
                self.assertTrue(
                    any(
                        screen.availableGeometry().intersects(geometry)
                        for screen in self.app.screens()
                    ),
                    "widget should be recentered when the saved position is off-screen",
                )
            finally:
                widget.close()

    def test_apply_settings_updates_refresh_language_and_size(self) -> None:
        from widget import CELL_SIZE

        with tempfile.TemporaryDirectory() as directory:
            settings = Settings.load(Path(directory) / "config.json")
            settings.update(
                refresh_ms=250,
                language="de",
                active_color="#ff0000",
                background_color="#000080",
                scale=1.5,
            )
            widget = self._make_widget(settings, "en")
            try:
                widget.apply_settings()
                self.assertEqual(widget._timer.interval(), 250)
                self.assertEqual(widget.locale.code, "de")
                self.assertEqual(widget._cell, CELL_SIZE * 1.5)
            finally:
                widget.close()

    def test_footer_grows_window_when_digital_enabled(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            settings = Settings.load(Path(directory) / "config.json")
            widget = self._make_widget(settings, "en")
            try:
                without_footer = widget.height()
                settings.update(show_digital=True, show_date=True)
                widget.apply_settings()
                self.app.processEvents()
                self.assertGreater(widget.height(), without_footer)
                self.assertFalse(widget.grab().isNull())
            finally:
                widget.close()

    def test_apply_preview_updates_in_memory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            settings = Settings.load(Path(directory) / "config.json")
            widget = self._make_widget(settings, "en")
            try:
                widget._apply_preview({"language": "de", "refresh_ms": 250})
                self.assertEqual(widget.locale.code, "de")
                self.assertEqual(widget._timer.interval(), 250)
            finally:
                widget.close()

    def test_tray_icon_and_creation_are_optional(self) -> None:
        from tray import create_tray, make_icon

        self.assertFalse(make_icon().isNull())
        with tempfile.TemporaryDirectory() as directory:
            settings = Settings.load(Path(directory) / "config.json")
            widget = self._make_widget(settings, "en")
            try:
                tray = create_tray(widget)
                self.assertTrue(tray is None or hasattr(tray, "hide"))
            finally:
                widget.close()

    def test_toggle_optional_switches_away_from_arabic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            settings = Settings.load(Path(directory) / "config.json")
            settings.set("enable_optional_locales", True)
            widget = self._make_widget(settings, "ar")
            try:
                widget._toggle_optional(False)
                self.assertEqual(widget.locale.code, "en")
                self.assertFalse(settings.get("enable_optional_locales"))
            finally:
                widget.close()


if __name__ == "__main__":
    unittest.main()
