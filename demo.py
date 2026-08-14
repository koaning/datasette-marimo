# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "marimo",
#     "moutils",
#     "httpx",
#     "pyodide-httpx",
#     "polars==1.22.0",
#     "requests==2.32.3",
#     "yarl==1.18.3",
# ]
# ///

import marimo

__generated_with = "0.10.19"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        # marimo × datasette

        This notebook runs entirely in your browser and is already connected to the
        datasette instance that served it. Pick a database and table below — the
        query updates live. Edit any cell to go further. (Refresh loses your work,
        so export anything worth keeping.)
        """
    )
    return


@app.cell(hide_code=True)
def _():
    # Patch httpx so it can make HTTP requests inside the browser (Pyodide/WASM).
    # In a normal Python process httpx already works, so the patch is a no-op there.
    try:
        from pyodide_httpx import patch_httpx

        patch_httpx()
    except ImportError:
        pass

    import json
    from functools import cached_property, lru_cache

    import marimo as mo
    import polars as pl
    import requests as rq
    from yarl import URL

    from moutils.db.datasette import DatasetteConnection, databases

    def marimo_host():
        """Base URL of the datasette instance that is hosting this notebook."""
        loc = URL(str(mo.notebook_location()))
        return f"{loc.scheme}://{loc.authority}"

    return (
        DatasetteConnection,
        URL,
        cached_property,
        databases,
        json,
        lru_cache,
        marimo_host,
        mo,
        pl,
        rq,
    )


@app.cell(hide_code=True)
def _(databases, marimo_host, mo):
    base_url = marimo_host()
    _db_names = databases(base_url)
    _default_db = mo.query_params().get("database")
    database = mo.ui.dropdown(
        options=_db_names,
        value=_default_db if _default_db in _db_names else _db_names[0],
        label="Database",
    )
    return base_url, database


@app.cell(hide_code=True)
def _(DatasetteConnection, base_url, database):
    # A moutils DatasetteConnection is a native marimo SQL connection, so it also
    # shows up in the data-sources panel on the left.
    conn = DatasetteConnection(base_url, database.value)
    return (conn,)


@app.cell(hide_code=True)
def _(conn, mo):
    _tables = sorted({row["table"] for row in conn.schema_rows()})
    _default_table = mo.query_params().get("table")
    table = mo.ui.dropdown(
        options=_tables,
        value=_default_table if _default_table in _tables else (_tables[0] if _tables else None),
        label="Table",
    )
    return (table,)


@app.cell(hide_code=True)
def _(database, mo, table):
    mo.hstack([database, table], justify="start", gap=1)
    return


@app.cell
def _(conn, mo, table):
    result = mo.sql(
        f'select * from "{table.value}" limit 100',
        engine=conn,
    )
    return (result,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        The older `Datasette` helper (`get_polars` / `sql_polars`) is still bundled
        for backwards compatibility — the code is folded away below.
        """
    )
    return


@app.cell(hide_code=True)
def _(URL, cached_property, json, lru_cache, marimo_host, pl, rq):
    class Datasette:
        def __init__(self, url=None):
            self.url = url if url else marimo_host()

        @cached_property
        def databases(self):
            resp = rq.get(f"{self.url}/-/databases.json")
            return [_["name"] for _ in resp.json()]

        @lru_cache
        def tables(self, database):
            if database not in self.databases:
                raise ValueError(f"{database} does not exist, options are: {self.databases}")
            resp = rq.get(f"{self.url}/{database}.json")
            return [_["name"] for _ in resp.json()["tables"]]

        def get_polars(self, database, table):
            return self.sql_polars(database, sql=f"select * from {table}")

        def sql_polars(self, database, sql):
            url = (URL(self.url) / f"{database}.json").with_query(sql=sql, _shape="array", _nl="on", _size="max")
            return pl.DataFrame([json.loads(_) for _ in rq.get(f"{url}").text.split("\n")])

    return (Datasette,)


if __name__ == "__main__":
    app.run()
