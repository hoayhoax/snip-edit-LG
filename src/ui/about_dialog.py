from PyQt6.QtWidgets import QMessageBox
from ..config.settings import Messages, AppInfo

class AboutDialog(QMessageBox):
    """About dialog for the application"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(Messages.ABOUT_TITLE)
        
        # Format the about text with app info
        about_text = Messages.ABOUT_TEXT.format(
            version=AppInfo.VERSION,
            author=AppInfo.AUTHOR,
            license=AppInfo.LICENSE
        )
        
        self.setText(about_text)
        self.setIcon(QMessageBox.Icon.Information)
