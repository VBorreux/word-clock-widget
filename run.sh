#!/usr/bin/env bash
#
# Create/refresh the isolated virtual environment and run the widget.
#
# Usage:
#   ./run.sh          # launch the clock
#   ./run.sh test     # run the unit tests inside the venv
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PYTHON="${PYTHON:-python3}"
PY_VERSION="$("$PYTHON" -c 'import sys; print("%d.%d" % sys.version_info[:2])')"

# A virtual environment is bound to the interpreter that created it.  When the
# project lives on a shared mount used by machines with different Python
# versions, fall back to a per-version directory instead of clobbering the
# existing one.
VENV_DIR="$SCRIPT_DIR/.venv"
if [ -f "$VENV_DIR/pyvenv.cfg" ]; then
    EXISTING_VERSION="$(sed -n 's/^version = //p' "$VENV_DIR/pyvenv.cfg" | cut -d. -f1,2)"
    if [ -n "$EXISTING_VERSION" ] && [ "$EXISTING_VERSION" != "$PY_VERSION" ]; then
        VENV_DIR="$SCRIPT_DIR/.venv-$PY_VERSION"
        echo "[run.sh] .venv uses Python $EXISTING_VERSION, current is $PY_VERSION"
        echo "[run.sh] Using $VENV_DIR instead"
    fi
fi

if [ ! -d "$VENV_DIR" ]; then
    echo "[run.sh] Creating virtual environment in $VENV_DIR"
    "$PYTHON" -m venv "$VENV_DIR"
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

echo "[run.sh] Installing dependencies"
python -m pip install --upgrade pip >/dev/null
python -m pip install -r requirements.txt

if [ "${1:-}" = "test" ]; then
    shift
    exec python -m unittest discover -s tests -v "$@"
fi

exec python main.py "$@"
