<<<<<<< HEAD
from datasette import hookimpl, Response, Request

import html
=======
from datasette import Response, hookimpl
>>>>>>> 7bf0e4a628063459f15ce5ebd02fb32ee9ae4c74


async def marimo(request):
    print(request.path)
    return Response.redirect("/-/static-plugins/datasette_marimo/index.html")


@hookimpl
def register_routes():
    return [(r"^/marimo/", marimo), (r"^/marimo", marimo)]
