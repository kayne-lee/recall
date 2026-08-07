.PHONY: check test fmt

# The full gate. CI runs exactly these four, in this order.
check:
	uv run ruff check .
	uv run ruff format --check .
	uv run mypy
	uv run pytest

test:
	uv run pytest

fmt:
	uv run ruff format .
