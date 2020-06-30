#!/usr/bin/env python

import os
import re

from setuptools import setup

extra = {}
try:
    from Cython.Build import cythonize
    p = os.path.join('src', 'wheezy', 'routing')
    extra['ext_modules'] = cythonize(
        [os.path.join(p, '*.py')],
        exclude=os.path.join(p, '__init__.py'),
        nthreads=2, quiet=True)
except ImportError:
    pass

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
VERSION = (
    re.search(
        r'__version__ = "(.+)"',
        open("src/wheezy/routing/__init__.py").read(),
    )
    .group(1)
    .strip()
)

setup(
    name='wheezy.routing',
    version=VERSION,
    description='A lightweight path routing library',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://bitbucket.org/akorn/wheezy.routing',
    author='Andriy Kornatskyy',
    author_email='andriy.kornatskyy@live.com',
    license='MIT',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords='routing path url patterns match web mapping',
    packages=['wheezy', 'wheezy.routing'],
    package_dir={'': 'src'},
    namespace_packages=['wheezy'],
    zip_safe=False,
    platforms='any',
    **extra
)
