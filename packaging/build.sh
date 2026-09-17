#!/usr/bin/env bash
#
# Build distributable packages (PyInstaller bundle, .deb, AppImage).
#
# Usage:
#   ./packaging/build.sh pyinstaller   # self-contained bundle
#   ./packaging/build.sh deb           # .deb package
#   ./packaging/build.sh appimage      # .AppImage
#   ./packaging/build.sh all
#   ./packaging/build.sh clean
#
set -euo pipefail

PACKAGING_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$PACKAGING_DIR/.." && pwd)"
BUILD_DIR="$ROOT/build"
DIST_DIR="$BUILD_DIR/dist"
WORK_DIR="$BUILD_DIR/work"
VENV_DIR="$BUILD_DIR/venv"
VERSION="${VERSION:-0.1.0}"
ARCH="${ARCH:-x86_64}"
APPIMAGE_TOOL_URL="https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-$ARCH.AppImage"

ensure_venv() {
    if [ ! -x "$VENV_DIR/bin/python" ]; then
        echo "[build.sh] Creating build virtual environment"
        python3 -m venv "$VENV_DIR"
    fi
    "$VENV_DIR/bin/python" -m pip install --upgrade pip >/dev/null 2>&1 || true
    "$VENV_DIR/bin/python" -m pip install -r "$ROOT/requirements.txt" pyinstaller
}

build_bundle() {
    ensure_venv
    "$VENV_DIR/bin/pyinstaller" --noconfirm --clean \
        --distpath "$DIST_DIR" --workpath "$WORK_DIR" \
        "$PACKAGING_DIR/qlocktwo.spec"
    echo "[build.sh] Bundle: $DIST_DIR/qlocktwo"
}

make_icon_png() {
    "$VENV_DIR/bin/python" "$PACKAGING_DIR/make_icon.py" "$1" >/dev/null
}

cmd_pyinstaller() {
    build_bundle
}

cmd_deb() {
    build_bundle
    local pkgroot="$BUILD_DIR/deb/qlocktwo"
    rm -rf "$pkgroot"
    mkdir -p "$pkgroot/DEBIAN" "$pkgroot/opt" \
        "$pkgroot/usr/bin" "$pkgroot/usr/share/applications" \
        "$pkgroot/usr/share/icons/hicolor/256x256/apps"
    cp -r "$DIST_DIR/qlocktwo" "$pkgroot/opt/qlocktwo"
    cat > "$pkgroot/usr/bin/qlocktwo" <<'EOF'
#!/bin/sh
exec /opt/qlocktwo/qlocktwo "$@"
EOF
    chmod 0755 "$pkgroot/usr/bin/qlocktwo"
    cp "$PACKAGING_DIR/qlocktwo.desktop" "$pkgroot/usr/share/applications/"
    make_icon_png "$pkgroot/usr/share/icons/hicolor/256x256/apps/qlocktwo.png"
    cat > "$pkgroot/DEBIAN/control" <<EOF
Package: qlocktwo
Version: $VERSION
Section: utils
Priority: optional
Architecture: amd64
Maintainer: Vincent <vincent@localhost>
Depends: libc6
Description: Qlocktwo-style desktop clock widget
 A frameless word-clock widget with 10 languages, customisable colours,
 opacity, size and refresh rate.
EOF
    dpkg-deb --build --root-owner-group "$pkgroot" \
        "$BUILD_DIR/qlocktwo_${VERSION}_amd64.deb"
    echo "[build.sh] Package: $BUILD_DIR/qlocktwo_${VERSION}_amd64.deb"
}

cmd_appimage() {
    build_bundle
    local appdir="$BUILD_DIR/AppDir"
    rm -rf "$appdir"
    mkdir -p "$appdir/usr/bin" "$appdir/usr/share/applications" \
        "$appdir/usr/share/icons/hicolor/256x256/apps"
    cp -r "$DIST_DIR/qlocktwo/." "$appdir/usr/bin/"
    cp "$PACKAGING_DIR/qlocktwo.desktop" "$appdir/qlocktwo.desktop"
    cp "$PACKAGING_DIR/qlocktwo.desktop" "$appdir/usr/share/applications/"
    make_icon_png "$appdir/qlocktwo.png"
    cp "$appdir/qlocktwo.png" \
        "$appdir/usr/share/icons/hicolor/256x256/apps/qlocktwo.png"
    cat > "$appdir/AppRun" <<'EOF'
#!/bin/sh
HERE="$(dirname "$(readlink -f "$0")")"
exec "$HERE/usr/bin/qlocktwo" "$@"
EOF
    chmod 0755 "$appdir/AppRun"

    local tool="$BUILD_DIR/tools/appimagetool-$ARCH.AppImage"
    if [ ! -x "$tool" ]; then
        mkdir -p "$BUILD_DIR/tools"
        echo "[build.sh] Downloading appimagetool"
        curl -fsSL -o "$tool" "$APPIMAGE_TOOL_URL"
        chmod +x "$tool"
    fi
    local output="$BUILD_DIR/qlocktwo-${VERSION}-$ARCH.AppImage"
    if ! ARCH="$ARCH" "$tool" --appimage-extract-and-run "$appdir" "$output"; then
        ARCH="$ARCH" "$tool" "$appdir" "$output"
    fi
    echo "[build.sh] AppImage: $output"
}

cmd_clean() {
    rm -rf "$BUILD_DIR"
    echo "[build.sh] Cleaned $BUILD_DIR"
}

case "${1:-all}" in
    pyinstaller | bundle) cmd_pyinstaller ;;
    deb) cmd_deb ;;
    appimage) cmd_appimage ;;
    all) cmd_deb; cmd_appimage ;;
    clean) cmd_clean ;;
    *)
        echo "Usage: $0 {pyinstaller|deb|appimage|all|clean}" >&2
        exit 2
        ;;
esac
