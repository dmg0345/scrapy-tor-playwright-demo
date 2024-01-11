"""Common definitions for pipelines, for details refer to:

    - https://docs.scrapy.org/en/latest/topics/item-pipeline.html"""

import logging

from ..defs import LoggerMixin


class PipelineBase(LoggerMixin):
    """Base class for pipelines, defines common functionality for all."""

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
        """Returns the logger.

        :return: The logger."""
        return self.__logger
