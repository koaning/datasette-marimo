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
    mo.md("""
    ## Marimo for Datasette

    This notebook runs completely in the frontend via WASM. That means that:

    - you do not have to install anything in order to run Python code against any data that lives in your datasette instance
    - all written code is lost when you refresh the page, so make sure you export any milestones that are valuable

    ## Talking to datasette

    This notebook connects to the datasette instance that is hosting it through a
    [marimo SQL connection](https://docs.marimo.io/guides/working_with_data/sql/)
    provided by [moutils](https://github.com/marimo-team/moutils). The `conn`
    object below shows up in marimo's data-sources panel, so you can browse the
    schema and write **native SQL cells** against it:

    ```python
    from moutils.db.datasette import DatasetteConnection, databases

    databases(base_url)                       # list databases on the instance
    conn = DatasetteConnection(base_url, db)   # connect to one database
    ```

    Then create a SQL cell and pick `conn` as the engine, or run SQL from Python
    with `mo.sql("select ...", engine=conn)`.

    To learn more about Marimo, feel free to explore the [docs](https://docs.marimo.io/getting_started/key_concepts/).
    """)
    return


@app.cell
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


@app.cell
def _(DatasetteConnection, databases, marimo_host, mo):
    # Connect to the current instance. The "Open in marimo" menu link can prefill
    # ?database=&table= so we land on the database you were just looking at.
    base_url = marimo_host()
    params = mo.query_params()
    db_names = databases(base_url)
    database = params.get("database") or (db_names[0] if db_names else None)
    conn = DatasetteConnection(base_url, database) if database else None
    conn
    return base_url, conn, database, db_names, params


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Pick a table below — the SQL cell that follows previews it. Swap in any SQL you like.""")
    return


@app.cell
def _(conn, params):
    tables = sorted({row["table"] for row in conn.schema_rows()}) if conn else []
    table = params.get("table") or (tables[0] if tables else None)
    tables
    return table, tables


@app.cell
def _(conn, mo, table):
    preview = mo.sql(
        f'select * from "{table}" limit 100',
        engine=conn,
    )
    return (preview,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Legacy helper (still supported)

        Before the moutils connection existed this notebook shipped a small
        `Datasette` class that fetched data through the JSON API. It still works,
        so any code that relied on `get_polars` / `sql_polars` keeps running — but
        the `DatasetteConnection` above is the recommended path.

        ```python
        ds = Datasette()                       # connect to the current instance
        ds.databases                           # list databases
        ds.tables(database="sqlite")           # list tables
        ds.get_polars(database="sqlite", table="chickweight")
        ds.sql_polars(database="sqlite", sql="select * from chickweight")
        ```
        """
    )
    return


@app.cell
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
