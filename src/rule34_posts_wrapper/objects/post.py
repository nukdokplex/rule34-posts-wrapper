from typing import List
from urllib3.util import Url

from ..utils import validator, is_list_of_safe_strings


class Post:
    """A Rule 34 post container."""

    def __init__(
        self,
        identifier: int,
        tags: List,
        link: Url,
        thumbnail: Url,
        file: Url,
        query: list,
    ):
        """Initializes rule34 post."""
        self.identifier = identifier
        self.tags = tags
        self.link = link
        self.thumbnail = thumbnail
        self.file = file
        self.query = query

    @property
    def identifier(self):
        """Identifier getter."""
        return self._identifier

    @identifier.setter
    def identifier(self, value):
        """Identifier setter."""
        self._identifier = value

    @property
    def tags(self):
        """Tags getter."""
        return self._tags

    @tags.setter
    @validator(
        lambda tags: not is_list_of_safe_strings(tags),
        ValueError(
            "Tags must be a list of strings consist of letters, numbers, dashes, underscores and "
            "apostrophes"
        ),
    )
    def tags(self, value):
        """Tags setter."""
        self._tags = value

    @property
    def link(self):
        """Link getter."""
        return self._link

    @link.setter
    def link(self, value):
        """Link setter."""
        self._link = value

    @property
    def thumbnail(self):
        """Thumbnail getter."""
        return self._thumbnail

    @thumbnail.setter
    def thumbnail(self, value):
        """Thumbnail setter."""
        self._thumbnail = value

    @property
    def file(self):
        """File getter."""
        return self._file

    @file.setter
    def file(self, value):
        """File setter."""
        self._file = value

    @property
    def query(self):
        """Query getter."""
        return self._query

    @query.setter
    @validator(
        lambda query: not is_list_of_safe_strings(query),
        ValueError(
            "Search must be a list of strings consist of letters, numbers, dashes, underscores and "
            "apostrophes"
        ),
    )
    def query(self, value):
        """Query setter."""
        self._query = value

    def __str__(self):
        """Returns str(self)."""
        return str(
            {
                "identifier": self._identifier,
                "tags": self._tags,
                "link": str(self._link),
                "thumbnail": str(self._thumbnail),
                "file": str(self._file),
                "query": self._query,
            }
        )
