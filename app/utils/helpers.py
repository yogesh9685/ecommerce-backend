import re
import unicodedata


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    text = text.strip("-")
    return text


def format_currency(amount: float, currency: str = "INR") -> str:
    if currency == "INR":
        return f"₹{amount:,.2f}"
    return f"{currency} {amount:,.2f}"


def mask_email(email: str) -> str:
    parts = email.split("@")
    if len(parts) != 2:
        return email
    local = parts[0]
    masked = local[:2] + "*" * (len(local) - 2)
    return f"{masked}@{parts[1]}"


def mask_phone(phone: str) -> str:
    if len(phone) < 4:
        return phone
    return "*" * (len(phone) - 4) + phone[-4:]
