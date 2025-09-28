"""
Snip & Edit - Main entry point
A powerful and simple screen capture tool inspired by Flameshot
"""
import sys
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from src.core.tray_manager import SystemTrayManager
from src.config.settings import Messages, AppSettings
from src.utils.helpers import resource_path


def setup_application() -> QApplication:
    """Setup the QApplication with proper settings"""
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path("icon.ico")))
    app.setQuitOnLastWindowClosed(False)  # Keep running when windows are closed
    
    return app


def check_system_tray() -> bool:
    """Check if system tray is available"""
    if not QSystemTrayIcon.isSystemTrayAvailable():
        print(Messages.ERROR_SYSTEM_TRAY)
        return False
    return True


def main() -> int:
    """Main application entry point"""
    app = setup_application()
    
    if not check_system_tray():
        return 1
    
    # Create and start the system tray manager
    tray_manager = SystemTrayManager(app, resource_path("icon.ico"))
    
    # Run the application
    return app.exec()


if __name__ == '__main__':
    sys.exit(main())
