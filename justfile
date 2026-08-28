set shell := ["zsh", "-cu"]

default:
    @just --list

sync:
    uv sync

sync-all:
    uv sync --all-groups

lock:
    uv lock

format:
    uv run ruff format src tests scripts

format-check:
    uv run ruff format --check src tests scripts

lint:
    uv run ruff check src tests scripts

lint-fix:
    uv run ruff check --fix src tests scripts

typecheck:
    uv run ty check

test:
    uv run pytest

check:
    uv run ruff format --check src tests scripts
    uv run ruff check src tests scripts
    uv run ty check
    uv run pytest

build:
    rm -rf dist build
    uv build

check-dist: build
    uv run twine check dist/*

check-asset-fields corva-api="../corva-api":
    uv run python scripts/check_asset_fields.py {{corva-api}}

publish:
    uv publish

publish-to index-url:
    uv publish --publish-url {{ index-url }}
