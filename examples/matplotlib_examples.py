# You should use the 'Agg' backend (for PNGs) when importing matplotlib 
# b/c otherwise a matplotlib will attempt to open a GUI app
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from diva import Diva, Dashboard
from diva.widgets import *

"""
As shown, you should use the object-oriented matplotlib functions.
Otherwise, two different functions may unintentionally be modifying
the axes of the same figure, which can cause confusion.

Since matplotlib maintains internal references to all figures you create,
they will not actually be garbage collected until you explicitly close them!
See here for a workaround: 
https://stackoverflow.com/questions/16334588/create-a-figure-that-is-reference-counted/16337909#16337909

These examples are adapted from:
https://matplotlib.org/users/pyplot_tutorial.html
"""

app = Diva()

@app.view('simple figure', [Int('x', 3)])
def matplot_fig(x):
    # make a new figure
    fig, ax = plt.subplots()
    ax.plot([3,1,4,1,x], 'ks-', mec='w', mew=5, ms=20)
    # plt.gcf is short for "get current figure"
    return fig

"""
There is some subtle error here. Only updates upon
increasing x
May have to do with overwriting fig 1?
"""
@app.view('subplots', [Float('x', 5.0)])
def subplots(x):
    def f(t):
        return np.exp(-t) * np.cos(2*np.pi*t)

    t1 = np.arange(0.0, x, 0.1)
    t2 = np.arange(0.0, x, 0.02)

    # Use the object-oriented matplotlib functions 
    # for subplots, 
    fig, axes = plt.subplots(2, 1)
    axes[0].plot(t1, f(t1), 'bo', t2, f(t2), 'k')
    axes[1].plot(t2, np.cos(2*np.pi*t2), 'r--')

    return fig

@app.view('matplotlib mutliple figures')
def multiple_figures():
    fig_a, ax_a = plt.subplots()
    ax_a.plot([1, 2, 3, 4, 5], 'ks-', mec='w', mew=5, ms=20)
    fig_b, ax_b = plt.subplots()
    ax_b.plot([6, 7, 8, 9, 10], 'ks-', mec='w', mew=5, ms=20)
    return Dashboard([fig_a, fig_b])

app.run(debug=True)
