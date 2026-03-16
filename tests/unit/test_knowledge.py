"""Tests for knowledge pipeline components."""

from pathlib import Path

from hu_ai_platform.knowledge.loader import (
    _extract_title,
    _split_by_headers,
    load_markdown,
)


class TestLoader:
    def test_extract_title(self) -> None:
        assert _extract_title("# My Title\nContent") == "My Title"
        assert _extract_title("No heading here") == "Untitled"

    def test_split_by_headers(self) -> None:
        text = "# Title\nIntro\n## Section 1\nContent 1\n## Section 2\nContent 2"
        sections = _split_by_headers(text)
        assert len(sections) >= 2

    def test_load_markdown_file(self, tmp_path: Path) -> None:
        md_file = tmp_path / "test.md"
        md_file.write_text("# Test\n\n## Section A\nSome content.\n\n## Section B\nMore content.")

        docs = load_markdown(md_file)
        assert len(docs) > 0
        assert all(d.metadata["source"] == "test.md" for d in docs)
        assert docs[0].metadata["title"] == "Test"
