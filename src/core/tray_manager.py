"""
System tray manager for Snip & Edit application
"""
from typing import Optional
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QObject
from ..config.settings import Messages, AppSettings
from src.utils.helpers import resource_path


class SystemTrayManager(QSystemTrayIcon):
    """Manages the system tray icon and its context menu"""

    def __init__(self, app: QApplication, icon_path: str = None, parent=None):
        if icon_path is None:
            icon_path = resource_path("icon.ico")
        super().__init__(QIcon(icon_path), parent)

        self.app = app
        self.about_dialog = None  # To hold the reference to the about dialog
        self.settings = AppSettings()
        self.capture_window = None
        self.icon_path = icon_path
        
        # Create and setup system tray icon
        self._create_tray_icon()
        self._create_context_menu()
        self._connect_signals()
        
        # Show tray icon and welcome message
        self.show()
        self._show_welcome_message()
    
    def _create_tray_icon(self) -> None:
        """Create the system tray icon"""
        self.setIcon(QIcon(self.icon_path))
        self.setToolTip(Messages.TRAY_TOOLTIP)
    
    def _create_context_menu(self) -> None:
        """Create context menu for system tray icon"""
        menu = QMenu()
        
        # Capture action
        capture_action = menu.addAction(Messages.MENU_CAPTURE)
        capture_action.triggered.connect(self.start_capture)
        
        menu.addSeparator()
        
        # About action
        about_action = menu.addAction(Messages.MENU_ABOUT)
        about_action.triggered.connect(self._show_about_dialog)
        
        # Exit action
        exit_action = menu.addAction(Messages.MENU_EXIT)
        exit_action.triggered.connect(self.exit_application)
        
        self.setContextMenu(menu)
    
    def _connect_signals(self) -> None:
        """Connect tray icon signals"""
        self.activated.connect(self._on_tray_icon_activated)
    
    def _show_welcome_message(self) -> None:
        """Show welcome message when application starts"""
        self.showMessage(
            Messages.TRAY_WELCOME_TITLE,
            Messages.TRAY_WELCOME_MESSAGE,
            QSystemTrayIcon.MessageIcon.Information,
            AppSettings.TRAY_MESSAGE_DURATION_MS
        )
    
    def _on_tray_icon_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        """Handle tray icon activation"""
        if reason in (QSystemTrayIcon.ActivationReason.Trigger, 
                     QSystemTrayIcon.ActivationReason.DoubleClick):
            self.start_capture()
            
    def _show_about_dialog(self) -> None:
        """Show the about dialog"""
        from ..ui.about_dialog import AboutDialog
        dialog = AboutDialog()
        dialog.exec()
    
    def start_capture(self) -> None:
        """Start screen capture process"""
        # Safely close existing capture window
        self._close_existing_capture_window()
        
        # Import here to avoid circular imports
        from ..ui.capture_window import CaptureWindow
        
        # Create new capture window
        self.capture_window = CaptureWindow(self)
        self.capture_window.finished.connect(self._on_capture_finished)
        self.capture_window.show()
    
    def _close_existing_capture_window(self) -> None:
        """Safely close existing capture window"""
        if self.capture_window:
            try:
                if hasattr(self.capture_window, 'close') and not self.capture_window.isHidden():
                    self.capture_window.close()
            except RuntimeError:
                # Object has been deleted
                pass
            finally:
                self.capture_window = None
    
    def _on_capture_finished(self) -> None:
        """Handle when capture window is finished"""
        self.capture_window = None
    
    def exit_application(self) -> None:
        """Exit the application"""
        self._close_existing_capture_window()
        self.hide()
        self.app.quit()
    
    def is_system_tray_available(self) -> bool:
        """Check if system tray is available"""
        return QSystemTrayIcon.isSystemTrayAvailable()
