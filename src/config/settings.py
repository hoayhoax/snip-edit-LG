"""
Configuration and settings management for Snip & Edit
"""
from typing import Dict, Any
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor


class AppSettings:
    """Application settings and configuration management"""
    
    # Default tool settings
    DEFAULT_TOOL: str = 'pen'
    DEFAULT_COLOR: Qt.GlobalColor = Qt.GlobalColor.red
    DEFAULT_THICKNESS: int = 3
    DEFAULT_FONT: QFont = QFont("Arial", 16)
    
    # UI Settings
    TOOLBAR_BACKGROUND_COLOR: str = "rgba(30, 30, 30, 220)"
    TOOLBAR_BORDER_RADIUS: int = 5
    TOOLBAR_PADDING: int = 5
    TOOLBAR_SPACING: int = 5
    
    # Text input settings
    TEXT_INPUT_BACKGROUND: str = "rgba(30, 30, 30, 180)"
    TEXT_INPUT_PADDING: int = 5
    TEXT_INPUT_WIDTH: int = 200
    
    # History settings
    MAX_UNDO_HISTORY: int = 20
    
    # Pixelate settings
    MIN_PIXEL_SIZE: int = 3
    
    # Font size calculation
    FONT_SIZE_BASE: int = 10
    FONT_SIZE_MULTIPLIER: int = 2
    
    # Minimum selection size
    MIN_SELECTION_WIDTH: int = 5
    MIN_SELECTION_HEIGHT: int = 5
    
    # Arrow settings
    ARROW_SIZE_MULTIPLIER: int = 3
    ARROW_ANGLE: float = 3.14159 / 6  # π/6
    
    # Marker settings
    MARKER_ALPHA: int = 50
    MARKER_WIDTH: int = 15
    
    # Timer delays
    CLOSE_DELAY_MS: int = 100
    TRAY_MESSAGE_DURATION_MS: int = 3000
    
    # Thickness range
    THICKNESS_MIN: int = 1
    THICKNESS_MAX: int = 20
    
    # Font size range
    FONT_SIZE_MIN: int = 8
    FONT_SIZE_MAX: int = 72

    # Text settings
    DEFAULT_FONT_FAMILY = "Arial"
    DEFAULT_FONT_SIZE = 14
    TEXT_INPUT_PADDING = 5
    FONT_SIZE_MULTIPLIER = 2

    # Counter tool settings
    COUNTER_SIZE_MULTIPLIER = 10

    # Screenshot format
    DEFAULT_FORMAT = "PNG"
    AVAILABLE_FORMATS = ["PNG", "JPG", "BMP"]


class Colors:
    """Color constants and utilities"""
    
    @staticmethod
    def get_contrasting_color(color: QColor) -> str:
        """Get contrasting color (white/black) based on color brightness"""
        return 'white' if color.value() < 128 else 'black'
    
    @staticmethod
    def get_border_color(color: QColor) -> QColor:
        """Get border color for text input based on main color"""
        return color.lighter(120) if color.value() < 128 else color.darker(120)


class Messages:
    """Application messages and strings"""
    
    # Tray icon messages
    TRAY_TOOLTIP: str = "Snip & Edit - Screen Capture Tool"
    TRAY_WELCOME_TITLE: str = "Snip & Edit"
    TRAY_WELCOME_MESSAGE: str = "Ứng dụng đã khởi động và chạy ở chế độ nền.\nClick vào icon để bắt đầu chụp màn hình!"
    
    # Menu items
    MENU_CAPTURE: str = "📸 Capture Screen"
    MENU_EXIT: str = "🚪 Exit"
    
    # Toolbar buttons
    TOOLBAR_SETTINGS: str = "Settings - Configure application settings"
    TOOLBAR_UNDO: str = "Undo - Revert the last action"
    TOOLBAR_REDO: str = "Redo - Reapply the last undone action"
    TOOLBAR_COPY: str = "Copy - Copy the image to the clipboard"
    TOOLBAR_SAVE: str = "Save - Save the image to a file"
    TOOLBAR_CLOSE: str = "Close - Discard changes and close"
    
    # Tools
    TOOL_PENCIL: str = "Pencil - Draw freeform lines"
    TOOL_LINE: str = "Line - Draw a straight line"
    TOOL_ARROW: str = "Arrow - Draw an arrow"
    TOOL_RECT: str = "Rectangle - Draw a rectangle"
    TOOL_CIRCLE: str = "Circle - Draw an ellipse or circle"
    TOOL_MARKER: str = "Marker - Highlight areas"
    TOOL_PIXELATE: str = "Pixelate - Obscure areas"
    TOOL_TEXT: str = "Text - Add text"
    TOOL_COUNTER: str = "Counter - Add auto-incrementing numbers"
    
    # Dialog titles
    SETTINGS_TITLE: str = "Settings"
    COLOR_DIALOG_TITLE: str = "Select Color"
    SAVE_DIALOG_TITLE: str = "Save Image"
    
    # Settings labels
    PEN_COLOR_LABEL: str = "Pen Color"
    THICKNESS_LABEL_BASE: str = "Pen & Shape Thickness"
    FONT_LABEL: str = "Text Font"
    
    # File filters
    PNG_FILTER: str = "PNG Images (*.png)"
    JPEG_FILTER: str = "JPEG Images (*.jpg)"
    
    # Error messages
    ERROR_SYSTEM_TRAY: str = "System tray is not available on this system."
    ERROR_SAVING_IMAGE: str = "Error saving image"
    ERROR_COPYING_CLIPBOARD: str = "Error copying to clipboard"
    ERROR_GETTING_FINAL_IMAGE: str = "Error getting final image"
    ERROR_CLEANUP: str = "Error during cleanup"
    
    # About Dialog
    MENU_ABOUT: str = "ℹ️ About"
    ABOUT_TITLE: str = "About Snip & Edit"
    ABOUT_TEXT: str = """
        <b>Snip & Edit v{version}</b><br><br>
        A simple and powerful screenshot and editing tool.<br><br>
        <b>Author:</b> {author}<br>
        <b>License:</b> {license}
    """


class AppInfo:
    """Application Information"""
    VERSION: str = "1.0.0"
    AUTHOR: str = "HoaNT"
    LICENSE: str = "GPL"


class FileFormats:
    """File format configurations"""
    
    PNG_EXTENSION: str = ".png"
    JPEG_EXTENSION: str = ".jpg"
    
    SAVE_FILTERS: str = f"{Messages.PNG_FILTER};;{Messages.JPEG_FILTER}"
