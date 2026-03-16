"""Bias and fairness evaluation tests."""

from hu_ai_platform.guardrails.language_check import detect_language
from hu_ai_platform.guardrails.pii_filter import detect_pii


class TestLanguageFairness:
    """Ensure the system handles both Dutch and English equitably."""

    def test_dutch_input_detected(self) -> None:
        assert detect_language("Ik zoek informatie over de AI opleiding") == "nl"

    def test_english_input_detected(self) -> None:
        assert detect_language("I am looking for information about the AI program") == "en"

    def test_short_input_does_not_crash(self) -> None:
        """Single-word inputs should not raise errors."""
        result = detect_language("Hello")
        assert result in ("nl", "en")


class TestPIIEquity:
    """Ensure PII detection works for Dutch-format personal data."""

    def test_dutch_phone_detected(self) -> None:
        detections = detect_pii("Bel me op 06-12345678")
        phones = [d for d in detections if d.pii_type == "phone"]
        assert len(phones) == 1

    def test_dutch_iban_detected(self) -> None:
        detections = detect_pii("Rekening NL91ABNA0417164300")
        ibans = [d for d in detections if d.pii_type == "IBAN"]
        assert len(ibans) == 1

    def test_no_false_positive_on_normal_text(self) -> None:
        """Normal university questions should not trigger PII detection."""
        detections = detect_pii("Hoeveel studenten heeft de Hogeschool Utrecht?")
        assert len(detections) == 0
