<img src="imgs/logo.png" alt="plugin logo" width="125" align="right"/>

### datasette-marimo

> Use [marimo](https://marimo.io) inside of [datasette](https://datasette.io/).

## Install

Install this plugin in the same environment as Datasette.

```
uv pip install datasette-marimo
datasette install datasette-marimo
```

## Demo

We host a [demo on Github pages](https://koaning.github.io/datasette-marimo/) that shows what the notebook experience could be like on a datasette server but we also have a [YouTube tutorial](https://youtu.be/32X4OYAxAaQ) that gives more details. 

## Usage

When you run a datasette server, open the top-right hamburger menu and click **"Open in marimo"** (or go to "/marimo" directly). From there you get Marimo running in WASM with a connection to your datasette instance. The benefit is that you can run all sorts of visualisation tools and machine learning on the data without having to install any software on your local machine.

> There is one big downside: refresh the page and you loose progress. Make sure you download beforehand. 

The "Open in marimo" menu link prefills the database (and table) of the page you clicked from, so the notebook lands ready to query it.

Inside the notebook you connect through a [marimo SQL connection](https://docs.marimo.io/guides/working_with_data/sql/) provided by [moutils](https://github.com/marimo-team/moutils). The connection shows up in marimo's data-sources panel, so you can browse the schema and write **native SQL cells** against it:

```python
from moutils.db.datasette import DatasetteConnection, databases

databases(base_url)                          # list databases on the instance
conn = DatasetteConnection(base_url, "sqlite")  # connect to one database

# then, in a SQL cell (or from Python):
mo.sql("select * from chickweight limit 100", engine=conn)
```

The older `Datasette` helper class (`get_polars` / `sql_polars`) is still shipped in the notebook for backwards compatibility, but `DatasetteConnection` is the recommended path.
