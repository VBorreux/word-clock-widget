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
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_NAME="qlocktwo"
CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"
SERVICE_DIR="$CONFIG_HOME/systemd/user"
UNIT_PATH="$SERVICE_DIR/$SERVICE_NAME.service"
AUTOSTART_DIR="$CONFIG_HOME/autostart"
DESKTOP_PATH="$AUTOSTART_DIR/$SERVICE_NAME.desktop"

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
    *)
        echo "Usage: $0 {install|uninstall|start|stop|restart|status|autostart|no-autostart}" >&2
        exit 2
        ;;
esac
