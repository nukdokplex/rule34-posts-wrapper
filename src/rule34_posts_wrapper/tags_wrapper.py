from __future__ import annotations

from collections.abc import Sequence
from typing import SupportsIndex

import requests
from requests import Response
from urllib3.util import Url

from .objects import Tag
from .utils import is_safe_string


class TagsWrapper(Sequence):
    """A wrapper for rule34.paheal.net tag autocomplete."""

    def __init__(self, query: str, proxy: dict = None):
        if not is_safe_string(query):
            raise ValueError(
                "Query must consist of letters, numbers, dashes, underscores and apostrophes"
            )
        self._proxy = proxy
        self._cookies = {"ui-tnc-agreed": "true"}
        self._headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/106.0.0.0 Safari/537.36",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,zh-CN;q=0.5,zh;q=0.4",
            "cache-control": "no-cache",
        }
        self._query = query
        self._tags = self._get_tags()

    @staticmethod
    def generate_autocomplete_url(query: str) -> Url:
        """Returns URL to rule34.paheal.net autocomplete API based on query."""
        return Url(
            scheme="https",
            host="rule34.paheal.net",
            path="/api/internal/autocomplete",
            query="s=" + query,
        )

    def _fetch_tags(self) -> Response:
        """Fetches tags from rule34.paheal.net internal API."""
        r = requests.get(
            str(TagsWrapper.generate_autocomplete_url(self._query)),
            cookies=self._cookies,
            headers=self._headers,
            proxies=self._proxy,
        )
        self._cookies = r.cookies
        return r

    def _get_tags(self) -> list[Tag]:
        """Returns list of tags based on query."""
        return Tag.parse_tags(self._fetch_tags().text)

    @property
    def query(self):
        """Query getter."""
        return self._query

    def __getitem__(self, index: SupportsIndex | slice):
        """x.__getitem__(y) <==> x[y]"""
        return self._tags.__getitem__(index)

    def index(
        self, value: Tag, start: SupportsIndex = ..., stop: SupportsIndex = ...
    ) -> int:
        """
        Returns first index of value.

        Raises ValueError if the value is not present.
        """
        return self._tags.index(value, start, stop)

    def count(self, value: Tag) -> int:
        """Returns number of occurrences of value."""
        return self._tags.count(value)

    def __contains__(self, value: object) -> bool:
        """Returns key in self."""
        return self._tags.__contains__(value)

    def __iter__(self):
        """Implements iter(self)."""
        return self._tags.__iter__()

    def __reversed__(self):
        """Returns a reverse iterator over the tags."""
        return self._tags.__reversed__()

    def __len__(self) -> int:
        """Returns len(self)."""
        return self._tags.__len__()
