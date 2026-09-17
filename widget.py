"""Frameless, draggable Qlocktwo-style desktop clock widget."""

from __future__ import annotations

import datetime as _dt

from PyQt6.QtCore import QPoint, QPointF, QRect, QRectF, Qt, QTimer
from PyQt6.QtGui import (
    QAction,
    QActionGroup,
    QColor,
    QFont,
    QFontDatabase,
    QKeySequence,
    QPainter,
    QShortcut,
)
from PyQt6.QtWidgets import QApplication, QColorDialog, QDialog, QMenu, QWidget

from flags import flag_icon
from i18n import tr
from locales import (
    DEFAULT_LANGUAGE,
    Locale,
    get_available_locales,
    get_locale,
    minute_dots,
)
from settings import Settings
from settings_dialog import SettingsDialog

CELL_SIZE = 30.0
BOARD_MARGIN = 22.0
CORNER_RADIUS = 20.0

_FONT_CANDIDATES: dict[str, list[str]] = {
    "zh": [
        "Noto Sans CJK SC",
        "Noto Sans SC",
        "Source Han Sans SC",
        "WenQuanYi Micro Hei",
        "AR PL UMing CN",
    ],
    "ar": ["Noto Naskh Arabic", "Noto Sans Arabic", "DejaVu Sans", "FreeSerif"],
    "ru": ["DejaVu Sans Mono", "Liberation Mono", "Noto Sans Mono"],
}
_DEFAULT_FONTS = [
    "DejaVu Sans Mono",
    "Liberation Mono",
    "Noto Sans Mono",
    "Ubuntu Mono",
    "FreeMono",
    "monospace",
]


def _pick_font(locale: Locale) -> str:
    try:
        available = set(QFontDatabase.families())
    except Exception:  # pragma: no cover - no QApplication / no font backend
        available = set()
    candidates = _FONT_CANDIDATES.get(locale.code, []) + _DEFAULT_FONTS
    for name in candidates:
        if name in available:
            return name
    return candidates[-1]


class ClockWidget(QWidget):
    def __init__(self, settings: Settings, locale: Locale) -> None:
        super().__init__(None)
        self.settings = settings
        self.locale = locale
        self._font_family = _pick_font(locale)
        self._refresh_font()
        self._drag_offset: QPoint | None = None
        self._system_move = False
        self._active_cells: set[tuple[int, int]] = set()
        self._active_segments: list[tuple[str, int, int, int]] = []
        self._cell = CELL_SIZE

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        for sequence in ("Ctrl+Q", "Esc"):
            QShortcut(QKeySequence(sequence), self, activated=self._quit)
        QShortcut(QKeySequence("Ctrl+,"), self, activated=self._open_settings)

        self._apply_window_flags()
        self._refresh_active()
        self._resize_to_board()
        self._restore_position()

        self._last_minute = _dt.datetime.now().minute
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._apply_refresh_rate()
        self._timer.start()

    # ------------------------------------------------------------------ window
    def _apply_window_flags(self) -> None:
        # A regular (frameless) window so that the compositor grants it focus:
        # this is required for dragging, the context menu and keyboard quit.
        flags = Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window
        if self.settings.get("always_on_top"):
            flags |= Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags)

    def _footer_height(self) -> float:
        if not (self.settings.get("show_digital") or self.settings.get("show_date")):
            return 0.0
        return self._cell * 1.1

    def _resize_to_board(self) -> None:
        scale = float(self.settings.get("scale") or 1.0)
        self._cell = CELL_SIZE * scale
        width = int(self.locale.width * self._cell + 2 * BOARD_MARGIN)
        height = int(
            self.locale.height * self._cell
            + 2 * BOARD_MARGIN
            + self._footer_height()
        )
        self.setFixedSize(width, height)

    def _apply_refresh_rate(self) -> None:
        try:
            interval = int(self.settings.get("refresh_ms"))
        except (TypeError, ValueError):
            interval = 1000
        self._timer.setInterval(max(100, min(5000, interval)))

    def _restore_position(self) -> None:
        position = self.settings.get("position")
        if self._position_is_visible(position):
            self.move(int(position[0]), int(position[1]))
            return
        self._center_on_screen()

    def _position_is_visible(self, position) -> bool:
        if not (
            isinstance(position, (list, tuple))
            and len(position) == 2
            and all(isinstance(value, (int, float)) for value in position)
        ):
            return False
        x, y = int(position[0]), int(position[1])
        rect = QRect(x, y, self.width(), self.height())
        return any(
            screen.availableGeometry().intersects(rect)
            for screen in QApplication.screens()
        )

    def _center_on_screen(self) -> None:
        screen = QApplication.primaryScreen()
        if screen is None:
            return
        geometry = screen.availableGeometry()
        self.move(
            geometry.x() + (geometry.width() - self.width()) // 2,
            geometry.y() + (geometry.height() - self.height()) // 2,
        )

    def _save_position(self) -> None:
        point = self.pos()
        if self._position_is_visible((point.x(), point.y())):
            self.settings.set("position", [point.x(), point.y()])

    # -------------------------------------------------------------------- time
    def _refresh_active(self) -> None:
        now = _dt.datetime.now()
        cells: set[tuple[int, int]] = set()
        segments: list[tuple[str, int, int, int]] = []
        for token in self.locale.build(now.hour, now.minute):
            for row, col, length in self.locale.segments(token):
                segments.append((token, row, col, length))
                for offset in range(length):
                    cells.add((row, col + offset))
        self._active_cells = cells
        self._active_segments = segments

    def _tick(self) -> None:
        now = _dt.datetime.now()
        self._last_minute = now.minute
        self._refresh_active()
        self.update()

    def _quit(self) -> None:
        application = QApplication.instance()
        if application is not None:
            application.quit()

    # ------------------------------------------------------------------- paint
    def paintEvent(self, event) -> None:  # noqa: N802 (Qt naming)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)

        opacity = float(self.settings.get("opacity") or 1.0)
        background = self._color_setting("background_color", "#101014")
        background.setAlphaF(max(0.05, min(1.0, opacity)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(background)
        try:
            radius = max(0.0, min(80.0, float(self.settings.get("corner_radius"))))
        except (TypeError, ValueError):
            radius = CORNER_RADIUS
        painter.drawRoundedRect(
            QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5),
            radius,
            radius,
        )

        cell = self._cell
        font = QFont(self._font_family)
        font.setPixelSize(max(8, int(cell * 0.6 * self._font_scale())))
        font.setWeight(QFont.Weight.Medium)
        painter.setFont(font)

        inactive = self._color_setting("inactive_color", "#222222")
        active = self._color_setting("active_color", "#FFFFFF")
        glow = bool(self.settings.get("glow"))
        strength = self._glow_strength()
        covered: set[tuple[int, int]] = set()

        if self.locale.rtl:
            for token, row, col, length in self._active_segments:
                rect = QRectF(
                    BOARD_MARGIN + col * cell,
                    BOARD_MARGIN + row * cell,
                    length * cell,
                    cell,
                )
                self._draw_text(
                    painter, rect, self.locale.label(token), active, glow, strength
                )
                for offset in range(length):
                    covered.add((row, col + offset))

        for row in range(self.locale.height):
            for col in range(self.locale.width):
                if (row, col) in covered:
                    continue
                rect = QRectF(
                    BOARD_MARGIN + col * cell,
                    BOARD_MARGIN + row * cell,
                    cell,
                    cell,
                )
                if (row, col) in self._active_cells:
                    self._draw_text(
                        painter,
                        rect,
                        self.locale.grid[row][col],
                        active,
                        glow,
                        strength,
                    )
                else:
                    painter.setPen(inactive)
                    painter.drawText(
                        rect,
                        Qt.AlignmentFlag.AlignCenter,
                        self.locale.grid[row][col],
                    )

        if self.settings.get("show_dots"):
            self._draw_dots(painter, cell)

        self._draw_footer(painter, active)

        painter.end()

    def _draw_footer(self, painter: QPainter, color: QColor) -> None:
        show_digital = bool(self.settings.get("show_digital"))
        show_date = bool(self.settings.get("show_date"))
        if not (show_digital or show_date):
            return
        now = _dt.datetime.now()
        lines: list[str] = []
        if show_digital:
            if self.settings.get("clock_24h"):
                lines.append(f"{now.hour:02d}:{now.minute:02d}")
            else:
                hour12 = now.hour % 12 or 12
                suffix = "AM" if now.hour < 12 else "PM"
                lines.append(f"{hour12}:{now.minute:02d} {suffix}")
        if show_date:
            lines.append(now.strftime("%a %d %b %Y"))

        board_bottom = BOARD_MARGIN + self.locale.height * self._cell
        footer = QRectF(
            0,
            board_bottom,
            self.width(),
            self.height() - board_bottom,
        )
        font = QFont(self._font_family)
        font.setPixelSize(max(8, int(self._cell * 0.42)))
        painter.setFont(font)
        painter.setPen(color)
        painter.drawText(
            footer,
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter,
            "\n".join(lines),
        )

    def _color_setting(self, key: str, fallback: str) -> QColor:
        color = QColor(str(self.settings.get(key)))
        if not color.isValid():
            color = QColor(fallback)
        return color

    def _refresh_font(self) -> None:
        configured = str(self.settings.get("font_family") or "").strip()
        self._font_family = configured or _pick_font(self.locale)

    def _font_scale(self) -> float:
        try:
            return max(0.4, min(2.0, float(self.settings.get("font_scale"))))
        except (TypeError, ValueError):
            return 1.0

    def _glow_strength(self) -> float:
        try:
            return max(0.0, min(3.0, float(self.settings.get("glow_strength"))))
        except (TypeError, ValueError):
            return 1.0

    def _draw_text(
        self,
        painter: QPainter,
        rect: QRectF,
        text: str,
        color: QColor,
        glow: bool,
        strength: float = 1.0,
    ) -> None:
        if glow and strength > 0:
            halo = QColor(color)
            halo.setAlpha(max(0, min(255, int(70 * strength))))
            painter.setPen(halo)
            offsets = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1)]
            if strength >= 1.6:
                offsets += [(-2, 0), (2, 0), (0, -2), (0, 2)]
            for dx, dy in offsets:
                painter.drawText(
                    rect.translated(dx, dy), Qt.AlignmentFlag.AlignCenter, text
                )
        painter.setPen(color)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, text)

    def _draw_dots(self, painter: QPainter, cell: float) -> None:
        count = minute_dots(_dt.datetime.now().minute)
        corners = ((0, 0), (1, 0), (1, 1), (0, 1))
        radius = max(2.0, cell * 0.09)
        board_height = self.locale.height * cell + 2 * BOARD_MARGIN
        painter.setPen(Qt.PenStyle.NoPen)
        for index, (rx, ry) in enumerate(corners):
            cx = BOARD_MARGIN / 2 + rx * (self.width() - BOARD_MARGIN)
            cy = BOARD_MARGIN / 2 + ry * (board_height - BOARD_MARGIN)
            painter.setBrush(QColor(255, 255, 255) if index < count else QColor(60, 60, 60))
            painter.drawEllipse(QPointF(cx, cy), radius, radius)

    # ------------------------------------------------------------------ events
    def mousePressEvent(self, event) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton:
            handle = self.windowHandle()
            if handle is not None and handle.startSystemMove():
                # Wayland (and some compositors) only allow the compositor to
                # move a window; startSystemMove hands the drag over to it.
                self._system_move = True
                event.accept()
                return
            self._drag_offset = (
                event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            )
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:  # noqa: N802
        if (
            self._drag_offset is not None
            and event.buttons() & Qt.MouseButton.LeftButton
        ):
            self.move(event.globalPosition().toPoint() - self._drag_offset)
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if self._system_move or self._drag_offset is not None:
            self._system_move = False
            self._drag_offset = None
            self._save_position()
            event.accept()
        else:
            super().mouseReleaseEvent(event)

    # ------------------------------------------------------------- context menu
    def contextMenuEvent(self, event) -> None:  # noqa: N802
        menu = self._build_menu()
        menu.exec(event.globalPos())
        event.accept()

    def _build_menu(self) -> QMenu:
        def t(key: str) -> str:
            return tr(self.locale.code, key)

        menu = QMenu(self)

        settings_action = menu.addAction(t("menu_settings"))
        settings_action.triggered.connect(self._open_settings)

        menu.addSeparator()

        language_menu = menu.addMenu(t("menu_language"))
        language_group = QActionGroup(language_menu)
        language_group.setExclusive(True)
        for locale in get_available_locales(self.settings.data):
            action = language_menu.addAction(flag_icon(locale.code), locale.name)
            action.setCheckable(True)
            action.setChecked(locale.code == self.locale.code)
            language_group.addAction(action)
            action.triggered.connect(
                lambda checked=False, code=locale.code: self._set_language(code)
            )

        opacity_menu = menu.addMenu(t("menu_opacity"))
        for value in (0.3, 0.5, 0.7, 0.85, 1.0):
            action = opacity_menu.addAction(f"{int(value * 100)} %")
            action.setCheckable(True)
            action.setChecked(
                abs(float(self.settings.get("opacity")) - value) < 1e-6
            )
            action.triggered.connect(
                lambda checked=False, v=value: self._set_opacity(v)
            )

        size_menu = menu.addMenu(t("menu_size"))
        for value in (0.7, 0.85, 1.0, 1.2, 1.5, 2.0):
            action = size_menu.addAction(f"×{value:g}")
            action.setCheckable(True)
            action.setChecked(abs(float(self.settings.get("scale")) - value) < 1e-6)
            action.triggered.connect(lambda checked=False, v=value: self._set_scale(v))

        colors_menu = menu.addMenu(t("menu_colors"))
        colors_menu.addAction(t("colors_active")).triggered.connect(
            lambda: self._pick_color("active_color")
        )
        colors_menu.addAction(t("colors_inactive")).triggered.connect(
            lambda: self._pick_color("inactive_color")
        )
        colors_menu.addAction(t("colors_background")).triggered.connect(
            lambda: self._pick_color("background_color")
        )

        menu.addSeparator()

        top_action = menu.addAction(t("always_on_top"))
        top_action.setCheckable(True)
        top_action.setChecked(bool(self.settings.get("always_on_top")))
        top_action.triggered.connect(self._toggle_on_top)

        optional_action = menu.addAction(t("optional_locales"))
        optional_action.setCheckable(True)
        optional_action.setChecked(bool(self.settings.get("enable_optional_locales")))
        optional_action.triggered.connect(self._toggle_optional)

        menu.addSeparator()
        quit_action = menu.addAction(t("menu_quit"))
        quit_action.triggered.connect(self._quit)

        return menu

    # ------------------------------------------------------------ menu handlers
    def _set_language(self, code: str) -> None:
        self.locale = get_locale(code)
        self._refresh_font()
        self.settings.set("language", code)
        self._refresh_active()
        self._resize_to_board()
        self.update()

    def _set_opacity(self, value: float) -> None:
        self.settings.set("opacity", value)
        self.update()

    def _set_scale(self, value: float) -> None:
        self.settings.set("scale", value)
        self._resize_to_board()
        self.update()

    def _toggle_on_top(self, checked: bool) -> None:
        self.settings.set("always_on_top", checked)
        self._apply_window_flags()
        self.show()

    def _toggle_optional(self, checked: bool) -> None:
        self.settings.set("enable_optional_locales", checked)
        if not checked and self.locale.optional:
            self._set_language(DEFAULT_LANGUAGE)

    def _open_settings(self) -> None:
        snapshot = self.settings.data
        dialog = SettingsDialog(self.settings, self)
        dialog.preview.connect(self._apply_preview)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.settings.merge(dialog.values(), save=True)
        else:
            self.settings.merge(snapshot, save=False)
        self.apply_settings()

    def _apply_preview(self, values: dict) -> None:
        self.settings.merge(values, save=False)
        self.apply_settings()

    def _pick_color(self, key: str) -> None:
        current = self._color_setting(key, "#FFFFFF")
        chosen = QColorDialog.getColor(
            current, self, tr(self.locale.code, "choose_color")
        )
        if chosen.isValid():
            self.settings.set(key, chosen.name())
            self.update()

    def apply_settings(self) -> None:
        code = str(self.settings.get("language"))
        if code != self.locale.code:
            try:
                self.locale = get_locale(code)
            except Exception:
                self.locale = get_locale(DEFAULT_LANGUAGE)
            self._refresh_font()
        self._apply_window_flags()
        self._apply_refresh_rate()
        self._refresh_active()
        self._resize_to_board()
        self.show()
        self.update()
