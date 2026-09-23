# BÁO CÁO THỰC HÀNH LAB 2 
**1. Khởi tạo và Cấu hình Git Hook**
- Thay vì dùng thư mục mặc định ẩn bên trong `.git/hooks`, em đã tạo thư mục `.githooks` ở ngay thư mục gốc để dễ dàng đồng bộ và quản lý chung với dự án.
- Chạy lệnh `git config core.hooksPath .githooks` để yêu cầu Git trỏ tiến trình thực thi hook về thư mục mới này.

**2. Xây dựng Kịch bản quét lỗi (pre-commit script)**
Em đã lập trình một file kịch bản bằng Python đóng vai trò như một "người gác cổng", có nhiệm vụ kiểm tra tất cả các file đang ở trạng thái chờ commit (`git diff --cached`). Script này tập trung vào 3 lớp phòng thủ:
- **Kiểm tra thông tin nhạy cảm:** Ứng dụng Biểu thức chính quy (Regex) để tự động nhận diện mọi chuỗi ký tự có cấu trúc giống với `password`, `secret`, `apikey` hoặc `AWS Token`.
- **Kiểm tra phân quyền (Permissions):** Quét xem file có bị lỗi gán quyền quá mức (*world-writable* - cho phép bất kỳ ai cũng có thể ghi) hay không.
- **Phân tích mã độc tĩnh:** Tích hợp công cụ `bandit` (đã cài đặt qua `requirements.txt`). Nếu `bandit` phát hiện lỗ hổng ở mức độ nghiêm trọng cao (*High Severity*), tiến trình sẽ bị chặn.

**3. Cơ chế Xử lý Vi phạm**
Nếu mã nguồn vi phạm bất kỳ lớp phòng thủ nào ở trên, script sẽ lập tức:
- In ra màn hình console dòng cảnh báo **`COMMIT BLOCKED by GitSecure`**.
- Lưu lại nhật ký lỗi chi tiết kèm thời gian vào file `gitsecure.log`.
- Gọi hàm `sys.exit(1)` để hủy bỏ ngay lập tức lệnh commit của lập trình viên.

Để kiểm chứng hệ thống, tạo một file giả lập mang tên `bad.py` và cố ý khai báo một đoạn mã lỗi: `password = "123456"`.
- **Lần 1 (Thử nghiệm chặn lỗi):** Khi chạy lệnh `git commit`, hệ thống đã lập tức phát hiện biến `password`, chặn đứng tiến trình và hiển thị thông báo lỗi. Log cũng được ghi nhận thành công.
- **Lần 2 (Thử nghiệm an toàn):** Sau khi xóa bỏ chuỗi mật khẩu trong file `bad.py`, mã nguồn đã vượt qua bài kiểm tra (nhận thông báo `All checks passed`) và được lưu vào kho lưu trữ Git an toàn. Ngoài ra, file nhật ký `gitsecure.log` cũng đã được đưa vào `.gitignore` để repo luôn được dọn dẹp sạch sẽ.
