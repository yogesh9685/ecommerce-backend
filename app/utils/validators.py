import re


def validate_phone(phone: str) -> bool:
    return bool(re.match(r"^\+?[1-9]\d{9,14}$", phone))


def validate_password_strength(password: str) -> bool:
    """At least 8 chars, 1 uppercase, 1 lowercase, 1 digit."""
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    return True


def validate_pincode(pincode: str) -> bool:
    return bool(re.match(r"^\d{6}$", pincode))
