"""Language detection — determines if input is Dutch or English."""

# Common Dutch words that rarely appear in English
_DUTCH_MARKERS = {
    "de",
    "het",
    "een",
    "van",
    "is",
    "dat",
    "dit",
    "niet",
    "voor",
    "zijn",
    "wordt",
    "maar",
    "ook",
    "aan",
    "bij",
    "als",
    "naar",
    "nog",
    "wel",
    "heeft",
    "kan",
    "moet",
    "uit",
    "veel",
    "zou",
    "meer",
    "dan",
    "waar",
    "hun",
    "deze",
    "die",
    "wat",
    "hoe",
    "welke",
    "graag",
    "alsjeblieft",
    "bedankt",
    "hogeschool",
    "opleiding",
    "studie",
    "informatie",
}

# Common English words that rarely appear in Dutch
_ENGLISH_MARKERS = {
    "the",
    "is",
    "and",
    "to",
    "of",
    "in",
    "that",
    "it",
    "for",
    "was",
    "with",
    "are",
    "but",
    "not",
    "you",
    "this",
    "have",
    "from",
    "they",
    "been",
    "would",
    "could",
    "should",
    "which",
    "about",
    "please",
    "thanks",
    "university",
    "program",
    "course",
    "information",
}


def detect_language(text: str) -> str:
    """Detect whether text is Dutch or English. Returns 'nl' or 'en'."""
    words = set(text.lower().split())

    dutch_score = len(words & _DUTCH_MARKERS)
    english_score = len(words & _ENGLISH_MARKERS)

    return "nl" if dutch_score > english_score else "en"
