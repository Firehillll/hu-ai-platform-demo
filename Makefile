.PHONY: install dev run chat team lint format typecheck test seed docker-up docker-down clean

install:
	uv sync

dev:
	uv sync --dev

run:
	uv run uvicorn hu_ai_platform.main:app --reload --host 0.0.0.0 --port 8000

chat:
	uv run python -m hu_ai_platform.cli assistant

team:
	uv run python -m hu_ai_platform.cli team

lint:
	uv run ruff check src/ tests/
	uv run ruff format --check src/ tests/

format:
	uv run ruff format src/ tests/
	uv run ruff check --fix src/ tests/

typecheck:
	uv run mypy src/

test:
	uv run pytest

seed:
	uv run python scripts/seed_knowledge.py

docker-up:
	docker compose up --build

docker-down:
	docker compose down

clean:
	rm -rf .venv __pycache__ .pytest_cache .mypy_cache data/
