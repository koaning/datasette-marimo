db:
	uv run --with sqlite-utils sqlite-utils insert sqlite.db chickweight chickweight.csv --csv

static:
	uv run marimo export html-wasm --output datasette_marimo/static --mode edit demo.py

pypi:
	uv build
	uv publish

clean:
	rm -rf dist build datasette_marimo.egg-info __pycache__