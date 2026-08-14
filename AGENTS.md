# Agent guide

This file gives guidance to agents that work in this repository. `CLAUDE.md` is a
symlink to this file.

## Project

`datasette-marimo` is a Datasette plugin. It serves a marimo notebook at `/marimo`
that runs in the browser with WebAssembly (WASM). The plugin hooks and routes are
in `datasette_marimo/__init__.py`. The `demo.py` notebook becomes the served
bundle in `datasette_marimo/static/`. The `pages.py` notebook becomes the GitHub
Pages demo in `docs/`.

## Development

- Install the plugin and test dependencies: `make install`.
- Run the checks (ruff and pytest): `make check`.
- Build the WASM bundles from the notebooks: `make static`.
- Build the sample database from `chickweight.csv`: `make db`.

The `make static` target regenerates `datasette_marimo/static/` and `docs/`. Run
it after you change `demo.py` or `pages.py`. Commit the regenerated bundles.

## Documentation

Apply the `simplified-technical-english` skill when you write or revise any
documentation. This rule covers the `README.md`, the `CHANGELOG.md`, the notebook
markdown cells, and pull request text.

## Changelog

`CHANGELOG.md` records the notable changes for each release.

Before you write or edit a changelog entry, apply the
`simplified-technical-english` skill. Add each user-visible change to the top
section. Group the change under `Added`, `Changed`, `Fixed`, or `Removed`.

## Pull requests

Apply the `simplified-technical-english` skill when you write the title and body
of a pull request.

## Releases

To prepare a release:

1. Set the new version in `pyproject.toml`.
2. Add a version section to `CHANGELOG.md`.
3. Run `make check`.
4. Build and publish with `make pypi`.
