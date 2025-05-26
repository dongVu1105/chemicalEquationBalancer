# chemicalEquationBalancer

Đây là một ứng dụng Python để cân bằng các phương trình hóa học. Ứng dụng sử dụng thư viện `tkinter` để tạo giao diện người dùng đồ họa (GUI).

## Chức năng chính

-   Nhận một phương trình hóa học dưới dạng chuỗi ký tự.
-   Phân tích và biểu diễn phương trình dưới dạng ma trận.
-   Sử dụng phương pháp khử Gauss để giải hệ phương trình và tìm ra các hệ số cân bằng.
-   Hiển thị phương trình đã được cân bằng trên giao diện người dùng.
-   Lưu trữ lịch sử các phương trình đã được cân bằng.

## Cấu trúc dự án

Tệp tin chính của dự án là `chemical_equation_text.py`, bao gồm các thành phần sau:

-   **Các hàm xử lý logic:**
    -   `parse_compound`: Phân tích cú pháp một hợp chất hóa học.
    -   `matrix`: Chuyển đổi một phương trình hóa học thành dạng ma trận.
    -   `solve`: Giải ma trận để tìm các hệ số cân bằng.
    -   `pthh`: Hàm chính điều phối quá trình từ việc nhận chuỗi phương trình đầu vào đến việc trả về phương trình đã được cân bằng.
-   **Lớp giao diện người dùng:**
    -   `ChemicalEquationBalancerApp`: Xây dựng và quản lý giao diện người dùng đồ họa (GUI) bằng `tkinter`, xử lý tương tác của người dùng.

