# Snipedit

<!-- Thêm ảnh GIF demo sản phẩm của bạn ở đây để README thêm sinh động -->
![Demo](https://example.com/demo.gif)

## Tính năng chính

Các tính năng được xây dựng dựa trên sự tiện lợi và tốc độ, giúp bạn xử lý ảnh chụp màn hình một cách nhanh chóng.

*   **Chụp ảnh theo vùng tùy chọn**: Khởi chạy ứng dụng, màn hình sẽ mờ đi và bạn chỉ cần kéo chuột để chọn vùng muốn chụp.
*   **Chỉnh sửa tức thì (In-app Editing)**: Một bộ công cụ chỉnh sửa sẽ xuất hiện ngay lập tức bên cạnh vùng bạn chọn.
*   **Bộ công cụ đa dạng**:
    *   **Pencil**: Vẽ tự do lên ảnh.
    *   **Line**: Kẻ đường thẳng.
    *   **Arrow**: Vẽ mũi tên để chỉ dẫn.
    *   **Rectangle / Circle**: Vẽ các hình khối cơ bản.
    *   **Marker**: Công cụ tô sáng/đánh dấu.
    *   **Counter Bubble**: Tự động thêm các số thứ tự (1, 2, 3...) để đánh dấu các bước.
    *   **Pixelate / Blur**: Làm mờ hoặc che đi các thông tin nhạy cảm.
    *   **Text**: Thêm chú thích văn bản vào ảnh.
*   **Tùy chỉnh công cụ**:
    *   **Color Picker**: Thay đổi màu sắc cho các công cụ vẽ.
    *   **Thickness**: Điều chỉnh độ dày/mỏng của nét vẽ.
*   **Hành động nhanh**:
    *   **Save**: Lưu ảnh chụp dưới dạng file (`.png`, `.jpg`).
    *   **Copy to Clipboard**: Sao chép ảnh vào bộ nhớ tạm để dán vào nơi khác (chat, email, ...).
*   **Phím tắt tiện lợi**:
    *   `Ctrl + S`: Lưu ảnh.
    *   `Ctrl + C`: Sao chép vào clipboard.
    *   `Ctrl + Z`: Hoàn tác (Undo) thao tác chỉnh sửa cuối cùng.
    *   `Esc`: Hủy bỏ thao tác chụp.

## Công nghệ sử dụng

*   **Ngôn ngữ**: Python 3 (3.10.11)
*   **Framework Giao diện**: PyQt6 (hoặc PySide6)
*   **Thư viện hỗ trợ**: Pillow (PIL Fork) để xử lý ảnh.

## Cài đặt

Để chạy dự án trên máy của bạn, hãy làm theo các bước sau:

1.  **Clone repository về máy:**
    ```
    git clone https://github.com/[tên-tài-khoản-của-bạn]/[tên-dự-án].git
    cd [tên-dự-án]
    ```

2.  **Tạo và kích hoạt môi trường ảo (khuyến khích):**
    ```
    # Dành cho macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # Dành cho Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Cài đặt các thư viện cần thiết:**
    ```
    pip install -r requirements.txt
    ```
    *(Ghi chú: File `requirements.txt` của bạn nên chứa các dòng như `PyQt6` và `Pillow`)*

## Sử dụng

Để khởi chạy ứng dụng, chạy lệnh sau trong thư mục gốc của dự án:

```
python main.py
```

## Tác giả

*   **HoaNT** - *Phát triển ban đầu*

