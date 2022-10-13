from collections.abc import Sequence
from typing import Iterator

import bs4
import urllib3

from .post import Post
from ..utils import validator, is_list_of_safe_strings


class Page(Sequence[Post]):
    """A container for Rule34 posts page."""

    def __init__(self, number: int, query: list[str], posts: list[Post]):
        self.number = number
        self.query = query
        self.posts = posts

    @staticmethod
    def from_html(html: str, number: int, query: list[str]):
        """Parses HTML of a page and returns a page instance with the pre-specified page number and query."""
        soup = bs4.BeautifulSoup(html, "lxml")
        images = soup.select("div.shm-thumb.thumb")
        posts = list[Post]()
        for image in images:
            thumb = image.select_one("a.shm-thumb-link img")
            thumbnail = thumb.attrs["src"]
            tags = image.attrs["data-tags"].split(" ")
            identifier = int(image.attrs["data-post-id"])
            # TODO Parse info from img title
            file = image.select_one('a:-soup-contains("File Only")').attrs["href"]
            posts.append(
                Post(
                    identifier=identifier,
                    tags=tags,
                    link=urllib3.util.parse_url(
                        "https://rule34.paheal.net/post/view/{identifier}".format(
                            identifier=identifier
                        )
                    ),
                    thumbnail=urllib3.util.parse_url(thumbnail),
                    file=urllib3.util.parse_url(file),
                    query=query,
                )
            )
        return Page(number, query, posts)

    @staticmethod
    def find_pages_count(html: str) -> int:
        """Parses HTML of a page and returns the number of the last page (number of pages) in the query."""
        soup = bs4.BeautifulSoup(html, "lxml")
        last_link = soup.select_one(".blockbody a:-soup-contains(Last)")
        if last_link is None:
            last_number = soup.select("div.blockbody b a")[-1]
            link = urllib3.util.parse_url(last_number.attrs["href"])
        else:
            link = urllib3.util.parse_url(last_link.attrs["href"])
        return int(link.path.split("/")[-1])

    @property
    def number(self):
        """Number getter."""
        return self._number

    @number.setter
    def number(self, value: int):
        """Number setter."""
        self._number = value

    @property
    def query(self):
        """Query getter."""
        return self._query

    @query.setter
    @validator(
        lambda query: not is_list_of_safe_strings(query),
        ValueError(
            "Query must be a list of string consist of letter, numbers, dashes, underscores and "
            "apostrophes"
        ),
    )
    def query(self, value):
        """Query setter."""
        self._query = value

    @property
    def posts(self):
        """Posts getter."""
        return self._posts

    @posts.setter
    def posts(self, value):
        """Posts setter."""
        self._posts = value

    def __getitem__(self, index: int | slice):
        """x.__getitem__(y) <==> x[y]"""
        if isinstance(index, slice):
            return self.__class__(self._number, self._query, self._posts[index])
        return self._posts[index]

    def index(self, value: Post, start: int = ..., stop: int = ...) -> int:
        """
        Returns first index of post.

        Raises ValueError if the value is not present.
        """
        return self._posts.index(value, start, stop)

    def count(self, value: Post) -> int:
        """Returns number of occurrences of value."""
        return self._posts.count(value)

    def __contains__(self, value: Post) -> bool:
        """Returns key in self."""
        return value in self._posts

    def __iter__(self) -> Iterator[Post]:
        """Implements iter(self)."""
        return self._posts.__iter__()

    def __reversed__(self) -> Iterator[Post]:
        """Returns a reverse iterator over the page."""
        return self._posts.__reversed__()

    def __len__(self) -> int:
        """Returns len(self)."""
        return self._posts.__len__()
