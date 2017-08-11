from diva import Diva
from diva.widgets import *
import pandas as pd

app = Diva()

def baz(a, b, *args, **kwargs):
    return '<p>{} {} {} {}</p>'.format(a, b, args, kwargs)

@app.view('shim example', [
    Int('choose an int'),
    Float('choose a float'),
    String('choose a string'),
    Bool('choose a bool')])
def baz_shim(my_int, my_float, my_str, my_bool):
    # in baz: a=my_int, b=my_float, args=(my_str), kwargs={'hi': my_bool}
    return baz(my_int, my_float, my_str, hi=my_bool) 

app.run()
