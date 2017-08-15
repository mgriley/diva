.. diva documentation master file, created by
   sphinx-quickstart on Thu Aug 10 16:35:43 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Diva
================================

Diva is a Python library for creating interactive web analytics dashboards. It supports popular analytics libraries like matplotlib, pandas, and bokeh.

The example below will serve a webpage where you can interact with the decorated functions ``foo`` and ``bar``. In this case, the pandas Series objects are converted to HTML tables for browser display. Please see the `demo server <https://fizznow.com>`_ and the User's Guide for more details.

.. literalinclude:: ../examples/minimal_example.py

.. toctree::
    :maxdepth: 2
    :caption: Contents:

    users_guide
    developers_guide

