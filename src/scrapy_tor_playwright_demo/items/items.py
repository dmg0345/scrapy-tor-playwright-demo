"""Items."""

import scrapy
import scrapy.item


class QuoteItem(scrapy.item.Item):
    """Quote item, serialized to JSON file."""

    #: The text of the quote.
    text = scrapy.item.Field()
    #: The name of the author of the quote.
    author = scrapy.item.Field()
    #: The tags associated to the quote.
    tags = scrapy.item.Field()


class AuthorItem(scrapy.item.Item):
    """Author item, serialized to JSON file."""

    #: Name of the author.
    name = scrapy.item.Field()
    #: Description of the author.
    description = scrapy.item.Field()


class HTMLItem(scrapy.item.Item):
    """HTML item, serialized to HTML file."""

    #: The text of a response.
    html = scrapy.item.Field()
