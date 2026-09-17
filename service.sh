#!/usr/bin/env bash
#
# Manage the Qlocktwo widget as a systemd --user service and/or an XDG
# autostart entry.
#
# Usage:
#   ./service.sh install        # create + enable + start the user service
#   ./service.sh uninstall      # stop + disable + remove the user service
#   ./service.sh start|stop|restart|status
#   ./service.sh autostart      # add a ~/.config/autostart entry
#   ./service.sh no-autostart   # remove it
#   ./service.sh desktop        # add the app to the applications list
#   ./service.sh no-desktop     # remove it
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_NAME="qlocktwo"
CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"
SERVICE_DIR="$CONFIG_HOME/systemd/user"
UNIT_PATH="$SERVICE_DIR/$SERVICE_NAME.service"
AUTOSTART_DIR="$CONFIG_HOME/autostart"
DESKTOP_PATH="$AUTOSTART_DIR/$SERVICE_NAME.desktop"
DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
APPLICATIONS_DIR="$DATA_HOME/applications"
ICON_DIR="$DATA_HOME/icons/hicolor/scalable/apps"
APP_ENTRY="$APPLICATIONS_DIR/$SERVICE_NAME.desktop"
APP_ICON="$ICON_DIR/$SERVICE_NAME.svg"

write_unit() {
    mkdir -p "$SERVICE_DIR"
    cat > "$UNIT_PATH" <<EOF
[Unit]
Description=Qlocktwo desktop clock widget
After=graphical-session.target
PartOf=graphical-session.target

[Service]
Type=simple
WorkingDirectory=$SCRIPT_DIR
Environment=XDG_RUNTIME_DIR=%t
Environment=WAYLAND_DISPLAY=wayland-0
Environment=DBUS_SESSION_BUS_ADDRESS=unix:path=%t/bus
ExecStart=$SCRIPT_DIR/run.sh --no-install
Restart=on-failure
RestartSec=3

[Install]
WantedBy=graphical-session.target
EOF
}

write_desktop() {
    mkdir -p "$AUTOSTART_DIR"
    cat > "$DESKTOP_PATH" <<EOF
[Desktop Entry]
Type=Application
Name=Qlocktwo
Comment=Qlocktwo desktop clock widget
Exec=$SCRIPT_DIR/run.sh
Terminal=false
X-GNOME-Autostart-enabled=true
EOF
}

write_app_entry() {
    mkdir -p "$APPLICATIONS_DIR" "$ICON_DIR"
    cp "$SCRIPT_DIR/assets/qlocktwo.svg" "$APP_ICON"
    cat > "$APP_ENTRY" <<EOF
[Desktop Entry]
Type=Application
Version=1.0
Name=Qlocktwo
GenericName=Word clock
Comment=Qlocktwo-style desktop clock widget
Exec=$SCRIPT_DIR/run.sh --no-install
Icon=$SERVICE_NAME
Terminal=false
Categories=Utility;Clock;
Keywords=clock;time;word;qlocktwo;
StartupWMClass=$SERVICE_NAME
EOF
    chmod 0644 "$APP_ENTRY" "$APP_ICON"
    if command -v update-desktop-database >/dev/null 2>&1; then
        update-desktop-database "$APPLICATIONS_DIR" >/dev/null 2>&1 || true
    fi
    if command -v gtk-update-icon-cache >/dev/null 2>&1; then
        gtk-update-icon-cache -f -t "$DATA_HOME/icons/hicolor" >/dev/null 2>&1 || true
    fi
}

require_systemd() {
    if ! systemctl --user show-environment >/dev/null 2>&1; then
        echo "[service.sh] systemd --user is not available in this session." >&2
        exit 1
    fi
}

case "${1:-}" in
    install)
        require_systemd
        if [ -f "$DESKTOP_PATH" ]; then
            rm -f "$DESKTOP_PATH"
            echo "[service.sh] Removed autostart entry (use one mechanism at a time)."
        fi
        write_unit
        systemctl --user daemon-reload
        systemctl --user enable --now "$SERVICE_NAME.service"
        echo "[service.sh] Service installed and started."
        echo "[service.sh] Control it with: systemctl --user status $SERVICE_NAME"
        ;;
    uninstall)
        require_systemd
        systemctl --user disable --now "$SERVICE_NAME.service" || true
        rm -f "$UNIT_PATH"
        systemctl --user daemon-reload
        echo "[service.sh] Service removed."
        ;;
    start|stop|restart|status)
        require_systemd
        systemctl --user "$1" "$SERVICE_NAME.service"
        ;;
    autostart)
        if [ -f "$UNIT_PATH" ] && systemctl --user show-environment >/dev/null 2>&1; then
            systemctl --user disable --now "$SERVICE_NAME.service" || true
            echo "[service.sh] Disabled the systemd service (use one mechanism at a time)."
        fi
        write_desktop
        echo "[service.sh] Autostart entry written to $DESKTOP_PATH"
        ;;
    no-autostart)
        rm -f "$DESKTOP_PATH"
        echo "[service.sh] Autostart entry removed."
        ;;
    desktop)
        write_app_entry
        echo "[service.sh] Application entry installed: $APP_ENTRY"
        echo "[service.sh] It should now appear in the applications list."
        ;;
    no-desktop)
        rm -f "$APP_ENTRY" "$APP_ICON"
        if command -v update-desktop-database >/dev/null 2>&1; then
            update-desktop-database "$APPLICATIONS_DIR" >/dev/null 2>&1 || true
        fi
        echo "[service.sh] Application entry removed."
        ;;
    *)
        echo "Usage: $0 {install|uninstall|start|stop|restart|status|autostart|no-autostart|desktop|no-desktop}" >&2
        exit 2
        ;;
esac
