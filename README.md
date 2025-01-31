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

Note, there are also some helper functions available that ensure that Marimo connects to the same datasette instance that is hosting it.

```python
from datasette_marimo import Datasette

# Fetch useful information about your datasette instance
datasette = Datasette()
datasette.databases
datasette.tables(database="sqlite")

# Two different methods to get your data as a Polars DataFrame
df = datasette.get_polars(database="sqlite", table="chickweight")
df = datasette.sql_polars(database="sqlite", sql="select * from chickweight")
```

### Fun detail 

You can also connect to another datasette instance that is hosted elsewhere if you want. The project assumes that you're main interest is running Marimo inside of datasette but you can also connect to another datasette instance if it is public.

```python
from datasette_marimo import Datasette

Datasette("https://calmcode-datasette.fly.dev/")
```