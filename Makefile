db:
	uv run --with sqlite-utils sqlite-utils insert sqlite.db chickweight chickweight.csv --csv

static:
	uv run marimo export html-wasm --output datasette_marimo/static --mode edit demo.py
