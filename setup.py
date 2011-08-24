"""
Wheezy Routing
--------------

Design URLs however you want, with no limitations.
"""

try:
    from setuptools import setup
except:
    from distutils.core import setup

setup(
    name = 'wheezy-routing',
    version = '0.1',
    url = 'https://bitbucket.org/akorn/wheezy-routing',

    author = 'Andriy Kornatskyy',
    author_email = 'andriy.kornatskyy@live.com',

    description = 'Design URLs however you want',
    long_description = __doc__,

    packages = [ 'wheezy', 'wheezy.routing' ],
    package_dir = { '': 'src' },

    zip_safe = True,

    platforms = 'any'
)
