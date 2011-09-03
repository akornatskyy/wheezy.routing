"""
Wheezy Routing
--------------

Lightweight path routing.
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
    author_email = 'andriy.kornatskyy at live.com',

    description = 'Lightweight path routing',
    long_description = __doc__,
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
