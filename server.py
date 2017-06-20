# TODO: import reports
import matplotlib
# use the Agg backend, which is non-interactivate (just for PNGs)
# this way, a separate script isn't started by matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, mpld3
import numpy as np
import pandas as pd
from enum import Enum
import inspect
from flask import Flask, render_template, request
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

class Widget:
    pass

class TextWidget(Widget):
    def __init__(self, default=""):
        self.default = default

    def generateHTML(self, widgetId):
        return render_template('text_widget.html', name=widgetId)

    def parseForm(self, formData):
        return formData

class FloatWidget(Widget):
    def __init__(self, default=0):
        self.default = default

    def generateHTML(self, widgetId):
        return render_template('float_widget.html', name=widgetId)

    def parseForm(self, formData):
        return float(formData)

report_generators = {}

# given map of form data, return a map of inputs 
def parse_widget_form_data(widgets, widgetFormData):
    inputs = {}
    for keyVal in widgets:
        name = keyVal[0]
        widget = keyVal[1]
        formData = widgetFormData.get(name, None)
        if formData == None:
            inputs[name] = widget.default;
        else:
            inputs[name] = widget.parseForm(formData)
    return inputs

def register_report(name, figure_generator, widgets=[]):
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

    report_generators[name] = {
            'figure_generator': decorated_generator,
            'widgets_generator': widgets_generator}

# generates an assertion error (unit test this later)
# def figure_too_few():
    # return '<p>dksjalf</p>'
# register_report('too_few', figure_too_few, [TextWidget('meh')])

def figure_extra(a, b=6):
    return '<p>{} {}</p>'.format(a, b)
register_report('too_many', figure_extra, [FloatWidget(6.5)])

def figure_dec(a, b, c):
    return '<p>{} {} {}</p>'.format(a, b, c)
register_report('dec', figure_dec, [TextWidget('yo'), FloatWidget(2.5), TextWidget('ha')])

# figure out how to do it like below. Decorators are made 
# for this purpose!
#@reports.add('report_name', [widget_list])
def figure_a(textName, floatName):
    print('inputs: {} {}'.format(textName, floatName))
    plt.figure()
    plt.plot([3,1,4,1,floatName], 'ks-', mec='w', mew=5, ms=20)
    htmlString = mpld3.fig_to_html(plt.gcf()) 
    return '<p>{}</p>{}'.format(textName, htmlString)
register_report('foo', figure_a, [TextWidget("yo"), FloatWidget(20)])

def figure_c():
    df = pd.DataFrame(np.random.randn(20, 20))
    tableString = df.to_string()
    # return '<pre>' + tableString + '</pre>'
    # TODO: set some basic formatting on the html table
    return df.to_html()
register_report('pan', figure_c)

def figure_d(textA, textB):
    print(inputs)
    return '<p>{} {}</p>'.format(textA, textB)
register_report('yoo', figure_d, [TextWidget("aaaaaaaa"), TextWidget('bbbbbbb')])

# for i in range(100):
    # name = 'foo{}'.format(i)
#     register_report(name, figure_a)

reports = []
for key, value in report_generators.items():
    reports.append({'name': key, 'href': key})

@app.route('/')
@app.route('/<reportname>')
def index(reportname=None):
    if reportname is None:
        return render_template(
                'index.html', reports=reports)
    figure_report = report_generators.get(reportname, None)
    if figure_report is None:
        abort(404)
    figure_html = figure_report['figure_generator']()
    widgets_html = figure_report['widgets_generator']()
    return render_template(
            'figure_report.html',
            reports=reports,
            figureHTML=figure_html,
            widgetsHTML=widgets_html)

@app.route('/<reportname>', methods=['POST'])
def updateFigure(reportname):
    print(request.get_json())
    figure_report = report_generators.get(reportname, None)
    if figure_report is None:
        abort(404)
    figure_generator = figure_report['figure_generator']
    reportHTML = figure_generator(request.get_json())
    return reportHTML

