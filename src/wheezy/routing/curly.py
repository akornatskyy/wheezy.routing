""" ``curly`` module.
"""

import re

from wheezy.routing.regex import RegexRoute
from wheezy.routing.utils import outer_split

RE_SPLIT = re.compile(r"(?P<n>{[\w:]+.*?})")


def try_build_curly_route(pattern, finishing=True, kwargs=None, name=None):
    """Convert pattern expression into regex with
    named groups and create regex route.
    """
    if isinstance(pattern, RegexRoute):
        return pattern
    if RE_SPLIT.search(pattern):
        return RegexRoute(convert(pattern), finishing, kwargs, name)
    return None


patterns = {
    # one or more digits
    "i": r"\d+",
    "int": r"\d+",
    "number": r"\d+",
    "digits": r"\d+",
    # one or more word characters
    "w": r"\w+",
    "word": r"\w+",
    # everything until ``/``
    "s": r"[^/]+",
    "segment": r"[^/]+",
    "part": r"[^/]+",
    # any
    "*": r".+",
    "a": r".+",
    "any": r".+",
    "rest": r".+",
}

default_pattern = "s"


def convert(s):
    """Convert curly expression into regex with
    named groups.
    """
    parts = outer_split(s, sep="[]")
    parts[1::2] = ["(%s)?" % p for p in map(convert, parts[1::2])]
    parts[::2] = map(convert_single, parts[::2])
    return "".join(parts)


def convert_single(s):
    """Convert curly expression into regex with
    named groups.
    """
    parts = RE_SPLIT.split(s)
    return "".join(map(replace, parts))


def replace(val):
    """Replace ``{group_name:pattern_name}`` by regex with
    named groups.
    """
    if val.startswith("{") and val.endswith("}"):
        group_name, pattern_name = parse(val[1:-1])
        pattern = patterns.get(pattern_name, pattern_name)
        return "(?P<%s>%s)" % (group_name, pattern)
    return val


def parse(s):
    """Parse ``s`` according to ``group_name:pattern_name``.

    There is just ``group_name``, return default
    ``pattern_name``.
    """
    if ":" in s:
        return tuple(s.split(":", 1))
    return s, default_pattern
