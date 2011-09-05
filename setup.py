#!/usr/bin/env python

try:
    from setuptools import setup
except:
    from distutils.core import setup

def read(fname):
    from os.path import dirname, join
    return open(join(dirname(__file__), fname)).read()

setup(
    name = 'wheezy-routing',
    version = '0.1',
    description = 'A lightweight path routing library',
    long_description = read('README'),
    url = 'https://bitbucket.org/akorn/wheezy-routing',

    author = 'Andriy Kornatskyy',
    author_email = 'andriy.kornatskyy at live.com',

    license = 'MIT',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ],
    packages = ['wheezy', 'wheezy.routing'],
    package_dir = {'': 'src'},

    zip_safe = True,
    install_requires = [
    ],
    extras_require = {
        'dev': [
            'wsgiref',
            'coverage',
            'nose',
            'mocker',
            'pytest',
            'pytest-pep8',
            'pytest-cov'
        ]
    },

    platforms = 'any'
)
