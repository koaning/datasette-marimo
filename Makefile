db:
	uv run --with sqlite-utils sqlite-utils insert sqlite.db chickweight chickweight.csv --csv

static:
	uv run marimo export html-wasm --output datasette_marimo/static --mode edit demo.py
	uv run marimo export html-wasm --output docs --mode edit pages.py

pypi:
	uv build
	uv publish

clean:
	rm -rf dist build datasette_marimo.egg-info __pycache__

install:
	python -m pip install uv 
	uv venv 
	uv pip install -e . 
	uv run datasette install datasette-marimo
	make db

check:
	uv run ruff check --fix datasette_marimo/
	uv run pytest
