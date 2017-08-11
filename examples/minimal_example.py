from diva import Diva
from diva.widgets import *
import pandas as pd

app = Diva()

@app.view('my sample view')
def foo():
    data = [p * 1.5 for p in range(20)]
    return pd.Series(data)

@app.view('my sample view with widgets',
        Int('choose a size', 20),
        Float('choose a factor', 1.5))
def bar(size, factor):
    data = [p * factor for p in range(size)]
    return pd.Series(data)

app.run()
