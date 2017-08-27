from diva import Diva
from diva.widgets import *
from diva.utilities import register_simple_util, register_widget_util, file_response
import pandas as pd
import tempfile

# if your utility has options that depend on the currently displayed value,
# of the figure, then use register_widget_util 

def my_util_widgets(val):
    """
    Allow the user to select which of the table's columns to export
    """
    column_names = [str(name) for name in list(val)]
    return [SelectSubset('select the columns you want', column_names)]

def my_util_apply(val, chosen_columns):
    """
    Export only the selected columns to csv
    """
    # convert the subset to a list of bools, with True for cols to include
    # and False ow
    all_col_names = [str(name) for name in list(val)]
    col_bools = [e in chosen_columns for e in all_col_names]
    my_file = tempfile.NamedTemporaryFile()
    val.to_csv(my_file.name, columns=col_bools)
    return file_response('your_file.csv', my_file.name)

register_widget_util('export columns', pd.DataFrame, my_util_widgets, my_util_apply)

# if, on the other hand, your utility does not depend on the currently displayed
# value, you can use register_simple_util, which is a wrapper around the above method
@register_simple_util('export with separator', pd.DataFrame, [String('enter a separator', ',')])
def another_util_apply(val, sep):
    my_file = tempfile.NamedTemporaryFile()
    val.to_csv(my_file.name, sep=sep)
    return file_response('your_file.csv', my_file.name)

app = Diva()

@app.view('my sample view')
def foo():
    return pd.DataFrame({'a': [1, 2], 'b': [3, 4], 'c': [5, 6]}) 

app.run()
