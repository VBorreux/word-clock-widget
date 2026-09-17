#!/usr/bin/env bash
#
# Create/refresh the isolated virtual environment and run the widget.
#
# Usage:
#   ./run.sh            # launch the clock
#   ./run.sh --settings # launch and open the settings dialog
#   ./run.sh test       # run the unit tests inside the venv
#
# The interpreter is auto-detected: the first one able to build a virtual
# environment (i.e. providing ensurepip) is used.  Override with PYTHON=...
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

find_python() {
    if [ -n "${PYTHON:-}" ]; then
        printf '%s\n' "$PYTHON"
        return 0
    fi
    local candidates=(
        python3.13 python3.12 python3.11 python3.10
        "$HOME/.local/bin/python3.13" "$HOME/.local/bin/python3.12"
        "$HOME/.local/bin/python3.11" "$HOME/.local/bin/python3.10"
        python3
    )
    local candidate
    for candidate in "${candidates[@]}"; do
        if command -v "$candidate" >/dev/null 2>&1 \
            && "$candidate" -c 'import ensurepip' >/dev/null 2>&1; then
            printf '%s\n' "$candidate"
            return 0
        fi
    done
    return 1
}

if ! PYTHON="$(find_python)"; then
    echo "[run.sh] No Python interpreter with venv/ensurepip support found." >&2
    echo "[run.sh] Install python3-venv or set PYTHON=/path/to/python3." >&2
    exit 1
fi
echo "[run.sh] Interpreter: $PYTHON ($("$PYTHON" --version 2>&1))"

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
        echo "[run.sh] .venv uses Python $EXISTING_VERSION, using $VENV_DIR instead"
    fi
fi

if [ -d "$VENV_DIR" ] && [ ! -x "$VENV_DIR/bin/python" ]; then
    echo "[run.sh] Removing incomplete virtual environment $VENV_DIR"
    rm -rf "$VENV_DIR"
fi

if [ ! -d "$VENV_DIR" ]; then
    echo "[run.sh] Creating virtual environment in $VENV_DIR"
    "$PYTHON" -m venv "$VENV_DIR"
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

if ! python -m pip --version >/dev/null 2>&1; then
    echo "[run.sh] pip is missing in $VENV_DIR, recreating it"
    deactivate 2>/dev/null || true
    rm -rf "$VENV_DIR"
    "$PYTHON" -m venv "$VENV_DIR"
    # shellcheck disable=SC1091
    source "$VENV_DIR/bin/activate"
fi

echo "[run.sh] Installing/updating dependencies"
python -m pip install --upgrade pip >/dev/null 2>&1 || true
python -m pip install -r requirements.txt

if [ "${1:-}" = "test" ]; then
    shift
    exec python -m unittest discover -s tests -v "$@"
fi

exec python main.py "$@"
