from datasette import hookimpl, Response

import requests as rq
import marimo as mo
from yarl import URL
import polars as pl
import json
from functools import cached_property, lru_cache
import html


async def marimo(request):
    return Response.redirect("/-/static-plugins/datasette_modatasette/index.html")


@hookimpl
def register_routes():
    return [(r"^/marimo/", marimo)]


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
        url = (URL(self.url) / "sqlite.json").with_query(sql=sql, _shape="array", _nl="on", _size="max")
        return pl.DataFrame([json.loads(_) for _ in rq.get(f"{url}").text.split("\n")])


def marimo_host(): 
    url = URL(str(mo.notebook_location()))
    return f"{url.scheme}://{url.authority}"