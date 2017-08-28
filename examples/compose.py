# TODO: import reports
import matplotlib
# use the Agg backend, which is non-interactivate (just for PNGs)
# this way, a separate script isn't started by matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
from diva import Diva, row_layout
from diva.widgets import *
from bokeh.plotting import figure
from functools import singledispatch

reporter = Diva()

@reporter.view('convert: pandas.DataFrame', [Int('l'), Int('w')], short='dat')
def pandas_df(a, b):
    df = pd.DataFrame(np.random.randn(a, b))
    return df;

@reporter.view('convert: pandas.Series', [Int('c'), Int('d')], short='ser')
def pandas_series(a, b):
    s = pd.Series([p for p in range(a * b)])
    return s

@reporter.view('convert: bokeh.plotting.figure.Figure', [Float('e'), Float('f')], short='bok')
def bokeh_fig(a, b):
    x = [1, 2, 3, 4, a]
    y = [6, 7, 2, 4, b]
    plot = figure(title="bokeh example", x_axis_label='x', y_axis_label='y')
    plot.line(x, y, legend="Temp", line_width=2)
    return plot

reporter.compose_view('composition view', ['dat', 'ser', 'bok'], short='c1')
reporter.compose_view('compose b', ['bok', 'ser'], short='c2')
reporter.compose_view('compose d', ['bok', 'ser', 'dat'], row_layout(1, 2))

# compose-ception
reporter.compose_view('compose c', ['c1', 'c2'], short='c4')

if __name__ == "__main__":
    reporter.run(debug=True)
