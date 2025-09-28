"""
Edit toolbar for the capture window
"""
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QIcon
from ..config.settings import Messages, AppSettings
from ..utils.helpers import resource_path


class EditToolbar(QWidget):
    """Toolbar with drawing tools and action buttons"""
    
    # Define signals
    tool_selected = pyqtSignal(str)
    save = pyqtSignal()
    copy = pyqtSignal()
    undo = pyqtSignal()
    redo = pyqtSignal()
    close_app = pyqtSignal()
    settings_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_widget()
        self._create_layout()
        self._add_tool_buttons()
        self._add_separators()
        self._add_action_buttons()

    def _setup_widget(self) -> None:
        """Setup widget properties"""
        self.setWindowFlags(Qt.WindowType.Tool | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

    def _create_layout(self) -> None:
        """Create main layout and frame"""
        # Main layout for the widget
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Frame to hold buttons with dark background
        self.frame = QFrame(self)
        self.frame.setStyleSheet(
            f"background-color: {AppSettings.TOOLBAR_BACKGROUND_COLOR}; "
            f"border-radius: {AppSettings.TOOLBAR_BORDER_RADIUS}px;"
        )
        main_layout.addWidget(self.frame)

        # Layout for the frame's content
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setContentsMargins(
            AppSettings.TOOLBAR_PADDING, AppSettings.TOOLBAR_PADDING,
            AppSettings.TOOLBAR_PADDING, AppSettings.TOOLBAR_PADDING
        )
        self.buttons_layout.setSpacing(AppSettings.TOOLBAR_SPACING)
        self.frame.setLayout(self.buttons_layout)

    def _add_tool_buttons(self) -> None:
        """Add drawing tool buttons"""
        tools = [
            ("pen", Messages.TOOL_PENCIL),
            ("line", Messages.TOOL_LINE),
            ("arrow", Messages.TOOL_ARROW),
            ("rect", Messages.TOOL_RECT),
            ("circle", Messages.TOOL_CIRCLE),
            ("marker", Messages.TOOL_MARKER),
            ("pixelate", Messages.TOOL_PIXELATE),
            ("text", Messages.TOOL_TEXT),
            ("counter", Messages.TOOL_COUNTER),
        ]
        
        for tool_name, tool_label in tools:
            self._add_tool_button(tool_name, tool_label, resource_path(f"icons/{tool_name}.svg"))

    def _add_separators(self) -> None:
        """Add visual separators"""
        for _ in range(2):
            separator = QFrame()
            separator.setFrameShape(QFrame.Shape.VLine)
            separator.setFrameShadow(QFrame.Shadow.Sunken)
            separator.setStyleSheet("color: #555;")
            self.buttons_layout.addWidget(separator)

    def _add_action_buttons(self) -> None:
        """Add action buttons"""
        actions = [
            ("settings", Messages.TOOLBAR_SETTINGS, self.settings_clicked.emit),
            ("undo", Messages.TOOLBAR_UNDO, self.undo.emit),
            ("redo", Messages.TOOLBAR_REDO, self.redo.emit),
            ("copy", Messages.TOOLBAR_COPY, self.copy.emit),
            ("save", Messages.TOOLBAR_SAVE, self.save.emit),
            ("close", Messages.TOOLBAR_CLOSE, self.close_app.emit),
        ]
        
        for name, tooltip, slot in actions:
            self._add_button(tooltip, slot, resource_path(f"icons/{name}.svg"))

    def _add_button(self, tooltip: str, slot, icon_path: str = None) -> QPushButton:
        """Create and add a button to the toolbar"""
        button = QPushButton()
        if icon_path:
            button.setIcon(QIcon(icon_path))
            button.setIconSize(QSize(20, 20)) # Kích thước icon
        button.setToolTip(tooltip)
        
        # Cập nhật stylesheet
        button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid #555;
                padding: 5px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #444;
            }
            QPushButton:pressed {
                background-color: #555;
            }
            QToolTip {
                background-color: #f0f0f0;
                color: #333333;
                border: 1px solid #cccccc;
                padding: 4px;
            }
        """)
        
        button.setFixedSize(32, 32) # Kích thước nút vuông
        button.clicked.connect(slot)
        self.buttons_layout.addWidget(button)
        return button

    def _add_tool_button(self, name: str, tooltip: str, icon_path: str) -> QPushButton:
        """Create and add a tool button"""
        return self._add_button(tooltip, lambda: self.tool_selected.emit(name), icon_path)
