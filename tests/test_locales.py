"""Consistency tests for every language definition."""

import unittest

from locales import (
    DEFAULT_LANGUAGE,
    LANGUAGES,
    get_available_locales,
    get_locale,
    validate_all,
)
from locales.base import LocaleError, minute_dots


class LocaleDataTests(unittest.TestCase):
    def test_validate_all(self) -> None:
        validate_all()

    def test_grid_is_rectangular(self) -> None:
        for code, locale in LANGUAGES.items():
            with self.subTest(code=code):
                self.assertTrue(locale.grid)
                width = len(locale.grid[0])
                self.assertGreaterEqual(width, 2)
                for row in locale.grid:
                    self.assertEqual(len(row), width)
                self.assertEqual(locale.width, width)
                self.assertEqual(locale.height, len(locale.grid))

    def test_word_segments_are_in_bounds(self) -> None:
        for code, locale in LANGUAGES.items():
            with self.subTest(code=code):
                for token, segments in locale.words.items():
                    self.assertTrue(token)
                    self.assertTrue(segments, f"{code}: {token!r} has no segment")
                    for row, col, length in segments:
                        self.assertGreater(length, 0)
                        self.assertGreaterEqual(row, 0)
                        self.assertLess(row, locale.height)
                        self.assertGreaterEqual(col, 0)
                        self.assertLessEqual(col + length, locale.width)

    def test_grid_matches_word_segments(self) -> None:
        for code, locale in LANGUAGES.items():
            with self.subTest(code=code):
                for token, segments in locale.words.items():
                    for row, col, length in segments:
                        found = locale.grid[row][col : col + length]
                        self.assertEqual(
                            found,
                            locale.label(token),
                            f"{code}: grid says {found!r}, token is {token!r}",
                        )

    def test_words_are_lit_in_reading_order(self) -> None:
        for code, locale in LANGUAGES.items():
            with self.subTest(code=code):
                for hour in range(1, 13):
                    for minute in range(0, 60, 5):
                        tokens = locale.build(hour, minute)
                        positions = [
                            min((row, col) for row, col, _ in locale.segments(token))
                            for token in tokens
                        ]
                        self.assertEqual(
                            positions,
                            sorted(positions),
                            f"{code} {hour}:{minute} -> {tokens}",
                        )

    def test_build_is_exhaustive(self) -> None:
        for code, locale in LANGUAGES.items():
            with self.subTest(code=code):
                for hour in range(0, 25):
                    for minute in range(0, 60):
                        tokens = locale.build(hour, minute)
                        self.assertTrue(tokens, f"{code}: empty at {hour}:{minute}")
                        for token in tokens:
                            self.assertIn(token, locale.words)
                            self.assertTrue(locale.segments(token))

    def test_quarter_buckets_light_expected_tokens(self) -> None:
        english = get_locale("en")

        def words(tokens):
            return [english.label(token) for token in tokens]

        self.assertEqual(
            words(english.build(10, 15)), ["IT", "IS", "QUARTER", "PAST", "TEN"]
        )
        self.assertEqual(
            words(english.build(10, 45)), ["IT", "IS", "QUARTER", "TO", "ELEVEN"]
        )
        self.assertEqual(words(english.build(10, 0)), ["IT", "IS", "TEN", "OCLOCK"])

    def test_french_reads_naturally(self) -> None:
        french = get_locale("fr")

        def words(tokens):
            return [french.label(token) for token in tokens]

        self.assertEqual(
            words(french.build(10, 45)),
            ["IL", "EST", "ONZE", "HEURES", "MOINS", "LE", "QUART"],
        )
        self.assertEqual(
            words(french.build(10, 35)),
            ["IL", "EST", "ONZE", "HEURES", "MOINS", "VINGT", "CINQ"],
        )
        self.assertEqual(
            words(french.build(10, 30)),
            ["IL", "EST", "DIX", "HEURES", "ET", "DEMIE"],
        )

    def test_minute_dots(self) -> None:
        for minute in range(60):
            self.assertEqual(minute_dots(minute), minute % 5)


class RegistryTests(unittest.TestCase):
    def test_default_language_is_registered(self) -> None:
        self.assertIn(DEFAULT_LANGUAGE, LANGUAGES)

    def test_ten_languages(self) -> None:
        self.assertEqual(len(LANGUAGES), 10)

    def test_unknown_language_raises(self) -> None:
        with self.assertRaises(LocaleError):
            get_locale("xx")

    def test_optional_locales_hidden_by_default(self) -> None:
        codes = [locale.code for locale in get_available_locales({})]
        self.assertNotIn("ar", codes)
        self.assertIn("en", codes)
        self.assertEqual(len(codes), 9)

    def test_optional_locales_enabled(self) -> None:
        codes = [
            locale.code
            for locale in get_available_locales({"enable_optional_locales": True})
        ]
        self.assertIn("ar", codes)
        self.assertEqual(len(codes), 10)


if __name__ == "__main__":
    unittest.main()
