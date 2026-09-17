"""Settings dialog: language, colours, opacity, size, refresh rate, ...

The whole interface follows the selected clock language.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import (
    QCheckBox,
    QColorDialog,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFontComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from flags import flag_icon
from i18n import tr
from locales import DEFAULT_LANGUAGE, get_available_locales
from presets import PRESET_LABEL_KEYS, PRESETS
from settings import DEFAULTS, Settings

_REFRESH_MIN = 100
_REFRESH_MAX = 5000


class ColorButton(QPushButton):
    """A button showing the current colour and opening a colour picker."""

    changed = pyqtSignal()

    def __init__(
        self, color: str, title: str = "Choose a colour", parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self._color = QColor(color)
        if not self._color.isValid():
            self._color = QColor("#000000")
        self._title = title
        self.setMinimumWidth(120)
        self.clicked.connect(self._choose)
        self._refresh()

    def set_title(self, title: str) -> None:
        self._title = title

    def _refresh(self) -> None:
        name = self._color.name().upper()
        text_color = "#000000" if self._color.lightness() > 128 else "#FFFFFF"
        self.setText(name)
        self.setStyleSheet(
            f"QPushButton {{ background-color: {self._color.name()}; "
            f"color: {text_color}; border: 1px solid #555; padding: 4px; }}"
        )

    def set_color(self, color: str) -> None:
        self._color = QColor(color)
        if not self._color.isValid():
            self._color = QColor("#000000")
        self._refresh()

    def _choose(self) -> None:
        chosen = QColorDialog.getColor(self._color, self, self._title)
        if chosen.isValid():
            self._color = chosen
            self._refresh()
            self.changed.emit()

    def color(self) -> str:
        return self._color.name()


class SettingsDialog(QDialog):
    preview = pyqtSignal(dict)

    def __init__(self, settings: Settings, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.settings = settings
        self._labels: dict[str, QLabel] = {}
        self._preset_buttons: dict[str, QPushButton] = {}
        self.setModal(True)

        form = QFormLayout()

        self.language_combo = QComboBox()
        self._add_row(form, "language", self.language_combo)

        self.optional_check = QCheckBox()
        self.optional_check.setChecked(bool(settings.get("enable_optional_locales")))
        self.optional_check.toggled.connect(self._rebuild_languages)
        form.addRow("", self.optional_check)

        self.active_button = ColorButton(str(settings.get("active_color")))
        self._add_row(form, "active_color", self.active_button)

        self.inactive_button = ColorButton(str(settings.get("inactive_color")))
        self._add_row(form, "inactive_color", self.inactive_button)

        self.background_button = ColorButton(str(settings.get("background_color")))
        self._add_row(form, "background_color", self.background_button)

        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setRange(5, 100)
        self.opacity_slider.setValue(int(round(float(settings.get("opacity")) * 100)))
        self.opacity_value = QSpinBox()
        self.opacity_value.setRange(5, 100)
        self.opacity_value.setSuffix(" %")
        self.opacity_value.setValue(self.opacity_slider.value())
        self.opacity_slider.valueChanged.connect(self.opacity_value.setValue)
        self.opacity_value.valueChanged.connect(self.opacity_slider.setValue)
        opacity_row = QHBoxLayout()
        opacity_row.addWidget(self.opacity_slider)
        opacity_row.addWidget(self.opacity_value)
        opacity_widget = QWidget()
        opacity_widget.setLayout(opacity_row)
        self._add_row(form, "background_opacity", opacity_widget)

        self.scale_spin = QDoubleSpinBox()
        self.scale_spin.setRange(0.5, 3.0)
        self.scale_spin.setSingleStep(0.05)
        self.scale_spin.setDecimals(2)
        self.scale_spin.setValue(float(settings.get("scale")))
        self._add_row(form, "size", self.scale_spin)

        self.refresh_spin = QSpinBox()
        self.refresh_spin.setRange(_REFRESH_MIN, _REFRESH_MAX)
        self.refresh_spin.setSingleStep(100)
        self.refresh_spin.setSuffix(" ms")
        self.refresh_spin.setValue(int(settings.get("refresh_ms")))
        self._add_row(form, "refresh_rate", self.refresh_spin)

        self.glow_check = QCheckBox()
        self.glow_check.setChecked(bool(settings.get("glow")))
        form.addRow("", self.glow_check)

        self.glow_strength_spin = QDoubleSpinBox()
        self.glow_strength_spin.setRange(0.0, 2.0)
        self.glow_strength_spin.setSingleStep(0.1)
        self.glow_strength_spin.setDecimals(1)
        self.glow_strength_spin.setValue(float(settings.get("glow_strength")))
        self._add_row(form, "glow_strength", self.glow_strength_spin)

        self.font_auto_check = QCheckBox()
        self.font_auto_check.setChecked(
            not str(settings.get("font_family") or "").strip()
        )
        form.addRow("", self.font_auto_check)

        self.font_combo = QFontComboBox()
        configured_font = str(settings.get("font_family") or "").strip()
        if configured_font:
            self.font_combo.setCurrentFont(QFont(configured_font))
        self.font_auto_check.toggled.connect(
            lambda auto: self.font_combo.setDisabled(auto)
        )
        self.font_combo.setDisabled(self.font_auto_check.isChecked())
        self._add_row(form, "font", self.font_combo)

        self.font_scale_spin = QDoubleSpinBox()
        self.font_scale_spin.setRange(0.5, 1.5)
        self.font_scale_spin.setSingleStep(0.05)
        self.font_scale_spin.setDecimals(2)
        self.font_scale_spin.setValue(float(settings.get("font_scale")))
        self._add_row(form, "font_size", self.font_scale_spin)

        self.corner_spin = QSpinBox()
        self.corner_spin.setRange(0, 60)
        self.corner_spin.setSingleStep(2)
        self.corner_spin.setSuffix(" px")
        self.corner_spin.setValue(int(settings.get("corner_radius")))
        self._add_row(form, "corner_radius", self.corner_spin)

        self.digital_check = QCheckBox()
        self.digital_check.setChecked(bool(settings.get("show_digital")))
        form.addRow("", self.digital_check)

        self.clock24_check = QCheckBox()
        self.clock24_check.setChecked(bool(settings.get("clock_24h")))
        form.addRow("", self.clock24_check)

        self.date_check = QCheckBox()
        self.date_check.setChecked(bool(settings.get("show_date")))
        form.addRow("", self.date_check)

        self.dots_check = QCheckBox()
        self.dots_check.setChecked(bool(settings.get("show_dots")))
        form.addRow("", self.dots_check)

        self.on_top_check = QCheckBox()
        self.on_top_check.setChecked(bool(settings.get("always_on_top")))
        form.addRow("", self.on_top_check)

        self._buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.RestoreDefaults
        )
        self._buttons.accepted.connect(self.accept)
        self._buttons.rejected.connect(self.reject)
        self._buttons.button(
            QDialogButtonBox.StandardButton.RestoreDefaults
        ).clicked.connect(self._restore_defaults)

        self.preset_label = QLabel()
        preset_row = QHBoxLayout()
        preset_row.addWidget(self.preset_label)
        for name in PRESETS:
            button = QPushButton()
            button.clicked.connect(
                lambda checked=False, n=name: self._apply_preset(n)
            )
            self._preset_buttons[name] = button
            preset_row.addWidget(button)
        preset_widget = QWidget()
        preset_widget.setLayout(preset_row)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(preset_widget)
        layout.addWidget(self._buttons)

        self._connect_preview()
        self._rebuild_languages()
        self.retranslate(str(settings.get("language") or DEFAULT_LANGUAGE))

    # ------------------------------------------------------------------ helpers
    def _add_row(self, form: QFormLayout, key: str, field: QWidget) -> None:
        label = QLabel()
        self._labels[key] = label
        form.addRow(label, field)

    def _connect_preview(self) -> None:
        for signal in (
            self.optional_check.toggled,
            self.opacity_slider.valueChanged,
            self.scale_spin.valueChanged,
            self.refresh_spin.valueChanged,
            self.glow_check.toggled,
            self.glow_strength_spin.valueChanged,
            self.font_auto_check.toggled,
            self.font_combo.currentFontChanged,
            self.font_scale_spin.valueChanged,
            self.corner_spin.valueChanged,
            self.digital_check.toggled,
            self.clock24_check.toggled,
            self.date_check.toggled,
            self.dots_check.toggled,
            self.on_top_check.toggled,
        ):
            signal.connect(self._emit_preview)
        for button in (self.active_button, self.inactive_button, self.background_button):
            button.changed.connect(self._emit_preview)
        self.language_combo.currentIndexChanged.connect(self._on_language_changed)

    def _on_language_changed(self, *args) -> None:
        code = self.language_combo.currentData()
        if code:
            self.retranslate(code)
        self._emit_preview()

    def _emit_preview(self, *args) -> None:
        self.preview.emit(self.values())

    def _apply_preset(self, name: str) -> None:
        preset = PRESETS[name]
        self.active_button.set_color(preset["active_color"])
        self.inactive_button.set_color(preset["inactive_color"])
        self.background_button.set_color(preset["background_color"])
        self.glow_check.setChecked(bool(preset["glow"]))
        self.glow_strength_spin.setValue(float(preset["glow_strength"]))
        self._emit_preview()

    def _rebuild_languages(self) -> None:
        current = self.language_combo.currentData()
        if current is None:
            current = str(self.settings.get("language"))
        self.language_combo.blockSignals(True)
        self.language_combo.clear()
        for locale in get_available_locales(
            {"enable_optional_locales": self.optional_check.isChecked()}
        ):
            self.language_combo.addItem(
                flag_icon(locale.code), locale.name, locale.code
            )
        index = self.language_combo.findData(current)
        if index < 0:
            index = self.language_combo.findData(DEFAULT_LANGUAGE)
        self.language_combo.setCurrentIndex(max(0, index))
        self.language_combo.blockSignals(False)

    def retranslate(self, code: str) -> None:
        self.setWindowTitle(tr(code, "settings_title"))
        for key, label in self._labels.items():
            label.setText(tr(code, key))
        self.optional_check.setText(tr(code, "optional_locales"))
        self.glow_check.setText(tr(code, "glow"))
        self.font_auto_check.setText(tr(code, "auto_font"))
        self.digital_check.setText(tr(code, "digital_time"))
        self.clock24_check.setText(tr(code, "format_24h"))
        self.date_check.setText(tr(code, "show_date"))
        self.dots_check.setText(tr(code, "minute_dots"))
        self.on_top_check.setText(tr(code, "always_on_top"))
        self.preset_label.setText(tr(code, "theme"))
        for name, button in self._preset_buttons.items():
            button.setText(tr(code, PRESET_LABEL_KEYS[name]))
        self._buttons.button(QDialogButtonBox.StandardButton.Ok).setText("OK")
        self._buttons.button(QDialogButtonBox.StandardButton.Cancel).setText(
            tr(code, "cancel")
        )
        self._buttons.button(
            QDialogButtonBox.StandardButton.RestoreDefaults
        ).setText(tr(code, "reset_defaults"))
        for button in (self.active_button, self.inactive_button, self.background_button):
            button.set_title(tr(code, "choose_color"))

    def _restore_defaults(self) -> None:
        self.language_combo.setCurrentIndex(
            max(0, self.language_combo.findData(DEFAULTS["language"]))
        )
        self.optional_check.setChecked(bool(DEFAULTS["enable_optional_locales"]))
        self.active_button.set_color(DEFAULTS["active_color"])
        self.inactive_button.set_color(DEFAULTS["inactive_color"])
        self.background_button.set_color(DEFAULTS["background_color"])
        self.opacity_slider.setValue(int(round(DEFAULTS["opacity"] * 100)))
        self.scale_spin.setValue(DEFAULTS["scale"])
        self.refresh_spin.setValue(DEFAULTS["refresh_ms"])
        self.glow_check.setChecked(bool(DEFAULTS["glow"]))
        self.glow_strength_spin.setValue(DEFAULTS["glow_strength"])
        self.font_auto_check.setChecked(not str(DEFAULTS["font_family"]).strip())
        self.font_scale_spin.setValue(DEFAULTS["font_scale"])
        self.corner_spin.setValue(DEFAULTS["corner_radius"])
        self.digital_check.setChecked(bool(DEFAULTS["show_digital"]))
        self.clock24_check.setChecked(bool(DEFAULTS["clock_24h"]))
        self.date_check.setChecked(bool(DEFAULTS["show_date"]))
        self.dots_check.setChecked(bool(DEFAULTS["show_dots"]))
        self.on_top_check.setChecked(bool(DEFAULTS["always_on_top"]))
        self._emit_preview()

    def values(self) -> dict:
        return {
            "language": self.language_combo.currentData() or DEFAULT_LANGUAGE,
            "enable_optional_locales": self.optional_check.isChecked(),
            "active_color": self.active_button.color(),
            "inactive_color": self.inactive_button.color(),
            "background_color": self.background_button.color(),
            "opacity": self.opacity_slider.value() / 100.0,
            "scale": self.scale_spin.value(),
            "refresh_ms": self.refresh_spin.value(),
            "glow": self.glow_check.isChecked(),
            "glow_strength": self.glow_strength_spin.value(),
            "font_family": ""
            if self.font_auto_check.isChecked()
            else self.font_combo.currentFont().family(),
            "font_scale": self.font_scale_spin.value(),
            "corner_radius": self.corner_spin.value(),
            "show_digital": self.digital_check.isChecked(),
            "clock_24h": self.clock24_check.isChecked(),
            "show_date": self.date_check.isChecked(),
            "show_dots": self.dots_check.isChecked(),
            "always_on_top": self.on_top_check.isChecked(),
        }

    def accept(self) -> None:  # noqa: D102
        self.settings.update(**self.values())
        super().accept()
