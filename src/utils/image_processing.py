"""
Image processing utilities for Snip & Edit
"""
from typing import Tuple
from PyQt6.QtGui import QPixmap, QImage, QPainter
from PyQt6.QtCore import QRect
from PIL import Image, ImageDraw


class ImageProcessor:
    """Image processing operations"""
    
    @staticmethod
    def pixelate_region(original_pixmap: QPixmap, selection_rect: QRect, 
                       pixelate_rect: QRect, pixel_size: int) -> QPixmap:
        """
        Apply pixelation effect to a specific region of the image
        
        Args:
            original_pixmap: Original screenshot pixmap
            selection_rect: Overall selection rectangle
            pixelate_rect: Rectangle to pixelate (relative to selection)
            pixel_size: Size of pixelation effect
            
        Returns:
            QPixmap with pixelated region applied to drawing canvas
        """
        # Get the part of the screenshot to pixelate
        screenshot_crop = original_pixmap.copy(selection_rect)
        qimage = screenshot_crop.toImage().convertToFormat(QImage.Format.Format_RGB888)

        # Convert to PIL Image
        buffer = qimage.bits().asstring(qimage.sizeInBytes())
        pil_img = Image.frombytes('RGB', (qimage.width(), qimage.height()), buffer, 'raw', 'RGB')

        # Crop the region to pixelate
        crop_rect = pixelate_rect.normalized()
        if (crop_rect.x() >= pil_img.width or crop_rect.y() >= pil_img.height or
            crop_rect.right() <= 0 or crop_rect.bottom() <= 0):
            # Invalid crop region
            return QPixmap()
            
        # Ensure crop coordinates are within image bounds
        x1 = max(0, crop_rect.x())
        y1 = max(0, crop_rect.y())
        x2 = min(pil_img.width, crop_rect.right())
        y2 = min(pil_img.height, crop_rect.bottom())
        
        if x2 <= x1 or y2 <= y1:
            return QPixmap()
            
        cropped = pil_img.crop((x1, y1, x2, y2))

        # Apply pixelation
        pixelated = Image.new('RGB', cropped.size)
        draw = ImageDraw.Draw(pixelated)

        for i in range(0, cropped.width, pixel_size):
            for j in range(0, cropped.height, pixel_size):
                # Get the top-left pixel of the block
                box = (i, j, i + pixel_size, j + pixel_size)
                # Ensure the box does not exceed image bounds
                clamped_box = (box[0], box[1], min(box[2], cropped.width), min(box[3], cropped.height))
                
                # Get the average color of the box
                region = cropped.crop(clamped_box)
                
                # Calculate average color
                # The 'getcolors' method returns a list of (count, color) tuples.
                # If the region is small, it's efficient.
                colors = region.getcolors(region.width * region.height)
                if colors:
                    dominant_color = max(colors, key=lambda item: item[0])[1]
                else:
                    # Fallback for complex regions, get the top-left pixel color
                    dominant_color = region.getpixel((0, 0))

                # Fill the block with the dominant color
                draw.rectangle(box, fill=dominant_color)

        # Convert back to QImage
        pil_img_bytes = pixelated.tobytes('raw', 'RGB')
        result_qimage = QImage(pil_img_bytes, pixelated.width, pixelated.height, 
                              QImage.Format.Format_RGB888)
        
        # Create a pixmap for the drawing canvas
        result_pixmap = QPixmap(crop_rect.size())
        result_pixmap.fill()
        
        painter = QPainter(result_pixmap)
        try:
            painter.drawImage(0, 0, result_qimage)
        finally:
            painter.end()
            
        return result_pixmap
    
    @staticmethod
    def combine_layers(base_pixmap: QPixmap, drawing_pixmap: QPixmap) -> QPixmap:
        """
        Combine base image with drawing layer
        
        Args:
            base_pixmap: Base image
            drawing_pixmap: Drawing layer to overlay
            
        Returns:
            Combined QPixmap
        """
        result = base_pixmap.copy()
        painter = QPainter(result)
        try:
            painter.drawPixmap(0, 0, drawing_pixmap)
        finally:
            painter.end()
        return result
    
    @staticmethod
    def validate_selection_size(width: int, height: int, 
                               min_width: int, min_height: int) -> bool:
        """
        Validate if selection size is large enough
        
        Args:
            width: Selection width
            height: Selection height
            min_width: Minimum required width
            min_height: Minimum required height
            
        Returns:
            True if selection is valid, False otherwise
        """
        return width >= min_width and height >= min_height
