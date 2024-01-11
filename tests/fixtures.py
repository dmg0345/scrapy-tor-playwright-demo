"""Pytest fixtures."""

import os
from collections.abc import Iterator

import pytest
import scrapy.http


@pytest.fixture()
def response(request: pytest.FixtureRequest) -> Iterator[scrapy.http.Response]:
    """A fixture that loads the contents of an HTML file into a HTTP response.

    The example below shows an example on how to use the fixture and its parameters:

    .. code-block:: python

        params_dict = {
            "url": "https://quotes.toscrape.com/author/Thomas-A-Edison/",
            "path": "quotes/author_page.html",
            "status": 200
        }

        @pytest.mark.parametrize("response", [params_dict], indirect=True)
        def test_example(response: str):
            pass

    The ``url`` where the contents where fetched from, this parameter is optional and defaults to
    ``https://127.0.0.1/``.

    The ``path`` is the path to the HTML file, relative to ``tests/assets`` this parameter is mandatory.

    The ``status`` is the status code for the HTTP response, this parameter is optional and defaults to 200.

    :param request: The Pytest request object.
    :raises RuntimeError: The HTML file does not exist.
    :returns: The HTML content of the file as a string."""
    # Fetch parameters from request.
    url: str = request.param.get("url", "https://127.0.0.1/")
    html_path: str = request.param["path"]
    status: int = request.param.get("status", 200)

    # Create the full path and ensure it exists.
    html_full_path = os.path.join(os.path.dirname(__file__), "assets", html_path)
    if not all([os.path.exists(html_full_path), os.path.isfile(html_full_path)]):
        raise RuntimeError(f"The file at '{html_full_path}' does not exist or it is not a file.")

    # Open file and get contents as a string.
    with open(html_full_path, "rb") as stream:
        html_contents = stream.read()

    # Yield the response.
    yield scrapy.http.HtmlResponse(request=scrapy.http.Request(url), url=url, body=html_contents, status=status)
