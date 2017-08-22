from diva import Diva, Dashboard, row_layout
from diva.widgets import *
import pandas as pd
import numpy as np

app = Diva()

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

app.run(debug=True)
