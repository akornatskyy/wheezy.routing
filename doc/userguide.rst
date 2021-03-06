
User Guide
==========

Pattern and Handler
-------------------

You create a mapping between: ``pattern`` (a remainder of the request URL,
script name, http schema, host name or whatever else) and ``handler``
(callable, string, etc.)::

    urls = [
         ('posts/2003', posts_for_2003),
         ('posts/{year}', posts_by_year),
         ('posts/(?P<year>\d+)/(?P<month>\d+)', posts_by_month)
    ]

It is completely up to you how to interpret ``pattern`` (you can add own
patterns interpretation) and/or ``handler``. If you have a look at
:ref:`helloworld` example you notice the following:

.. literalinclude:: ../demos/hello/helloworld.py
   :lines: 36-38

or more specifically::

    environ['PATH_INFO']

This operation takes the WSGI environment variable ``PATH_INFO`` and passes it to
router for matching against available mappings. ``handler`` in this case is a
simple callable that represents WSGI call handler.

.. literalinclude:: ../demos/hello/helloworld.py
   :lines: 15-19

Extend Mapping
--------------

Since ``mapping`` is nothing more than python list, you can make any
manipulation you like, e.g. add other mappings, construct them dynamically,
etc. Here is snippet from :ref:`server time` example:

.. literalinclude:: ../demos/time/urls.py
   :lines: 10-

``home`` mapping has been extended by simple adding another list.

Mapping Inclusion
-----------------

Your application may be constructed with several modules, each of them
can have own url mapping. You can easily include them as a ``handler`` (the
system checks if the handler is another mapping it creates nested
``PathRouter``). Here is an example from :ref:`server time`:

.. literalinclude:: ../demos/time/urls.py
   :lines: 8-

``server_urls`` included into ``server/`` subpath. So effective path for
``server_time`` handler is ``server/time``.

Note that the route selected for ``'server/'`` pattern is *intermediate* (it is not
*finishing* since there is another pattern included after it). The ``'time'`` pattern is
*finishing* since it is the last in the match chain.

Named Groups
------------

Named groups are something that you can retrieve from the url mapping::

    urls = [
        ('posts/{year}', posts_by_year),
        ('posts/(?P<year>\d+)/(?P<month>\d+)', posts_by_month)
    ]

``kwargs`` is assigned a ``dict`` that represends key-value pairs
from the match::

   >>> handler, kwargs = r.match('posts/2011/09')
   >>> kwargs
   {'month': '09', 'year': '2011'}

Extra Parameters
----------------

While ``named groups`` get some information from the matched ``path``, you
can also merge these with some extra values during initialization of the mapping
(this is third parameter in tuple)::

    urls = [
        ('posts', latest_posts, {'blog_id': 100})
    ]

Note, that any values from the path match override extra parameters passed
during initialization.

``url`` helper
--------------

There is :py:func:`wheezy.routing.router.url` function that let you
make your url mappings more readable::

    from wheezy.routing import url


    urls = [
        url('posts', latest_posts, kwargs={'blog_id': 100})
    ]

All it does just convers arguments to a tuple of four.

.. _named:

Named Mapping
-------------

Each path mapping you create is automatically named after the handler name.
The convention as to the name is: translate handler name from camel case
to underscore name and remove any ending like 'handler', 'controller', etc.
So ``LatestPostsHandler`` is named as ``latest_posts``.

You can also specify an explicit name during mapping, it is convenient to use
:py:func:`~wheezy.routing.router.url`) function for this::

    urls = [
        url('posts', latest_posts, name='posts')
    ]

When you know the name for a url mapping, you can reconstruct its path.

Adding Routes
-------------

You have an instance of :py:class:`~wheezy.routing.router.PathRouter`.
Call its method :py:meth:`~wheezy.routing.router.PathRouter.add_routes`
to add any pattern mapping you have. Here is how we do it in
the :ref:`helloworld` example:

.. literalinclude:: ../demos/hello/helloworld.py
   :lines: 30-33

... or :ref:`server time`:

.. literalinclude:: ../demos/time/app.py
   :lines: 5-9

Route Builders
--------------

Every pattern mapping you add to router is translated to an appropriate route
match strategy. The available routing match strategies are definded in
:py:mod:`~wheezy.routing.config` module by ``route_builders`` list and
include:

#. plain
#. regex
#. curly

You can easily extend this list with your own route strategies.

Plain Route
~~~~~~~~~~~

The plain route is selected in case the path satisfy the following regular
expression (at least one ``word``, ``'/'`` or ``'-'`` character):

.. literalinclude:: ../src/wheezy/routing/plain.py
   :lines: 8-8

The matching paths include: ``account/login``, ``blog/list``, etc. The
strategy performs string matching.

Finishing routes are matched by exact string ``equals`` operation, intermediate
routes are matched with ``startswith`` string operation.

Regex Route
~~~~~~~~~~~

Any valid regular expression will match this strategy. However there are a few
limitations that apply if you would like to build paths by name (reverse
function to path matching). Use regex syntax only inside named groups,
create as many as necessary. The path build strategy simply replaces
named groups with values supplied. Optional named groups are supported.

Curly Route
~~~~~~~~~~~

This is just a simplified version of regex routes. Curly route is something
that matches the following regular expression:

.. literalinclude:: ../src/wheezy/routing/curly.py
   :lines: 11-11

You define a named group by using curly brakets. The form of
curly expression (``pattern`` is optional and corresponds to segment by
default)::

    {name[:pattern]}

The curly expression ``abc/{id}`` is converted into regex ``abc/(?P<id>[^/]+)``.

The name inside the curly expression can be constrained with the following
patterns:

- ``i``, ``int``, ``number``, ``digits`` - one or more digits
- ``w``, ``word`` - one or more word characters
- ``s``, ``segment``, ``part`` - everything until ``'/'`` (path segment)
- ``*``, ``a``, ``any``, ``rest`` - match anything

Note that if the pattern constraint doesn't correspond to anything mentioned
above, then it will be interpreted as a regular expression::

    locale:(en|ru)}/home => (?P<locale>(en|ru))/home

Curly routes also support optional values (these should be taken into
square brackets)::

    [{locale:(en|ru)}/]home => ((?P<locale>(en|ru))/)?home

Here are examples of valid expressions::

    posts/{year:i}/{month:i}
    account/{name:w}

You can extend the recognized curly patterns::

    from wheezy.routing.curly import patterns

    patterns['w'] = r'\w+'

This way you can add your custom patterns.

Building Paths
--------------

Once you have defined routes you can build paths from them. See :ref:`named`
how the name of url mapping is constructed. Here is a example from
:ref:`server time`:

.. literalinclude:: ../demos/time/views.py
   :lines: 14-15

You can pass optional values (``kwargs`` argument) that will be used
to replace named groups of the path matching pattern::

    >>> r = RegexRoute(
    ...     r'abc/(?P<month>\d+)/(?P<day>\d+)',
    ...     kwargs=dict(month=1, day=1)
    ... )
    >>> r.path_for(dict(month=6, day=9))
    'abc/6/9'
    >>> r.path_for(dict(month=6))
    'abc/6/1'
    >>> r.path_for()
    'abc/1/1'

Values passed to the :py:meth:`~wheezy.routing.router.PathRouter.path_for`
method override any values used during initialization of url mapping.

:py:class:`KeyError` is raised in case you try to build a path
that doesn't exist or provide insufficient arguments for building a path.
