from __future__ import annotations

import json

from rule34_posts_wrapper.utils import validator, is_safe_string


class Tag:
    """A container for tag."""

    def __init__(self, name: str, count: int):
        """Initializes tag."""
        self.name = name
        self.count = count

    @property
    def name(self):
        """Name getter."""
        return self._name

    @name.setter
    @validator(
        lambda name: not is_safe_string(name),
        ValueError(
            "Name must consist of letters, numbers, dashes, underscores and apostrophes"
        ),
    )
    def name(self, value):
        """Name setter."""
        self._name = value

    @property
    def count(self):
        """Count getter."""
        return self._count

    @count.setter
    @validator(
        lambda count: count is not int or count < 0,
        ValueError("Count must be a positive integer"),
    )
    def count(self, value):
        """Count setter."""
        self._count = value

    @staticmethod
    def parse_tags(json_str: str) -> list[Tag]:
        """Parses JSON and returns tags."""
        tags = list[Tag]()
        t = json.loads(json_str)
        if len(t) == 0:
            return tags
        [tags.append(tag) for tag in t]
        return tags
