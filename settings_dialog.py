"""Settings dialog: language, colours, opacity, size, refresh rate, ..."""

from __future__ import annotations

from PyQt6.QtCore import Qt
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
    QPushButton,
    QSlider,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from locales import DEFAULT_LANGUAGE, get_available_locales
from settings import DEFAULTS, Settings

_REFRESH_MIN = 100
_REFRESH_MAX = 5000


class ColorButton(QPushButton):
    """A button showing the current colour and opening a colour picker."""

    def __init__(self, color: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._color = QColor(color)
        if not self._color.isValid():
            self._color = QColor("#000000")
        self.setMinimumWidth(120)
        self.clicked.connect(self._choose)
        self._refresh()

    def _refresh(self) -> None:
        name = self._color.name().upper()
        text_color = "#000000" if self._color.lightness() > 128 else "#FFFFFF"
        self.setText(name)
        self.setStyleSheet(
            f"QPushButton {{ background-color: {self._color.name()}; "
            f"color: {text_color}; border: 1px solid #555; padding: 4px; }}"
        )

    def _choose(self) -> None:
        chosen = QColorDialog.getColor(self._color, self, "Choisir une couleur")
        if chosen.isValid():
            self._color = chosen
            self._refresh()

    def color(self) -> str:
        return self._color.name()


class SettingsDialog(QDialog):
    def __init__(self, settings: Settings, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.settings = settings
        self.setWindowTitle("Réglages du widget")
        self.setModal(True)

        form = QFormLayout()

        self.language_combo = QComboBox()
        form.addRow("Langue", self.language_combo)

        self.optional_check = QCheckBox("Afficher les langues optionnelles (arabe)")
        self.optional_check.setChecked(bool(settings.get("enable_optional_locales")))
        self.optional_check.toggled.connect(self._rebuild_languages)
        form.addRow("", self.optional_check)

        self.active_button = ColorButton(str(settings.get("active_color")))
        form.addRow("Couleur des lettres actives", self.active_button)

        self.inactive_button = ColorButton(str(settings.get("inactive_color")))
        form.addRow("Couleur des lettres inactives", self.inactive_button)

        self.background_button = ColorButton(str(settings.get("background_color")))
        form.addRow("Couleur de fond", self.background_button)

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
        form.addRow("Opacité du fond", opacity_widget)

        self.scale_spin = QDoubleSpinBox()
        self.scale_spin.setRange(0.5, 3.0)
        self.scale_spin.setSingleStep(0.05)
        self.scale_spin.setDecimals(2)
        self.scale_spin.setValue(float(settings.get("scale")))
        form.addRow("Taille", self.scale_spin)

        self.refresh_spin = QSpinBox()
        self.refresh_spin.setRange(_REFRESH_MIN, _REFRESH_MAX)
        self.refresh_spin.setSingleStep(100)
        self.refresh_spin.setSuffix(" ms")
        self.refresh_spin.setValue(int(settings.get("refresh_ms")))
        form.addRow("Vitesse de rafraîchissement", self.refresh_spin)

        self.glow_check = QCheckBox("Effet lumineux (glow)")
        self.glow_check.setChecked(bool(settings.get("glow")))
        form.addRow("", self.glow_check)

        self.glow_strength_spin = QDoubleSpinBox()
        self.glow_strength_spin.setRange(0.0, 2.0)
        self.glow_strength_spin.setSingleStep(0.1)
        self.glow_strength_spin.setDecimals(1)
        self.glow_strength_spin.setValue(float(settings.get("glow_strength")))
        form.addRow("Intensité du glow", self.glow_strength_spin)

        self.font_auto_check = QCheckBox("Police automatique (selon la langue)")
        self.font_auto_check.setChecked(not str(settings.get("font_family") or "").strip())
        form.addRow("", self.font_auto_check)

        self.font_combo = QFontComboBox()
        configured_font = str(settings.get("font_family") or "").strip()
        if configured_font:
            self.font_combo.setCurrentFont(QFont(configured_font))
        self.font_auto_check.toggled.connect(
            lambda auto: self.font_combo.setDisabled(auto)
        )
        self.font_combo.setDisabled(self.font_auto_check.isChecked())
        form.addRow("Police", self.font_combo)

        self.font_scale_spin = QDoubleSpinBox()
        self.font_scale_spin.setRange(0.5, 1.5)
        self.font_scale_spin.setSingleStep(0.05)
        self.font_scale_spin.setDecimals(2)
        self.font_scale_spin.setValue(float(settings.get("font_scale")))
        form.addRow("Taille du texte", self.font_scale_spin)

        self.corner_spin = QSpinBox()
        self.corner_spin.setRange(0, 60)
        self.corner_spin.setSingleStep(2)
        self.corner_spin.setSuffix(" px")
        self.corner_spin.setValue(int(settings.get("corner_radius")))
        form.addRow("Arrondi des coins", self.corner_spin)

        self.digital_check = QCheckBox("Heure numérique sous la grille")
        self.digital_check.setChecked(bool(settings.get("show_digital")))
        form.addRow("", self.digital_check)

        self.clock24_check = QCheckBox("Format 24 h (numérique)")
        self.clock24_check.setChecked(bool(settings.get("clock_24h")))
        form.addRow("", self.clock24_check)

        self.date_check = QCheckBox("Afficher la date")
        self.date_check.setChecked(bool(settings.get("show_date")))
        form.addRow("", self.date_check)

        self.dots_check = QCheckBox("Points des minutes dans les coins")
        self.dots_check.setChecked(bool(settings.get("show_dots")))
        form.addRow("", self.dots_check)

        self.on_top_check = QCheckBox("Toujours au-dessus")
        self.on_top_check.setChecked(bool(settings.get("always_on_top")))
        form.addRow("", self.on_top_check)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.RestoreDefaults
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        buttons.button(QDialogButtonBox.StandardButton.RestoreDefaults).clicked.connect(
            self._restore_defaults
        )

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(buttons)

        self._rebuild_languages()

    # ------------------------------------------------------------------ helpers
    def _rebuild_languages(self) -> None:
        current = self.language_combo.currentData()
        if current is None:
            current = str(self.settings.get("language"))
        self.language_combo.clear()
        for locale in get_available_locales(
            {"enable_optional_locales": self.optional_check.isChecked()}
        ):
            self.language_combo.addItem(locale.name, locale.code)
        index = self.language_combo.findData(current)
        if index < 0:
            index = self.language_combo.findData(DEFAULT_LANGUAGE)
        self.language_combo.setCurrentIndex(max(0, index))

    def _restore_defaults(self) -> None:
        self.language_combo.setCurrentIndex(
            max(0, self.language_combo.findData(DEFAULTS["language"]))
        )
        self.optional_check.setChecked(bool(DEFAULTS["enable_optional_locales"]))
        self.active_button._color = QColor(DEFAULTS["active_color"])
        self.active_button._refresh()
        self.inactive_button._color = QColor(DEFAULTS["inactive_color"])
        self.inactive_button._refresh()
        self.background_button._color = QColor(DEFAULTS["background_color"])
        self.background_button._refresh()
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
