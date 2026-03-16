"""PII detection and filtering — GDPR compliance for Dutch personal data."""

import re
from dataclasses import dataclass

# Dutch BSN (Burger Service Nummer): 9 digits with 11-check
BSN_PATTERN = re.compile(r"\b\d{9}\b")

# Dutch IBAN
IBAN_PATTERN = re.compile(r"\b[A-Z]{2}\d{2}[A-Z]{4}\d{10}\b")

# Email addresses
EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")

# Dutch phone numbers (06-12345678, +31612345678, etc.)
PHONE_PATTERN = re.compile(r"\b(?:\+31|0)[\s-]?[1-9][\s-]?\d{1,3}[\s-]?\d{4,8}\b")


@dataclass
class PIIDetection:
    """A detected PII occurrence."""

    pii_type: str
    value: str
    start: int
    end: int


def _validate_bsn(candidate: str) -> bool:
    """Validate a BSN using the 11-check algorithm."""
    if len(candidate) != 9 or not candidate.isdigit():
        return False
    digits = [int(d) for d in candidate]
    total = sum(d * (9 - i) for i, d in enumerate(digits[:8])) - digits[8]
    return total % 11 == 0 and total != 0


def detect_pii(text: str) -> list[PIIDetection]:
    """Scan text for Dutch PII patterns. Returns list of detections."""
    detections: list[PIIDetection] = []

    for match in BSN_PATTERN.finditer(text):
        if _validate_bsn(match.group()):
            detections.append(PIIDetection("BSN", match.group(), match.start(), match.end()))

    for match in IBAN_PATTERN.finditer(text):
        detections.append(PIIDetection("IBAN", match.group(), match.start(), match.end()))

    for match in EMAIL_PATTERN.finditer(text):
        detections.append(PIIDetection("email", match.group(), match.start(), match.end()))

    for match in PHONE_PATTERN.finditer(text):
        detections.append(PIIDetection("phone", match.group(), match.start(), match.end()))

    return detections


def redact_pii(text: str) -> tuple[str, list[PIIDetection]]:
    """Replace detected PII with redaction markers. Returns (redacted_text, detections)."""
    detections = detect_pii(text)
    if not detections:
        return text, []

    # Process replacements from end to start to preserve indices
    redacted = text
    for detection in sorted(detections, key=lambda d: d.start, reverse=True):
        placeholder = f"[{detection.pii_type} REDACTED]"
        redacted = redacted[: detection.start] + placeholder + redacted[detection.end :]

    return redacted, detections


def contains_pii(text: str) -> bool:
    """Quick check: does the text contain any PII?"""
    return len(detect_pii(text)) > 0
