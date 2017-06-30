from diy_dashboard.reporter import Reporter
from diy_dashboard.widgets import *
import pandas as pd

reporter = Reporter()

@reporter.display('report 0')
def foo():
    return pd.Series([p for p in range(10)])

@reporter.display('report 1')
def bar():
    return pd.Series([p for p in range(20)])

@reporter.display('report 2')
def baz():
    return pd.Series([p for p in range(30)])

reporter.run(debug=True)
