"""Seed the local FAISS vector store with sample data."""

import logging
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from hu_ai_platform.config import Settings
from hu_ai_platform.knowledge.loader import load_directory
from hu_ai_platform.knowledge.vectorstore import FAISSVectorStore

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    settings = Settings()

    if not settings.openai_api_key:
        logger.error(
            "OPENAI_API_KEY is not set. "
            "Copy .env.example to .env and add your API key to generate embeddings."
        )
        sys.exit(1)

    sample_dir = Path(__file__).resolve().parent.parent / "sample_data"
    if not sample_dir.exists():
        logger.error("Sample data directory not found: %s", sample_dir)
        sys.exit(1)

    logger.info("Loading documents from %s ...", sample_dir)
    documents = load_directory(sample_dir)
    logger.info("Loaded %d document chunks", len(documents))

    logger.info("Creating embeddings and building FAISS index ...")
    store = FAISSVectorStore(settings)
    added = store.add_documents(documents)
    store.save()

    logger.info("Done! %d chunks indexed and saved to %s", added, settings.faiss_index_path)


if __name__ == "__main__":
    main()
