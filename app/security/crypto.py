"""Cryptographic primitives used by the password manager.

The master password never encrypts records directly. Argon2id derives a 256-bit
vault key from the master password and a per-user random salt. Each field is
then encrypted independently with AES-256-GCM and a fresh random nonce.
"""
import os
from argon2.low_level import Type, hash_secret_raw
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

SALT_SIZE = 16
KEY_SIZE = 32
NONCE_SIZE = 12
ARGON_TIME = 3
ARGON_MEMORY = 64 * 1024
ARGON_PARALLELISM = 2


def new_salt() -> bytes:
    return os.urandom(SALT_SIZE)


def derive_key(password: str, salt: bytes) -> bytes:
    if not password:
        raise ValueError("Password must not be empty")
    return hash_secret_raw(
        password.encode("utf-8"), salt,
        time_cost=ARGON_TIME,
        memory_cost=ARGON_MEMORY,
        parallelism=ARGON_PARALLELISM,
        hash_len=KEY_SIZE,
        type=Type.ID,
    )


def encrypt(plaintext: str, key: bytes, aad: bytes = b"vault-field-v1") -> bytes:
    nonce = os.urandom(NONCE_SIZE)
    ciphertext = AESGCM(key).encrypt(nonce, plaintext.encode("utf-8"), aad)
    return nonce + ciphertext


def decrypt(blob: bytes, key: bytes, aad: bytes = b"vault-field-v1") -> str:
    if len(blob) <= NONCE_SIZE:
        raise ValueError("Invalid encrypted value")
    nonce, ciphertext = blob[:NONCE_SIZE], blob[NONCE_SIZE:]
    plaintext = AESGCM(key).decrypt(nonce, ciphertext, aad)
    return plaintext.decode("utf-8")
