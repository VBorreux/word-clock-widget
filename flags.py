"""Small, hand-drawn flag icons for the language selector.

Flags are drawn with QPainter instead of shipped image files so the project
stays dependency-free and works offline.  They are deliberately simplified.
"""

from __future__ import annotations

import math

from PyQt6.QtCore import QPointF, QRectF, Qt
from PyQt6.QtGui import QColor, QIcon, QPainter, QPainterPath, QPen, QPixmap, QPolygonF

_CACHE: dict[tuple[str, int, int], QIcon] = {}


def flag_icon(code: str, width: int = 22, height: int = 15) -> QIcon:
    key = (code, width, height)
    cached = _CACHE.get(key)
    if cached is not None:
        return cached
    icon = QIcon(_render(code, width, height))
    _CACHE[key] = icon
    return icon


def _render(code: str, width: int, height: int) -> QPixmap:
    pixmap = QPixmap(width, height)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    clip = QPainterPath()
    clip.addRoundedRect(QRectF(0, 0, width, height), 2.5, 2.5)
    painter.setClipPath(clip)
    _draw(painter, code, width, height)
    painter.setClipping(False)
    painter.setPen(QPen(QColor(0, 0, 0, 90), 1))
    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.drawRoundedRect(QRectF(0.5, 0.5, width - 1, height - 1), 2.5, 2.5)
    painter.end()
    return pixmap


def _vstripes(painter: QPainter, w: int, h: int, colors: list[str]) -> None:
    band = w / len(colors)
    for index, color in enumerate(colors):
        painter.fillRect(QRectF(index * band, 0, band + 1, h), QColor(color))


def _hstripes(painter: QPainter, w: int, h: int, colors: list[str]) -> None:
    band = h / len(colors)
    for index, color in enumerate(colors):
        painter.fillRect(QRectF(0, index * band, w, band + 1), QColor(color))


def _star(
    painter: QPainter, cx: float, cy: float, radius: float, color: str, points: int = 5
) -> None:
    polygon = QPolygonF()
    for index in range(points * 2):
        angle = -math.pi / 2 + index * math.pi / points
        r = radius if index % 2 == 0 else radius * 0.4
        polygon.append(QPointF(cx + r * math.cos(angle), cy + r * math.sin(angle)))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor(color))
    painter.drawPolygon(polygon)


def _spain(painter: QPainter, w: int, h: int) -> None:
    painter.fillRect(QRectF(0, 0, w, h), QColor("#AA151B"))
    painter.fillRect(QRectF(0, h * 0.25, w, h * 0.5), QColor("#F1BF00"))


def _portugal(painter: QPainter, w: int, h: int) -> None:
    painter.fillRect(QRectF(0, 0, w * 0.4, h), QColor("#006600"))
    painter.fillRect(QRectF(w * 0.4, 0, w * 0.6, h), QColor("#FF0000"))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor("#FFCC00"))
    painter.drawEllipse(QPointF(w * 0.4, h * 0.5), h * 0.28, h * 0.28)
    painter.setBrush(QColor("#FF0000"))
    painter.drawEllipse(QPointF(w * 0.4, h * 0.5), h * 0.16, h * 0.16)


def _union_jack(painter: QPainter, w: int, h: int) -> None:
    painter.fillRect(QRectF(0, 0, w, h), QColor("#012169"))
    painter.setPen(QPen(QColor("#FFFFFF"), h * 0.22))
    painter.drawLine(QPointF(0, 0), QPointF(w, h))
    painter.drawLine(QPointF(w, 0), QPointF(0, h))
    painter.setPen(QPen(QColor("#C8102E"), h * 0.10))
    painter.drawLine(QPointF(0, 0), QPointF(w, h))
    painter.drawLine(QPointF(w, 0), QPointF(0, h))
    painter.fillRect(QRectF(0, h * 0.35, w, h * 0.3), QColor("#FFFFFF"))
    painter.fillRect(QRectF(w * 0.4, 0, w * 0.2, h), QColor("#FFFFFF"))
    painter.fillRect(QRectF(0, h * 0.425, w, h * 0.15), QColor("#C8102E"))
    painter.fillRect(QRectF(w * 0.45, 0, w * 0.1, h), QColor("#C8102E"))


def _china(painter: QPainter, w: int, h: int) -> None:
    painter.fillRect(QRectF(0, 0, w, h), QColor("#DE2910"))
    _star(painter, w * 0.2, h * 0.32, h * 0.22, "#FFDE00")
    for dx, dy in ((0.4, 0.12), (0.48, 0.3), (0.48, 0.52), (0.4, 0.7)):
        _star(painter, w * dx, h * dy, h * 0.09, "#FFDE00")


def _arabic(painter: QPainter, w: int, h: int) -> None:
    painter.fillRect(QRectF(0, 0, w, h), QColor("#006C35"))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor("#FFFFFF"))
    painter.drawEllipse(QPointF(w * 0.42, h * 0.5), h * 0.26, h * 0.26)
    painter.setBrush(QColor("#006C35"))
    painter.drawEllipse(QPointF(w * 0.5, h * 0.5), h * 0.24, h * 0.24)
    _star(painter, w * 0.62, h * 0.5, h * 0.12, "#FFFFFF")


def _draw(painter: QPainter, code: str, w: int, h: int) -> None:
    if code == "fr":
        _vstripes(painter, w, h, ["#0055A4", "#FFFFFF", "#EF4135"])
    elif code == "it":
        _vstripes(painter, w, h, ["#009246", "#FFFFFF", "#CE2B37"])
    elif code == "de":
        _hstripes(painter, w, h, ["#000000", "#DD0000", "#FFCE00"])
    elif code == "nl":
        _hstripes(painter, w, h, ["#AE1C28", "#FFFFFF", "#21468B"])
    elif code == "ru":
        _hstripes(painter, w, h, ["#FFFFFF", "#0039A6", "#D52B1E"])
    elif code == "es":
        _spain(painter, w, h)
    elif code == "pt":
        _portugal(painter, w, h)
    elif code == "en":
        _union_jack(painter, w, h)
    elif code == "zh":
        _china(painter, w, h)
    elif code == "ar":
        _arabic(painter, w, h)
    else:
        _vstripes(painter, w, h, ["#888888", "#CCCCCC", "#888888"])
