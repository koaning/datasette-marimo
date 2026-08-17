db:
	uv run --with sqlite-utils sqlite-utils insert sqlite.db chickweight chickweight.csv --csv

static:
	uv run marimo export html-wasm --output datasette_marimo/static --mode edit demo.py
	uv run marimo export html-wasm --output docs --mode edit pages.py

pypi: check
	uv build
	uv publish

clean:
	rm -rf dist build datasette_marimo.egg-info __pycache__

install:
	uv venv
	uv pip install -e ".[test]"
	uv run datasette install datasette-marimo
	make db

check:
	uv run ruff check --fix datasette_marimo/
	uv run pytest

# Run the tests against the Datasette 0.x line.
check-v0:
	uv run --extra test --with "datasette<1" pytest

# Run the tests against the Datasette 1.0 line (newest alpha).
check-v1:
	uv run --extra test --prerelease=allow --with "datasette>=1.0a0" pytest

# Run the tests against both Datasette lines, like the CI matrix.
check-both: check-v0 check-v1

# Primary test entrypoint: lint, then test both Datasette lines.
test:
	uv run --extra test ruff check datasette_marimo/
	$(MAKE) check-both
