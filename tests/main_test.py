import pytest
from diva import Diva
from diva.widgets import *
from diva.converters import convert_to_html
from jsonschema.exceptions import ValidationError
from diva.exceptions import ValidationError as DivaValidationError, WidgetsError

import matplotlib
# use the Agg backend, which is non-interactivate (just for PNGs)
# this way, a separate script isn't started by matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from bokeh.plotting import figure

@pytest.fixture()
def minapp():
    app = Diva()
    @app.view('foo')
    def foo():
        return 0
    @app.view('bar', [Int('my int')])
    def bar(i):
        return i
    return app

class TestWidgetArgs():
    def test_correct_num_args(self):
        app = Diva()
        @app.view('hi', [Float('a'), Int('b')])
        def sample(a, b):
            return a, b
        
        form_data = {'a': "1.0", 'b': "2"}
        app.generate_figure_html(app.reports[0], form_data)

    def test_too_many_widgets(self):
        app = Diva()
        with pytest.raises(WidgetsError):
            @app.view('hi', [Float('a')])
            def sample():
                return 0

    def test_too_few_widgets(self):
        app = Diva()
        @app.view('hi')
        def sample(a):
            return a
        form_data = {}
        with pytest.raises(WidgetsError):
            app.generate_figure_html(app.reports[0], form_data)

    def test_defaults(self):
        app = Diva()
        @app.view('hi', [Int('a')])
        def sample(a, b=2):
            return b
        form_data = {'a': "1"}
        app.generate_figure_html(app.reports[0], form_data)

    def test_varargs(self):
        app = Diva()
        with pytest.raises(WidgetsError):
            @app.view('hi', [Int('a')])
            def sample(*varargs):
                return varargs

    def test_kwargs(self):
        app = Diva()
        with pytest.raises(WidgetsError):
            @app.view('hi', [Int('b')])
            def sample(**kwargs):
                return kwargs

class TestReporter():
    def test_index_bounds(self, minapp):
        minapp.validate_request({'reportIndex': 0, 'widgetValues': {'bar': 0}})
        with pytest.raises(DivaValidationError):
            minapp.validate_request({'reportIndex': 2, 'widgetValues': {'bar': 0}})
        with pytest.raises(DivaValidationError):
            minapp.validate_request({'reportIndex': -1, 'widgetValues': {'bar': 0}})

    def test_missing_data(self, minapp):
        with pytest.raises(DivaValidationError):
            minapp.validate_request({'widgetValues': {'bar': 0}})
        with pytest.raises(DivaValidationError):
            minapp.validate_request({'reportIndex': 0})

    def missing_widget_value(self):
        with pytest.raises(DivaValidationError):
            minapp.validate_request({'reportIndex': 0, 'widgetValues': {}})

class TestWidgets():
    def test_string(self):
        w = String('a')
        w.validate_input('hi')
        with pytest.raises(ValidationError):
            w.validate_input(1)
        assert w.parseForm('hi') == 'hi'

    def test_float(self):
        w = Float('f')
        w.validate_input('1.5')
        with pytest.raises(ValueError):
            w.validate_input('a')
        assert w.parseForm('2.0') == 2

    def test_float_bounds(self):
        w = Float('f', 0, 0, 1)
        with pytest.raises(ValueError):
            w.validate_input("-1.1")
        with pytest.raises(ValueError):
            w.validate_input("1.1")

    def test_bool(self):
        w = Bool('b')
        w.validate_input(True)
        with pytest.raises(ValidationError):
            w.validate_input('0')
        assert w.parseForm(True) == True

    def test_selectone(self):
        w = SelectOne('s', ['a', 'b'])
        w.validate_input('a')
        with pytest.raises(ValidationError):
            w.validate_input('c')
        assert w.parseForm('a') == 'a'
        
    def test_selectsubset(self):
        w = SelectSubset('s', ['a', 'b'])
        w.validate_input([])
        w.validate_input(['a'])
        w.validate_input(['a', 'b'])
        with pytest.raises(ValidationError):
            w.validate_input(['a', 'b', 'c'])
        with pytest.raises(ValidationError):
            w.validate_input(['a', 'a'])
        assert w.parseForm(['a', 'b']) == ['a', 'b']

    def test_date(self):
        w = Date('d')
        w.validate_input('2017-08-16')
        with pytest.raises(ValueError):
            w.validate_input('2017/08/16')

    def test_daterange(self):
        w = DateRange('d')
        data = ['2017-08-16', '2017-08-17']
        w.validate_input(data)
        with pytest.raises(ValueError):
            w.validate_input(['foo', 'bar'])
        with pytest.raises(ValidationError):
            w.validate_input(['2017-08-16'])

    def test_time(self):
        w = Time('d')
        w.validate_input('23:01')
        with pytest.raises(ValueError):
            w.validate_input('01:10AM')

class TestConverters():
    def test_matplot(self):
        plt.figure()
        plt.plot([3,1,4,1,20], 'ks-', mec='w', mew=5, ms=20)
        convert_to_html(plt.gcf())

    def test_pandas(self):
        convert_to_html(pd.DataFrame(np.random.randn(20, 20)))

    def test_bokeh(self):
        x = [1, 2, 3, 4, 5]
        y = [6, 7, 2, 4, 5]
        plot = figure(title="bokeh example", x_axis_label='x', y_axis_label='y')
        plot.line(x, y, legend="Temp", line_width=2)
        convert_to_html(plot)

