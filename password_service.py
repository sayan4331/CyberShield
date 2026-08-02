"""Heuristic password strength scoring.

Rule-based approximation (length, character variety, entropy, common-
password / pattern checks) intended for an educational dashboard. It is
not a cryptographic guarantee, and the raw password is never persisted —
only the resulting score is written to history.
"""
import math
import re

from sqlalchemy.orm import Session

from app.services import history_service

COMMON_PASSWORDS = {
    "password", "123456", "123456789", "12345678", "12345", "qwerty",
    "abc123", "password1", "111111", "123123", "letmein", "welcome",
    "admin", "iloveyou", "monkey", "dragon", "football", "baseball",
    "trustno1", "sunshine", "master", "shadow", "superman", "qazwsx",
    "michael", "login", "princess", "starwars", "passw0rd", "solo",
}

KEYBOARD_RUNS = ["qwerty", "asdfgh", "zxcvbn", "12345", "09876", "qazwsx"]


def _char_classes(pw: str) -> dict:
    return {
        "lower": bool(re.search(r"[a-z]", pw)),
        "upper": bool(re.search(r"[A-Z]", pw)),
        "digit": bool(re.search(r"\d", pw)),
        "symbol": bool(re.search(r"[^a-zA-Z0-9]", pw)),
    }


def _pool_size(classes: dict) -> int:
    size = 0
    if classes["lower"]:
        size += 26
    if classes["upper"]:
        size += 26
    if classes["digit"]:
        size += 10
    if classes["symbol"]:
        size += 33
    return size or 1


def _entropy_bits(pw: str, classes: dict) -> float:
    return len(pw) * math.log2(_pool_size(classes)) if pw else 0.0


def _crack_time_label(entropy_bits: float) -> str:
    # Assume a generous offline attack rate of 10 billion guesses/sec.
    seconds = (2 ** entropy_bits) / 1e10
    if seconds < 1:
        return "instantly"
    units = [("second", 60), ("minute", 60), ("hour", 24), ("day", 365), ("year", 100), ("century", float("inf"))]
    value, label = seconds, "second"
    for name, factor in units:
        label = name
        if value < factor:
            break
        value /= factor
    value = max(value, 1)
    return f"~{value:,.0f} {label}{'s' if value != 1 else ''}"


def analyze_password(pw: str) -> dict:
    pw = pw or ""
    classes = _char_classes(pw)
    length = len(pw)
    lower_pw = pw.lower()

    checks = {
        "length_8": length >= 8,
        "length_12": length >= 12,
        "has_upper": classes["upper"],
        "has_lower": classes["lower"],
        "has_digit": classes["digit"],
        "has_symbol": classes["symbol"],
        "not_common": lower_pw not in COMMON_PASSWORDS,
        "no_keyboard_run": not any(run in lower_pw for run in KEYBOARD_RUNS),
        "no_repeats": not re.search(r"(.)\1{2,}", pw),
    }

    score = min(length, 16) * 3
    score += 10 if classes["upper"] else 0
    score += 10 if classes["lower"] else 0
    score += 10 if classes["digit"] else 0
    score += 12 if classes["symbol"] else 0
    if lower_pw in COMMON_PASSWORDS:
        score = min(score, 15)
    if any(run in lower_pw for run in KEYBOARD_RUNS):
        score -= 15
    if re.search(r"(.)\1{2,}", pw):
        score -= 10
    score = max(0, min(100, score))

    if length == 0:
        strength = "None"
    elif score < 30:
        strength = "Very Weak"
    elif score < 50:
        strength = "Weak"
    elif score < 70:
        strength = "Fair"
    elif score < 90:
        strength = "Strong"
    else:
        strength = "Very Strong"

    entropy = round(_entropy_bits(pw, classes), 1)

    return {
        "score": score,
        "strength": strength,
        "length": length,
        "entropy_bits": entropy,
        "estimated_crack_time": _crack_time_label(entropy),
        "checks": checks,
    }


def check_and_log(db: Session, password: str) -> dict:
    result = analyze_password(password)
    history_service.log_scan(
        db, scan_type="password", label=result["strength"], score=result["score"],
        subject=None,  # never store anything derived from the raw password as a subject
        details={"length": result["length"], "entropy_bits": result["entropy_bits"]},
    )
    return result
