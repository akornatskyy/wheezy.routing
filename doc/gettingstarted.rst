
Getting Started
===============

Install
-------

`wheezy-routing`_ requires `python`_ version 2.4 to 2.7 or 3.2.
It is independent of operating system. You can install it using
`setuptools`_::

    easy_install wheezy-routing


Develop
-------

Get the `source code`_ using `mercurial`_::

    hg clone https://bitbucket.org/akorn/wheezy-routing
    cd wheezy-routing

Prepare virtualenv environment in *env* directory and run
all tests for python2.6 (default)::

    make env test VERSION=2.6

doctests can be run with python3.2::

    make env doctest-cover VERSION=3.2
    
Generate documentation::

	make doc

If you run into any issue or have comments, go ahead and add on
`bitbucket`_.

.. _`wheezy-routing`: http://pypi.python.org/pypi/wheezy-routing
.. _`python`: http://www.python.org
.. _`setuptools`: http://pypi.python.org/pypi/setuptools
.. _`bitbucket`: https://bitbucket.org/akorn/wheezy-routing
.. _`source code`: https://bitbucket.org/akorn/wheezy-routing/src
.. _`mercurial`: http://mercurial.selenic.com/

