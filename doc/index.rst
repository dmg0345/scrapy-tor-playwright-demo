Introduction
========================================================================================================================

|ProjectFriendlyName| shows an example integration of the following tools:

- `Scrapy, scraping framework for Python <https://github.com/scrapy/scrapy>`_.
- `Playwright, headless cross-platform browser <https://playwright.dev/>`_.
- `Scrapy rotating proxies <https://github.com/TeamHG-Memex/scrapy-rotating-proxies>`_.
- `TOR network proxies <https://registry.hub.docker.com/r/pickapp/tor-proxy>`_.
- `Playwright stealth <https://github.com/AtuboDad/playwright_stealth>`_.
- `Beautiful Soup <https://github.com/wention/BeautifulSoup4>`_.

The target used in this demo are the following authorized playgrounds:

- `Quotes, non Javascript version <https://quotes.toscrape.com/>`_.
- `Quotes, Javascript version <https://quotes.toscrape.com/js>`_.

The following websites are also used to get more information about the proxies and the web browser:

- `IP and geolocation details <https://api.seeip.org/geoip/>`_.
- `Web-Browser checks #1 <https://bot.sannysoft.com/>`_.
- `Web-Browser checks #2 <https://arh.antoinevastel.com/bots/areyouheadless>`_.

The demo also includes some testing, focused on the parsers, refer to
`Test Results HTML Report <_static/_test_results/test_report.html>`_ and
`Code Coverage HTML report <_static/_test_coverage/index.html>`_.

The source code for |ProjectFriendlyName| is hosted at `Github <https://github.com/dmg0345/scrapy_tor_playwright_demo>`_
and related *Docker* images for development containers are located at
`DockerHub <https://hub.docker.com/r/dmg00345/scrapy_tor_playwright_demo>`_.

.. note::

    This is the documentation for |ProjectFriendlyName|, version |ProjectVersion|.

License
-----------------------------------------------------------------------------------------------------------------------

.. literalinclude:: ../LICENSE

.. toctree::
    :caption: Main
    :titlesonly:
    :hidden:

    self
    Use Cases <usecases/scrapy_tor_playwright_demo>

.. toctree::
    :caption: API
    :titlesonly:
    :hidden:

    Spiders <api/spiders>
    Middlewares <api/middlewares>
    Items <api/items>
    Pipelines <api/pipelines>
    Commons <api/commons>
