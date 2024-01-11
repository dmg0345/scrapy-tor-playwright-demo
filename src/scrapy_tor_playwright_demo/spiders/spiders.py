"""Spiders."""

from collections.abc import AsyncIterator
from typing import Any, Literal

import scrapy
import scrapy.crawler
import scrapy.exceptions
import scrapy.http
import scrapy.item
import scrapy.settings

from ..items import QuotesParser
from .defs import SpiderBase


class QuotesSpider(SpiderBase):
    """Quotes spider, this is a sample spider to test ideas and use as a playground. It can be executed as below:

    .. code-block:: powershell

        # No JavaScript website.
        ./manage.ps1 scrapy crawl quotes `-a mode='nojs'
        # JavaScript website.
        ./manage.ps1 scrapy crawl quotes `-a mode='nojs'
        # Obtain stealth and IP statuses.
        ./manage.ps1 scrapy crawl quotes `-a mode='test'
    """

    # pylint: disable=abstract-method

    #: The name of the spider.
    name: str = "quotes"
    #: The domains the spider is allowed to crawl.
    allowed_domains: list[str] = ["quotes.toscrape.com"]
    #: Custom settings, will override project-wide settings.
    custom_settings: dict[str, str | int | bool | list[str | int | bool]] = {}
    #: Crawler object to which the spider is bound.
    crawler: scrapy.crawler.Crawler
    #: Configuration for running the spider.
    settings: scrapy.settings.Settings
    #: A dictionary that can be used to persist data across batches.
    state: dict[str, Any] = {}

    ## Private API #####################################################################################################
    def __init__(self, mode: Literal["nojs", "js", "test"], *args, **kwargs) -> None:
        """Spider constructor.

        Called by :meth:`scrapy.Spider.from_crawler` when Scrapy creates spiders.

        :param mode: The mode under which to run the spider."""
        # Call the parent constructor.
        super().__init__(*args, **kwargs)

        # Signal that initialization has started.
        self._log_debug("Initializing spider...")

        if mode not in ("nojs", "js", "test"):
            raise RuntimeError(f"An invalid mode '{mode}' was supplied.")

        #: The mode under which the spider will run.
        self.__mode = mode
        self._log_debug(f"Mode set to '{self.__mode}'...")

        # Signal that initialization has finished.
        self._log_debug("Spider initialized.")

    def __del__(self, *args, **kwargs) -> None:
        """Spider destructor."""
        # Deinitialization trigerred thus signal, can't signal when it finishes as logger is not guaranteed to exist.
        self._log_debug("Deinitializing spider...")

    ## Protected API ###################################################################################################

    ## Public API ######################################################################################################
    def start_requests(self) -> list[scrapy.http.Request]:
        """Generates the requests on which to start scraping.

        :raises RuntimeError: The start requests could not be generated.
        :return: A list with the start requests."""
        # Signal that generation of start requests has started.
        self._log_debug("Generating start requests...")

        # Create requests, depending on whether scraping website with JavaScript or not.
        if self.__mode == "nojs":
            urls = ["https://quotes.toscrape.com/"]
        elif self.__mode == "js":
            urls = ["https://quotes.toscrape.com/js/"]
        elif self.__mode == "test":
            urls = [
                "https://bot.sannysoft.com/",
                "https://api.seeip.org/geoip",
                "https://arh.antoinevastel.com/bots/areyouheadless",
            ]
        else:
            raise RuntimeError(f"Invalid mode '{self.__mode}', can't generate start requests.")

        # Create the the requests and log them, then signal that generation of start requests has finished.
        reqs = [self._to_playwright_request(scrapy.http.Request(url, self.aparse)) for url in urls]
        _ = [self._log_debug(f"Generated request for URL '{request.url}'...") for request in reqs]
        self._log_debug(f"Generated {len(reqs)} start requests.")

        return reqs

    async def aparse(
        self,
        response: scrapy.http.Response,
        *args,
        **kwargs,
    ) -> AsyncIterator[scrapy.http.Request | scrapy.item.Item]:
        """Asynchronous callback to parse responses, this is suitable when using Playwright and it needs to be passed
        explicitly to each request.

        :param response: The reponse to process.
        :param args: Remaining Scrapy positional arguments.
        :param kwargs: Remaining Scrapy keyword arguments.
        :raises scrapy.exceptions.CloseSpider: If a response has no associated request, necessary to handle Playwright.
        :returns: Request to follow."""
        # pylint: disable=unused-argument

        self._log_debug(f"Asynchronously parsing responses from '{response.url}' with HTTP code '{response.status}'...")

        # Ensure there is a response for the request, Playwright requires the original request for handling.
        if response.request is None:
            raise scrapy.exceptions.CloseSpider("No associated request for response.")

        # CLose Playwright context.
        self._log_debug("Closing context of Playwright request")
        await self._close_playwright_context(response.request)
        self._log_debug("Playwright context closed.")

        # Parse response.
        parser = QuotesParser(response, self.logger.logger).parse()
        # Yield requests.
        for request in parser.requests:
            yield request
        # Yield items.
        for item in parser.items:
            yield item

        self._log_debug("Asynchronously parsed response.")
