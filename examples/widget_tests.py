from diy_dashboard.reporter import Reporter
from diy_dashboard.widgets import *

reporter = Reporter()

@reporter.display('String', [String('string', 'hello')])
@reporter.display('Float', [Float('float', 1.5, -5, 5, 0.1)])
@reporter.display('Int', [Int('int', 2, 0, 10)])
@reporter.display('Bool', [Bool('bool', True)])
@reporter.display('SelectOne', [SelectOne(['foo', 'bar', 'baz'], 'bar')])
@reporter.display('SelectSubset', [SelectSubset(['foo', 'bar', 'baz'], ['foo', 'baz'])])
@reporter.display('Color', [Color('color', '#ff0000')])
@reporter.display('Date', [Date('default date')])
@reporter.display('Time', [Time('default time')])
@reporter.display('DateRange', [DateRange('default date range')])
def test_a(a):
    return '<p>{}</p>'.format(a) 

@reporter.display('Slider', [Slider('slider', 0, (-10, 10), 2)])
def float_test(a):
    return '<p>{:f}</p>'.format(a)

reporter.run(debug=True)
