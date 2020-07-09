
Examples
========

Before we proceed let's setup a `virtualenv`_ environment, activate it and
install::

    $ pip install wheezy.routing


.. _helloworld:

Hello World
-----------

`helloworld.py`_ shows you how to use :ref:`wheezy.routing` in a pretty
simple `WSGI`_ application:

.. literalinclude:: ../demos/hello/helloworld.py
   :lines: 5-

Let's have a look through each line in this application. First of all we
import :py:class:`~wheezy.routing.PathRouter` that is actually just an
exporting name for :py:class:`~wheezy.routing.router.PathRouter`:

.. literalinclude:: ../demos/hello/helloworld.py
   :lines: 7

Next we create a pretty simple WSGI handler to provide a response.

.. literalinclude:: ../demos/hello/helloworld.py
   :lines: 15-19

In addition let's add a handler for the 'not found' response.

.. literalinclude:: ../demos/hello/helloworld.py
   :lines: 22-26

The declaration and mapping of patterns to handlers follows. We create an
instance of ``PathRouter`` class and pass it a mapping, that in this particular case
is a tuple of two values: ``pattern`` and ``handler``.

.. literalinclude:: ../demos/hello/helloworld.py
   :lines: 29-33

The first pattern ``'/'`` will match only the root path of the request (it is
finishing route in the match chain). The second pattern ``'/{any}'`` is a curly
expression, that is translated to regular expression, that ultimately matches
any path and is a finishing route as well.

``main`` function serves as `WSGI`_ application entry point. The only thing
we do here is to get a value of `WSGI`_ environment variable ``PATH_INFO``
(the remainder of the request URL's path) and pass it to the router
:py:meth:`~wheezy.routing.router.PathRouter.match` method. In return we
get ``handler`` and ``kwargs`` (parameters discovered from matching rule,
that we ignore for now).

.. literalinclude:: ../demos/hello/helloworld.py
   :lines: 36-38

The rest in the ``helloworld`` application launches a simple wsgi server.
Try it by running::

    $ python helloworld.py

Visit http://localhost:8080/.

.. _server time:

Server Time
-----------

The server `time`_ application consists of two screens. The first one has a link
to the second that shows the time on the server. The second page will be mapped
as a separate application with its own routing. The design used in this
sample is modular. Let's start with ``config`` module. The only thing we
need here is an instance of ``PathRouter``.

.. literalinclude:: ../demos/time/config.py
   :lines: 4-6

The ``view`` module is pretty straight: a ``welcome`` view with a link to
``server_time`` view. The server time page returns the server time. And finally
a catch all ``not_found`` handler to display http 404 error, page not found.

.. literalinclude:: ../demos/time/views.py
   :lines: 5-

So what is interesting in the ``welcome`` view is a way how we get a url for
``server_time`` view.

.. literalinclude:: ../demos/time/views.py
   :lines: 14-15

The name ``now`` was used during url mapping as you can see below (module
``urls``):

.. literalinclude:: ../demos/time/urls.py
   :lines: 5-

``server_urls`` are then included under the parent path ``server/``, so
anything that starts with the path ``server/`` will be directed to the
``server_urls`` url mapping. Lastly we add a curly expression that maps
any url match to our ``not_found`` handler.

We combine that all together in ``app`` module.


.. literalinclude:: ../demos/time/app.py
   :lines: 5-

Try it by running::

    $ python app.py

Visit http://localhost:8080/.

.. _`virtualenv`: http://pypi.python.org/pypi/virtualenv
.. _`helloworld.py`: https://bitbucket.org/akorn/wheezy.routing/src/tip/demos/hello/helloworld.py
.. _`time`: https://bitbucket.org/akorn/wheezy.routing/src/tip/demos/time
.. _`WSGI`: http://www.python.org/dev/peps/pep-3333
