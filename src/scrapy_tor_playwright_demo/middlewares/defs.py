"""Common definitions for spider and downloader middlewares, for details refer to:

    - https://docs.scrapy.org/en/latest/topics/spider-middleware.html
    - https://docs.scrapy.org/en/latest/topics/downloader-middleware.html"""

import logging

from ..defs import LoggerMixin


class MiddlewareBase(LoggerMixin):
    """Base class for middlewares, defines common functionality for all."""

    # pylint: disable=too-few-public-methods

    ## Private API #####################################################################################################
    def __init__(self, logger: logging.Logger | None = None) -> None:
        """Class constructor.

        :param logger: The logger for the parser."""
        #: The logger to use internally in the parser.
        self.__logger = logger if logger is not None else logging.getLogger("dummy")

    ## Protected API ###################################################################################################

    ## Public API ######################################################################################################
    @property
    def logger(self) -> logging.Logger:
        """Returns the logger, required by :class:LoggerMixin.

        :return: The logger."""
        return self.__logger
