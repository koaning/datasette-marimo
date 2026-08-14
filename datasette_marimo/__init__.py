from urllib.parse import quote, unquote

from datasette import Response, hookimpl

STATIC_INDEX = "/-/static-plugins/datasette_marimo/index.html"


async def marimo(request):
    target = STATIC_INDEX
    # Forward any query string (e.g. ?database=&table=) so the WASM notebook can
    # read it via mo.query_params() and auto-connect to the right database.
    if request.query_string:
        target = f"{target}?{request.query_string}"
    return Response.redirect(target)


def _current_db_table(request, datasette):
    """Best-effort read of the (database, table) the current page is showing."""
    if request is None:
        return None, None
    parts = [unquote(p) for p in request.path.split("/") if p]
    if parts and parts[0] in datasette.databases:
        table = parts[1] if len(parts) > 1 else None
        return parts[0], table
    return None, None


@hookimpl
def menu_links(datasette, actor, request):
    href = datasette.urls.path("/marimo/")
    database, table = _current_db_table(request, datasette)
    if database:
        href = f"{href}?database={quote(database)}"
        if table:
            href = f"{href}&table={quote(table)}"
    return [{"href": href, "label": "Open in marimo"}]


@hookimpl
def register_routes():
    return [(r"^/marimo/", marimo), (r"^/marimo", marimo)]
