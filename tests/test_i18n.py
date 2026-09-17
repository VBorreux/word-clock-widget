"""Tests for the UI translations."""

import unittest

from i18n import TRANSLATIONS, tr
from locales import LANGUAGES


class I18nTests(unittest.TestCase):
    def test_every_locale_has_a_translation_table(self) -> None:
        for code in LANGUAGES:
            self.assertIn(code, TRANSLATIONS, code)

    def test_tables_share_the_same_keys(self) -> None:
        reference = set(TRANSLATIONS["en"])
        for code, table in TRANSLATIONS.items():
            missing = reference - set(table)
            self.assertFalse(missing, f"{code} is missing {sorted(missing)}")

    def test_no_empty_translation(self) -> None:
        for code, table in TRANSLATIONS.items():
            for key, value in table.items():
                self.assertTrue(value.strip(), f"{code}.{key} is empty")

    def test_fallback_to_english(self) -> None:
        self.assertEqual(tr("xx", "menu_quit"), TRANSLATIONS["en"]["menu_quit"])
        self.assertEqual(tr("fr", "menu_quit"), "Quitter")


if __name__ == "__main__":
    unittest.main()
