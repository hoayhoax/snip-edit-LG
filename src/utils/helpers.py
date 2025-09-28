"""
Utility functions and helpers for Snip & Edit
"""
import sys
import os
from typing import Optional
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QByteArray


def resource_path(relative_path: str) -> str:
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # Running as a PyInstaller bundle
        # The assets are in the 'assets' folder at the root of the bundle
        base_path = os.path.join(sys._MEIPASS, 'assets')
    else:
        # Running as a script
        # The assets are in 'src/assets' from the project root.
        base_path = os.path.join(os.path.abspath('.'), 'src', 'assets')

    return os.path.join(base_path, relative_path)


def create_icon(base64_data: bytes) -> QIcon:
    """
    Create QIcon from base64 data
    
    Args:
        base64_data: Base64 encoded image data
        
    Returns:
        QIcon object
    """
    pixmap = QPixmap()
    pixmap.loadFromData(QByteArray.fromBase64(base64_data))
    return QIcon(pixmap)


def safe_disconnect(signal, slot) -> None:
    """
    Safely disconnect signal from slot, ignoring if already disconnected
    
    Args:
        signal: PyQt signal to disconnect
        slot: Slot function to disconnect from signal
    """
    try:
        signal.disconnect(slot)
    except (TypeError, RuntimeError):
        # Already disconnected or object deleted
        pass


def safe_close_widget(widget) -> None:
    """
    Safely close and delete a widget
    
    Args:
        widget: QWidget to close and delete
    """
    if widget:
        try:
            if hasattr(widget, 'close') and not widget.isHidden():
                widget.close()
            widget.setParent(None)
            widget.deleteLater()
        except RuntimeError:
            # Object has been deleted
            pass


def clamp(value: float, min_value: float, max_value: float) -> float:
    """
    Clamp value between min and max values
    
    Args:
        value: Value to clamp
        min_value: Minimum allowed value
        max_value: Maximum allowed value
        
    Returns:
        Clamped value
    """
    return max(min_value, min(max_value, value))


def calculate_font_size(base_size: int, thickness: int, multiplier: int) -> int:
    """
    Calculate font size based on thickness setting
    
    Args:
        base_size: Base font size
        thickness: Current thickness setting
        multiplier: Size multiplier
        
    Returns:
        Calculated font size
    """
    return base_size + thickness * multiplier


def format_thickness_label(base_label: str, thickness: int) -> str:
    """
    Format thickness label with current value
    
    Args:
        base_label: Base label text
        thickness: Current thickness value
        
    Returns:
        Formatted label string
    """
    return f"{base_label}: {thickness}"
