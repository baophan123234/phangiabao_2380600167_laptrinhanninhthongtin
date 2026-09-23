# 🛡️ Giải thích Test Case - Lab 1 

## 1. Kiểm tra Email (Email Validation)
> **Cơ chế:** Sử dụng Biểu thức chính quy (Regex) để đảm bảo đầu vào đúng chuẩn định dạng của một email.

✅ **Hợp lệ:** `sinhvien123@truongdaihoc.edu.vn`
* **Kết quả:** `True`
* **Giải thích:** Tuân thủ hoàn toàn định dạng `tên@tên_miền.mở_rộng`. Chỉ chứa các ký tự hợp lệ (chữ, số, dấu chấm, @).

❌ **Từ chối:** `sinhvien @gmail.com`
* **Kết quả:** `False`
* **Giải thích:** Chuỗi này có chứa dấu cách (khoảng trắng). Hàm Regex `^[\w\.-]+@[\w\.-]+\.\w+$` sẽ bắt lỗi và từ chối đầu vào này.

---

## 2. Kiểm tra URL (URL Validation)
> **Cơ chế:** Phân tích đường dẫn URL để ngăn chặn các cuộc tấn công SSRF (Server-Side Request Forgery) hoặc truy cập file nội bộ.

✅ **Hợp lệ:** `http://localhost:8000/api/data`
* **Kết quả:** `True`
* **Giải thích:** Sử dụng giao thức web chuẩn (`http://`) và có địa chỉ máy chủ rõ ràng. Đây là một URL web an toàn.

❌ **Từ chối:** `file:///C:/Windows/System32/cmd.exe`
* **Kết quả:** `False`
* **Giải thích:** Sử dụng giao thức `file://` hòng lừa máy chủ đọc file cục bộ nhạy cảm trên hệ thống. Ứng dụng chặn lại vì chỉ cho phép `http` và `https`.

---

## 3. Kiểm tra Tên File (Filename Validation)
> **Cơ chế:** Bảo vệ máy chủ khỏi lỗi **Path Traversal** (Duyệt thư mục trái phép).

✅ **Hợp lệ:** `huong_dan_su_dung.docx`
* **Kết quả:** `True`
* **Giải thích:** Là một tên file thuần túy, không chứa các ký tự điều hướng thư mục.

❌ **Từ chối:** `..\..\..\Windows\System32\config\SAM`
* **Kết quả:** `False`
* **Giải thích:** Chứa ký tự `..\` hòng thoát khỏi thư mục an toàn, lùi về thư mục gốc để đọc file `SAM` (chứa mật khẩu Windows). Bị vô hiệu hóa vì chứa `.` và `\`.

---

## 4. Lọc Dữ liệu SQL (SQL Injection Sanitization)
> **Cơ chế:** Lọc các từ khóa và ký tự nguy hiểm nhằm tránh truy vấn cơ sở dữ liệu bị bóp méo (Tấn công SQL Injection).

✅ **Hợp lệ:** `Tran Van Teo 2023`
* **Kết quả:** `Tran Van Teo 2023`
* **Giải thích:** Văn bản bình thường không chứa ký tự SQL, được giữ nguyên.

❌ **Bị lọc:** `" UNION SELECT username, password FROM users; --`
* **Kết quả:** `username, password FROM users`
* **Giải thích:** Kẻ tấn công dùng `"` đóng chuỗi, `UNION SELECT` lấy cắp dữ liệu, `--` để comment. Hàm đã nhận diện và xóa sổ các từ khóa `"`, `;`, `UNION`, `SELECT` và `--`.

---

## 5. Lọc Dữ liệu HTML (XSS Sanitization)
> **Cơ chế:** Sử dụng kỹ thuật *HTML Escaping* để phòng chống lỗ hổng **Cross-Site Scripting (XSS)**.

✅ **Hợp lệ:** `Van ban thuong khong chua ma HTML`
* **Kết quả:** `Van ban thuong khong chua ma HTML`
* **Giải thích:** Văn bản thuần túy không chứa thẻ HTML, hiển thị bình thường.

❌ **Mã hóa:** `<img src="x" onerror="alert('Hacked')">`
* **Kết quả:** `&lt;img src=&quot;x&quot; onerror=&quot;alert(&#x27;Hacked&#x27;)&quot;&gt;`
* **Giải thích:** Dùng thẻ ảnh lỗi để lén chạy Javascript. Hàm `html.escape` đã biến `<` thành `&lt;`, `"` thành `&quot;`, khiến mã độc trở thành dòng chữ vô hại.
