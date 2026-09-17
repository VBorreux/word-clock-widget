"""Optional system tray icon giving reliable access to the widget.

On GNOME the tray requires an AppIndicator extension; when no tray is
available the function simply returns ``None`` and the widget keeps working.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QIcon, QPainter, QPen, QPixmap
from PyQt6.QtWidgets import QMenu, QSystemTrayIcon, QWidget


def make_icon() -> QIcon:
    size = 64
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    painter.setBrush(QColor("#101014"))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawRoundedRect(2, 2, size - 4, size - 4, 14, 14)
    pen = QPen(QColor("#FFFFFF"))
    pen.setWidth(3)
    painter.setPen(pen)
    painter.drawEllipse(16, 16, 32, 32)
    painter.drawLine(32, 32, 32, 19)
    painter.drawLine(32, 32, 43, 38)
    painter.end()
    return QIcon(pixmap)


def create_tray(widget: QWidget) -> QSystemTrayIcon | None:
    if not QSystemTrayIcon.isSystemTrayAvailable():
        return None

    tray = QSystemTrayIcon(make_icon(), widget)
    tray.setToolTip("Qlocktwo")

    menu = QMenu()

    toggle_action = menu.addAction("Afficher / Masquer")
    toggle_action.triggered.connect(
        lambda: widget.setVisible(not widget.isVisible())
    )

    settings_action = menu.addAction("Réglages…")
    settings_action.triggered.connect(widget._open_settings)

    top_action = menu.addAction("Toujours au-dessus")
    top_action.setCheckable(True)
    top_action.setChecked(bool(widget.settings.get("always_on_top")))
    top_action.triggered.connect(widget._toggle_on_top)

    menu.addSeparator()
    quit_action = menu.addAction("Quitter")
    quit_action.triggered.connect(widget._quit)

    tray.setContextMenu(menu)
    tray.activated.connect(
        lambda reason: widget.setVisible(not widget.isVisible())
        if reason == QSystemTrayIcon.ActivationReason.Trigger
        else None
    )
    tray.show()
    return tray
