"""Common definitions for the project."""

import logging
import uuid
from typing import Any

import playwright_stealth
import scrapy
import scrapy.http
import twisted.python.failure


class PlaywrightMixin:
    """A mixin that provides Playwight utils and functionality."""

    # pylint: disable=too-few-public-methods

    ## Private API #####################################################################################################
    @staticmethod
    async def __playwright_stealth_init_page_callback(page: Any, request: scrapy.http.Request) -> None:
        """Callback suitable for ``playwright_page_init_callback`` that adds stealth to playwright requests.

        :param page: The ``page`` parameter of the callback.
        :param request: The ``request`` parameter of the callback."""
        # pylint: disable=unused-argument

        await playwright_stealth.stealth_async(page)

    @staticmethod
    async def __playwright_request_errback(failure: twisted.python.failure.Failure) -> None:
        """Callback for requests that result in error, where it closes the Playwright context.

        :param failure: The failure as raised by Scrapy."""
        await PlaywrightMixin._close_playwright_context(getattr(failure, "request"))

    ## Protected API ###################################################################################################
    @staticmethod
    def _is_playwright_request(request: scrapy.http.Request) -> bool:
        """Determines if a given request is intended for use with Playwright.

        :param request: The request to check for.
        :return: ``True`` if a Playwright request, ``False`` otherwise."""
        return "playwright" in request.meta

    @staticmethod
    def _to_playwright_request(request: scrapy.http.Request) -> scrapy.http.Request:
        """Converts a request suitable for Playwright.

        :param request: The request.
        :return: The Playwright request."""
        # If the request is already a Playwright request, then ignore.
        if not PlaywrightMixin._is_playwright_request(request):
            # Set request as Playwright request.
            request.meta["playwright"] = True
            # Ensure there is a new context per request by generating it with a unique identifier.
            request.meta["playwright_context"] = f"{uuid.uuid4()}"
            # Set default context arguments.
            request.meta["playwright_context_kwargs"] = {}
            # Include page, so that it is possible to close the context gracefully later.
            request.meta["playwright_include_page"] = True
            # Set callbacks.
            if request.errback is None:
                request.errback = PlaywrightMixin.__playwright_request_errback
            request.meta["playwright_page_init_callback"] = PlaywrightMixin.__playwright_stealth_init_page_callback

        return request

    @staticmethod
    def _add_playwright_proxy(request: scrapy.http.Request) -> scrapy.http.Request:
        """Adds a proxy added to the request by ``scrapy-rotating-proxies`` in Playwright format.

        :param request: The request to add a proxy in Playwright format to.
        :return: The Playwright request."""
        if PlaywrightMixin._is_playwright_request(request):
            # Get proxy data from rotating proxies metadata.
            if request.meta.get("_rotating_proxy", False):
                request.meta["playwright_context_kwargs"]["proxy"] = {"server": request.meta["proxy"]}

        return request

    @staticmethod
    def _get_playwright_proxy(request: scrapy.http.Request) -> str | None:
        """Returns the proxy of the request added by ``scrapy-rotating-proxies``.

        :param request: The Playwright request.
        :return: The proxy of the request, or ``None`` if not a Playwright request."""
        if PlaywrightMixin._is_playwright_request(request):
            return request.meta["playwright_context_kwargs"]["proxy"].get("server", None)

        return None

    @staticmethod
    def _get_playwright_context_id(request: scrapy.http.Request) -> str | None:
        """Returns the Playwright context identifier.

        :param request: The Playwright request.
        :return: The context identifier of the request, or ``None`` if not a Playwright request."""
        if PlaywrightMixin._is_playwright_request(request):
            return request.meta["playwright_context"]

        return None

    @staticmethod
    async def _close_playwright_context(request: scrapy.http.Request) -> None:
        """Given a request, closes the associated Playwright page and context.

        :param request: Playwright request."""
        if PlaywrightMixin._is_playwright_request(request):
            # Get page and close it.
            page = request.meta["playwright_page"]
            await page.close()
            # Afterwards, close the context.
            await page.context.close()

    ## Public API ######################################################################################################


class LoggerMixin:
    """A mixin that provides logging utils and functionality.

    This mixin expects a ``logger`` property to exist and return an object of type :class:`logging.Logger` in the
    derived class."""

    # pylint: disable=too-few-public-methods

    ## Private API #####################################################################################################
    @classmethod
    def __init_subclass__(cls) -> None:
        """Verifies that the schema imposed by the mixin is respected in the child class.

        :raises RuntimeError: The schema is not respected."""
        if not hasattr(cls, "logger"):
            raise RuntimeError(f"Class {cls.__name__} is missing a 'logger' property.")

    def __get_logger(self) -> logging.Logger:
        """Obtains the logger for the spider.

        :return: The logger of the spider."""
        # This is expected to exist.
        return getattr(self, "logger")

    ## Protected API ###################################################################################################
    def _log_debug(self, msg: str) -> None:
        """Prints a message to the log at debug level.

        :param msg: The debug message to print."""
        self.__get_logger().log(logging.DEBUG, msg)

    def _log_info(self, msg: str) -> None:
        """Prints a message to the log at information level.

        :param msg: The information message to print."""
        self.__get_logger().log(logging.INFO, msg)

    def _log_error(self, msg: str) -> None:
        """Prints a message to the log at error level.

        :param msg: The error message to print."""
        self.__get_logger().log(logging.ERROR, msg)

    ## Public API ######################################################################################################
