import unittest
from securevalidator import (
    validate_email, validate_url, validate_filename,
    sanitize_sql_input, sanitize_html_input
)

class TestValidators(unittest.TestCase):
    def setUp(self):
        print("\n Running:", self._testMethodName)

    def test_validate_email_valid(self):
        self.assertTrue(validate_email("sinhvien123@truongdaihoc.edu.vn"))

    def test_validate_email_invalid(self):
        self.assertFalse(validate_email("sinhvien @gmail.com"))

    def test_validate_url_valid(self):
        self.assertTrue(validate_url("http://localhost:8000/api/data"))

    def test_validate_url_invalid(self):
        self.assertFalse(validate_url("file:///C:/Windows/System32/cmd.exe"))

    def test_validate_filename_valid(self):
        self.assertTrue(validate_filename("huong_dan_su_dung.docx"))

    def test_validate_filename_traversal(self):
        self.assertFalse(validate_filename("..\\..\\..\\Windows\\System32\\config\\SAM"))

    def test_sanitize_sql_input_injection(self):
        input_str = '" UNION SELECT username, password FROM users; --'
        sanitized = sanitize_sql_input(input_str)
        self.assertNotIn('"', sanitized)
        self.assertNotIn(";", sanitized)
        self.assertNotIn("UNION", sanitized.upper())
        self.assertNotIn("--", sanitized)
        
    def test_sanitize_sql_input_safe_text(self):
        input_str = "Tran Van Teo 2023"
        sanitized = sanitize_sql_input(input_str)
        self.assertEqual(sanitized, "Tran Van Teo 2023")

    def test_sanitize_html_input_script(self):
        input_str = '<img src="x" onerror="alert(\'Hacked\')">'
        sanitized = sanitize_html_input(input_str)
        self.assertEqual(sanitized, '&lt;img src=&quot;x&quot; onerror=&quot;alert(&#x27;Hacked&#x27;)&quot;&gt;')

    def test_sanitize_html_input_safe_text(self):
        input_str = "Van ban thuong khong chua ma HTML"
        sanitized = sanitize_html_input(input_str)
        self.assertEqual(sanitized, "Van ban thuong khong chua ma HTML")
