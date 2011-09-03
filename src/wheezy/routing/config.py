
""" ``config`` module.
"""

from builders import try_build_plain_route
from builders import try_build_curly_route
from builders import try_build_regex_route

from curly import patterns as curly_patterns
from curly import default_pattern as curly_default_pattern

route_builders = [
    try_build_plain_route,
    try_build_curly_route,
    try_build_regex_route
]
