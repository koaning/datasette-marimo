# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "marimo",
#     "moutils",
#     "httpx",
#     "pyodide-httpx",
#     "altair",
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
        # datasette-marimo

        This page gives an impression of what it could be like to use Marimo from datasette. Right now it just points to a public instance ([datasette.exe.xyz](https://datasette.exe.xyz)), but you can ship the same experience from within datasette.

        ## Connect via a marimo SQL connection

        We connect to a datasette instance with
        [moutils](https://github.com/marimo-team/moutils)'
        `DatasetteConnection`. It is a first-class marimo SQL connection, so the
        `conn` object shows up in the data-sources panel and you can run **native
        SQL cells** against it.
        """
    )
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

    return (
        DatasetteConnection,
        URL,
        cached_property,
        databases,
        json,
        lru_cache,
        mo,
        pl,
        rq,
    )


@app.cell
def _(DatasetteConnection):
    conn = DatasetteConnection("https://datasette.exe.xyz", "sleep_and_gpa")
    conn
    return (conn,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""You can list the databases attached to the instance.""")
    return


@app.cell
def _(conn):
    conn.databases()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""And you can browse the tables and columns the connection exposes.""")
    return


@app.cell
def _(conn):
    conn.schema_rows()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Spot a table you want to investigate? Run SQL against it — this is a native marimo SQL cell using `conn` as the engine.""")
    return


@app.cell
def _(conn, mo):
    _preview = mo.sql(
        "select * from students limit 5",
        engine=conn,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Pull the table into a dataframe and you get Python back, so plotting and machine learning become easy. Here we look at how average sleep relates to term GPA.""")
    return


@app.cell
def _(conn, mo):
    df_students = mo.sql(
        "select avg_sleep_hours, term_gpa, gender from students",
        engine=conn,
    )
    return (df_students,)


@app.cell
def _(df_students):
    df_students.plot.scatter("avg_sleep_hours", "term_gpa", color="gender")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Legacy helper (still supported)

        The older `Datasette` helper class that fetched data through the JSON API
        still works, so existing `get_polars` / `sql_polars` code keeps running.
        The `DatasetteConnection` above is the recommended path.
        """
    )
    return


@app.cell
def _(URL, cached_property, json, lru_cache, mo, pl, rq):
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

    def marimo_host():
        url = URL(str(mo.notebook_location()))
        return f"{url.scheme}://{url.authority}"

    return (Datasette,)


if __name__ == "__main__":
    app.run()
