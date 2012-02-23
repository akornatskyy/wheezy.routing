
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
   :lines: 29-31

or more precisely::

    environ['PATH_INFO']

This operation takes WSGI environment varible ``PATH_INFO`` and pass to
router for matching against available mapping. ``handler`` in this case is a
simple callable that represents WSGI call handler.

.. literalinclude:: ../demos/hello/helloworld.py
   :lines: 9-13

Extend Mapping
--------------

Since ``mapping`` is nothing more than python list, you can make any
manipulation you like, e.g. add other mappings, construct them dynamically,
etc. Here is snippet from :ref:`server time` example:

.. literalinclude:: ../demos/time/urls.py
   :lines: 12-19

``home`` mapping has been extended by simple adding another list.

Mapping Inclusion
-----------------

Your application may be constructed with several modules, each of them
can have own url mapping. You can easily include them as a ``handler`` (the
system checks if the handler is another mapping it creates nested
``PathRouter``). Here is an example from :ref:`server time`:

.. literalinclude:: ../demos/time/urls.py
   :lines: 8-15

``server_urls`` included into ``server/`` subpath. So effective path for
``server_time`` handler is ``server/time``.

Note that route selected for ``'server/'`` pattern is intermediate (it is not
finishing since there is included another after it). ``'time'`` pattern is
finishing since it is the last in the match chain.

Named Groups
------------

Named groups is something that you can get out from url mapping::

    urls = [
        ('posts/{year}', posts_by_year),
        ('posts/(?P<year>\d+)/(?P<month>\d+)', posts_by_month)
    ]

If we get back to :ref:`helloworld` example:

.. literalinclude:: ../demos/hello/helloworld.py
   :lines: 22-24

``kwargs`` is assigned with ``dict`` that represends a key-value pair
from match::

   >>> handler, kwargs = r.match('posts/2011/09')
   >>> kwargs
   {'month': '09', 'year': '2011'}

Extra Parameters
----------------

While ``named groups`` get some information from matched ``path``, you
can also merge with some extra values during initialization of mapping
(this is third parameter in tupple)::

    urls = [
        ('posts', latest_posts, {'blog_id': 100})
    ]

Note, that any non-empty values from path match override extra parameters
passed during initialization.

``url`` helper
--------------

There is :py:func:`wheezy.routing.router.url` function that let you
make your url mapping more readable::

    from wheezy.routing import url


    urls = [
        url('posts', latest_posts, kwargs={'blog_id': 100})
    ]

All it does just convers arguments to a tupple of four.

.. _named:

Named Mapping
-------------

Each path mapping you create is automatically named after the handler name.
The convention as to the name is: translate handler name from camel case
to underscope name and remove anything ended by handler, controller, etc.
So ``LatestPostsHandler`` is named as ``latest_posts``.

You can specify other name during mapping, it is convenient to use
:py:func:`~wheezy.routing.router.url`) function for this::

    urls = [
        url('posts', latest_posts, name='posts')
    ]

When you know name for url mapping you can reconstruct it path.

Adding Routes
-------------

You have an instance of :py:class:`~wheezy.routing.router.PathRouter`.
Call it method :py:meth:`~wheezy.routing.router.PathRouter.add_routes`
to add any pattern mapping you have. Here is how we do it in
:ref:`helloworld` example:

.. literalinclude:: ../demos/hello/helloworld.py
   :lines: 24-27

... or :ref:`server time`:

.. literalinclude:: ../demos/time/app.py
   :lines: 5-9

Route Builders
--------------

Every pattern mapping you add to router is translated to appropriate route
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

.. literalinclude:: ../src/wheezy/routing/builders.py
   :lines: 14-14

The matching paths include: ``account/login``, ``blog/list``, etc. The
strategy performs string marching.

Finishing routes are matched by exact string ``equals`` operation, intermediate
routes are matched with ``startswith`` string operation.

Regex Route
~~~~~~~~~~~

Any valid regular expression will match this strategy. However there few
limitation that applies if you would like to build paths by name (reverse
function to path matching). Use regex syntax only inside named groups,
create them as much as necessary. The path build strategy simply replaces
named groups with values supplied. Optional named groups are supported.

Curly Route
~~~~~~~~~~~

This is just a simplified version of regex routes. Curly route is something
that match the following regular expression:

.. literalinclude:: ../src/wheezy/routing/curly.py
   :lines: 9-9

You define a named group by using curly brakets. The form of
curly expression (``pattern`` is optional and corresponds to segment by
default)::

    {name[:pattern]}

The curly expression ``abc/{id}`` is convered into regex ``abc/(?P<id>[^/]+)``.

The name inside curly expression can be constrained with the following
patterns:

- ``i``, ``int``, ``number``, ``digits`` - one or more digits
- ``w``, ``word`` - one or more word characters
- ``s``, ``segment``, ``part`` - everything until ``'/'`` (path segment)
- ``*``, ``a``, ``any``, ``rest`` - match anything

Note that if pattern constraint doesn't corresponds to anything mentioned
above than it is interpreted as a regular expression::

    locale:(en|ru)}/home => (?P<locale>(en|ru))/home

Curly route also supports optional values (these should be taken into
square brackets)::

    [{locale:(en|ru)}/]home => ((?P<locale>(en|ru))/)?home

Here are examples of valid expressions::

    posts/{year:i}/{month:i}
    account/{name:w}

You can extend recognized curly patterns::

    from wheezy.routing.curly import patterns

    patterns['w'] = r'\w+'

This way you can add your custom patterns.

Building Paths
--------------

Once you have defined routes you can build paths from them. See :ref:`named`
how the name of url mapping is cunstructed. Here is a example from
:ref:`server time`:

.. literalinclude:: ../demos/time/views.py
   :lines: 14-15

You can pass optional values (``kwargs`` argument) that will be used
to replace named groups of the path matching pattern::

    >>> r = RegexRoute(
    ...     r'abc/(?P<month>\d+)/(?P<day>\d+)'
    ... )
    >>> r.path_for(dict(month=6, day=9))
    'abc/6/9'
    >>> r.path_for(dict(month=6))
    'abc/6'
    >>> r.path_for()
    'abc'

Values passed to :py:meth:`~wheezy.routing.router.PathRouter.path_for`
method override any values used during initialization of url mapping.
