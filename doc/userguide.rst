
User Guide
==========

Path and Handler
----------------

You create a mapping between: a remainder of the request URL (virtual
location or url ``path``) and a ``handler``.::

    urls = [
         ('posts/2003', posts_for_2003),
         ('posts/{year}', posts_by_year),
         ('posts/(?P<year>\d+)/(?P<month>\d+)', posts_by_month)
    ]

It is completely up to you what is ``path`` or ``handler``. If you have
a look at :ref:`helloworld` example you notice the following:

.. literalinclude:: ../demos/hello/helloworld.py
   :lines: 21-23

or more precisely::

    environ['PATH_INFO']

This operation takes WSGI environment varible ``PATH_INFO`` and pass to
router for matching against available mapping. ``handler`` in this case is a
simple callable that represents WSGI call handler.

.. literalinclude:: ../demos/hello/helloworld.py
   :lines: 8-12

Extend Mapping
--------------

Since ``mapping`` is nothing more than python list, you can make any
manipulation you like, e.g. add other mappings, construct them dynamically,
etc. Here is example from :ref:`server time` example:

.. literalinclude:: ../demos/time/urls.py
   :lines: 12-19

``home`` mapping has been extended by simple adding another list.

Mapping Inclusion
-----------------

Your application may be constructed with several modules, each of them
can have own urls mapping. You can easily include them in case a ``handler``
place is used by other mapping. Here is an example from :ref:`server time`:

.. literalinclude:: ../demos/time/urls.py
   :lines: 8-15

``server_urls`` included into ``server/`` subpath. So effective path for
``server_time`` handler is ``server/time``.

Named Groups
------------

Named groups is something that you can get out from url mapping::

    urls = [
        ('posts/{year}', posts_by_year),
        ('posts/(?P<year>\d+)/(?P<month>\d+)', posts_by_month)
    ]

If we get back to :ref:`helloworld` example:

.. literalinclude:: ../demos/hello/helloworld.py
   :lines: 21-23

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

There is :py:func:`wheezy.routing.url` function (that is actually just
an exporting name for :py:func:`~wheezy.routing.router.url`) that let you
make your url mapping more readable::

    from wheezy.routing import url


    urls = [
        url('posts', latest_posts, kwargs={'blog_id': 100})
    ]

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

You have an instance of :py:class:`wheezy.routing.Router`
(:py:class:`~wheezy.routing.router.PathRouter`). Call it method
:py:meth:`~wheezy.routing.router.PathRouter.add_routes` to add any
mapping you have. Here is how we do it in :ref:`helloworld` example:

.. literalinclude:: ../demos/hello/helloworld.py
   :lines: 15-18

... or :ref:`server time`:

.. literalinclude:: ../demos/time/app.py
   :lines: 5-9

Route Builders
--------------

Every path mapping you add to router is translated to appropriate route
match strategy. The avaiable routing match strategies are definded in
:py:mod:`~wheezy.routing.config` module by ``route_builders`` list include:

#. plain
#. regex
#. curly

Plain Route
~~~~~~~~~~~

The plain route is selected in case the path satisfy the following regular
expression (at least one ``word``, ``'/'`` or ``'-'`` character)::

    ^[\w/-]+$

The matching paths include: ``account/login``, ``blog/list``, etc. The
strategy performs exact string marching. In case the matching string ends
with path segment delimiter character ``'/'``, the strategy is changed to
match the beginning of path, thus ``server/`` pattern match any path starting
with ``server/``, e.g. ``server/info``, etc.

Regex Route
~~~~~~~~~~~

Any valid regular expression will match this strategy. However there few
limitation that applies if you would like to build paths by name (reverse
function to path matching). Use regex syntax only inside named groups,
create them as much as necessary. The path build strategy simply replaces
named groups with values supplied.

Curly Route
~~~~~~~~~~~

This is just a simplified version of regex routes. You define a named group
by using curly brakets. The curly expression ``abc/{id}`` is convered into
regex ``abc/(?P<id>[^/]+)``. The form of curly expression (``pattern`` is
optional and corresponds to segment by default)::

    {name[:pattern]}

The name inside curly expression can be
constrained with the following patterns:

- ``i``, ``int``, ``number``, ``digits`` - one or more digits
- ``w``, ``word`` - one or more word characters
- ``s``, ``segment``, ``part`` - everything until ``'/'`` (path segment)
- ``a``, ``any``, ``rest`` - match anything

Here are examples of valid expressions::

    posts/{year:i}/{month:i}
    account/{name:w}

Building Paths
--------------

Once you have defined routes you can build paths from them. See :ref:`named`
how the name of url mapping is cunstructed. Here is a example from
:ref:`server time`:

.. literalinclude:: ../demos/time/views.py
   :lines: 14-15

You can pass optional ``values`` that will be used to replace named groups
of the path matching pattern::

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
