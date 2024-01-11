"""Common definitions for spiders, for details refer to:

    - https://docs.scrapy.org/en/latest/topics/spiders.html"""

import scrapy

from ..defs import LoggerMixin, PlaywrightMixin


class SpiderBase(PlaywrightMixin, LoggerMixin, scrapy.Spider):  # pylint: disable=abstract-method
    """Base class for spiders, defines common functionality for all."""

    ## Private API #####################################################################################################

    ## Protected API ###################################################################################################

    ## Public API ######################################################################################################
