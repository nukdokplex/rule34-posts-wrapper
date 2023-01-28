import urllib.parse

from collections.abc import Sequence
from typing import Iterator

from requests import Response

from .objects import Page
from .objects import Post
import requests

from .utils import is_list_of_safe_strings

PER_PAGE = 70


class PostsWrapper(Sequence):
    """A wrapper for Rule34 posts"""

    def __init__(self, query: list[str], proxy: dict = None):
        """Creates instance of Posts Wrapper."""
        self._query = query

        if not is_list_of_safe_strings(self._query):
            raise ValueError(
                "Tags must be a list of strings consist of letters, numbers, dashes, underscores and "
                "apostrophes"
            )
        if len(query) > 3:
            raise ValueError(
                "Query can't have more than 3 tags due to rule34.paheal.net restrictions"
            )

        self._proxy = proxy
        self._loaded_pages = dict()
        self._cookies = {"ui-tnc-agreed": "true"}
        self._headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/106.0.0.0 Safari/537.36",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,zh-CN;q=0.5,zh;q=0.4",
            "cache-control": "no-cache",
        }
        first_page = self._fetch_page(0)
        if first_page.status_code == 404:
            self._count = 0
            self._page_count = 0
            return
        self._loaded_pages[0] = Page.from_html(first_page.text, 1, self._query)
        self._page_count = Page.find_pages_count(first_page.text)
        last_page = self._get_page(self._page_count - 1)
        self._count = PER_PAGE * (self._page_count - 1) + len(last_page)
        self._loaded_pages[self._page_count - 1] = last_page

    @staticmethod
    def get_page_url(search: list[str], page: int):
        """Generates Rule34 page URL."""
        return "https://rule34.paheal.net/post/list/{query}/{page}".format(
            query=urllib.parse.quote(str.join(" ", search)), page=page + 1
        )

    def _fetch_page(self, page: int = 0) -> Response:
        """Fetches response from Rule34 page."""
        try:
            r = requests.get(
                PostsWrapper.get_page_url(self._query, page),
                cookies=self._cookies,
                headers=self._headers,
                proxies=self._proxy,
            )
        except requests.exceptions.RequestException as err:
            raise err
        return r

    def _get_page(self, page: int = 0) -> Page:
        """Fetches response from Rule34 page and parses it."""
        return Page.from_html(self._fetch_page(page).text, page, self._query)

    def load_page(self, page: int = 0, force: bool = False) -> None:
        """
        Fetches page from server, parses it and add it to loaded pages.

        If page is already present in loaded pages it will do nothing unless parameter force is true.
        """
        if page not in self._loaded_pages.keys() or force:
            self._loaded_pages[page] = self._get_page(page)

    def load_all_pages(self, force: bool = False) -> None:
        """Runs self.load_page() for all pages."""
        for page in range(self._page_count):
            self.load_page(page, force)

    @property
    def query(self):
        """Query getter."""
        return self._query

    @staticmethod
    def _get_post_page_number(index: int) -> int:
        """Returns page number where post with specified index appears."""
        if index < 0:
            raise ValueError("Index must be a positive integer")
        return index // PER_PAGE
        # 0, 1, 2 ... 67, 68, 69 | 70, 71, 72 ... 137, 138, 139 | 140, 141, 142 ... 207, 208, 209 | index
        # 0, 0, 0 ... 0,  0,  0  | 1,  1,  1  ... 1,   1,   1   | 2,   2,   2,  ... 2,   2,   2   | index // PER_PAGE

    def _get_post_page(self, index: int) -> int:
        """Returns page where post with specified index appears."""
        page = PostsWrapper._get_post_page_number(index)
        if page not in self._loaded_pages:
            self.load_page(page)
        return self._loaded_pages[page]

    @staticmethod
    def _pages_including_posts(start: int, end: int) -> range:
        """Returns page numbers range that includes posts from start to end."""
        if start < 0 or end < 0:
            raise ValueError("Start and end must be a positive integers")
        if start > end:
            raise ValueError("Start must be less than or equal to end")
        return range(
            PostsWrapper._get_post_page_number(start),
            PostsWrapper._get_post_page_number(end) + 1,
        )

    @staticmethod
    def _get_post_index_in_page(index: int):
        """Returns inner page's post index."""
        if index < 0:
            raise ValueError("Index must be a positive integer")
        return index % PER_PAGE
        # 0, 1, 2 ... 67, 68, 69 | 70, 71, 72 ... 137, 138, 139 | 140, 141, 142 ... 207, 208, 209 | index
        # 0, 1, 2 ... 67, 68, 69 | 0,  1,  2  ... 67,  68,  69  | 0,   1,   2   ... 67,  68,  69

    def __getitem__(self, index: int | slice):
        """x.__getitem__(y) <==> x[y]"""
        if isinstance(index, slice):
            posts = list[Post]()
            for page in PostsWrapper._pages_including_posts(index.start, index.stop):
                self.load_page(page)
            for i in slice.indices(index, self._count):
                if i > self._count - 1:
                    continue
                posts.append(self.__getitem__(i))
        if index > self._count - 1:
            raise IndexError
        page = PostsWrapper._get_post_page_number(index)
        self.load_page(page)
        return self._loaded_pages[page][PostsWrapper._get_post_index_in_page(index)]

    def index(self, value: Post, start: int = None, stop: int = None) -> int:
        """
        Returns first index of value.

        Raises ValueError if the value is not present.
        """
        if start is None:
            start = -1
        if stop is None:
            stop = self._count
        for post in range(start + 1, stop):
            self.load_page(PostsWrapper._get_post_page_number(post))
            if self.__getitem__(post) == value:
                return post
        raise ValueError(f"{value} is not in posts")

    def count(self, value: Post) -> int:
        """Returns number of occurrences of value."""
        count = 0
        for page in range(self._page_count):
            self.load_page(page)
            count += self._loaded_pages[page].count(value)
        return count

    def __contains__(self, value: Post) -> bool:
        """Returns True if self contains value otherwise False."""
        for post in range(self._count):
            self.load_page(PostsWrapper._get_post_page_number(post))
            if self.__getitem__(post) == value:
                return True
        return False

    def __iter__(self) -> Iterator:
        """Implements iter(self)."""
        return PostsWrapperIterator(self)

    def __reversed__(self) -> Iterator:
        """Returns a reverse iterator over the list."""
        return PostsWrapperReversedIterator(self)

    def __len__(self) -> int:
        """Returns len(self)."""
        return self._count


class PostsWrapperIterator(Iterator):
    """An iterator for Posts Wrapper."""

    def __init__(self, posts_wrapper: PostsWrapper):
        """Initializes iterator for Posts Wrapper."""
        self._posts_wrapper = posts_wrapper
        self._index = 0

    def __next__(self):
        """Returns next iteration of Posts Wrapper."""
        if self._index < len(self._posts_wrapper):
            post = self._posts_wrapper[self._index]
            self._index += 1
            return post
        raise StopIteration

    def __iter__(self):
        """Returns itself."""
        return self


class PostsWrapperReversedIterator(Iterator):
    """A reversed iterator for Posts Wrapper."""

    def __init__(self, posts_wrapper: PostsWrapper):
        """Initializes reversed iterator for Posts Wrapper."""
        self._posts_wrapper = posts_wrapper
        self._index = len(self._posts_wrapper) - 1

    def __next__(self):
        """Returns next iteration of Posts Wrapper."""
        if self._index > -1:
            post = self._posts_wrapper[self._index]
            self._index -= 1
            return post
        raise StopIteration

    def __iter__(self):
        """Returns itself."""
        return self
