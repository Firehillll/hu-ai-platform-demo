# ADR 002: uv as Package Manager

## Status
Accepted

## Context
Python projects at HU traditionally use pip + virtualenv or Poetry. We need a fast, reliable package manager for the AI platform.

## Decision
We chose **uv** (by Astral) as the package manager.

## Rationale
- **Speed**: 10-100x faster than pip for dependency resolution and installation (Rust-based)
- **Single tool**: Replaces pip, pip-tools, virtualenv, and pyenv in one binary
- **Lockfile**: Deterministic builds via `uv.lock` — consistent across dev, CI, and production
- **pyproject.toml native**: Works with standard PEP 621 metadata, no vendor lock-in
- **CI-friendly**: Fast installs reduce GitHub Actions build times significantly

## Consequences
- Team members need to install uv (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- Some CI environments may not have uv pre-installed (solved with `astral-sh/setup-uv` action)
- Falls back gracefully to pip if needed (`uv pip install` is compatible)
