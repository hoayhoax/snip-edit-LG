"""
Drawing tools for the capture editor
"""
import math
from typing import Optional
from PyQt6.QtGui import QPainter, QPen, QColor, QFont
from PyQt6.QtCore import QPoint, QRect, Qt
from ..config.settings import AppSettings
from ..utils.helpers import calculate_font_size


class DrawingTool:
    """Base class for drawing tools"""
    
    def __init__(self, color: QColor, thickness: int):
        self.color = color
        self.thickness = thickness
    
    def setup_painter(self, painter: QPainter) -> None:
        """Setup painter with tool-specific settings"""
        pen = QPen(self.color, self.thickness)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)


class PenTool(DrawingTool):
    """Pencil/pen drawing tool"""
    
    def draw_line(self, painter: QPainter, start: QPoint, end: QPoint) -> None:
        """Draw a line from start to end point"""
        self.setup_painter(painter)
        painter.drawLine(start, end)


class MarkerTool(DrawingTool):
    """Highlighter/marker tool with transparency"""
    
    def setup_painter(self, painter: QPainter) -> None:
        """Setup painter with marker-specific settings"""
        color = QColor(self.color)
        marker_color = QColor(color.red(), color.green(), color.blue(), 
                             AppSettings.MARKER_ALPHA)
        pen = QPen(marker_color, self.thickness)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    def draw_line(self, painter: QPainter, start: QPoint, end: QPoint) -> None:
        """Draw a marker line from start to end point"""
        self.setup_painter(painter)
        painter.drawLine(start, end)


class LineTool(DrawingTool):
    """Straight line drawing tool"""
    
    def draw_line(self, painter: QPainter, start: QPoint, end: QPoint) -> None:
        """Draw a straight line from start to end point"""
        self.setup_painter(painter)
        painter.drawLine(start, end)


class RectangleTool(DrawingTool):
    """Rectangle drawing tool"""
    
    def draw_rectangle(self, painter: QPainter, start: QPoint, end: QPoint) -> None:
        """Draw a rectangle from start to end point"""
        self.setup_painter(painter)
        rect = QRect(start, end)
        painter.drawRect(rect)


class CircleTool(DrawingTool):
    """Circle/ellipse drawing tool"""
    
    def draw_circle(self, painter: QPainter, start: QPoint, end: QPoint) -> None:
        """Draw a circle/ellipse from start to end point"""
        self.setup_painter(painter)
        rect = QRect(start, end)
        painter.drawEllipse(rect)


class ArrowTool(DrawingTool):
    """Arrow drawing tool"""
    
    def draw_arrow(self, painter: QPainter, start: QPoint, end: QPoint) -> None:
        """Draw an arrow from start to end point"""
        self.setup_painter(painter)
        
        # Draw main line
        painter.drawLine(start, end)
        
        # Calculate arrow head
        line_angle = math.atan2(end.y() - start.y(), end.x() - start.x())
        arrow_size = self.thickness * AppSettings.ARROW_SIZE_MULTIPLIER
        arrow_angle = AppSettings.ARROW_ANGLE
        
        # Arrow head points
        arrow_point1 = QPoint(
            int(end.x() - arrow_size * math.cos(line_angle - arrow_angle)),
            int(end.y() - arrow_size * math.sin(line_angle - arrow_angle))
        )
        arrow_point2 = QPoint(
            int(end.x() - arrow_size * math.cos(line_angle + arrow_angle)),
            int(end.y() - arrow_size * math.sin(line_angle + arrow_angle))
        )
        
        # Draw arrow head
        painter.drawLine(end, arrow_point1)
        painter.drawLine(end, arrow_point2)


class TextTool:
    """Text drawing tool"""
    
    def __init__(self, color: QColor, font: QFont):
        self.color = color
        self.font = font
    
    def draw_text(self, painter: QPainter, text_rect: QRect, text: str, 
                  alignment: Qt.AlignmentFlag) -> None:
        """Draw text at the specified position"""
        painter.setFont(self.font)
        painter.setPen(QPen(self.color))
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Add padding to match the QLineEdit
        padding = AppSettings.TEXT_INPUT_PADDING
        padded_rect = text_rect.adjusted(padding, padding, -padding, -padding)
        
        # Combine horizontal and vertical alignment
        final_alignment = alignment | Qt.AlignmentFlag.AlignVCenter
        
        painter.drawText(padded_rect, int(final_alignment), text)


class CounterTool(DrawingTool):
    """Counter bubble drawing tool"""

    def __init__(self, color: QColor, thickness: int, font: QFont):
        super().__init__(color, thickness)
        self.font = font

    def draw_counter_bubble(self, painter: QPainter, position: QPoint, number: int) -> None:
        """Draw a counter bubble with a number"""
        self.setup_painter(painter)
        
        # Calculate bubble size based on thickness
        radius = self.thickness * AppSettings.COUNTER_SIZE_MULTIPLIER
        
        # Draw circle
        painter.setBrush(self.color)
        painter.drawEllipse(position, int(radius), int(radius))
        
        # Adjust font size based on thickness
        dynamic_font_size = calculate_font_size(
            AppSettings.DEFAULT_FONT_SIZE, 
            self.thickness, 
            AppSettings.FONT_SIZE_MULTIPLIER
        )
        self.font.setPointSize(dynamic_font_size)
        painter.setFont(self.font)
        
        # Draw text
        text_pen = QPen(QColor("white")) # White text for contrast
        painter.setPen(text_pen)
        
        # Center text in the circle
        text_rect = QRect(
            int(position.x() - radius), int(position.y() - radius),
            int(radius * 2), int(radius * 2)
        )
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, str(number))


class ToolFactory:
    """Factory for creating drawing tools"""
    
    @staticmethod
    def create_tool(tool_type: str, color: QColor, thickness: int, 
                   font: Optional[QFont] = None) -> Optional[DrawingTool]:
        """
        Create a drawing tool of the specified type
        
        Args:
            tool_type: Type of tool to create
            color: Drawing color
            thickness: Line thickness
            font: Font for text tool (optional)
            
        Returns:
            Drawing tool instance or None if tool type is invalid
        """
        tool_map = {
            'pen': PenTool,
            'marker': MarkerTool,
            'line': LineTool,
            'rect': RectangleTool,
            'circle': CircleTool,
            'arrow': ArrowTool,
        }
        
        if tool_type == 'text' and font:
            return TextTool(color, font)
        if tool_type == 'counter' and font:
            return CounterTool(color, thickness, font)
        
        tool_class = tool_map.get(tool_type)
        if tool_class:
            return tool_class(color, thickness)
        
        return None
