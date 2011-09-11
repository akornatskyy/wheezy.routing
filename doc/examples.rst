
Examples
========

We start with a simple `helloworld`_ example, than add a bit more
modularity in `server time`_.

.. _helloworld:

Hello World
-----------

`helloworld.py`_ shows you how to use :ref:`wheezy-routing` in pretty
simple `WSGI`_ application:

.. literalinclude:: ../demos/hello/helloworld.py
   :lines: 5-

Let have a look through each line in this application. First of all we
import :py:class:`~wheezy.routing.Router` that is actually just an
exporting name for :py:class:`~wheezy.routing.router.PathRouter`:

.. literalinclude:: ../demos/hello/helloworld.py
   :lines: 5

Next we create a pretty simple WSGI handler to provide a response.

.. literalinclude:: ../demos/hello/helloworld.py
   :lines: 8-12

The declaration and mapping of path to handler following. We create an
instance of ``Router`` class and pass mapping that in this partucular case
is a tuple of two values: ``path`` and ``handler``.

.. literalinclude:: ../demos/hello/helloworld.py
   :lines: 15-18

``main`` function serves as `WSGI`_ application entry point. The only thing
we do here is to get a value of `WSGI`_ environment variable ``PATH_INFO``
(the remainder of the request URL's path) and pass to router
:py:meth:`~wheezy.routing.router.PathRouter.match` method, in return we
get ``handler`` and ``kwargs`` (parameters discovered from matching rule,
that we ignore for now). Due to specific of the route that ends with ``/``
our handler will match any incomming request.

.. literalinclude:: ../demos/hello/helloworld.py
   :lines: 21-23

The rest in the ``helloworld`` application launch a simple wsgi server.
Try it by running::

    make run-hello

Visit http://localhost:8080/.

.. _server time:

Server Time
-----------

Server `time`_ application consists of two screens. The first one has a link
to the second that shows the time on server. The second page will be mapped
as a separate application with its own routing. The disign used in this
sample is moular. Let's start with ``config`` module. The only thing we
need here is an instance of ``Route``.

.. literalinclude:: ../demos/time/config.py
   :lines: 5-8

``view`` module is pretty straight: a ``welcome`` view with a link to
``server_time`` view. The time page returns the server time. And finally
catch all ``not_found`` handler to display http 404 error, page not found.

.. literalinclude:: ../demos/time/views.py
   :lines: 5-

So what is interesting in ``welcome`` view is a way how we get an url for
``server_time`` view.

.. literalinclude:: ../demos/time/views.py
   :lines: 14-15

The name ``now`` was used during url mapping that you can see below (module
``urls``):

.. literalinclude:: ../demos/time/urls.py
   :lines: 5-

``server_urls`` than included under the parent path ``server/``, so
anything tha starts from ``server/`` path will be directed to
``server_urls`` url mapping. Lastly we add a curly expression that maps
any url to our ``not_found`` handler.

We combine that all together in ``app`` module.


.. literalinclude:: ../demos/time/app.py
   :lines: 5-

Try it by running::

    make run-time

Visit http://localhost:8080/.

.. _`helloworld.py`: https://bitbucket.org/akorn/wheezy-routing/src/tip/demos/hello/helloworld.py
.. _`time`: https://bitbucket.org/akorn/wheezy-routing/src/tip/demos/time
.. _`WSGI`: http://www.python.org/dev/peps/pep-3333/
