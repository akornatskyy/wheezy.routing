
""" ``config`` module.
"""

from builders import try_build_plain_route
from builders import try_build_regex_route

route_builders = [
    try_build_plain_route,
    try_build_regex_route
]
