"""
Script test nhanh 5 API endpoints cua DAST-Tool de chup anh bao cao
Cach dung:
1. Mo terminal 1, chay: python app.py
2. Mo terminal 2, chay: python test_api.py
"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_endpoints():
    endpoints = [
        ("GET", "/api/monitor", None),
        ("GET", "/api/memory", None),
        ("GET", "/api/network", None),
        ("GET", "/api/security", None),
        ("POST", "/api/sandbox", {"command": "echo Hello from DAST Sandbox API"})
    ]

    for method, path, payload in endpoints:
        print("=" * 60)
        print(f"[*] Testing {method} {BASE_URL}{path}")
        try:
            if method == "GET":
                res = requests.get(f"{BASE_URL}{path}")
            else:
                res = requests.post(f"{BASE_URL}{path}", json=payload)
            print(f"Status Code: {res.status_code}")
            print("Response JSON:")
            print(json.dumps(res.json(), indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"Error: {e}")
        print()

if __name__ == "__main__":
    test_endpoints()
