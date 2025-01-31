import marimo

__generated_with = "0.10.18"
app = marimo.App()


@app.cell
def _(DATASETTE_HOST, pl, rq):
    from functools import cached_property, lru_cache

    class Datasette:
        def __init__(self, url):
            self.url = url

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
            return pl.read_csv(f"{self.url}/{database}/{table}.csv?_dl=on&_stream=on&_size=max")

    Datasette(DATASETTE_HOST).tables("sqlite")
    return Datasette, cached_property, lru_cache


@app.cell
def _(widget):
    DATASETTE_HOST = widget.datasette_host
    return (DATASETTE_HOST,)


@app.cell
def _(URLWidget, mo):
    widget = mo.ui.anywidget(URLWidget())
    widget
    return (widget,)


@app.cell
def _():
    import marimo as mo
    from yarl import URL
    import anywidget
    import traitlets
    import pathlib
    import polars

    class URLWidget(anywidget.AnyWidget):
        # Python-side trait to store the URL
        current_url = traitlets.Unicode("").tag(sync=True)
        _esm = """
            function render({model, el}) {
                console.log("loaded")
                model.set('current_url', window.location.href);
                model.save_changes();
            }

            export default {render}
        """

        @property
        def datasette_host(self):
            url = URL(self.current_url)
            return f"{url.scheme}://{url.authority}"


    def datasette_host(): 
        widget = mo.ui.anywidget(URLWidget())
        print(widget.current_url)
        url = URL(widget.current_url)
        return f"{url.scheme}://{url.authority}"
    return (
        URL,
        URLWidget,
        anywidget,
        datasette_host,
        mo,
        pathlib,
        polars,
        traitlets,
    )


@app.cell
def _():
    import requests as rq
    return (rq,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
