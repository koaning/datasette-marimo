<img src="imgs/logo.png" alt="plugin logo" width="125" align="right"/>

### datasette-marimo

> Use [marimo](https://marimo.io) inside of [datasette](https://datasette.io/).

## Install

Install this plugin in the same environment as Datasette.

```
uv pip install datasette-marimo
datasette install datasette-marimo
```

## Usage

When you run a datasette server, go to "/marimo" in the browser. From there you get Marimo running in WASM with some helper tools to grab data our of datasette. The benefit is that you can run all sorts of visualisation tools and machine learning on the data without having to install any software on your local machine.

> There is one big downside: refresh the page and you loose progress. Make sure you download beforehand. 

Note, when you open the notebook you'll spot helpers that ensure that Marimo connects to the same datasette instance that is hosting it. Here's what it roughly looks like:

```python
# Fetch useful information about your datasette instance
datasette = Datasette()
datasette.databases                  # List of databases
datasette.tables(database="sqlite")  # List of tables in a database

# Two different methods to get your data as a Polars DataFrame
df = datasette.get_polars(database="sqlite", table="chickweight")
df = datasette.sql_polars(database="sqlite", sql="select * from chickweight")
```
