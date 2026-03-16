"""Knowledge management endpoints — ingest and search."""

import tempfile
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile
from pydantic import BaseModel

from hu_ai_platform.api.dependencies import get_settings
from hu_ai_platform.config import Settings
from hu_ai_platform.knowledge.loader import load_markdown
from hu_ai_platform.knowledge.vectorstore import SearchResult, create_vector_store

router = APIRouter(prefix="/knowledge")


class IngestResponse(BaseModel):
    chunks_added: int
    total_documents: int


class SearchResponse(BaseModel):
    results: list[SearchResult]
    query: str


@router.post("/ingest", response_model=IngestResponse)
async def ingest_document(
    file: UploadFile,
    settings: Settings = Depends(get_settings),
) -> IngestResponse:
    """Upload a markdown file to be chunked and added to the knowledge base."""
    if not settings.openai_api_key:
        raise HTTPException(
            status_code=503,
            detail="OpenAI API key required for embedding generation.",
        )

    if not file.filename or not file.filename.endswith(".md"):
        raise HTTPException(status_code=400, detail="Only markdown (.md) files are supported.")

    content = await file.read()

    with tempfile.NamedTemporaryFile(suffix=".md", delete=False, mode="wb") as tmp:
        tmp.write(content)
        tmp_path = Path(tmp.name)

    try:
        documents = load_markdown(tmp_path)
        store = create_vector_store(settings)
        added = store.add_documents(documents)
        store.save()

        return IngestResponse(chunks_added=added, total_documents=store.document_count)
    finally:
        tmp_path.unlink(missing_ok=True)


@router.get("/search", response_model=SearchResponse)
async def search_knowledge(
    q: str = Query(..., min_length=1, description="Search query"),
    k: int = Query(5, ge=1, le=20, description="Number of results"),
    settings: Settings = Depends(get_settings),
) -> SearchResponse:
    """Search the knowledge base for relevant documents."""
    if not settings.openai_api_key:
        raise HTTPException(
            status_code=503,
            detail="OpenAI API key required for search.",
        )

    store = create_vector_store(settings)
    if store.document_count == 0:
        return SearchResponse(results=[], query=q)

    results = store.search(q, k=k)
    return SearchResponse(results=results, query=q)
