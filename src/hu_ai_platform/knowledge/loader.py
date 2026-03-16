"""Document loading and chunking for the knowledge pipeline."""

import logging
import re
from pathlib import Path

from hu_ai_platform.knowledge.vectorstore import Document

logger = logging.getLogger(__name__)

# Approximate tokens-per-character ratio for English/Dutch text
CHARS_PER_TOKEN = 4
MAX_CHUNK_TOKENS = 500
MAX_CHUNK_CHARS = MAX_CHUNK_TOKENS * CHARS_PER_TOKEN


def _extract_title(text: str) -> str:
    """Extract the first markdown heading from text."""
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip()
    return "Untitled"


def _split_by_headers(text: str) -> list[str]:
    """Split markdown text by ## or ### headers, keeping headers with their content."""
    sections = re.split(r"(?=^#{2,3}\s)", text, flags=re.MULTILINE)
    return [s.strip() for s in sections if s.strip()]


def _chunk_section(section: str, max_chars: int = MAX_CHUNK_CHARS) -> list[str]:
    """Split a section into chunks that fit within the token budget."""
    if len(section) <= max_chars:
        return [section]

    chunks = []
    paragraphs = section.split("\n\n")
    current_chunk: list[str] = []
    current_len = 0

    for para in paragraphs:
        para_len = len(para)
        if current_len + para_len > max_chars and current_chunk:
            chunks.append("\n\n".join(current_chunk))
            current_chunk = []
            current_len = 0
        current_chunk.append(para)
        current_len += para_len

    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    return chunks


def load_markdown(file_path: Path) -> list[Document]:
    """Load a markdown file and split it into document chunks."""
    text = file_path.read_text(encoding="utf-8")
    title = _extract_title(text)
    source = file_path.name

    sections = _split_by_headers(text)
    documents: list[Document] = []

    for section in sections:
        chunks = _chunk_section(section)
        for chunk in chunks:
            documents.append(
                Document(
                    content=chunk,
                    metadata={"source": source, "title": title},
                )
            )

    logger.info("Loaded %d chunks from %s", len(documents), file_path)
    return documents


def load_directory(dir_path: Path) -> list[Document]:
    """Load all markdown files from a directory."""
    documents: list[Document] = []
    for md_file in sorted(dir_path.glob("*.md")):
        documents.extend(load_markdown(md_file))

    logger.info("Loaded %d total chunks from %s", len(documents), dir_path)
    return documents
