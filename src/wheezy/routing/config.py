
""" ``config`` module.
"""

from wheezy.routing.builders import try_build_plain_route
from wheezy.routing.builders import try_build_curly_route
from wheezy.routing.builders import try_build_regex_route

from wheezy.routing.curly import patterns as curly_patterns
from wheezy.routing.curly import default_pattern as curly_default_pattern

route_builders = [
    try_build_plain_route,
    try_build_curly_route,
    try_build_regex_route
]
