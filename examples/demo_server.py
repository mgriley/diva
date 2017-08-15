# TODO: import reports
import matplotlib
# use the Agg backend, which is non-interactivate (just for PNGs)
# this way, a separate script isn't started by matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
from diva import Diva
from diva.widgets import *
from bokeh.plotting import figure
from functools import singledispatch

reporter = Diva()

@singledispatch
def type_to_str(val):
    # strip off the tags or the HTML will not work
    s = str(type(val))
    return s[1:-1]

# helper for printing the types that widgets output:
def type_of_iterable(val):
    s = ''
    for item in val:
        s += type_to_str(item) + ', '
    return s

@type_to_str.register(tuple)
def tuple_type(val):
    return '({})'.format(type_of_iterable(val))

@type_to_str.register(list)
def list_type(val):
    return '[{}]'.format(type_of_iterable(val))

# Provide an overview pages for all of the available widgets
all_widgets = [
        String('some text', 'hello'),
        Float('a float', 1.5),
        Int('an integer', 2),
        Bool('a bool', True),
        SelectOne('pick a name', ['foo', 'bar', 'baz'], 'bar'),
        SelectSubset('pick names', ['foo', 'bar', 'baz'], ['foo', 'baz']),
        Color('pick a color', '#ff0000'),
        Slider('a float'),
        Date('pick a date'),
        Time('pick a time'),
        DateRange('pick a date range')
    ]
@reporter.view('all widgets', all_widgets)
def widgets_test(wstr, wflo, wint, wbool, wso, wss, wcol, wsli, wdate, wtime, wdaterange):
    args = [wstr, wflo, wint, wbool, wso, wss, wcol, wsli, wdate, wtime, wdaterange]
    formats = ['{}', '{}', '{}', '{}', '{}', '{}', '{}', '{:f}', '{}', '{}', '{}']
    body = ''
    for w, arg, f in zip(all_widgets, args, formats):
        arg_type = type_to_str(arg)
        class_name = w.__class__.__name__
        body += "widget class: {}<br />type: {}<br />value: {}<br /><br />".format(class_name, arg_type, f.format(arg))
    return '<p>{}</p>'.format(body)

@reporter.view('convert: str')
def raw_html():
    return '<h1>Raw HTML</h1><p>If a string is returned, it is assumed to be raw HTML</p>'

@reporter.view('convert: matplotlib.figure.Figure')
def matplot_fig():
    plt.figure()
    plt.plot([3,1,4,1,20], 'ks-', mec='w', mew=5, ms=20)
    return plt.gcf()

@reporter.view('convert: pandas.DataFrame')
def pandas_df():
    df = pd.DataFrame(np.random.randn(20, 20))
    return df;

@reporter.view('convert: pandas.Series')
def pandas_series():
    s = pd.Series([p for p in range(100)])
    return s

@reporter.view('convert: bokeh.plotting.figure.Figure')
def bokeh_fig():
    x = [1, 2, 3, 4, 5]
    y = [6, 7, 2, 4, 5]
    plot = figure(title="bokeh example", x_axis_label='x', y_axis_label='y')
    plot.line(x, y, legend="Temp", line_width=2)
    return plot

@reporter.view('convert: none of the above (ex. datetime.time)')
def na():
    return datetime.now()

reporter.run()
