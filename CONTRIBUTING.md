# Contributing

Thanks for your interest! A few simple rules.

## Attribution (important)

Any contribution, reuse or modified version must keep the credit to the original
author, **Vincent Borreux**, in the credits or documentation (see
[NOTICE](NOTICE) and [LICENSE](LICENSE)).

## Setup

```bash
git clone https://github.com/VBorreux/word-clock-widget.git word-clock
cd word-clock
./run.sh test        # creates the venv, installs PyQt6 and runs the tests
./run.sh             # launches the widget
```

## Before submitting a change

- Run the test suite: `./run.sh test` (no test may fail).
- Follow the existing style (Python 3.10+, `from __future__ import annotations`,
  no extra dependency without justification).
- For a new language: add `locales/xx.py`, register it in
  `locales/__init__.py`, complete `i18n.py` and `flags.py`, then make sure the
  reading-order test passes.
- Describe the change clearly in the pull request.

## Reporting an issue

Mention your distribution, the session type (Wayland/X11), the Python version
and the output of `./run.sh test` if possible.
