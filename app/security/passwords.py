import re
import secrets
import string
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError

PASSWORD_HASHER = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=2)


def hash_master_password(password: str) -> str:
    return PASSWORD_HASHER.hash(password)


def verify_master_password(password_hash: str, password: str) -> bool:
    try:
        return PASSWORD_HASHER.verify(password_hash, password)
    except (VerifyMismatchError, VerificationError, ValueError):
        return False


def password_strength(password: str) -> dict:
    score = 0
    checks = {
        "length": len(password) >= 12,
        "uppercase": bool(re.search(r"[A-Z]", password)),
        "lowercase": bool(re.search(r"[a-z]", password)),
        "digit": bool(re.search(r"\d", password)),
        "symbol": bool(re.search(r"[^A-Za-z0-9]", password)),
    }
    score = sum(checks.values())
    if len(password) >= 20:
        score += 1
    labels = {0: "Very Weak", 1: "Very Weak", 2: "Weak", 3: "Fair", 4: "Strong", 5: "Very Strong", 6: "Excellent"}
    return {"score": score, "label": labels[score], "checks": checks}


def generate_password(length=24, use_symbols=True):
    if not 12 <= length <= 128:
        raise ValueError("Password length must be between 12 and 128")
    groups = [string.ascii_lowercase, string.ascii_uppercase, string.digits]
    if use_symbols:
        groups.append("!@#$%^&*()-_=+[]{}:,.?/")
    chars = [secrets.choice(group) for group in groups]
    alphabet = "".join(groups)
    chars.extend(secrets.choice(alphabet) for _ in range(length - len(chars)))
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)
