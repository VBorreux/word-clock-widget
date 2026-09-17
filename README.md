# Word Clock — a Qlocktwo-style textual clock

A Linux desktop widget that spells the current time in words on a letter grid:
the words for the current time light up, the others stay dim. Inspired by the
**Qlocktwo** clock by Biegert & Funk (this project is not affiliated — see the
*Trademark* section).

**Languages:** French, English, German, Spanish, Italian, Dutch, Portuguese,
Russian, Chinese, Arabic (optional).

---

## Preview

Example at 10:15 in French:

```
I L E S T Q U A T R E
D O U Z E T R O I S A
O N Z E C I N Q B C D
S E P T H U I T E F G
N E U F D E U X U N E
S I X D I X H I J K L
H E U R E S H E U R E
M O I N S E T L E M N
Q U A R T D E M I E O
V I N G T C I N Q P Q
D I X R S T U V W X Y
```

The letters `IL EST DIX HEURES ET QUART` are lit; they read in order, top to
bottom. Four dots in the corners show the exact minutes (1 to 4 past the
five-minute step).

## Features

- Frameless, translucent, rounded-corner window, draggable with the mouse.
- Illumination with a configurable glow effect.
- 10 languages, with grids laid out so every phrase reads naturally.
- Interface and menus translated into the application language.
- Language selector with flags (drawn, no external images).
- Right-click menu: settings, language, opacity, size, colours, always on top,
  quit.
- Full settings dialog: colours, background, opacity, size, font, glow
  strength, corner radius, refresh rate, digital time (12/24 h) and date,
  minute dots.
- Live preview and preset themes (Dark, Light, Neon, Amber, Minimal).
- System-tray icon (menu and show/hide).
- Per-machine configuration in `~/.config/qlocktwo/`.
- `systemd --user` service and XDG autostart entry.
- Packaging: PyInstaller bundle, `.deb`, AppImage.
- No dependency other than PyQt6, fully installed inside a `venv`.

## Requirements

- Linux with a graphical session (Wayland or X11).
- Python 3.10+ with `venv` support (`python3-venv`).
- PyQt6 (installed automatically into `.venv`).

## Quick start

```bash
git clone https://github.com/VBorreux/word-clock-widget.git word-clock
cd word-clock
./run.sh
```

`run.sh` finds a Python interpreter able to create a virtual environment,
creates `.venv` if needed, installs the dependencies and launches the widget.
Nothing is installed on the host system.

Variants:

```bash
./run.sh --settings   # open the settings dialog directly
./run.sh test         # run the test suite inside the venv
./run.sh --no-install # launch without reinstalling dependencies
```

To pick the interpreter: `PYTHON=/usr/bin/python3.12 ./run.sh`.

## Usage

- **Move**: hold the left mouse button (drag).
- **Menu**: right-click → Settings, Language, Opacity, Size, Colours, Always on
  top, Quit.
- **Shortcuts**: `Ctrl+,` (settings), `Ctrl+Q` / `Escape` (quit).
- The position, language and every setting are saved in
  `~/.config/qlocktwo/config.json` (override with `QLOCKTWO_CONFIG`).

## Configuration

| Key | Default | Description |
| --- | --- | --- |
| `language` | `en` | Language code (`fr`, `en`, `de`, `es`, `it`, `nl`, `pt`, `ru`, `zh`, `ar`) |
| `active_color` / `inactive_color` | `#FFFFFF` / `#222222` | Letter colours |
| `background_color` | `#101014` | Background colour |
| `opacity` | `0.85` | Background opacity (0.05–1.0) |
| `scale` | `1.0` | Grid size |
| `glow` / `glow_strength` | `true` / `1.0` | Glow effect and strength |
| `font_family` / `font_scale` | `""` / `1.0` | Font (`""` = auto) and text size |
| `corner_radius` | `20` | Corner radius |
| `show_dots` | `true` | Minute dots |
| `show_digital` / `clock_24h` / `show_date` | `false` / `true` / `false` | Digital time and date |
| `refresh_ms` | `1000` | Refresh interval |
| `always_on_top` | `false` | Always on top |
| `enable_optional_locales` | `false` | Show Arabic |
| `show_tray` | `true` | System-tray icon |

## Languages

Grids are defined in `locales/`. Each module exposes a grid, a word-to-segments
mapping and a `build(hour, minute)` function. A test guarantees the words always
light up in reading order.

To add a language: create `locales/xx.py` following an existing language, then
register it in `locales/__init__.py`. Add the UI translation in `i18n.py` and a
flag in `flags.py`.

## systemd service and autostart

```bash
./service.sh install     # systemd --user service (starts with the session)
./service.sh uninstall
./service.sh start|stop|restart|status
./service.sh autostart   # alternative: XDG autostart entry
./service.sh no-autostart
```

Service control: `systemctl --user status qlocktwo`.

## Packaging

```bash
./packaging/build.sh pyinstaller   # standalone bundle (build/dist/qlocktwo)
./packaging/build.sh deb           # .deb package
./packaging/build.sh appimage      # AppImage
./packaging/build.sh all
./packaging/build.sh clean
```

Artifacts are produced in `build/` (ignored by git).

## Project structure

```
locales/           grids and time logic (10 languages)
flags.py           flags drawn with Qt
i18n.py            interface translations
presets.py         colour themes
settings.py        configuration (XDG) + defaults
settings_dialog.py settings window
widget.py          window and grid rendering
tray.py            system-tray icon
main.py            entry point
run.sh             virtual environment + launch
service.sh         systemd --user service / autostart
packaging/         PyInstaller, .deb, AppImage
tests/             unit tests (unittest)
```

## Tests

```bash
./run.sh test
# or, inside a venv with PyQt6:
python -m unittest discover -s tests -v
```

The tests cover grids and reading order, configuration, i18n, flags and the
offscreen rendering of the widget.

## Credits and license

- **Author: Vincent Borreux** — © 2026.
- Released under the **MIT** license (see [LICENSE](LICENSE)).
- Any use, copy, modification or redistribution, in whole or in part, must
  **keep the credit to the original author** and credit **Vincent Borreux** in
  the project's credits or documentation. Modified versions must also state that
  they are based on this original work (see [NOTICE](NOTICE)).

Please credit "Word Clock by Vincent Borreux" when you reuse or modify this
code.

## Trademark

"Qlocktwo" / "QlockTwo" is a trademark of its owner (Biegert & Funk). This
project is an independent, non-affiliated tribute and is not endorsed by the
trademark owner. It uses none of the original clock's assets.
