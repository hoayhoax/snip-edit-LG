"""
Main capture window for screen capture and editing
"""
from typing import Optional, List, TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget, QApplication, QFileDialog, QLineEdit
)
from PyQt6.QtGui import (
    QPainter, QPen, QColor, QKeySequence, QShortcut, QIcon,
    QPixmap, QCloseEvent, QFont, QFontMetrics, QCursor
)
from PyQt6.QtCore import Qt, QRect, QPoint, pyqtSignal, QTimer, QSize
from ..config.settings import AppSettings, Messages, Colors, FileFormats
from ..utils.helpers import safe_close_widget, safe_disconnect, calculate_font_size, resource_path
from ..utils.image_processing import ImageProcessor
from ..tools.drawing_tools import ToolFactory
from .edit_toolbar import EditToolbar
from .settings_dialog import SettingsDialog

if TYPE_CHECKING:
    from ..core.tray_manager import SystemTrayManager


class CaptureWindow(QWidget):
    """Main window for screen capture and editing"""
    
    finished = pyqtSignal()
    
    def __init__(self, tray_manager: Optional['SystemTrayManager'] = None):
        super().__init__()
        self.tray_manager = tray_manager
        
        # Initialize state variables
        self._init_state_variables()
        
        # Setup window
        self._setup_window()
        
        # Setup shortcuts
        self._setup_shortcuts()
        
        # Take screenshot
        self._take_screenshot()

    def _init_state_variables(self) -> None:
        """Initialize all state variables"""
        # Selection state
        self.begin = QPoint()
        self.end = QPoint()
        self.is_selecting = False
        self.selection_rect = QRect()
        
        # Drawing state
        self.drawing_pixmap = QPixmap()
        self.is_drawing = False
        self.last_draw_point = QPoint()
        self.begin_draw = QPoint()
        self.end_draw = QPoint()
        
        # Tool state
        self.current_tool = AppSettings.DEFAULT_TOOL
        self.current_color = AppSettings.DEFAULT_COLOR
        self.current_thickness = AppSettings.DEFAULT_THICKNESS
        self.current_font = AppSettings.DEFAULT_FONT
        self.current_alignment = Qt.AlignmentFlag.AlignLeft
        
        # UI components
        self.tools_widget: Optional[EditToolbar] = None
        self.settings_dialog: Optional[SettingsDialog] = None
        self.text_input: Optional[QLineEdit] = None
        self.text_input_size = QSize()
        
        # History for undo functionality
        self.history: List[QPixmap] = []
        self.redo_history: List[QPixmap] = []
        self.counter_value: int = 0

    def _setup_window(self) -> None:
        """Setup window properties"""
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setCursor(Qt.CursorShape.CrossCursor)
        self.setWindowIcon(QIcon(resource_path("icon.ico")))

    def _setup_shortcuts(self) -> None:
        """Setup keyboard shortcuts"""
        QShortcut(QKeySequence("Esc"), self, self.close)
        QShortcut(QKeySequence("Ctrl+C"), self, self.copy_to_clipboard)
        QShortcut(QKeySequence("Ctrl+S"), self, self.save_image)
        QShortcut(QKeySequence("Ctrl+Z"), self, self.undo)
        QShortcut(QKeySequence("Ctrl+Y"), self, self.redo)

    def _take_screenshot(self) -> None:
        """Take full screen screenshot"""
        screen = QApplication.primaryScreen()
        self.full_screenshot = screen.grabWindow(0)
        self.setGeometry(screen.geometry())

    def closeEvent(self, event: QCloseEvent) -> None:
        """Cleanup when window is closing"""
        try:
            self._cleanup_on_close()
        except Exception as e:
            print(f"{Messages.ERROR_CLEANUP}: {e}")
        finally:
            event.accept()

    def _cleanup_on_close(self) -> None:
        """Perform cleanup operations"""
        # Disconnect toolbar signals
        self._disconnect_toolbar_signals()
        
        # Cleanup widgets
        safe_close_widget(self.tools_widget)
        safe_close_widget(self.settings_dialog)
        safe_close_widget(self.text_input)
        
        # Clear references
        self.tools_widget = None
        self.settings_dialog = None
        self.text_input = None
        self.text_input_size = QSize()
        
        # Clear pixmaps to free memory
        self.full_screenshot = None
        self.drawing_pixmap = None
        
        # Clear history
        self.history.clear()
        self.redo_history.clear()
        
        # Emit finished signal
        self.finished.emit()

    def paintEvent(self, event) -> None:
        """Paint the capture window"""
        painter = QPainter(self)
        try:
            self._paint_background(painter)
            self._paint_selection(painter)
        finally:
            painter.end()

    def _paint_background(self, painter: QPainter) -> None:
        """Paint dimmed background"""
        painter.setBrush(QColor(0, 0, 0, 120))
        painter.drawRect(self.rect())

    def _paint_selection(self, painter: QPainter) -> None:
        """Paint selection area and drawings"""
        if not self.selection_rect.isNull():
            # Draw selected area
            selected_pixmap = self.full_screenshot.copy(self.selection_rect)
            painter.drawPixmap(self.selection_rect.topLeft(), selected_pixmap)
            # Draw drawings on top
            painter.drawPixmap(self.selection_rect.topLeft(), self.drawing_pixmap)
            # Draw preview shape
            if self.is_drawing and self.current_tool in ['rect', 'circle', 'line', 'arrow', 'pixelate']:
                self._draw_preview_shape(painter)
        elif self.is_selecting:
            # Draw selection rectangle while dragging
            painter.setPen(QPen(Qt.GlobalColor.red, 1, Qt.PenStyle.DashLine))
            painter.setBrush(QColor(0, 0, 0, 0))
            painter.drawRect(QRect(self.begin, self.end))

    def mousePressEvent(self, event) -> None:
        """Handle mouse press events"""
        if self._handle_text_tool_click(event):
            return
            
        if self._is_click_in_selection(event):
            self._handle_drawing_start(event)
        else:
            self._handle_selection_start(event)

    def _handle_text_tool_click(self, event) -> bool:
        """Handle text tool specific logic"""
        # Finalize existing text input if clicking with non-text tool
        if self.current_tool != 'text' and self.text_input:
            self._finalize_text_input()
            return True
            
        # Handle text tool clicks
        if (self.current_tool == 'text' and self.tools_widget and 
            self.selection_rect.contains(event.pos())):
            
            # Finalize existing text input if clicking outside it
            if (self.text_input and 
                not self.text_input.geometry().contains(event.pos())):
                self._finalize_text_input()
            
            # Create new text input if none exists
            if not self.text_input:
                self._create_text_input(event.pos())
            return True
            
        return False

    def _is_click_in_selection(self, event) -> bool:
        """Check if click is within selection area"""
        return self.tools_widget and self.selection_rect.contains(event.pos())

    def _handle_drawing_start(self, event) -> None:
        """Handle start of drawing operation"""
        self.is_drawing = True
        self.last_draw_point = event.pos() - self.selection_rect.topLeft()
        self._save_history()
        
        if self.current_tool == 'counter':
            self._draw_counter_bubble(self.last_draw_point)
            self.is_drawing = False # Counter is a single click action
        elif self.current_tool in ['rect', 'circle', 'line', 'arrow', 'pixelate']:
            self.begin_draw = self.last_draw_point
            self.end_draw = self.last_draw_point

    def _handle_selection_start(self, event) -> None:
        """Handle start of selection operation"""
        if self.text_input:
            self._finalize_text_input()
            
        self.is_selecting = True
        self.begin = event.pos()
        self.end = event.pos()
        
        if self.tools_widget:
            self.tools_widget.hide()
        self.update()

    def mouseMoveEvent(self, event) -> None:
        """Handle mouse move events"""
        if self.is_drawing:
            self._handle_drawing_move(event)
        else:
            self._handle_selection_move(event)

    def _handle_drawing_move(self, event) -> None:
        """Handle drawing during mouse move"""
        current_point = event.pos() - self.selection_rect.topLeft()
        
        if self.current_tool in ['pen', 'marker']:
            self._draw_continuous_line(current_point)
        elif self.current_tool in ['rect', 'circle', 'line', 'arrow', 'pixelate']:
            self.end_draw = current_point
            self.update()

    def _draw_continuous_line(self, current_point: QPoint) -> None:
        """Draw continuous line for pen/marker tools"""
        tool = ToolFactory.create_tool(self.current_tool, self.current_color, 
                                      self.current_thickness)
        if tool:
            painter = QPainter(self.drawing_pixmap)
            try:
                tool.draw_line(painter, self.last_draw_point, current_point)
            finally:
                painter.end()
            self.last_draw_point = current_point
            self.update()

    def _draw_preview_shape(self, painter: QPainter) -> None:
        """Draw a preview of the shape being drawn"""
        preview_tool_type = self.current_tool
        if self.current_tool == 'pixelate':
            preview_tool_type = 'rect'

        tool = ToolFactory.create_tool(
            preview_tool_type, self.current_color, self.current_thickness
        )
        if not tool:
            return

        painter.save()
        painter.translate(self.selection_rect.topLeft())

        if self.current_tool in ['rect', 'pixelate']:
            tool.draw_rectangle(painter, self.begin_draw, self.end_draw)
        elif self.current_tool == 'circle':
            tool.draw_circle(painter, self.begin_draw, self.end_draw)
        elif self.current_tool == 'line':
            tool.draw_line(painter, self.begin_draw, self.end_draw)
        elif self.current_tool == 'arrow':
            tool.draw_arrow(painter, self.begin_draw, self.end_draw)

        painter.restore()

    def _draw_counter_bubble(self, position: QPoint) -> None:
        """Draw a counter bubble at the given position"""
        self.counter_value += 1
        
        tool = ToolFactory.create_tool(
            self.current_tool, self.current_color, self.current_thickness, self.current_font
        )
        if not tool:
            return

        painter = QPainter(self.drawing_pixmap)
        try:
            tool.draw_counter_bubble(painter, position, self.counter_value)
        finally:
            painter.end()
        self.update()

    def _handle_selection_move(self, event) -> None:
        """Handle selection rectangle during mouse move"""
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event) -> None:
        """Handle mouse release events"""
        if self.is_drawing:
            self._handle_drawing_end(event)
        elif self.is_selecting:
            self._handle_selection_end()

    def _handle_drawing_end(self, event) -> None:
        """Handle end of drawing operation"""
        self.is_drawing = False
        current_point = event.pos() - self.selection_rect.topLeft()
        
        if self.current_tool == 'pixelate':
            self._apply_pixelate_effect(current_point)
        elif self.current_tool in ['rect', 'circle', 'line', 'arrow']:
            self._draw_shape(current_point)
        
        self.update()

    def _apply_pixelate_effect(self, current_point: QPoint) -> None:
        """Apply pixelate effect to selected area"""
        pixelate_rect = QRect(self.begin_draw, current_point)
        pixel_size = max(AppSettings.MIN_PIXEL_SIZE, self.current_thickness)
        
        pixelated_pixmap = ImageProcessor.pixelate_region(
            self.full_screenshot, self.selection_rect, pixelate_rect, pixel_size
        )
        
        if not pixelated_pixmap.isNull():
            painter = QPainter(self.drawing_pixmap)
            try:
                painter.drawPixmap(pixelate_rect.topLeft(), pixelated_pixmap)
            finally:
                painter.end()

    def _draw_shape(self, current_point: QPoint) -> None:
        """Draw shape for shape tools"""
        tool = ToolFactory.create_tool(self.current_tool, self.current_color, 
                                      self.current_thickness)
        if not tool:
            return
            
        painter = QPainter(self.drawing_pixmap)
        try:
            if self.current_tool == 'rect':
                tool.draw_rectangle(painter, self.begin_draw, current_point)
            elif self.current_tool == 'circle':
                tool.draw_circle(painter, self.begin_draw, current_point)
            elif self.current_tool == 'line':
                tool.draw_line(painter, self.begin_draw, current_point)
            elif self.current_tool == 'arrow':
                tool.draw_arrow(painter, self.begin_draw, current_point)
        finally:
            painter.end()

    def _handle_selection_end(self) -> None:
        """Handle end of selection operation"""
        self.is_selecting = False
        self.selection_rect = QRect(self.begin, self.end).normalized()
        
        # Validate selection size
        if not ImageProcessor.validate_selection_size(
            self.selection_rect.width(), self.selection_rect.height(),
            AppSettings.MIN_SELECTION_WIDTH, AppSettings.MIN_SELECTION_HEIGHT
        ):
            self.close()
            return
            
        # Initialize drawing canvas
        self.drawing_pixmap = QPixmap(self.selection_rect.size())
        self.drawing_pixmap.fill(Qt.GlobalColor.transparent)
        
        # Reset counter for new selection
        self.counter_value = 0
        
        # Show tools
        self._show_tools()
        self.update()

    def _show_tools(self) -> None:
        """Show the editing toolbar"""
        if not self.tools_widget:
            self.tools_widget = EditToolbar(self)
            self._connect_toolbar_signals()

        # Position toolbar
        self._position_toolbar()
        self.tools_widget.show()

    def _connect_toolbar_signals(self) -> None:
        """Connect toolbar signals"""
        if self.tools_widget:
            self.tools_widget.tool_selected.connect(self.set_tool)
            self.tools_widget.save.connect(self.save_image)
            self.tools_widget.copy.connect(self.copy_to_clipboard)
            self.tools_widget.undo.connect(self.undo)
            self.tools_widget.redo.connect(self.redo)
            self.tools_widget.close_app.connect(self._delayed_close)
            self.tools_widget.settings_clicked.connect(self._show_settings)

    def _position_toolbar(self) -> None:
        """Position toolbar near selection"""
        if not self.tools_widget:
            return
            
        x = self.selection_rect.left()
        y = self.selection_rect.bottom() + 5
        
        # Adjust if toolbar goes off-screen
        if y + self.tools_widget.height() > self.height():
            y = self.selection_rect.top() - self.tools_widget.height() - 5
        if x + self.tools_widget.width() > self.width():
            x = self.width() - self.tools_widget.width() - 5

        self.tools_widget.move(x, y)

    def _create_text_input(self, pos: QPoint) -> None:
        """Create text input widget at position"""
        self.text_input = QLineEdit(self)
        
        # Setup font and size
        font = QFont(self.current_font)
        font_size = calculate_font_size(
            AppSettings.FONT_SIZE_BASE, self.current_thickness, 
            AppSettings.FONT_SIZE_MULTIPLIER
        )
        font.setPointSize(font_size)
        self.text_input.setFont(font)
        
        # Calculate size
        metrics = QFontMetrics(font)
        padding = AppSettings.TEXT_INPUT_PADDING
        self.text_input.setFixedSize(
            AppSettings.TEXT_INPUT_WIDTH, 
            metrics.height() + 2 * padding
        )
        self.text_input_size = self.text_input.size()
        
        # Setup styling
        color = QColor(self.current_color)
        border_color = Colors.get_border_color(color)
        contrasting_color = Colors.get_contrasting_color(color)
        
        self.text_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {AppSettings.TEXT_INPUT_BACKGROUND};
                border: 1px solid {border_color.name()};
                color: {color.name()};
                padding: {padding}px;
            }}
        """)
        self.text_input.setAlignment(self.current_alignment)
        
        # Position and show
        self.text_input.move(pos)
        self.text_input.editingFinished.connect(self._finalize_text_input)
        self.text_input.show()
        self.text_input.setFocus()

    def _finalize_text_input(self) -> None:
        """Finalize text input and draw text to canvas"""
        if not self.text_input:
            return
            
        text = self.text_input.text()
        pos_global = self.text_input.pos()
        font = QFont(self.current_font)
        
        # Disconnect signal to prevent re-entrancy
        safe_disconnect(self.text_input.editingFinished, self._finalize_text_input)
        
        # Cleanup widget
        self.text_input.deleteLater()
        self.text_input = None
        
        # Draw text if not empty
        if text:
            self._draw_text_to_canvas(text, pos_global, font)
        else:
            self.text_input_size = QSize()

    def _draw_text_to_canvas(self, text: str, pos_global: QPoint, font: QFont) -> None:
        """Draw text to the drawing canvas"""
        self._save_history()
        
        # Calculate position relative to selection and handle alignment
        pos_relative = pos_global - self.selection_rect.topLeft()
        text_rect = QRect(pos_relative, self.text_input_size)
        self.text_input_size = QSize() # Reset after use
        
        # Draw text
        text_tool = ToolFactory.create_tool('text', self.current_color, 
                                           self.current_thickness, font)
        if text_tool:
            painter = QPainter(self.drawing_pixmap)
            try:
                # Pass alignment to the drawing tool
                text_tool.draw_text(painter, text_rect, text, self.current_alignment)
            finally:
                painter.end()
            self.update()

    # Tool and settings methods
    def set_tool(self, tool: str) -> None:
        """Set current drawing tool"""
        if self.text_input:
            self._finalize_text_input()
            
        self.current_tool = tool
        cursor = (Qt.CursorShape.IBeamCursor if tool == 'text' 
                 else Qt.CursorShape.CrossCursor)
        self.setCursor(cursor)

        if self.settings_dialog:
            self.settings_dialog.set_text_tool_mode(tool == 'text')

    def set_color(self, color) -> None:
        """Set current drawing color"""
        if color and QColor(color).isValid():
            self.current_color = QColor(color)
            if self.settings_dialog:
                self.settings_dialog.update_color_button(self.current_color)

    def set_thickness(self, value: int) -> None:
        """Set current line thickness"""
        self.current_thickness = value
        if self.settings_dialog:
            self.settings_dialog.update_thickness_slider(value)

    def set_font(self, font: QFont) -> None:
        """Set current font"""
        self.current_font = font
        if self.settings_dialog:
            self.settings_dialog.update_font_widgets(font)

    def set_alignment(self, alignment: Qt.AlignmentFlag) -> None:
        """Set current text alignment"""
        self.current_alignment = alignment
        if self.settings_dialog:
            self.settings_dialog.update_alignment_buttons(alignment)

    def _save_history(self) -> None:
        """Save current state to history for undo"""
        self.history.append(self.drawing_pixmap.copy())
        if len(self.history) > AppSettings.MAX_UNDO_HISTORY:
            self.history.pop(0)
        self.redo_history.clear()

    def undo(self) -> None:
        """Undo last drawing operation"""
        if self.history:
            self.redo_history.append(self.drawing_pixmap.copy())
            self.drawing_pixmap = self.history.pop()
            self.update()

    def redo(self) -> None:
        """Redo last drawing operation"""
        if self.redo_history:
            self.history.append(self.drawing_pixmap.copy())
            self.drawing_pixmap = self.redo_history.pop()
            self.update()

    def _show_settings(self) -> None:
        """Show settings dialog"""
        if not self.settings_dialog:
            self.settings_dialog = SettingsDialog(self)
            self.settings_dialog.color_changed.connect(self.set_color)
            self.settings_dialog.thickness_changed.connect(self.set_thickness)
            self.settings_dialog.font_changed.connect(self.set_font)
            self.settings_dialog.alignment_changed.connect(self.set_alignment)
            self.settings_dialog.finished.connect(self._settings_dialog_closed)

        # Update settings dialog for current tool
        self.settings_dialog.set_text_tool_mode(self.current_tool == 'text')

        # Position dialog
        if self.tools_widget:
            toolbar_pos = self.tools_widget.mapToGlobal(
                self.tools_widget.rect().topRight()
            )
            self.settings_dialog.move(toolbar_pos.x() + 10, toolbar_pos.y())
        
        self.settings_dialog.show()
        self.settings_dialog.activateWindow()

    def _settings_dialog_closed(self) -> None:
        """Handle settings dialog closure"""
        self.settings_dialog = None

    # Action methods
    def get_final_image(self) -> QPixmap:
        """Get final combined image"""
        base_pixmap = self.full_screenshot.copy(self.selection_rect)
        return ImageProcessor.combine_layers(base_pixmap, self.drawing_pixmap)

    def save_image(self) -> None:
        """Save image to file"""
        try:
            final_image = self.get_final_image()
            path, _ = QFileDialog.getSaveFileName(
                self, Messages.SAVE_DIALOG_TITLE, "", FileFormats.SAVE_FILTERS
            )
            if path:
                final_image.save(path)
                self.close()
        except Exception as e:
            print(f"{Messages.ERROR_SAVING_IMAGE}: {e}")

    def copy_to_clipboard(self) -> None:
        """Copy image to clipboard"""
        try:
            self._disconnect_toolbar_signals()
            final_image = self.get_final_image()
            QApplication.clipboard().setPixmap(final_image)
            self._delayed_close()
        except Exception as e:
            print(f"{Messages.ERROR_COPYING_CLIPBOARD}: {e}")
            self._disconnect_toolbar_signals()
            self._delayed_close()

    def _disconnect_toolbar_signals(self) -> None:
        """Safely disconnect toolbar signals"""
        if self.tools_widget:
            self.tools_widget.hide()
            # Disconnect all signals
            for signal_name in ['close_app', 'copy', 'save', 'undo', 'redo',
                               'tool_selected', 'settings_clicked']:
                signal = getattr(self.tools_widget, signal_name, None)
                if signal:
                    try:
                        signal.disconnect()
                    except TypeError:
                        pass

    def _delayed_close(self) -> None:
        """Close with delay to allow events to complete"""
        QTimer.singleShot(AppSettings.CLOSE_DELAY_MS, self.close)
