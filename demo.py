# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "drawdata==0.3.7",
#     "marimo",
#     "polars==1.22.0",
#     "quak==0.2.2",
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

    ## Utilities

    This notebooks also features a `Datasette` utility class that makes it easy to fetch data. The following methods are relevant: 

    ```python
    # Automatically connect to the current datasette instance
    ds = Datasette()

    # Show all databases in datasette
    ds.databases

    # Show all datables in a database in datasette
    ds.tables(database=)

    # Get a table as a polars dataframe (uses the JSON api)
    ds.get_polars(database=, table=)

    # Use SQL to get the data in the right polars format
    ds.sql_polars(database=, sql=)
    ```

    In theory you could also re-use the same class to connect to another datasette instance that is hosted elsewhere. 

    ```python
    ds = Datasette(url=)
    ```

    To learn more about Marimo, feel free to explore the [docs](https://docs.marimo.io/getting_started/key_concepts/). 
    """)
    return


@app.cell
def _(Datasette):
    ds = Datasette()
    ds.databases
    return (ds,)


@app.cell
def _():
    import marimo as mo
    import requests as rq
    from yarl import URL
    import polars as pl
    import json
    from functools import cached_property, lru_cache


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
    return (
        Datasette,
        URL,
        cached_property,
        json,
        lru_cache,
        marimo_host,
        mo,
        pl,
        rq,
    )


if __name__ == "__main__":
    app.run()
