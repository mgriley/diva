from diva import Diva
from diva.converters import convert_to_html
from datetime import date

@convert_to_html.register(date)
def my_converter(d):
    return '<p>year: {}, month: {}, day: {}<p>'.format(d.year, d.month, d.day) 

app = Diva()

@app.view('my sample view')
def foo():
    return date(2017, 8, 11)

app.run()
