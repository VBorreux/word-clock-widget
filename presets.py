"""Colour presets offered in the settings dialog."""

from __future__ import annotations

PRESETS: dict[str, dict] = {
    "Sombre": {
        "active_color": "#FFFFFF",
        "inactive_color": "#222222",
        "background_color": "#101014",
        "glow": True,
        "glow_strength": 1.0,
    },
    "Clair": {
        "active_color": "#111111",
        "inactive_color": "#CFCFCF",
        "background_color": "#F5F5F5",
        "glow": False,
        "glow_strength": 0.0,
    },
    "Néon": {
        "active_color": "#00E5FF",
        "inactive_color": "#20303A",
        "background_color": "#05070A",
        "glow": True,
        "glow_strength": 1.4,
    },
    "Ambre": {
        "active_color": "#FFB000",
        "inactive_color": "#3A2A10",
        "background_color": "#0A0805",
        "glow": True,
        "glow_strength": 1.2,
    },
    "Minimal": {
        "active_color": "#FFFFFF",
        "inactive_color": "#2A2A2A",
        "background_color": "#000000",
        "glow": False,
        "glow_strength": 0.0,
    },
}
