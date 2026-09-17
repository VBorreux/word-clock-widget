"""Optional system tray icon giving reliable access to the widget.

On GNOME the tray requires an AppIndicator extension; when no tray is
available the function simply returns ``None`` and the widget keeps working.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QIcon, QPainter, QPen, QPixmap
from PyQt6.QtWidgets import QMenu, QSystemTrayIcon, QWidget

from i18n import tr


def make_icon(size: int = 64) -> QIcon:
    scale = size / 64.0
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    painter.setBrush(QColor("#101014"))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawRoundedRect(
        int(2 * scale),
        int(2 * scale),
        int(size - 4 * scale),
        int(size - 4 * scale),
        14 * scale,
        14 * scale,
    )
    pen = QPen(QColor("#FFFFFF"))
    pen.setWidthF(3 * scale)
    painter.setPen(pen)
    painter.drawEllipse(
        int(16 * scale), int(16 * scale), int(32 * scale), int(32 * scale)
    )
    painter.drawLine(int(32 * scale), int(32 * scale), int(32 * scale), int(19 * scale))
    painter.drawLine(int(32 * scale), int(32 * scale), int(43 * scale), int(38 * scale))
    painter.end()
    return QIcon(pixmap)


def create_tray(widget: QWidget) -> QSystemTrayIcon | None:
    if not QSystemTrayIcon.isSystemTrayAvailable():
        return None

    tray = QSystemTrayIcon(make_icon(), widget)
    tray.setToolTip("Qlocktwo")

    def t(key: str) -> str:
        return tr(getattr(widget, "locale").code, key)

    menu = QMenu()

    toggle_action = menu.addAction(t("tray_show_hide"))
    toggle_action.triggered.connect(
        lambda: widget.setVisible(not widget.isVisible())
    )

    settings_action = menu.addAction(t("menu_settings"))
    settings_action.triggered.connect(widget._open_settings)

    top_action = menu.addAction(t("always_on_top"))
    top_action.setCheckable(True)
    top_action.setChecked(bool(widget.settings.get("always_on_top")))
    top_action.triggered.connect(widget._toggle_on_top)

    menu.addSeparator()
    quit_action = menu.addAction(t("menu_quit"))
    quit_action.triggered.connect(widget._quit)

    tray.setContextMenu(menu)
    tray.activated.connect(
        lambda reason: widget.setVisible(not widget.isVisible())
        if reason == QSystemTrayIcon.ActivationReason.Trigger
        else None
    )
    tray.show()
    return tray
