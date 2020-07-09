""" ``config`` module.
"""

from wheezy.routing.choice import try_build_choice_route
from wheezy.routing.curly import (
    default_pattern as curly_default_pattern,
    patterns as curly_patterns,
    try_build_curly_route,
)
from wheezy.routing.plain import try_build_plain_route
from wheezy.routing.regex import try_build_regex_route

assert curly_default_pattern
assert curly_patterns

route_builders = [
    try_build_plain_route,
    try_build_choice_route,
    try_build_curly_route,
    try_build_regex_route,
]
