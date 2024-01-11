"""Tests for the Quotes spider and related functionality."""

import logging

import pytest
import pytest_check as check
import scrapy.http

from scrapy_tor_playwright_demo.items import QuotesParser


class TestQuotesParser:
    """A collection of tests for the quotes parser."""

    # pylint: disable=no-self-use

    ## Private API #####################################################################################################

    ## Protected API ###################################################################################################

    ## Public API ######################################################################################################
    @pytest.mark.parametrize(
        "response",
        [{"url": "https://quotes.toscrape.com/page/1/", "path": "quotes/first_page_nojs.html"}],
        indirect=True,
    )
    def test_parse_first_page_nojs(self, response: scrapy.http.Response) -> None:
        """Tests the parsing of a first page containing quotes.

        :param response: The response to parse."""
        parser = QuotesParser(response, logger=logging.getLogger()).parse()

        check.equal(len(parser.requests), 11)
        check.equal(len(parser.items), 10)

    @pytest.mark.parametrize(
        "response",
        [{"url": "https://quotes.toscrape.com/page/2/", "path": "quotes/second_page_nojs.html"}],
        indirect=True,
    )
    def test_parse_second_page_nojs(self, response: scrapy.http.Response) -> None:
        """Tests the parsing of an intermediate page containing quotes.

        :param response: The response to parse."""
        parser = QuotesParser(response, logger=logging.getLogger()).parse()

        check.equal(len(parser.requests), 11)
        check.equal(len(parser.items), 10)

    @pytest.mark.parametrize(
        "response",
        [{"url": "https://quotes.toscrape.com/page/10/", "path": "quotes/last_page_nojs.html"}],
        indirect=True,
    )
    def test_parse_last_page_nojs(self, response: scrapy.http.Response) -> None:
        """Tests the parsing of a last page containing quotes.

        :param response: The response to parse."""
        parser = QuotesParser(response, logger=logging.getLogger()).parse()

        check.equal(len(parser.requests), 10)
        check.equal(len(parser.items), 10)

    @pytest.mark.parametrize(
        "response",
        [{"url": "https://quotes.toscrape.com/author/Thomas-A-Edison/", "path": "quotes/author_page_nojs.html"}],
        indirect=True,
    )
    def test_parse_author_page_nojs(self, response: scrapy.http.Response) -> None:
        """Tests the parsing of an author page containing quotes.

        :param response: The response to parse."""
        parser = QuotesParser(response, logger=logging.getLogger()).parse()

        check.equal(len(parser.requests), 0)
        check.equal(len(parser.items), 1)

    @pytest.mark.parametrize(
        "response",
        [{"url": "https://quotes.toscrape.com/js/page/1/", "path": "quotes/first_page_js.html"}],
        indirect=True,
    )
    def test_parse_first_page_js(self, response: scrapy.http.Response) -> None:
        """Tests the parsing of a first page containing quotes.

        :param response: The response to parse."""
        parser = QuotesParser(response, logger=logging.getLogger()).parse()

        check.equal(len(parser.requests), 1)
        check.equal(len(parser.items), 10)

    @pytest.mark.parametrize(
        "response",
        [{"url": "https://quotes.toscrape.com/js/page/2/", "path": "quotes/second_page_js.html"}],
        indirect=True,
    )
    def test_parse_second_page_js(self, response: scrapy.http.Response) -> None:
        """Tests the parsing of a second page containing quotes.

        :param response: The response to parse."""
        parser = QuotesParser(response, logger=logging.getLogger()).parse()

        check.equal(len(parser.requests), 1)
        check.equal(len(parser.items), 10)

    @pytest.mark.parametrize(
        "response",
        [{"url": "https://quotes.toscrape.com/js/page/10/", "path": "quotes/last_page_js.html"}],
        indirect=True,
    )
    def test_parse_last_page_js(self, response: scrapy.http.Response) -> None:
        """Tests the parsing of a last page containing quotes.

        :param response: The response to parse."""
        parser = QuotesParser(response, logger=logging.getLogger()).parse()

        check.equal(len(parser.requests), 0)
        check.equal(len(parser.items), 10)
