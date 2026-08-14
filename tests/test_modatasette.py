import pytest
from datasette.app import Datasette

import datasette_marimo


@pytest.mark.asyncio
async def test_plugin_is_installed():
    datasette = Datasette(memory=True)
    response = await datasette.client.get("/-/plugins.json")
    assert response.status_code == 200
    installed_plugins = {p["name"] for p in response.json()}
    assert "datasette-marimo" in installed_plugins


@pytest.mark.asyncio
async def test_menu_link_present_on_homepage():
    datasette = Datasette(memory=True)
    response = await datasette.client.get("/")
    assert response.status_code == 200
    assert "Open in marimo" in response.text
    assert "/marimo/" in response.text


def test_menu_link_prefills_current_database():
    datasette = Datasette(memory=True)

    class Req:
        path = "/_memory/sqlite_master"

    (link,) = datasette_marimo.menu_links(datasette, actor=None, request=Req())
    assert link["label"] == "Open in marimo"
    assert link["href"] == "/marimo/?database=_memory&table=sqlite_master"


def test_menu_link_generic_when_not_on_a_database():
    datasette = Datasette(memory=True)

    class Req:
        path = "/-/plugins"

    (link,) = datasette_marimo.menu_links(datasette, actor=None, request=Req())
    assert link["href"] == "/marimo/"


@pytest.mark.asyncio
async def test_marimo_redirect_preserves_query_string():
    datasette = Datasette(memory=True)
    response = await datasette.client.get("/marimo/?database=foo&table=bar")
    assert response.status_code == 302
    location = response.headers["location"]
    assert location.startswith(
        "/-/static-plugins/datasette_marimo/index.html?"
    )
    assert "database=foo" in location
    assert "table=bar" in location
