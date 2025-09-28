"""
Settings dialog for the Snip & Edit application
"""
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QPushButton, QLabel, QSlider, 
    QFontComboBox, QSpinBox, QColorDialog, QHBoxLayout, QCheckBox, QGroupBox,
    QButtonGroup
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor
from ..config.settings import Messages, AppSettings
from ..utils.helpers import format_thickness_label

if TYPE_CHECKING:
    from .capture_window import CaptureWindow


class SettingsDialog(QDialog):
    """Settings dialog for configuring drawing tools"""
    
    # Signals to notify the main window of changes
    color_changed = pyqtSignal(str)
    thickness_changed = pyqtSignal(int)
    font_changed = pyqtSignal(QFont)
    alignment_changed = pyqtSignal(Qt.AlignmentFlag)

    def __init__(self, parent: 'CaptureWindow'):
        super().__init__(parent)
        self.main_window = parent
        self._setup_dialog()
        self._create_widgets()
        self._setup_layout()
        self._connect_signals()
        self._init_from_main_window()

    def _setup_dialog(self) -> None:
        """Setup dialog properties"""
        self.setWindowTitle(Messages.SETTINGS_TITLE)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        self.setModal(False)  # Make it non-modal

    def _create_widgets(self) -> None:
        """Create all widgets"""
        # Color setting
        self.color_button = QPushButton(Messages.PEN_COLOR_LABEL)
        
        # Thickness setting
        self.thickness_label = QLabel(
            format_thickness_label(Messages.THICKNESS_LABEL_BASE, AppSettings.DEFAULT_THICKNESS)
        )
        self.thickness_slider = QSlider(Qt.Orientation.Horizontal)
        self.thickness_slider.setRange(AppSettings.THICKNESS_MIN, AppSettings.THICKNESS_MAX)
        
        # Font setting
        self.font_label = QLabel(Messages.FONT_LABEL)
        self.font_combo = QFontComboBox()
        self.font_size_spinbox = QSpinBox()
        self.font_size_spinbox.setRange(AppSettings.FONT_SIZE_MIN, AppSettings.FONT_SIZE_MAX)

        # Font style settings (for text tool)
        self.font_style_group = QGroupBox("Font Style")
        font_style_layout = QHBoxLayout()
        self.bold_checkbox = QCheckBox("Bold")
        self.italic_checkbox = QCheckBox("Italic")
        self.underline_checkbox = QCheckBox("Underline")
        self.strike_checkbox = QCheckBox("Strike")
        font_style_layout.addWidget(self.bold_checkbox)
        font_style_layout.addWidget(self.italic_checkbox)
        font_style_layout.addWidget(self.underline_checkbox)
        font_style_layout.addWidget(self.strike_checkbox)
        self.font_style_group.setLayout(font_style_layout)

        # Text alignment settings
        self.alignment_group = QGroupBox("Text Alignment")
        alignment_layout = QHBoxLayout()
        self.align_left_button = QPushButton("Left")
        self.align_center_button = QPushButton("Center")
        self.align_right_button = QPushButton("Right")
        self.align_left_button.setCheckable(True)
        self.align_center_button.setCheckable(True)
        self.align_right_button.setCheckable(True)
        self.alignment_button_group = QButtonGroup(self)
        self.alignment_button_group.addButton(self.align_left_button, int(Qt.AlignmentFlag.AlignLeft))
        self.alignment_button_group.addButton(self.align_center_button, int(Qt.AlignmentFlag.AlignCenter))
        self.alignment_button_group.addButton(self.align_right_button, int(Qt.AlignmentFlag.AlignRight))
        alignment_layout.addWidget(self.align_left_button)
        alignment_layout.addWidget(self.align_center_button)
        alignment_layout.addWidget(self.align_right_button)
        self.alignment_group.setLayout(alignment_layout)
        self.align_left_button.setChecked(True) # Default

    def _setup_layout(self) -> None:
        """Setup dialog layout"""
        layout = QVBoxLayout(self)
        
        layout.addWidget(self.color_button)
        layout.addWidget(self.thickness_label)
        layout.addWidget(self.thickness_slider)
        layout.addWidget(self.font_label)
        layout.addWidget(self.font_combo)
        layout.addWidget(self.font_size_spinbox)
        layout.addWidget(self.font_style_group)
        layout.addWidget(self.alignment_group)

    def _connect_signals(self) -> None:
        """Connect widget signals"""
        self.color_button.clicked.connect(self._select_color)
        self.thickness_slider.valueChanged.connect(self._on_thickness_changed)
        self.font_combo.currentFontChanged.connect(self._on_font_changed)
        self.font_size_spinbox.valueChanged.connect(self._on_font_changed)
        self.bold_checkbox.stateChanged.connect(self._on_font_changed)
        self.italic_checkbox.stateChanged.connect(self._on_font_changed)
        self.underline_checkbox.stateChanged.connect(self._on_font_changed)
        self.strike_checkbox.stateChanged.connect(self._on_font_changed)
        self.alignment_button_group.idClicked.connect(self._on_alignment_changed)

    def _init_from_main_window(self) -> None:
        """Initialize widgets with current settings from the main window"""
        self.update_color_button(self.main_window.current_color)
        self.update_thickness_slider(self.main_window.current_thickness)
        self.update_font_widgets(self.main_window.current_font)
        self.update_alignment_buttons(self.main_window.current_alignment)

    def _select_color(self) -> None:
        """Open color dialog and emit color change signal"""
        current_color = QColor(self.main_window.current_color)
        color = QColorDialog.getColor(current_color, self, Messages.COLOR_DIALOG_TITLE)
        if color.isValid():
            self.color_changed.emit(color.name())

    def _on_thickness_changed(self, value: int) -> None:
        """Handle thickness slider change"""
        self.thickness_label.setText(
            format_thickness_label(Messages.THICKNESS_LABEL_BASE, value)
        )
        self.thickness_changed.emit(value)

    def _on_alignment_changed(self, button_id: int) -> None:
        """Handle alignment button click"""
        self.alignment_changed.emit(Qt.AlignmentFlag(button_id))

    def _on_font_changed(self) -> None:
        """Handle font change"""
        font = self.font_combo.currentFont()
        font.setPointSize(self.font_size_spinbox.value())
        font.setBold(self.bold_checkbox.isChecked())
        font.setItalic(self.italic_checkbox.isChecked())
        font.setUnderline(self.underline_checkbox.isChecked())
        font.setStrikeOut(self.strike_checkbox.isChecked())
        self.font_changed.emit(font)

    # Public methods to update UI from outside
    def update_color_button(self, color) -> None:
        """Update color button appearance"""
        if not isinstance(color, QColor):
            color = QColor(color)
        
        if not color.isValid():
            return

        text_color = 'white' if color.value() < 128 else 'black'
        self.color_button.setStyleSheet(
            f"background-color: {color.name()}; color: {text_color};"
        )

    def update_thickness_slider(self, value: int) -> None:
        """Update thickness slider value"""
        self.thickness_slider.setValue(value)
        self.thickness_label.setText(
            format_thickness_label(Messages.THICKNESS_LABEL_BASE, value)
        )

    def update_font_widgets(self, font: QFont) -> None:
        """Update font widgets"""
        self.font_combo.setCurrentFont(font)
        self.font_size_spinbox.setValue(font.pointSize())
        self.bold_checkbox.setChecked(font.bold())
        self.italic_checkbox.setChecked(font.italic())
        self.underline_checkbox.setChecked(font.underline())
        self.strike_checkbox.setChecked(font.strikeOut())

    def update_alignment_buttons(self, alignment: Qt.AlignmentFlag) -> None:
        """Update the alignment button states"""
        button = self.alignment_button_group.button(int(alignment))
        if button:
            button.setChecked(True)

    def set_text_tool_mode(self, is_text_tool: bool) -> None:
        """Show/hide text-specific font style options"""
        self.font_style_group.setVisible(is_text_tool)
        self.alignment_group.setVisible(is_text_tool)
