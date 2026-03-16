"""FAISS-based local vector store for RAG knowledge retrieval.

Implements Agno's KnowledgeProtocol so the agent can query the store directly.
"""

import json
import logging
from collections.abc import Callable
from pathlib import Path
from typing import Any

import faiss  # type: ignore[import-untyped]
import numpy as np
from agno.knowledge.document.base import Document as AgnoDocument
from openai import OpenAI
from pydantic import BaseModel

from hu_ai_platform.config import Settings

logger = logging.getLogger(__name__)


class Document(BaseModel):
    """A document chunk with content and metadata."""

    content: str
    metadata: dict[str, str]


class SearchResult(BaseModel):
    """A search result with relevance score."""

    content: str
    metadata: dict[str, str]
    score: float


class FAISSVectorStore:
    """Local vector store backed by FAISS and OpenAI embeddings.

    Implements Agno's KnowledgeProtocol so it can be passed as `knowledge=` to an Agent.
    """

    EMBEDDING_DIM = 1536  # text-embedding-3-small dimension

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._client = OpenAI(api_key=settings.openai_api_key)
        self._index = faiss.IndexFlatIP(self.EMBEDDING_DIM)
        self._documents: list[Document] = []
        self._index_path = Path(settings.faiss_index_path)

    def _embed(self, texts: list[str]) -> np.ndarray:
        """Generate embeddings for a list of texts."""
        response = self._client.embeddings.create(
            model=self._settings.openai_embedding_model,
            input=texts,
        )
        embeddings = np.array([e.embedding for e in response.data], dtype=np.float32)
        # L2-normalize for cosine similarity via inner product
        faiss.normalize_L2(embeddings)
        return embeddings

    def add_documents(self, documents: list[Document]) -> int:
        """Add documents to the vector store. Returns number of documents added."""
        if not documents:
            return 0

        texts = [doc.content for doc in documents]
        embeddings = self._embed(texts)

        self._index.add(embeddings)
        self._documents.extend(documents)

        logger.info(
            "Added %d documents to vector store (total: %d)",
            len(documents),
            len(self._documents),
        )
        return len(documents)

    def search(self, query: str, k: int = 5) -> list[SearchResult]:
        """Search for the most relevant documents."""
        if self._index.ntotal == 0:
            return []

        query_embedding = self._embed([query])
        k = min(k, self._index.ntotal)
        scores, indices = self._index.search(query_embedding, k)

        results = []
        for score, idx in zip(scores[0], indices[0], strict=True):
            if idx < 0:
                continue
            doc = self._documents[idx]
            results.append(
                SearchResult(
                    content=doc.content,
                    metadata=doc.metadata,
                    score=float(score),
                )
            )
        return results

    def save(self) -> None:
        """Persist the index and documents to disk."""
        self._index_path.mkdir(parents=True, exist_ok=True)

        faiss.write_index(self._index, str(self._index_path / "index.faiss"))

        docs_data = [doc.model_dump() for doc in self._documents]
        (self._index_path / "documents.json").write_text(
            json.dumps(docs_data, ensure_ascii=False, indent=2)
        )
        logger.info(
            "Saved vector store to %s (%d documents)",
            self._index_path,
            len(self._documents),
        )

    def load(self) -> bool:
        """Load index and documents from disk. Returns True if successful."""
        index_file = self._index_path / "index.faiss"
        docs_file = self._index_path / "documents.json"

        if not index_file.exists() or not docs_file.exists():
            return False

        self._index = faiss.read_index(str(index_file))
        docs_data = json.loads(docs_file.read_text())
        self._documents = [Document(**d) for d in docs_data]

        logger.info(
            "Loaded vector store from %s (%d documents)",
            self._index_path,
            len(self._documents),
        )
        return True

    @property
    def document_count(self) -> int:
        return len(self._documents)

    # --- Agno KnowledgeProtocol implementation ---

    def build_context(self, **kwargs: Any) -> str:
        """Provide instructions for the agent's system prompt."""
        return (
            "You have access to a knowledge base about Hogeschool Utrecht. "
            "Use the search tool to find relevant information before answering. "
            "Always cite the source when using retrieved information."
        )

    def get_tools(self, **kwargs: Any) -> list[Callable[..., Any]]:
        """Return search as a tool the agent can call."""

        def search_hu_knowledge(query: str) -> str:
            """Search the Hogeschool Utrecht knowledge base for relevant information."""
            results = self.search(query, k=5)
            if not results:
                return "No relevant information found in the knowledge base."
            parts = []
            for i, r in enumerate(results, 1):
                source = r.metadata.get("source", "unknown")
                parts.append(f"[{i}] (source: {source})\n{r.content}")
            return "\n\n---\n\n".join(parts)

        return [search_hu_knowledge]

    async def aget_tools(self, **kwargs: Any) -> list[Callable[..., Any]]:
        """Async version — delegates to sync since FAISS is CPU-bound."""
        return self.get_tools(**kwargs)

    def retrieve(self, query: str, **kwargs: Any) -> list[AgnoDocument]:
        """Retrieve relevant documents for context injection."""
        results = self.search(query, k=kwargs.get("k", 5))
        return [
            AgnoDocument(
                content=r.content,
                name=r.metadata.get("source", "unknown"),
                meta_data=dict(r.metadata),
            )
            for r in results
        ]

    async def aretrieve(self, query: str, **kwargs: Any) -> list[AgnoDocument]:
        """Async version — delegates to sync since FAISS is CPU-bound."""
        return self.retrieve(query, **kwargs)


def create_vector_store(settings: Settings) -> FAISSVectorStore:
    """Factory: create a vector store and load existing data if available."""
    store = FAISSVectorStore(settings)
    store.load()
    return store
