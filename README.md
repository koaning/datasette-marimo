# datasette-marimo

Use [marimo](https://marimo.io) inside of Datasette.

## Installation

Install this plugin in the same environment as Datasette.

```
uv pip install datasette-marimo
datasette install datasette-marimo
```

## Usage

When you run a datasette server, go to "/marimo" in the browser. From there you get Marimo running in WASM with some helper tools to grab data our of datasette. The benefit is that you can run all sorts of visualisation tools and machine learning on the data without having to install any software on your local machine.

There is one big downside: refresh the page and you loose progress. Make sure you download beforehand. 

Note, there are also some helper functions available. 

```python
from datasette_marimo import Datasette

# Two different methods to get your data as a Polars DataFrame
df = Datasette().get_polars(database="sqlite", table="chickweight")
df = Datasette().sql_polars(database="sqlite", sql="select * from chickweight")
```
