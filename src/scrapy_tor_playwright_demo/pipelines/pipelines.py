"""Pipelines."""

import json
import os
import shutil
import uuid
from typing import cast

import scrapy
import scrapy.crawler
import scrapy.item
import twisted.internet.defer

from ..items import HTMLItem
from .defs import PipelineBase


class FileSystemPipeline(PipelineBase):
    """Pipeline that serializes items to the local filesystem."""

    ## Private API #####################################################################################################
    def __init__(self, *args, **kwargs) -> None:
        """Pipeline constructor.

        Called by :meth:`scrapy.Spider.from_crawler` when Scrapy creates pipelines."""
        # Call the parent constructor.
        super().__init__(*args, **kwargs)
        #: Base path to the folder where the serialized items will be stored.
        self.__folder = os.path.normpath(os.path.join(os.path.dirname(__file__), "fs"))
        #: Path in the folder where the files will be stored.
        self.__store_path = None

    ## Protected API ###################################################################################################

    ## Public API ######################################################################################################
    @classmethod
    def from_crawler(cls, crawler: scrapy.crawler.Crawler) -> "FileSystemPipeline":
        """Method in Scrapy workflow that will create a new instance of the pipeline.

        :param crawler: Crawler that uses this pipeline.
        :return: The instance of the pipeline."""
        return FileSystemPipeline(logger=crawler.spider.logger if crawler.spider is not None else None)

    def open_spider(self, spider: scrapy.Spider) -> None:
        """Called when the spider is opened.

        :param spider: The spider which scraped the item."""
        # Create folder for spider.
        self.__store_path = os.path.join(self.__folder, spider.name)

        # If the path to the folder exists, then delete it and recreate it anew.
        if os.path.exists(self.__store_path):
            shutil.rmtree(self.__store_path)
        os.makedirs(self.__store_path)

        self._log_debug(f"Creating local folder at '{self.__store_path}'...")

    def process_item(
        self,
        item: scrapy.item.Item,
        spider: scrapy.crawler.Spider,
    ) -> scrapy.item.Item | twisted.internet.defer.Deferred:
        """Called for every item pipeline component. Must return an item, a deferred or raise an exception to drop the
        item.

        :param item: The scraped item.
        :param spider: The spider which scraped the item.
        :return: An item or a deferred."""
        # Determine in which format to store the item.
        if isinstance(item, HTMLItem):
            # Create path to file.
            filepath = os.path.join(cast(str, self.__store_path), f"{uuid.uuid4()}.html")
            self._log_debug(f"Storing HTML response at '{filepath}' for spider '{spider.name}'...")

            # Write contents to file.
            with open(filepath, "w+", encoding="utf8") as stream:
                stream.write(item["html"])
        else:
            # Create path to file.
            filepath = os.path.join(cast(str, self.__store_path), f"{uuid.uuid4()}.json")
            self._log_debug(f"Storing item at '{filepath}' for spider '{spider.name}'...")

            # Write contents to file, make the JSON readable.
            with open(filepath, "w+", encoding="utf8") as stream:
                stream.write(json.dumps(dict(item), indent=2))

        return item
