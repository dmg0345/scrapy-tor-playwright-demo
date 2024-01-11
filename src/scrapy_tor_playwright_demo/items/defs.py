"""Common definitions for items and their parsers, for details refer to:

    - https://docs.scrapy.org/en/latest/topics/items.html"""

import logging
from abc import ABC, abstractmethod
from urllib.parse import urlparse

import bs4
import scrapy
import scrapy.http
import scrapy.item

from ..defs import LoggerMixin, PlaywrightMixin


class BSMixin:
    """A mixin for parsers that includes functionality related to Beautiful Soup 4."""

    # pylint: disable=too-few-public-methods

    ## Private API #####################################################################################################

    ## Protected API ###################################################################################################
    @staticmethod
    def _as_bs4_obj(html: str) -> bs4.BeautifulSoup:
        """Loads the given HTML content as a Beautiful Soup 4 object.

        :param html: The HTML to load.
        :return: The Beautiful Soup 4 object."""
        return bs4.BeautifulSoup(html, "html.parser")

    @staticmethod
    def _remove_whitespace(text: str, rem_chars: str = "") -> str:
        """When retrieving text from tags, it can be filled with line endings or weird whitespace, this method
        removes whitespace from a text and joins everything in a single line.

        :param text: The text to remove whitespace from.
        :param rem_chars: Additional characters to remove from the text.
        :return: The text as a single line."""
        # Remove all whitespace and join every word with a space.
        processed_text = " ".join([line.strip() for line in text.split()])
        # Remove additional characters if any.
        for char in rem_chars:
            processed_text = processed_text.replace(char, "")
        # Return processed text.
        return processed_text

    @staticmethod
    def _get_url_base(url: str) -> str:
        """Gets the protocol, host and domain from the given absolute URL.

        For example, for ``http://www.example.com/path``, it returns ``http://www.example.com``.

        :param url: The URL.
        :return: The URL base."""
        parsed_url = urlparse(url)
        return f"{parsed_url.scheme}://{parsed_url.netloc}"

    @staticmethod
    def _join_url(url_base: str, path: str) -> str:
        """Joins a URL base and a path.

        :param url_base: The URL base.
        :param path: The path to add to the URL base.
        :return: The URL."""
        return f"{url_base}/{path[1:] if path.startswith('/') else path}"

    ## Public API ######################################################################################################


class ParserBase(BSMixin, LoggerMixin, PlaywrightMixin, ABC):
    """Base class for parsers, defines common functionality for all."""

    ## Private API #####################################################################################################
    def __init__(
        self,
        response: scrapy.http.Response,
        logger: logging.Logger | None = None,
    ) -> None:
        """Class constructor.

        :param response: The HTTP response to parse.
        :param logger: The logger for the parser."""
        #: The HTTP response object passed during initialization.
        self._response = response
        #: The raw HTML contents extracted from the response.
        self._html = response.text
        #: A Beautiful Soup 4 object with parsed HTML content.
        self._root = self._as_bs4_obj(self._html)
        #: The items parsed from the response.
        self.__items: list[scrapy.item.Item] = []
        #: The requests parsed from the response.
        self.__requests: list[scrapy.http.Request] = []
        #: The logger to use internally in the parser.
        self.__logger = logger if logger is not None else logging.getLogger("dummy")

    ## Protected API ###################################################################################################
    def _add_request_from_response(self, path: str) -> "ParserBase":
        """Creates a request from the response and the path given.

        :param path: The path for the request, this is tipically the ``href`` argument.
        :return: The same instance of the class on which this method was called."""
        # Create the URL.
        url = self._join_url(self._get_url_base(self._response.url), path)
        # Ensure there is a request associated for the response.
        if self._response.request is None:
            raise RuntimeError("No request to response.")
        # Add the request to the collection.
        request = scrapy.http.Request(url, self._response.request.callback)
        if self._is_playwright_request(self._response.request):
            request = self._to_playwright_request(request)
        # Append request.
        self.__requests.append(request)

        return self

    def _add_item(self, item: scrapy.item.Item | list[scrapy.item.Item]) -> "ParserBase":
        """Adds an item or multiple items to the collection of parsed items.

        :papram item: The item or items to add.
        :return: The same instance of the class on which this method was called."""
        # Check if single item or multiple and add them.
        if isinstance(item, scrapy.item.Item):
            self.__items.append(item)
        else:
            self.__items.extend(item)

        return self

    ## Public API ######################################################################################################
    @abstractmethod
    def parse(self) -> "ParserBase":
        """Performs the parsing process.

        :return: Same instance of the class on which this method was called."""

    @property
    def logger(self) -> logging.Logger:
        """Returns the logger.

        :return: The logger."""
        return self.__logger

    @property
    def requests(self) -> list[scrapy.http.Request]:
        """The requests parsed from the links in the response.

        :return: The requests."""
        return self.__requests

    @property
    def items(self) -> list[scrapy.item.Item]:
        """The items parsed from the links in the response.

        :return: The requests."""
        return self.__items
