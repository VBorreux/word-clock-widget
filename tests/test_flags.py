"""Tests for the generated flag icons (skipped when PyQt6 is unavailable)."""

import os
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

try:
    from PyQt6.QtWidgets import QApplication

    HAVE_QT = True
except Exception:  # pragma: no cover - depends on the environment
    HAVE_QT = False

from locales import LANGUAGES


@unittest.skipUnless(HAVE_QT, "PyQt6 is not installed")
class FlagTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = QApplication.instance() or QApplication([])

    def test_every_locale_has_a_flag(self) -> None:
        from flags import flag_icon

        for code in LANGUAGES:
            with self.subTest(code=code):
                icon = flag_icon(code)
                self.assertFalse(icon.isNull())
                self.assertFalse(icon.pixmap(22, 15).isNull())


if __name__ == "__main__":
    unittest.main()
