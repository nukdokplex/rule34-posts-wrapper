import re
from collections.abc import Sequence, MutableSequence

r = re.compile("[, ]")


def validator(cmp, exc):
    def decorator(setter):  # a decorator for the setter
        def wrapper(self, value):  # the wrapper around your setter
            if cmp(value):  # if cmp function returns True, raise the passed exception
                raise exc
            setter(self, value)  # otherwise just call the setter to do its job

        return wrapper

    return decorator


def is_safe_string(s: str) -> bool:
    """Checks if string consist of letters, numbers, underscores, dashes and apostrophes"""
    if not isinstance(s, str):
        return False
    if len(s) == 0:
        return False
    if r.match(s) is None:
        return True
    return False


def is_list_of_safe_strings(s: Sequence[str] | MutableSequence[str]) -> bool:
    """Checks if each element of the string list consists of letters, numbers, underscores, dashes and apostrophes"""
    if not isinstance(s, Sequence) or not isinstance(s, MutableSequence):
        return False
    for string in s:
        if not is_safe_string(string):
            return False
    return True


def check_duplicate_column(s: list[object], attr: str) -> bool:
    """Checks if there are items with matching attributes in the list of objects."""
    # TODO Optimize
    column = []
    for obj in s:
        a = getattr(obj, attr)
        if a in column:
            return False
        column.append(a)
    return True
