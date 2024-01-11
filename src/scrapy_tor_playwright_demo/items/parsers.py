"""Parsers for items."""


import re
from typing import Literal

from .defs import ParserBase
from .items import AuthorItem, HTMLItem, QuoteItem

# pyright: reportGeneralTypeIssues=false,reportOptionalSubscript=false,reportOptionalMemberAccess=false


class QuotesParser(ParserBase):
    """A parser for items."""

    ## Private API #####################################################################################################
    def __get_html_contents_type(self) -> Literal["quotes_nojs", "quotes_js", "author", "html"]:
        """Retrieves the type of the HTML contents.

        :return: The type of HTML content."""
        # If there is a tags box, then it is a 'quotes_nojs' type of HTML.
        if self._root.find("div", {"class": "tags-box"}) is not None:
            html_type = "quotes_nojs"
        # If there is an import of jquery, then it is a 'quotes_js' type of HTML.
        elif self._root.find("script", {"src": re.compile(r".*jquery.js")}) is not None:
            html_type = "quotes_js"
        # If there is author details, then it is an 'author' type of HTML.
        elif self._root.find("div", {"class": "author-details"}) is not None:
            html_type = "author"
        # If not recognized, then save as HTML as a fallback.
        else:
            html_type = "html"

        return html_type

    def __parse_html_contents_quotes(self) -> "QuotesParser":
        """Parses HTML contents of quotes type.

        :raises RuntimeError: The parsing of the HTML failed to extract data failed.
        :return: The same instance of the class on which this method was called."""
        self._log_debug(f"Parsing HTML contents of 'quotes' type from '{self._response.url}'...")

        # Loop all the quotes.
        for i, quote in enumerate(self._root.find_all("div", {"class": "quote"})):
            self._log_debug(f"Parsing quote #{i + 1} in page...")

            # Get the text.
            elem = quote.find_next("span", {"class": "text"})
            text = self._remove_whitespace(elem.get_text(), "“”")
            self._log_debug(f"Found text '{text}'...")

            # Get the author.
            elem = elem.find_next("span")
            author = self._remove_whitespace(elem.find("small", {"class": "author"}).get_text())
            self._log_debug(f"Found author '{author}'...")

            # Get the link to the author details in the no javascript version.
            if self.__get_html_contents_type() == "quotes_nojs":
                author_link = self._remove_whitespace(elem.find("a")["href"])
                self._log_debug(f"Found link to author details '{author_link}'...")
                self._add_request_from_response(author_link)

            # Get the tags for the quote.
            tag_texts = []
            for tag in elem.find_next("div", {"class": "tags"}).find_all("a", {"class": "tag"}):
                # Get the text.
                tag_texts.append(self._remove_whitespace(tag.get_text()))
                self._log_debug(f"Found tag '{tag_texts[-1]}'...")

                # Get the link in the no javascript version.
                if self.__get_html_contents_type() == "quotes_nojs":
                    tag_link = self._remove_whitespace(tag["href"])
                    self._log_debug(f"Found tag link '{tag_link}'...")

            # Add item with the quote.
            self._log_debug("Added 'quote' item to collection of parsed items...")
            self._add_item(QuoteItem(text=text, author=author, tags=tag_texts))

            self._log_debug(f"Finished parsing quote #{i + 1}.")

        # There is only a tag box in the no javascript version.
        if self.__get_html_contents_type() == "quotes_nojs":
            # Get the tags box with the top tags.
            if (tags_box := self._root.find("div", {"class": "tags-box"})) is None:
                raise RuntimeError("Could not find tags box.")

            # Loop all the top tags.
            for i, tag in enumerate(tags_box.find_all("span", {"class": "tag-item"})):
                self._log_debug(f"Parsing top tag #{i + 1} in page...")

                # Get the tag text.
                elem = tag.find_next("a")
                tag_text = self._remove_whitespace(elem.get_text())
                self._log_debug(f"Found text '{tag_text}'...")

                # Get the tag link.
                tag_link = self._remove_whitespace(elem["href"])
                self._log_debug(f"Found link '{tag_link}'...")

                self._log_debug(f"Finished parsing top tag #{i + 1}.")

        # Get navigation bar.
        if (nav := self._root.find("nav")) is None:
            raise RuntimeError("Could not find navigation.")

        # Check if there is a next page.
        if (next_page := nav.find("li", {"class": "next"})) is not None:
            # Get the link to the next page.
            elem = next_page.find_next("a")
            next_page_link = self._remove_whitespace(elem["href"])
            self._log_debug(f"Found next page link '{next_page_link}'...")
            self._add_request_from_response(next_page_link)

        self._log_debug("Parsing of HTML contents of type 'quotes' finished.")

        return self

    def __parse_html_contents_author(self) -> "QuotesParser":
        """Parses HTML contents of author type.

        :return: The same instance of the class on which this method was called."""
        self._log_debug(f"Parsing HTML contents of 'author' type from '{self._response.url}'...")

        # The HTML on this site is badly formatted, just fix it and parse again.
        root = self._as_bs4_obj(self._html.replace("</h2>", "</h3>"))

        # Get the author details.
        if (author_details := root.find("div", {"class": "author-details"})) is None:
            raise RuntimeError("Could not find author details.")

        # Get the author name.
        elem = author_details.find("h3", {"class": "author-title"})
        author = self._remove_whitespace(elem.get_text())
        self._log_debug(f"Found author name '{author}'...")

        # Get the author description.
        elem = elem.find_next("div", {"class": "author-description"})
        author_description = self._remove_whitespace(elem.get_text())
        self._log_debug(f"Found author description '{author_description}'...")

        # Add item.
        self._add_item(AuthorItem(name=author, description=author_description))
        self._log_debug("Added 'author' item to collection of parsed items...")

        self._log_debug("Parsing of HTML contents of type 'author' finished.")

        return self

    def __parse_html_contents_html(self) -> "QuotesParser":
        """Parses HTML contents of HTML type.

        :return: The same instance of the class on which this method was called."""
        self._log_debug(f"Parsing HTML contents of 'html' type from '{self._response.url}'...")

        # Add item.
        self._add_item(HTMLItem(html=self._response.text))
        self._log_debug("Added 'html' item to collection of parsed items...")

        self._log_debug("Parsing of HTML contents of type 'html' finished.")

        return self

    ## Protected API ###################################################################################################

    ## Public API ######################################################################################################
    def parse(self) -> "QuotesParser":
        """Runs the parsing process.

        :raises RuntimeError: The type of HTML content identified could not be handled.
        :return: The same instance of the class on which this method was called."""
        self._log_debug("Starting parsing of HTML...")

        # Get the type of the HTML.
        html_type = self.__get_html_contents_type()
        self._log_debug(f"HTML contents are of type '{html_type}'...")

        ## Handle 'quotes_nojs' and 'quotes_js' HTML contents ##########################################################
        if html_type in {"quotes_nojs", "quotes_js"}:
            self.__parse_html_contents_quotes()
        ## Handle 'author' HTML contents ###############################################################################
        elif html_type == "author":
            self.__parse_html_contents_author()
        ## Handle 'html' HTML contents #################################################################################
        elif html_type == "html":
            self.__parse_html_contents_html()
        ## Handle unknown HTML contents ################################################################################
        else:
            raise RuntimeError(f"An type of HTML contents of '{html_type}' could not be handled.")

        self._log_debug("Parsing of HTML finished.")

        return self
