User's Guide
*************

Setup
============

This library requires Python 3. Assuming you already have Python 3 and pip installed, you can setup your project like this::

    $ mkdir myproj
    $ cd myproj
    $ python3 -m venv myvenv
    $ source myvenv/bin/activate
    $ pip install diva

The command ``python3 -m venv myvenv`` creates a directory called ``myvenv`` to handle your project's virtual environment. A virtual environment is a mechanism that gives the illusion (hence "virtual") that your project's version of the Python interpreter and any required libraries are installed locally. This isolates your project from other projects that may use different versions of Python (and thus different library versions). Virtual environments prevent conflicts of the form: Project A uses Python 2 and Project B uses Python3, and both depend on ``somelibrary``, which is installed globally. Project A is broken because it thinks it should use the latest installed version of ``somelibrary``, which only works for Python 3.

When you start working on your project, you must activate the environment with ``$ source myenv/bin/activate`` (which should prepend the environment name to your prompt like ``(myvenv) ... $``), and you should deactivate it when you're done using ``$ deactivate``.

Introduction
=============

Let's start with an example:

.. literalinclude:: ../examples/minimal_example.py

You can run the example like:

.. image:: images/example_console.png

Going to the given address in your browser should display:

.. image:: images/example_screenshot_a.png

You should be able to change the report, and play with the widget values.

.. image:: images/example_screenshot_b.png

First, we create a ``Diva`` object. Next, we use python's `decorator syntax <https://realpython.com/blog/python/primer-on-python-decorators/>`_ to register our analytics functions ``foo`` and ``bar`` with our ``Diva`` object. The ``view`` decorator *does not modify the underlying function* (``view`` just stores a reference to it in the ``Diva`` object). You can call ``foo`` or ``bar`` elsewhere in your code as if you weren't using diva at all. Finally, we call ``app.run()``, which serves the website linked above. The site contains a report for every function we register with our ``Diva`` object.

You can pass a list of widgets to ``view``. The ``bar`` function takes an integer and a float, so we pass the ``Int`` and ``Float`` objects to ``view``. As you can see, the webserver generates appropriate HTML widgets. When we reload the ``bar`` report, the values of these widgets are sent to the server, passed to ``bar``, and the result of ``bar`` is sent back to the browser (converted to HTML).

API
====

.. function:: Diva()
    
    This internally creates ``self.server``, a Flask object, which is is started by ``run``. More complex uses of Diva may require directly modifying this Flask object.

.. function:: Diva.view(name, widgets=[])
    
    ``name`` is what the view will be called in the web interface. ``widgets`` is an optionally empty list of ``diva.widgets.Widget`` objects. Please see the Widgets section for a list of available widgets and what values they pass to the underlying function. Intuitively, the widget values are passed to the function in the order that the widgets appear in the list.

    Consider:

    .. literalinclude:: ../examples/minimal_example.py
        :pyobject: bar

    Suppose you choose values of 2 and 3.5 for the widgets then reload the report. Internally, ``bar`` will be called like ``bar(a=2, b=3.5)``. To keep things simple, just make the number of widgets the same as the number of function arguments. If your function takes ``*args``, ``**kwargs``, specifies defaults, or is otherwise complex, you must suffer this mild inconvenience:

    .. literalinclude:: ../examples/other_examples.py
        :pyobject: baz

    .. literalinclude:: ../examples/other_examples.py
        :pyobject: baz_shim
            
.. function:: Diva.run(host=None, port=None, debug=None, **options)

    ``run`` internally looks like this::
        
        # self.server is a Flask object
        self.server.run(host, port, debug, **options)

    Please see the `Flask documentation <http://flask.pocoo.org/docs/0.12/api/>`_ for an explanation of ``run``'s arguments. Briefly, setting ``debug=True`` will open an interactive debugger when an exception occurs, and also attempt to reload the server when the code changes.

    .. warning::
        
        The interactive debugger allows one to run arbitrary Python code on your server, so don't use ``debug=True`` on a publically accessable site.

    .. warning::

        If you want to make your diva app production ready, follow `these steps <http://flask.pocoo.org/docs/0.12/deploying/#deployment>`_ to make the underlying Flask server production ready. Also see the Security section below.

.. function:: Diva.__call__(environ, start_response)

    This is likely only relevant to you if you'd like to deploy the server, in which case you should first read an article on WSGI servers and also refer to `Flask's documentation <http://flask.pocoo.org/docs/0.12/deploying/#deployment>`_. The ``Diva`` object is callable as a WSGI entry point. It simply passes the args to the Flask server's (``self.server``) WSGI entry point and returns the result. Please see the source directory ``diva/examples/demo_server`` for an example.

Widgets
========

The built-in widgets (available via ``from diva.widgets import *``) are:

* String
* Float
* Int
* Bool
* SelectOne
* SelectSubset
* Color
* Slider
* Date
* DateRange
* Time

You can see each widget in action on the `demo server <https://fizznow.com>`_. The first argument passed to every widget constructor is the description of the widget in the web interface (such as, "choose a scale"). 

.. automodule:: diva.widgets
    :members:

Converters
===========

Diva attempts to convert the return value of your functions to HTML. The following conversions are supported:

* string: the string is assumed to be HTML.
* matplotlib.figure.Figure (using the mpld3 library)
* pandas.DataFrame & pandas.Series
* bokeh.plotting.figure.Figure
* *other*: the value is converted to a string and wrapped in HTML

You can see an example of each conversion on the `demo server <https://fizznow.com>`_. Conversion internally uses the `single dispatch decorator from functools <https://docs.python.org/3/library/functools.html>`_, so you can add your own converter like this:

.. literalinclude:: ../examples/custom_converter.py

Security
=========

**Input Sanitation**

If you are allowing public access to your site, you are responsible for sanitizing user input. Diva performs some trivial sanitation, like ensuring the value of a string widget is actually passed to your function as a string and not an int. However, if your underlying functions are accessing sensitive information, be careful.

**Password Protection**

diva currently doesn't support password management. It may support simple password protection in the future, but likely not a full user access system. 

However, you can modify the underlying Flask object to add your authentication code like this::

    app = Diva()

    # decorate some functions, like normal

    flask_server = app.server

    # Modify flask_server to add your auth code

    # this is the same as flask_server.run()
    app.run()

You can modify the Flask object's view functions (`docs here <http://flask.pocoo.org/docs/0.12/api/>`_) to add your auth code. See the functin ``setup_server`` from the diva source file ``diva/diva/reporter.py`` to see what endpoints diva uses.

If that doesn't work, things get more complex. Suppose you already have a publically accessible server with a user management system. Perhaps it isn't written in python. You could run diva as a local server (not publically exposed, that is), and setup a password-protected endpoint in your public server that acts as a reverse proxy between your public server and the diva server.

Alternatives
=============

Jupyter has its own widget library, and `you can interact with functions like this <http://ipywidgets.readthedocs.io/en/latest/examples/Using%20Interact.html>`_. To share a Jupyter notebook, you can archive the .ipynb file in your GitHub, then use the tools nbviewer or mybinder to give others access to your notebook. You can also take a look at `IPython Dashboards <https://github.com/litaotao/IPython-Dashboard>`_. 
