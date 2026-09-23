# BÁO CÁO THỰC HÀNH LAB 3 
**1. Khởi tạo cấu trúc và tái sử dụng module**
- Tái sử dụng lại thư mục `securevalidator` từ Lab 1 (chứa các hàm làm sạch dữ liệu đầu vào như `validate_email`, `sanitize_sql_input`).
- Khởi tạo thư mục `securelogger` chứa logic xử lý log an toàn. Cấu hình gói thư viện thông qua `requirements.txt`.

**2. Xây dựng Secure Logger (`logger.py`)**
Em đã triển khai 4 kỹ thuật bảo mật log cốt lõi trong file này:
- **Masking PII (Che giấu thông tin cá nhân):** Sử dụng hàm `mask_pii()` kết hợp Regex để quét mọi tin nhắn log trước khi ghi. Các chuỗi giống email, password, apikey tự động bị thay thế bằng thẻ `<email_masked>`, `<token_masked>`.
- **JSON Formatting:** Sử dụng `JSONFormatter` để chuẩn hóa toàn bộ log dưới dạng JSON thay vì text thuần, giúp các hệ thống phân tích log (như ELK stack) dễ dàng đọc hiểu và tránh lỗi Log Injection (Chèn mã vào nhật ký).
- **Tamper Detection (Chống giả mạo):** Mỗi khi một dòng log được ghi, hàm `append_signature()` sẽ băm (Hash SHA256) nội dung dòng đó và ghi mã băm vào file `secure.log.sig`. Việc này giúp phát hiện ngay lập tức nếu kẻ xấu lén lút sửa đổi nội dung file log để xóa dấu vết.
- **Log Rotation & GZip:** Sử dụng `SecureRotatingFileHandler` và `GZipRotator` để tự động cắt file log sang file mới khi dung lượng vượt quá 1MB, đồng thời nén file cũ lại bằng `.gz` để tiết kiệm dung lượng lưu trữ.

**3. Tích hợp Backend API (`app.py`)**
Khởi tạo một API `/validate` bằng Flask. API này có nhiệm vụ tiếp nhận chuỗi JSON từ người dùng, đưa qua bộ lọc `securevalidator` để làm sạch, và gọi `secure_logger` để ghi lại nhật ký (cả dữ liệu đầu vào và kết quả đầu ra).

- Khởi động thành công máy chủ Flask tại `localhost:5000`.
- Sử dụng Postman (hoặc công cụ gửi Request tương đương) để gửi một gói tin JSON chứa dữ liệu thử nghiệm (bao gồm email thật, mã SQL Injection `OR 1=1 --`, và mã XSS `<script>alert(1)</script>`).
- **Kết quả:** Hệ thống đã trả về kết quả Validation thành công (Mã HTTP 200). 
- Kiểm tra file `secure.log`, toàn bộ Payload đầu vào đã được ghi lại bằng cấu trúc JSON, trong đó giá trị Email đã bị che giấu hoàn hảo thành `<email_masked>`. Kèm theo đó là file `secure.log.sig` chứa chữ ký mã băm tương ứng.


