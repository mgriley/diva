from functools import singledispatch
# use matplotlib with the Agg backend to avoid opening an app
# to view the matplotlib figures
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, mpld3
import numpy as np
import pandas as pd
from bokeh.plotting.figure import Figure
from bokeh.resources import CDN
from bokeh.embed import components

# Keep in mind:
# Inserting a script tag into the DOM using innerHTML does not
# execute any script tags in the transplanted HTML.

@singledispatch
def convert_to_html(val):
    # default is to just display the value as a string
    return '<p>{}</p>'.format(str(val))

# assume a raw string is valid HTML
@convert_to_html.register(str)
def str_to_html(html_string):
    return html_string

@convert_to_html.register(matplotlib.figure.Figure)
def fig_to_html(fig):
    return mpld3.fig_to_html(fig)

# TODO: any way to do this for a plot with multiple figures?

@convert_to_html.register(pd.DataFrame)
def dataframe_to_html(df):
    # Bootstrap table classes
    css_classes = ['table', 'table-bordered', 'table-hover', 'table-sm']
    return df.to_html(classes=css_classes)    

@convert_to_html.register(pd.Series)
def series_to_html(series):
    return dataframe_to_html(series.to_frame())

# see: http://bokeh.pydata.org/en/latest/docs/user_guide/embed.html
@convert_to_html.register(Figure)
def bokeh_figure_to_html(figure):
    # NB: cannot just use file_html due to the issue mentioned above
    script, div = components(figure)
    return '{}{}'.format(div, script)

