import base64
import hashlib
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def _key(secret_key: str) -> bytes:
    return hashlib.sha256(secret_key.encode("utf-8")).digest()


def protect(value: bytes, secret_key: str) -> str:
    nonce = os.urandom(12)
    blob = nonce + AESGCM(_key(secret_key)).encrypt(nonce, value, b"vault-session-v1")
    return base64.urlsafe_b64encode(blob).decode()


def unprotect(value: str, secret_key: str) -> bytes:
    blob = base64.urlsafe_b64decode(value.encode())
    return AESGCM(_key(secret_key)).decrypt(blob[:12], blob[12:], b"vault-session-v1")
