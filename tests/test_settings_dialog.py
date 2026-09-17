"""Tests for the settings dialog (skipped when PyQt6 is unavailable)."""

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

from settings import Settings


@unittest.skipUnless(HAVE_QT, "PyQt6 is not installed")
class SettingsDialogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = QApplication.instance() or QApplication([])

    def _dialog(self, directory: str):
        from settings_dialog import SettingsDialog

        settings = Settings.load(Path(directory) / "config.json")
        return settings, SettingsDialog(settings)

    def test_defaults_are_loaded_into_the_form(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, dialog = self._dialog(directory)
            try:
                values = dialog.values()
                self.assertEqual(values["language"], "en")
                self.assertEqual(values["active_color"], "#ffffff")
                self.assertEqual(values["inactive_color"], "#222222")
                self.assertEqual(values["background_color"], "#101014")
                self.assertAlmostEqual(values["opacity"], 0.85)
                self.assertEqual(values["refresh_ms"], 1000)
                self.assertFalse(values["enable_optional_locales"])
                self.assertFalse(values["show_digital"])
                self.assertTrue(values["clock_24h"])
                self.assertFalse(values["show_date"])
                self.assertEqual(values["font_family"], "")
                self.assertEqual(values["glow_strength"], 1.0)
                self.assertEqual(values["corner_radius"], 20)
            finally:
                dialog.close()

    def test_optional_toggle_adds_arabic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, dialog = self._dialog(directory)
            try:
                self.assertEqual(dialog.language_combo.findData("ar"), -1)
                dialog.optional_check.setChecked(True)
                self.assertGreaterEqual(dialog.language_combo.findData("ar"), 0)
            finally:
                dialog.close()

    def test_preset_applies_colours_and_emits_preview(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, dialog = self._dialog(directory)
            received = []
            dialog.preview.connect(received.append)
            try:
                dialog._apply_preset("neon")
                self.assertEqual(dialog.active_button.color(), "#00e5ff")
                self.assertTrue(received)
            finally:
                dialog.close()

    def test_preview_emitted_on_control_change(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, dialog = self._dialog(directory)
            received = []
            dialog.preview.connect(received.append)
            try:
                dialog.scale_spin.setValue(1.5)
                self.assertTrue(received)
            finally:
                dialog.close()

    def test_dialog_follows_application_language(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, dialog = self._dialog(directory)
            try:
                dialog.retranslate("fr")
                self.assertEqual(dialog.windowTitle(), "Réglages du widget")
                self.assertEqual(dialog._labels["language"].text(), "Langue")
                dialog.retranslate("de")
                self.assertEqual(dialog.windowTitle(), "Widget-Einstellungen")
            finally:
                dialog.close()

    def test_language_combo_has_flag_icons(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, dialog = self._dialog(directory)
            try:
                self.assertFalse(dialog.language_combo.itemIcon(0).isNull())
            finally:
                dialog.close()

    def test_accept_persists_values(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            settings, dialog = self._dialog(directory)
            try:
                dialog.refresh_spin.setValue(250)
                dialog.active_button._color.setNamedColor("#ff0000")
                dialog.active_button._refresh()
                dialog.accept()
            finally:
                dialog.close()
            self.assertEqual(settings.get("refresh_ms"), 250)
            self.assertEqual(settings.get("active_color"), "#ff0000")


if __name__ == "__main__":
    unittest.main()
