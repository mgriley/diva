Developer's Guide
******************

In case you'd like to contribute, here is an explanation of how the parts fit together.

First, see the file diva/diva/reporter.py. Notice the constructor creates a Flask object ``self.server``, and an array to store the user's decorated functions. Calling the ``view`` decorator stores a reference to the user's function in a map, along with the widget values. Next, see ``run``, which is simply delegated to the underlying Flask object. 

The index endpoint (/) is the HTML that is returned when you go the root of the site. This produces the menu of reports, widgets for each report, and all other HTML. The index.html template refers to diva/diva/templates/index.html. Next, there is the update endpoint. Whenever the user reloads a report, the widgets values are gathered into a JSON object and sent to this endpoint. This function calls ``generate_figure_html``, which converts the JSON to the relevant Python datatypes, calls your function (remember that ``view`` stores a reference to it), and converts its result to HTML using ``convert_to_html``. ``convert_to_html`` is defined in diva/diva/converters.py file, alongside all of the supported types that can be converted.

Before we get to the Javascript, let's look at the widgets. A widget must be able to: 

#. generate HTML allowing the user to select its value
#. retrieve the current value of the widget from the HTML DOM
#. convert this retrieved value into the python object that the user expects
#. for convenience, provide a default value. The user can restore a report to its default values.

Parts 1, 3, and 4 are done in diva/diva/widgets.py. You will see that parts 3 and 4 are straightforward. The ``generateHTML`` functions render templates in the diva/diva/templates folder. Many of the widgets are thin wrappers around HTML input tags, so these widgets extend the ``InputTagWidget`` class. Part 2 ventures into Javascript: through diva/static/reports.js and diva/static/widgets.js.

Let's look at diva/diva/templates/index.html. The <head> contains a bunch of Bootstrap components, which are used for layout and to replace unsupported input tags (like type date and time). Some parts of the <body> may seem strange, like the fact that the links in the dropdown menu don't link anywhere. This is because the webpage is tabbed. When you change the report, the current report is just hidden in case you want to see it again later. In some cases the loop index of a templating loop is used as an id. This is used to refer to specific reports later. Note that the ``{{ widget.html | safe }}`` statement is where the HTML from ``generateHTML`` is transplanted into the page.

The Javascript files are found in diva/diva/static. JQuery is heavily used. The file report.js creates a global Reports object. It has a list of Report objects (created by the newReport function), a property Widgets that contains ``setupMap``, and functions for adding new report objects to the global state. Each report maintains a list of its widgets. The most important function for a report is ``object.update``, given in the ``newReport`` function. ``update`` is where the Flask server's update endpoint is called, and the DOM is updated with the HTML received. As you can see, the JSON sent to the server requires collecting the values of the report's widgets (via ``obj.widgets.getValues()``). Scrolling up to ``newFigureWidgets``, you can see that this just calls ``getCurrentValue`` on each widget object. These functions are defined in widgets.js (alongside the a ``resetToDefault`` function, which is less important). In widget.js you will see an entry in Reports.Widgets.setupMap for every widgets class in diva/diva/widget.py. Finally, in script.js we iterate through relevant sections of the index.html DOM, and use the data passed to the index.html Jinja template from the server side (see ``generate_widget_data`` in reporter.py, for ex.) to build the following structure:

* Reports
    * Report 0
        * Widget a
        * Widget b
        * ...
    * ...
