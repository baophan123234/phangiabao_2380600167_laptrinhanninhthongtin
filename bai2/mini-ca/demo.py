import os
import sys
import io

# Fix Unicode output on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from cryptography import x509
from ca_utils import (
    create_root_ca,
    create_intermediate_ca,
    issue_certificate,
    verify_certificate_chain,
    load_cert
)
from revoke_utils import (
    revoke_certificate,
    check_revocation_status
)

root_key = None
root_cert = None
inter_key = None
inter_cert = None


def setup_ca():
    global root_key, root_cert, inter_key, inter_cert
    print("[1] Tao Root CA...")
    root_key, root_cert = create_root_ca()
    print(f"Root CA: {root_key}, {root_cert}")

    print("[2] Tao Intermediate CA...")
    inter_key, inter_cert = create_intermediate_ca(root_key, root_cert)
    print(f"Intermediate CA: {inter_key}, {inter_cert}")

    return root_key, root_cert, inter_key, inter_cert


def issue_cert_demo():
    subject_info = {
        "common_name": "Phuoc_Nguyen",
        "org": "PHUOCNTMH Company",
        "country": "VN"
    }
    print("[3] Phat hanh chung chi nguoi dung cuoi...")
    cert_key, cert = issue_certificate(inter_key, inter_cert, subject_info)
    cert_path = os.path.join("certs", f"{subject_info['common_name']}_cert.pem")
    key_path = os.path.join("certs", f"{subject_info['common_name']}_key.pem")
    print(f"Da phat hanh: {cert_path}, {key_path}")
    return cert_path


def verify_chain_demo(user_cert_path):
    print("[4] Kiem tra chuoi chung chi...")
    chain_paths = [
        os.path.join("certs", "intermediate_cert.pem"),
        os.path.join("certs", "root_ca_cert.pem")
    ]
    chain_certs = [load_cert(p) for p in chain_paths]
    user_cert = load_cert(user_cert_path)
    valid = verify_certificate_chain(user_cert, chain_certs)
    print(f"Chuoi hop le: {valid}")
    return valid


def revoke_demo():
    print("[5] Thu hoi chung chi user1...")
    revoke_certificate(
        os.path.join("certs", "Phuoc_Nguyen_cert.pem"),
        os.path.join("certs", "intermediate_cert.pem"),
        os.path.join("certs", "intermediate_key.pem"),
        reason=x509.ReasonFlags.key_compromise
    )
    print("Da thu hoi")


def ocsp_check_demo():
    print("[6] Kiem tra trang thai OCSP cua Phuoc_Nguyen_cert.pem...")
    status = check_revocation_status(os.path.join("certs", "Phuoc_Nguyen_cert.pem"))
    print(f"Trang thai: {'Revoked' if status else 'Valid'}")


def run_all():
    setup_ca()
    user_cert = issue_cert_demo()
    verify_chain_demo(user_cert)
    revoke_demo()
    ocsp_check_demo()


if __name__ == "__main__":
    run_all()
