Scrapy, TOR and Playwright Demo Use Cases
========================================================================================================================

This sections cover some typical use cases for |ProjectFriendlyName|, for a description of the all functionality refer
to the *API* section. The examples below assume the relevant Docker containers are up and running and the commands are
executed from the *Scrapy* project directory.

Note that for simplicity, there is no error handling in the examples shown.

#1: Targetting non Javascript website
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. code-block:: powershell

    scrapy crawl quotes -a mode='nojs'

Targets `https://quotes.toscrape.com/` and saves all the relevant items to `pipelines/fs` folder.

#2: Targetting Javascript website
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. code-block:: powershell

    scrapy crawl quotes -a mode='js'

Targets `https://quotes.toscrape.com/js` and saves all the relevant items to `pipelines/fs` folder.

#2: Obtaining IP details and web browser information
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. code-block:: powershell

    scrapy crawl quotes -a mode='test'

Targets `https://api.seeip.org/geoip`, `https://bot.sannysoft.com/` and
`https://arh.antoinevastel.com/bots/areyouheadless` and saves all the relevant items to `pipelines/fs` folder.

Note that at time of writing these websites detect the web browser as headless, however it is not the purpose of the
demo to bypass those checks and they are simply provided for informational purposes.
