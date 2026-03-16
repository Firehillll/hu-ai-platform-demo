# Multi-stage production image
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install dependencies
COPY pyproject.toml uv.lock* README.md ./
RUN uv sync --no-dev --frozen 2>/dev/null || uv sync --no-dev

# Copy application code
COPY src/ src/
COPY sample_data/ sample_data/
COPY scripts/ scripts/

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "hu_ai_platform.main:app", "--host", "0.0.0.0", "--port", "8000"]
