"""Input checks for the menu. Each returns a clean value or raises ValueError."""

from __future__ import annotations

from academics import GradeCalculator


def validate_required(text: str, label: str) -> str:

    text = text.strip()
    if not text:
        raise ValueError(f"{label} cannot be empty.")
    return text


def validate_email(text: str) -> str:
    """Return the cleaned email, or raise ValueError if it is invalid."""
    text = text.strip()
    local, at, domain = text.partition("@")
    if not local or not at:
        raise ValueError("Email must contain '@' with text before it.")
    if "." not in domain or domain.startswith(".") or domain.endswith("."):
        raise ValueError("Email needs a domain like example.com.")
    return text


def validate_id(text: str) -> int:
    """Convert text to a positive whole-number id."""
    try:
        value = int(text)
    except ValueError:
        raise ValueError("Id must be a whole number.") from None
    if value < 1:
        raise ValueError("Id must be 1 or more.")
    return value


def validate_whole(text: str, low: int, high: int, label: str) -> int:
    """Convert text to a whole number between low and high."""
    try:
        value = int(text)
    except ValueError:
        raise ValueError(f"{label} must be a whole number.") from None
    if not low <= value <= high:
        raise ValueError(f"{label} must be between {low} and {high}.")
    return value


def validate_marks(text: str) -> float:
    """Convert text to marks between 0 and 100."""
    try:
        marks = float(text)
    except ValueError:
        raise ValueError("Grade must be a number.") from None
    if not GradeCalculator.is_valid_mark(marks):
        raise ValueError("Grade must be between 0 and 100.")
    return marks