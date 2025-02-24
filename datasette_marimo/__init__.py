from datasette import Response, hookimpl


async def marimo(request):
    print(request.path)
    return Response.redirect("/-/static-plugins/datasette_marimo/index.html")


@hookimpl
def register_routes():
    return [(r"^/marimo/", marimo), (r"^/marimo", marimo)]
