# TODO: import reports
import matplotlib
# use the Agg backend, which is non-interactivate (just for PNGs)
# this way, a separate script isn't started by matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import *
from diy_dashboard.reporter import Reporter
from diy_dashboard.widgets import *
from bokeh.plotting import figure

reporter = Reporter()

# generates an assertion error (unit test this later)
# def figure_too_few():
    # return '<p>dksjalf</p>'
# register_report('too_few', figure_too_few, [TextWidget('meh')])

@reporter.display('basic widget test', [
        String('text', 'hello'),
        Float('float', 1.5),
        Int('integer', 2),
        Bool('checkbox', True),
        SelectOne(['foo', 'bar', 'baz'], 'bar'),
        SelectSubset(['foo', 'bar', 'baz'], ['foo', 'baz']),
        Color('my color', '#ff0000'),
        Slider('my default slider'),
        Slider('my param slider', 0, (-10, 10), 0)])
def widgets_test(a, b, c, d, e, f, g, h, i):
    return '<p>{} {} {} {} {} {} {} {:f} {:f}</p>'.format(a, b, c, d, e, f, g, h, i)

@reporter.display('datetime widgets',
        [
            DateRange('default date range'),
            DateRange('abs date range', '2017-01-02', '2018-02-03'),
            DateRange('last __ range', relativedelta(weeks=3)),
            DateRange('rel range', relativedelta(days=7), relativedelta(days=1)),
            DateRange('date to present', '2017-01-02', timedelta()),
            Date('default date'),
            Date('date relative', relativedelta(days=7)),
            Date('date absolute', '2017-01-11'),
            Time('default'),
            Time('param', time(5, 10, 15))
        ])
def date_range_test(a, b, c, d, e, f, g, h, i, j):
    return '<p>{} | {} | {} | {} | {} | {} | {} | {} | {} | {}</p>'.format(a, b, c, d, e, f, g, h, i, j)

@reporter.display('unknown type')
def unknown_figure():
    dict = {'foo': 10, 'bar': 47}
    return dict

@reporter.display('invalid HTML string')
def invalid_string():
    return 'this is not valid html'

@reporter.display('valid HTML string')
def valid_string():
    return '<p>foo</p><br><br><p>bar</p>'

@reporter.display('too_many', [Float('floating', 6.5)])
def figure_extra(a, b=6):
    return '<p>{} {}</p>'.format(a, b)

@reporter.display('matplotlib figure', [String('textbox', 'yo'), Float('floatzilla', 20)])
def figure_a(textName, floatName):
    print('inputs: {} {}'.format(textName, floatName))
    plt.figure()
    plt.plot([3,1,4,1,floatName], 'ks-', mec='w', mew=5, ms=20)
    return plt.gcf()

@reporter.display('pd.DataFrame test')
def figure_c():
    df = pd.DataFrame(np.random.randn(20, 20))
    return df;

@reporter.display('pd.Series test')
def figure_d():
    s = pd.Series([p for p in range(100)])
    return s

@reporter.display('bokeh figure')
def figure_e():
    x = [1, 2, 3, 4, 5]
    y = [6, 7, 2, 4, 5]
    plot = figure(title="bokeh example", x_axis_label='x', y_axis_label='y')
    plot.line(x, y, legend="Temp", line_width=2)
    return plot

# for i in range(100):
    # name = 'foo{}'.format(i)
#     register_report(name, figure_a)

reporter.run(debug=True)
