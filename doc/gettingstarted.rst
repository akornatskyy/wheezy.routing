
Getting Started
===============

Install
-------

:ref:`wheezy.routing` requires `python`_ version 2.4 to 2.7 or 3.2+.
It is independent of operating system. You can install it from `pypi`_
site using `setuptools`_::

    $ easy_install wheezy.routing

If you are using `virtualenv`_::

    $ virtualenv env
    $ env/bin/easy_install wheezy.routing

Develop
-------

You can get the `source code`_ using `mercurial`_::

    $ hg clone https://bitbucket.org/akorn/wheezy.routing
    $ cd wheezy.routing

Prepare `virtualenv`_ environment in *env* directory ::

    $ make env

... and run all tests::

    $ make test

You can read how to compile from source code different versions of
`python`_ in the `article`_ published on `mind reference`_ blog.

You can run certain make targets with specific python version. Here
we are going to run `doctest`_ with python3.2::

    $ make env doctest-cover VERSION=3.2

Generate documentation with `sphinx`_::

	$ make doc

If you run into any issue or have comments, go ahead and add on
`bitbucket`_.

.. _`pypi`: http://pypi.python.org/pypi/wheezy.routing
.. _`python`: http://www.python.org
.. _`setuptools`: http://pypi.python.org/pypi/setuptools
.. _`bitbucket`: https://bitbucket.org/akorn/wheezy.routing/issues
.. _`source code`: https://bitbucket.org/akorn/wheezy.routing/src
.. _`mercurial`: http://mercurial.selenic.com/
.. _`virtualenv`: http://pypi.python.org/pypi/virtualenv
.. _`article`: http://mindref.blogspot.com/2011/09/compile-python-from-source.html
.. _`mind reference`: http://mindref.blogspot.com/
.. _`doctest`: http://docs.python.org/library/doctest.html
.. _`sphinx`: http://sphinx.pocoo.org/
