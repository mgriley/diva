from functools import singledispatch
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, mpld3
import numpy as np
import pandas as pd

@singledispatch
def convert_to_html(val):
    # TODO: improve this error msg by listing valid types, and explaining how to register your
    # own converter
    print(type(val))
    return '<p>Could not convert value of type < {} > to HTML</p><p>{}</p>'.format(type(val).__name__, val)

# assume a raw string is valid HTML
@convert_to_html.register(str)
def str_to_html(html_string):
    return html_string

@convert_to_html.register(matplotlib.figure.Figure)
def fig_to_html(fig):
    return mpld3.fig_to_html(fig)

# TODO: any way to do this for a plot with multiple figures?

# TODO: the default formatting is hideous
@convert_to_html.register(pd.DataFrame)
def dataframe_to_html(df):
    return df.to_html()    

@convert_to_html.register(pd.Series)
def series_to_html(series):
    return dataframe_to_html(series.to_frame())

