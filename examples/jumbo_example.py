from diva import Diva, Dashboard, row_layout
from diva.widgets import *
# only required if adding your own converter:
from diva.converters import convert_to_html
 
import numpy as np
import pandas as pd
from bokeh.plotting import figure
from datetime import *

app = Diva()

"""
No Widgets
Reloading will always give the same figure
"""
@app.view('no widgets')
def no_widgets():
    return pd.Series([x for x in range(20)])

"""
Simple Widgets
Reloading passes the values of the widgets to the func
"""
@app.view('simple widgets', [String('enter name'), Int('enter age')])
def simple_widgets(name, age):
    return name, age

"""
Many widgets
"""
@app.view('many widgets', [
    String('some text'),
    Float('a float'),
    Int('an int'),
    Bool('a bool'),
    SelectOne('choose one', ['a', 'b', 'c']),
    SelectSubset('select many', ['foo', 'baz', 'baz'], ['foo']),
    Color('pick a color'),
    Slider('a float'),
    Date('a date'),
    Time('a time'),
    DateRange('a date range')
])
def many_widgets(*widget_values):
    return widget_values

"""
Date Widgets
There are many ways to specify the defaults, see the docs for details
"""
@app.view('date widgets', [
    # this defaults to: the exact date in ISO format
    Date('date a', '2017-08-21'),
    # defaults to: 7 days ago
    Date('date b', relativedelta(weeks=1)),
    # defaults to: the range between the exact dates in ISO format
    DateRange('range a', '2017-08-21', '2017-08-26'),
    # you can also use relative dates
    # defaults to: the last week
    DateRange('range b', relativedelta(days=7), relativedelta()),
    # or a combination of exact and relative
    # defaults to: exact date to present
    DateRange('range c', '2017-07-15', relativedelta())
])
def date_widgets(date_a, date_b, range_a, range_b, range_c):
    return date_a, date_b, range_a, range_b, range_c

"""
Converter Examples:
An example of using each type that can be converted to HTML
is given.
See the matplotlib example for the matplotlib.figure.Figure converter
"""

"""
A string is assumed to be raw HTML
"""
@app.view('convert: str')
def raw_html():
    return '<h1>Raw HTML</h1><p>If a string is returned, it is assumed to be raw HTML</p>'

@app.view('convert: pandas.DataFrame')
def pandas_df():
    df = pd.DataFrame(np.random.randn(20, 20))
    return df;

@app.view('convert: pandas.Series')
def pandas_series():
    s = pd.Series([p for p in range(100)])
    return s

@app.view('convert: bokeh.plotting.figure.Figure')
def bokeh_fig():
    x = [1, 2, 3, 4, 5]
    y = [6, 7, 2, 4, 5]
    plot = figure(title="bokeh example", x_axis_label='x', y_axis_label='y')
    plot.line(x, y, legend="Temp", line_width=2)
    return plot

"""
If Diva does not support the type, it's string representation is
converted to HTML
"""
@app.view('convert: none of the above (ex. array of ints)')
def na():
    return [i for i in range(10)]

@app.view('convert: Dashboard')
def dashboard_view():
    a = pd.DataFrame(np.random.randn(10, 10))
    b = pd.DataFrame(np.random.randn(10, 10))
    c = pd.DataFrame(np.random.randn(10, 10))
    # will arrange the views such that a takes up the full first row
    # and the second row is split between b and c
    return Dashboard([a, b, c], row_layout(1, 2))

@app.view('convert: another Dashboard')
def dashboard_view():
    a = pd.DataFrame(np.random.randn(20, 5))
    b = pd.DataFrame(np.random.randn(10, 10))
    c = pd.DataFrame(np.random.randn(10, 10))
    # this uses a custom layout instead of row_layout
    # a will take up the left half of the view, and the right half
    # will be horizontally split, with b on top of c
    return Dashboard([a, b, c], [[0, 0, 1, 2], [1, 0, 1, 1], [1, 1, 1, 1]])

"""
You can create a dashboard view by composing existing views
"""

@app.view('view a', [Int('enter num', 5)])
def view_a(foo):
    return pd.Series([foo for i in range(10)])

@app.view('some very long and tedious name', [String('enter name', 'foo')], short='view b')
def view_b(bar):
    return pd.DataFrame([bar for i in range(10)])

# provide a list of the names of the views you want to compose.
# If a short name is provided for the view, you must use that name
app.compose_view('composed view', ['view a', 'view b'], row_layout(2)) 

"""
Register a new converter.
Now if you register a view that returns a datetime.date object, it will
return the HTML from this function
"""
@convert_to_html.register(date)
def my_converter(d):
    return '<p>year: {}, month: {}, day: {}</p>'.format(d.year, d.month, d.day) 

@app.view('my sample view')
def foo():
    # this will use the new converter
    return date(2017, 8, 11)

# Setting debug=True will allow live code reload and display a debugger (via Flask)
# if an exception is thrown.
app.run(debug=True)
