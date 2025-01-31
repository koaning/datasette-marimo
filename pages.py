import marimo

__generated_with = "0.10.19"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        # datasette-marimo 

        This page gives an impression of what it could be like to use Marimo from datasette. Right now it just points to a public instance, but you can ship the same experience from within datasette. 

        ## Explore the mini-API

        You can connect to an instance by using the `Datasette` class. This is provided by the notebook.
        """
    )
    return


@app.cell
def _(Datasette):
    datasette = Datasette("https://calmcode-datasette.fly.dev")
    return (datasette,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Just to mention a few helpers, we've got this one that allows you to fetch all the databases attached to the datasette instance.""")
    return


@app.cell
def _(datasette):
    datasette.databases
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Given a database, you can also check for all the available tables.""")
    return


@app.cell
def _(datasette):
    datasette.tables(database="calmcode")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Spot a table you want to investigate? You can run SQL against it!""")
    return


@app.cell
def _(datasette):
    datasette.sql_polars(database="calmcode", sql="select * from chickweight LIMIT 5;")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""There is also a helper method to pull in the entire table. Just be aware that this can get slow because we don't access the SQlite database directly. All the data is pulled in via the JSON api.""")
    return


@app.cell
def _(datasette):
    df_chickweight = datasette.get_polars(database="calmcode", table="chickweight")
    return (df_chickweight,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""One nice thing about bringing the data into a polars dataframe is that you have access to Python again, so plotting is super easy and machine learning also suddenly becomes an option!""")
    return


@app.cell
def _(df_chickweight, pl):
    p1 = df_chickweight.plot.scatter("Time", "weight")
    p2 = (
        df_chickweight
        .with_columns(diet=pl.col("Diet").cast(pl.String()))
        .group_by("diet", "Time")
        .mean()
        .plot.line("Time", "weight", color="diet")
    )
    p1 + p2
    return p1, p2


@app.cell(hide_code=True)
def _():
    import altair 
    import marimo as mo
    import requests as rq
    import marimo as mo
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
        altair,
        cached_property,
        json,
        lru_cache,
        marimo_host,
        mo,
        pl,
        rq,
    )


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
