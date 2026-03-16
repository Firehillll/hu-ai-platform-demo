"""Tests for guardrail components."""

from hu_ai_platform.guardrails.eu_ai_act import add_transparency_notice
from hu_ai_platform.guardrails.language_check import detect_language
from hu_ai_platform.guardrails.pii_filter import (
    contains_pii,
    detect_pii,
    redact_pii,
)


class TestPIIFilter:
    def test_detect_valid_bsn(self) -> None:
        # 111222333 passes the 11-check
        detections = detect_pii("My BSN is 111222333")
        assert len(detections) == 1
        assert detections[0].pii_type == "BSN"

    def test_ignore_invalid_bsn(self) -> None:
        detections = detect_pii("Random number 123456789")
        bsn_detections = [d for d in detections if d.pii_type == "BSN"]
        assert len(bsn_detections) == 0

    def test_detect_email(self) -> None:
        detections = detect_pii("Contact me at student@hu.nl")
        emails = [d for d in detections if d.pii_type == "email"]
        assert len(emails) == 1
        assert emails[0].value == "student@hu.nl"

    def test_detect_iban(self) -> None:
        detections = detect_pii("Pay to NL91ABNA0417164300")
        ibans = [d for d in detections if d.pii_type == "IBAN"]
        assert len(ibans) == 1

    def test_detect_phone(self) -> None:
        detections = detect_pii("Call me at 06-12345678")
        phones = [d for d in detections if d.pii_type == "phone"]
        assert len(phones) == 1

    def test_redact_pii(self) -> None:
        text = "Email me at test@example.com please"
        redacted, detections = redact_pii(text)
        assert "[email REDACTED]" in redacted
        assert "test@example.com" not in redacted
        assert len(detections) == 1

    def test_no_pii(self) -> None:
        assert not contains_pii("What programs does HU offer?")

    def test_contains_pii(self) -> None:
        assert contains_pii("My email is info@hu.nl")


class TestLanguageCheck:
    def test_detect_dutch(self) -> None:
        assert detect_language("Wat is de opleiding voor AI bij Hogeschool Utrecht?") == "nl"

    def test_detect_english(self) -> None:
        assert detect_language("What programs does the university offer?") == "en"

    def test_mixed_defaults_to_dominant(self) -> None:
        result = detect_language("Wat is the best program?")
        assert result in ("nl", "en")


class TestEUAIAct:
    def test_transparency_notice_english(self) -> None:
        result = add_transparency_notice("Hello!", language="en")
        assert "AI system" in result
        assert "Hello!" in result

    def test_transparency_notice_dutch(self) -> None:
        result = add_transparency_notice("Hallo!", language="nl")
        assert "AI-systeem" in result
        assert "Hallo!" in result
