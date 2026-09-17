"""Tests for configuration loading and persistence."""

import json
import tempfile
import unittest
from pathlib import Path

from settings import DEFAULTS, Settings


class SettingsTests(unittest.TestCase):
    def test_defaults_when_file_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            settings = Settings.load(Path(directory) / "config.json")
            for key, value in DEFAULTS.items():
                self.assertEqual(settings.get(key), value)

    def test_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            settings = Settings.load(path)
            settings.set("language", "de")
            settings.set("scale", 1.5)
            settings.set("position", [12, 34])

            reloaded = Settings.load(path)
            self.assertEqual(reloaded.get("language"), "de")
            self.assertEqual(reloaded.get("scale"), 1.5)
            self.assertEqual(reloaded.get("position"), [12, 34])

    def test_corrupt_file_falls_back_to_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            path.write_text("{not valid json", encoding="utf-8")
            settings = Settings.load(path)
            self.assertEqual(settings.get("language"), DEFAULTS["language"])

    def test_update_writes_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            settings = Settings.load(path)
            settings.update(language="fr", opacity=0.5)
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(payload["language"], "fr")
            self.assertEqual(payload["opacity"], 0.5)


if __name__ == "__main__":
    unittest.main()
