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

The [demo on GitHub Pages](https://koaning.github.io/datasette-marimo/) shows the notebook experience on a Datasette server. 

## Usage

Run a Datasette server. Open the top-right hamburger menu and click **Open in marimo**. You can also open `/marimo` directly.

marimo then runs in WASM with a connection to your Datasette instance. You can run visualization and machine learning tools on the data. You do not install any software on your local machine.

> Warning: if you refresh the page, you lose your work. Export your work before you refresh.

The **Open in marimo** link reads the page you came from. It prefills the database and table, so the notebook opens ready to query that table.

Inside the notebook you connect through a [marimo SQL connection](https://docs.marimo.io/guides/working_with_data/sql/) from [moutils](https://github.com/marimo-team/moutils). The connection appears in marimo's data-sources panel. You can browse the schema and write **native SQL cells** against it:

```python
from moutils.db.datasette import DatasetteConnection, databases

databases(base_url)                          # list databases on the instance
conn = DatasetteConnection(base_url, "sqlite")  # connect to one database

# then, in a SQL cell (or from Python):
mo.sql("select * from chickweight limit 100", engine=conn)
```

The moutils connection runs synchronous HTTP in the browser. It needs a browser with JSPI support, such as Chrome or Edge. On other browsers, use the legacy helper below.

The notebook still includes the older `Datasette` helper class (`get_polars` / `sql_polars`) for backward compatibility. `DatasetteConnection` is the recommended path.
