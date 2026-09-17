"""Tests for configuration loading and persistence."""

import json
import os
import tempfile
import unittest
from pathlib import Path

import settings as settings_module
from settings import DEFAULTS, Settings, default_path


class _Env:
    def __init__(self, **values: str) -> None:
        self.values = values
        self.saved: dict[str, str | None] = {}

    def __enter__(self):
        for key, value in self.values.items():
            self.saved[key] = os.environ.get(key)
            os.environ[key] = value
        return self

    def __exit__(self, *exc):
        for key, value in self.saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


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


class ConfigLocationTests(unittest.TestCase):
    def test_default_path_uses_xdg_config_home(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with _Env(XDG_CONFIG_HOME=directory, QLOCKTWO_CONFIG=""):
                os.environ.pop("QLOCKTWO_CONFIG", None)
                self.assertEqual(
                    default_path(), Path(directory) / "qlocktwo" / "config.json"
                )

    def test_qlocktwo_config_overrides_location(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "custom.json"
            with _Env(QLOCKTWO_CONFIG=str(target)):
                self.assertEqual(default_path(), target)

    def test_load_migrates_legacy_config(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            legacy = Path(directory) / "legacy.json"
            legacy.write_text(json.dumps({"language": "de"}), encoding="utf-8")
            original = settings_module.legacy_path
            settings_module.legacy_path = lambda: legacy
            try:
                with _Env(XDG_CONFIG_HOME=directory):
                    os.environ.pop("QLOCKTWO_CONFIG", None)
                    settings = Settings.load()
                    self.assertEqual(settings.get("language"), "de")
                    migrated = Path(directory) / "qlocktwo" / "config.json"
                    self.assertTrue(migrated.exists())
                    self.assertEqual(
                        json.loads(migrated.read_text(encoding="utf-8"))["language"],
                        "de",
                    )
            finally:
                settings_module.legacy_path = original


if __name__ == "__main__":
    unittest.main()
