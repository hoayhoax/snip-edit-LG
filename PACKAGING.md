### Bối cảnh
*   **Tên ứng dụng:** SnipEdit
*   **File Python chính:** `main.py`
*   **Thư mục chứa tài nguyên (icon, v.v.):** `src/assets/`
*   **Icon ứng dụng:** `src/assets/icon.ico`

***

### Giai đoạn 1: Đóng gói thành file `.exe` với PyInstaller

Mục tiêu của giai đoạn này là tạo ra một file `SnipEdit.exe` duy nhất có thể chạy độc lập.

#### Bước 1: Chuẩn bị môi trường

1.  Mở Command Prompt (CMD) hoặc PowerShell.
2.  Di chuyển đến thư mục gốc của dự án của bạn:
    ```bash
    cd duong_dan_den_du_an_cua_ban
    ```
3.  Cài đặt PyInstaller nếu bạn chưa có:
    ```bash
    pip install pyinstaller
    ```

#### Bước 2: Chạy PyInstaller

1.  Thực thi lệnh sau trong terminal. Lệnh này sẽ đóng gói ứng dụng của bạn và tất cả tài nguyên đi kèm.

    ```bash
    pyinstaller --onefile --windowed --name="SnipEdit" --icon="src/assets/icon.ico" --add-data="src/assets;assets" main.py
    ```

    **Giải thích chi tiết lệnh:**
    *   `--onefile`: Gói tất cả mọi thứ (code, thư viện, Python interpreter) vào một file `.exe` duy nhất.
    *   `--windowed`: Ẩn cửa sổ dòng lệnh màu đen khi ứng dụng chạy. **Bắt buộc** cho ứng dụng giao diện.
    *   `--name="SnipEdit"`: Đặt tên cho file thực thi đầu ra là `SnipEdit.exe`.
    *   `--icon="src/assets/icon.ico"`: Gán file `src/assets/icon.ico` làm icon cho file `.exe`.
    *   `--add-data="src/assets;assets"`: **Rất quan trọng!** Lệnh này báo cho PyInstaller sao chép thư mục `src/assets` vào gói ứng dụng. Dấu chấm phẩy `;` (trên Windows) ngăn cách nguồn và đích. `src/assets;assets` có nghĩa là "sao chép thư mục `src/assets` ở nguồn vào một thư mục tên là `assets` trong gói cuối cùng", khớp với cách ứng dụng của bạn tìm kiếm tài nguyên.

2.  Đợi quá trình đóng gói hoàn tất. PyInstaller sẽ tạo ra một vài thư mục mới.

#### Bước 3: Lấy kết quả

1.  Mở thư mục `dist` vừa được tạo ra.
2.  Bên trong, bạn sẽ thấy file **`SnipEdit.exe`**. Đây chính là file ứng dụng đã được đóng gói hoàn chỉnh. Bạn có thể thử chạy nó để kiểm tra xem mọi thứ có hoạt động đúng không, bao gồm cả việc các icon chức năng có hiển thị không.

**Giai đoạn 1 hoàn tất!** Bây giờ bạn đã có một file `.exe` độc lập. Tiếp theo, chúng ta sẽ tạo một trình cài đặt chuyên nghiệp cho nó.

***

### Giai đoạn 2: Tạo trình cài đặt với Inno Setup

Mục tiêu là tạo ra một file `SnipEdit-Setup.exe` để người dùng có thể cài đặt ứng dụng một cách chuyên nghiệp.

#### Bước 1: Cài đặt và khởi chạy Inno Setup

1.  Tải và cài đặt Inno Setup từ trang chủ chính thức: [https://jrsoftware.org/isinfo.php](https://jrsoftware.org/isinfo.php).
2.  Mở Inno Setup. Một cửa sổ chào mừng sẽ hiện ra. Chọn **"Create a new script file using the Script Wizard"** và nhấn **OK**.

#### Bước 2: Sử dụng Script Wizard

Wizard sẽ dẫn bạn qua từng bước để tạo file kịch bản cài đặt (`.iss`).

1.  **Application Information:**
    *   **Application Name:** `SnipEdit`
    *   **Application Version:** `1.0.0` (hoặc phiên bản hiện tại của bạn)
    *   **Application Publisher:** `Tên của bạn hoặc công ty`
    *   **Application Website:** (Tùy chọn)
    *   Nhấn **Next**.

2.  **Application Destination:**
    *   Để các giá trị mặc định. Inno Setup sẽ tự động đề xuất cài vào `C:\Program Files (x86)\SnipEdit`.
    *   Nhấn **Next**.

3.  **Application Files:**
    *   **Application main executable file:** Nhấn **Browse...** và chọn file **`SnipEdit.exe`** bạn đã tạo ở Giai đoạn 1 (nằm trong thư mục `dist`).
    *   Nhấn **Next**.

4.  **Application Icons:**
    *   Để mặc định các tùy chọn tạo shortcut ở Start Menu.
    *   Tích vào ô **"Create a desktop icon"** nếu bạn muốn có shortcut trên màn hình desktop.
    *   Nhấn **Next**.

5.  **Application Documentation:** (Tùy chọn)
    *   Bạn có thể thêm các file như `License.txt` hoặc `Readme.md` ở bước này. Nếu không có, cứ nhấn **Next**.

6.  **Setup Languages:**
    *   Chọn `English` hoặc ngôn ngữ bạn muốn.
    *   Nhấn **Next**.

7.  **Compiler Settings:**
    *   **Custom compiler output folder:** Chọn nơi bạn muốn lưu file cài đặt cuối cùng.
    *   **Compiler output base file name:** Đặt tên cho file cài đặt, ví dụ: `SnipEdit-Setup`.
    *   **Custom Setup icon file:** (Tùy chọn) Nhấn **Browse...** và chọn lại file `src/assets/icon.ico` để file cài đặt của bạn cũng có icon đẹp.
    *   Nhấn **Next**.

8.  **Inno Setup Preprocessor:**
    *   Nhấn **Next**.

9.  **Finish:**
    *   Wizard đã hoàn tất! Nhấn **Finish**.
    *   Một cửa sổ sẽ hiện ra hỏi **"Would you like to compile the new script now?"**, chọn **Yes**.
    *   Một cửa sổ khác hỏi **"Would you like to save the script before compiling?"**, chọn **Yes**. Lưu file kịch bản `.iss` này lại để có thể chỉnh sửa và biên dịch lại sau này mà không cần chạy lại Wizard.

#### Bước 3: Biên dịch và nhận kết quả

1.  Inno Setup sẽ bắt đầu quá trình biên dịch.
2.  Khi hoàn tất, bạn sẽ thấy thông báo thành công.
3.  Tìm đến thư mục output bạn đã chọn ở Bước 2.7. Bạn sẽ thấy file **`SnipEdit-Setup.exe`**.

**Giai đoạn 2 hoàn tất!** File `SnipEdit-Setup.exe` này chính là sản phẩm cuối cùng bạn sẽ gửi cho người dùng. Khi họ chạy nó, một trình cài đặt quen thuộc sẽ hiện ra, sao chép ứng dụng vào Program Files, tạo shortcut và cung cấp tùy chọn gỡ cài đặt.
