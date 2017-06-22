# TODO: import reports
import matplotlib
# use the Agg backend, which is non-interactivate (just for PNGs)
# this way, a separate script isn't started by matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, mpld3
import numpy as np
import pandas as pd
import inspect
from flask import render_template, request
from diy_dashboard import app
from diy_dashboard.widgets import *

def get_report_generators(figure_generator, widgets=[]):
    # transform widgets to tuple array, of (argName, widget)
    # this gives each widget a unique key b/c arg names must be unique
    argNames = inspect.getargspec(figure_generator)[0]
    assert len(argNames) >= len(widgets), \
            ("there are more widgets than function "
            "arguments for function \"{}\"").format(figure_generator.__name__)
    for index, widget in enumerate(widgets):
        widgets[index] = (argNames[index], widget)
    print(widgets)

    def decorated_generator(widgetFormData={}):
        inputs = parse_widget_form_data(widgets, widgetFormData)
        return figure_generator(**inputs)

    # NB: widgets must also be generated b/c jinja render_templates
    # requires an app context to run
    def widgets_generator():
        widgetsHTML = []
        for keyVal in widgets:
            name = keyVal[0]
            widget = keyVal[1]
            widgetsHTML.append(widget.generateHTML(name))
        return widgetsHTML

    return  {'figure_generator': decorated_generator,
            'widgets_generator': widgets_generator}

class Reporter:
    def __init__(self):
        self.report_generators = {}
    
    def display(self, name, widgets=[]):
        def real_decorator(func):
            generators = get_report_generators(func, widgets)
            self.report_generators[name] = generators
            return func
        return real_decorator
    
    def get_reports(self):
        reports = []
        for key, value in self.report_generators.items():
            reports.append({'name': key, 'href': key})
        return reports

reporter = Reporter()

# generates an assertion error (unit test this later)
# def figure_too_few():
    # return '<p>dksjalf</p>'
# register_report('too_few', figure_too_few, [TextWidget('meh')])

@reporter.display('widget test', [TextWidget('text', 'hello'),
        FloatWidget('float', 1.5),
        IntWidget('integer', 2),
        CheckBox('checkbox')])
def widgets_test(a, b, c, d):
    return '<p>{} {} {} {}</p>'.format(a, b, c, d)

@reporter.display('simple')
def simple_figure():
    return '<p>simple foo</p>'

@reporter.display('too_many', [FloatWidget('floating', 6.5)])
def figure_extra(a, b=6):
    return '<p>{} {}</p>'.format(a, b)

@reporter.display('foo', [TextWidget('textbox', 'yo'), FloatWidget('floatzilla', 20)])
def figure_a(textName, floatName):
    print('inputs: {} {}'.format(textName, floatName))
    plt.figure()
    plt.plot([3,1,4,1,floatName], 'ks-', mec='w', mew=5, ms=20)
    htmlString = mpld3.fig_to_html(plt.gcf()) 
    return '<p>{}</p>{}'.format(textName, htmlString)

# def figure_c():
    # df = pd.DataFrame(np.random.randn(20, 20))
    # tableString = df.to_string()
    # # return '<pre>' + tableString + '</pre>'
    # # TODO: set some basic formatting on the html table
    # return df.to_html()
# register_report('pan', figure_c)

# def figure_d(textA, textB):
    # print(inputs)
    # return '<p>{} {}</p>'.format(textA, textB)
# register_report('yoo', figure_d, [TextWidget("aaaaaaaa"), TextWidget('bbbbbbb')])

# for i in range(100):
    # name = 'foo{}'.format(i)
#     register_report(name, figure_a)

@app.route('/')
@app.route('/<reportname>')
def index(reportname=None):

    # TODO: if no reportname specified, select the first report
    # (provided there are actually reports)
    if reportname is None:
        return render_template(
                'index.html',
                reports=reporter.get_reports())
    figure_report = reporter.report_generators.get(reportname, None)
    if figure_report is None:
        abort(404)
    figure_html = figure_report['figure_generator']()
    widgets_html = figure_report['widgets_generator']()
    return render_template(
            'figure_report.html',
            selectedReport=reportname,
            reports=reporter.get_reports(),
            figureHTML=figure_html,
            widgetsHTML=widgets_html)

@app.route('/<reportname>', methods=['POST'])
def updateFigure(reportname):
    print(request.get_json())
    figure_report = reporter.report_generators.get(reportname, None)
    if figure_report is None:
        abort(404)
    figure_generator = figure_report['figure_generator']
    reportHTML = figure_generator(request.get_json())
    return reportHTML

