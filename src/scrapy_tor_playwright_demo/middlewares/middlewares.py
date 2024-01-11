"""Spider and downloader middlewares."""

import scrapy
import scrapy.crawler
import scrapy.exceptions
import scrapy.http
import scrapy.signals

from ..defs import PlaywrightMixin
from .defs import MiddlewareBase


class PlaywrightMiddleware(PlaywrightMixin, MiddlewareBase):
    """Playwright downloader middleware.

    If using ``scrapy-rotating-proxies`` it must be called immediately after it, for example:

    .. code-block:: python

        DOWNLOADER_MIDDLEWARES = {
            "rotating_proxies.middlewares.RotatingProxyMiddleware": 610,
            "scrapy_tor_playwright_demo.proxies.middlewares.PlaywrightProxyDownloaderMiddleware": 615,
            "rotating_proxies.middlewares.BanDetectionMiddleware": 620,
        }"""

    ## Private API #####################################################################################################
    def __init__(self, *args, **kwargs) -> None:
        """Class constructor."""
        super().__init__(*args, **kwargs)

    ## Protected API ###################################################################################################

    ## Public API ######################################################################################################
    @classmethod
    def from_crawler(cls, crawler: scrapy.crawler.Crawler) -> "PlaywrightMiddleware":
        """Method in Scrapy workflow that will create a new instance of the middleware.

        :param crawler: Crawler that uses this middleware.
        :return: The instance of the middleware."""
        return PlaywrightMiddleware(logger=crawler.spider.logger if crawler.spider is not None else None)

    def process_request(self, request: scrapy.http.Request, spider: scrapy.crawler.Spider) -> None:
        """Processes the request, by fetching the proxy configured by ``scrapy-rotating-proxies`` if there is one
        and adding it in the Playwright context in a suitable format.

        If the request is not a Playwright request, then there is no processing on the request.

        :param request: The request with an associated proxy and
        :param spider: The spider that performed the request."""
        # pylint: disable=unused-argument

        # Process request if a Playwright request.
        if self._is_playwright_request(request):
            self._add_playwright_proxy(request)
            if (proxy := self._get_playwright_proxy(request)) is not None:
                identifier = self._get_playwright_context_id(request)
                self._log_debug(f"Added proxy '{proxy}' to Playwright request with context ID {identifier}.")

    def process_response(
        self,
        request: scrapy.http.Request,
        response: scrapy.http.Response,
        spider: scrapy.crawler.Spider,
    ) -> scrapy.http.Response | scrapy.http.Request | None:
        """Processes the response, doing nothing to it and returning it as is.

        :param request: The request that originated the response.
        :param response: The response being processed.
        :param spider: The spider that performed the request.
        :returns: The response."""
        # pylint: disable=unused-argument,no-self-use

        # Return response as is, without further processing.
        return response

    def process_exception(
        self,
        request: scrapy.http.Request,
        exception: Exception,
        spider: scrapy.crawler.Spider,
    ) -> scrapy.http.Response | scrapy.http.Request | None:
        """Called when a download handler or the processing of a request of the download middleware raises an exception.
        Must return none, a response object or a request object.

        :param request: The request that generated the exception.
        :param exception: The raised exception.
        :param spider: The spider for which this request is intended."""
        # pylint: disable=unused-argument

        if self._is_playwright_request(request):
            self._log_debug(f"Request to '{request.url}' ended with exception '{exception}'...")
