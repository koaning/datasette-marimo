from datasette import hookimpl, Response

import html


async def marimo(request):
    return Response.redirect("/-/static-plugins/datasette_marimo/index.html")


@hookimpl
def register_routes():
    return [(r"^/marimo/", marimo), (r"^/marimo", marimo)]
