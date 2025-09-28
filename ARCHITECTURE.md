# Cấu trúc Code - Snip & Edit

## Tổng quan về kiến trúc

Dự án đã được tái cấu trúc theo nguyên tắc **Separation of Concerns** và **Single Responsibility Principle** để dễ dàng maintain và mở rộng.

## Cấu trúc thư mục

Dưới đây là tổng quan về cấu trúc thư mục của dự án:

```
snip-edit/
├── main.py                # Điểm vào chính của ứng dụng
├── requirements.txt         # Các dependency của project
├── Readme.md                # File Readme
├── PACKAGING.md             # Hướng dẫn đóng gói ứng dụng
├── src/
│   ├── assets/              # Chứa các tài nguyên tĩnh
│   │   ├── icons/           # Chứa các file icon SVG
│   │   └── icon.ico         # Icon chính của ứng dụng
│   ├── config/              # Cấu hình
│   ├── core/                # Các thành phần cốt lõi (vd: tray manager)
│   ├── tools/               # Các công cụ vẽ
│   ├── ui/                  # Các thành phần giao diện người dùng
│   └── utils/               # Các hàm tiện ích
└── ...
```

## Chi tiết các module

### 1. `src/config/settings.py`
**Mục đích**: Quản lý tất cả cấu hình và constants của ứng dụng

**Các class chính**:
- `AppSettings`: Chứa tất cả settings mặc định
- `Colors`: Utilities để xử lý màu sắc
- `Messages`: Tất cả text và messages của ứng dụng
- `FileFormats`: Cấu hình cho file formats

**Lợi ích**:
- Dễ dàng thay đổi settings mà không cần sửa code logic
- Tập trung hóa tất cả constants
- Dễ dàng localization trong tương lai

### 2. `src/core/tray_manager.py`
**Mục đích**: Quản lý system tray và lifecycle của ứng dụng

**Tính năng**:
- Tạo và quản lý system tray icon
- Xử lý context menu
- Khởi tạo capture window
- Quản lý exit application

**Lợi ích**:
- Tách biệt logic system tray khỏi UI components
- Dễ dàng test và maintain

### 3. `src/tools/drawing_tools.py`
**Mục đích**: Implement các drawing tools theo pattern Strategy

**Các class chính**:
- `DrawingTool`: Base class cho tất cả tools
- `PenTool`, `MarkerTool`, `LineTool`, etc.: Concrete implementations
- `ToolFactory`: Factory pattern để tạo tools

**Lợi ích**:
- Dễ dàng thêm tools mới
- Code reuse và maintainability
- Separation of concerns

### 4. `src/ui/` - UI Components
**Mục đích**: Chứa tất cả UI components được tách biệt

#### `capture_window.py`
- Cửa sổ chính cho capture và editing
- Xử lý mouse events và keyboard shortcuts
- Quản lý drawing state và history

#### `edit_toolbar.py`
- Thanh công cụ với drawing tools và actions
- Sử dụng signals để giao tiếp với parent

#### `settings_dialog.py`
- Dialog cài đặt cho colors, thickness, fonts
- Non-modal dialog với real-time updates

### 5. `src/utils/` - Utilities
**Mục đích**: Chứa các helper functions và image processing

#### `helpers.py`
- Các utility functions chung
- Safe cleanup functions
- Helper calculations

#### `image_processing.py`
- Xử lý ảnh (pixelate, combine layers)
- PIL integration
- Image validation

## Nguyên tắc thiết kế đã áp dụng

### 1. **Single Responsibility Principle (SRP)**
- Mỗi class chỉ có một lý do để thay đổi
- Ví dụ: `SystemTrayManager` chỉ quản lý system tray, `CaptureWindow` chỉ xử lý capture UI

### 2. **Dependency Inversion Principle (DIP)**
- Sử dụng abstractions thay vì concrete implementations
- Ví dụ: `ToolFactory` tạo tools thông qua interface chung

### 3. **Open/Closed Principle (OCP)**
- Mở để mở rộng, đóng để sửa đổi
- Ví dụ: Thêm tool mới chỉ cần implement `DrawingTool` interface

### 4. **Separation of Concerns**
- UI logic tách biệt với business logic
- Configuration tách biệt khỏi implementation

## Type Hints và Documentation

### Type Hints
Tất cả functions và methods đều có type hints:
```python
def create_tool(tool_type: str, color: QColor, thickness: int, 
               font: Optional[QFont] = None) -> Optional[DrawingTool]:
```

### Docstrings
Tất cả classes và methods có docstrings chi tiết:
```python
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
```

## Error Handling

### Improved Error Handling
- Try-catch blocks với specific error messages
- Safe cleanup functions
- Graceful degradation

### Logging
- Consistent error messaging through `Messages` class
- Print statements for debugging (có thể thay bằng proper logging sau)

## Lợi ích của kiến trúc mới

### 1. **Maintainability**
- Code dễ đọc và hiểu
- Các components độc lập
- Dễ dàng debug và fix bugs

### 2. **Extensibility** 
- Dễ dàng thêm tools mới
- Dễ dàng thêm UI components
- Dễ dàng thay đổi cấu hình

### 3. **Testability**
- Các components có thể test riêng biệt
- Dependency injection
- Mock-friendly design

### 4. **Code Reuse**
- Shared utilities và helpers
- Factory patterns
- Base classes

### 5. **Configuration Management**
- Tập trung hóa settings
- Dễ dàng customization
- Environment-specific configs

## Hướng dẫn sử dụng

### Chạy ứng dụng mới
```bash
python main_new.py
```

### Thêm tool mới
1. Tạo class kế thừa `DrawingTool` trong `drawing_tools.py`
2. Thêm vào `ToolFactory`
3. Thêm button trong `EditToolbar`
4. Thêm label trong `Messages`

### Thay đổi cấu hình
- Chỉnh sửa các constants trong `src/config/settings.py`
- Không cần sửa code logic

### Debug
- Error messages đã được standardized
- Mỗi component có error handling riêng
- Dễ dàng trace issues

## Kết luận

Kiến trúc mới tuân theo các best practices của software engineering:
- **Clean Code**: Readable, maintainable, testable
- **SOLID Principles**: Single responsibility, Open/closed, etc.
- **Design Patterns**: Factory, Strategy, Observer (signals)
- **Type Safety**: Type hints cho tất cả interfaces
- **Documentation**: Comprehensive docstrings
