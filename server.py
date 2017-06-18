# TODO: import reports
import matplotlib
# use the Agg backend, which is non-interactivate (just for PNGs)
# this way, a separate script isn't started by matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, mpld3
import numpy as np
import pandas as pd
from enum import Enum
from flask import Flask, render_template
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

class Widget:
    def jsonToValue(self, json):
        return json['value']

class TextWidget(Widget):
    def __init__(self, default=""):
        self.default = default

    def generateHTML(self, widgetId):
        return render_template('text_widget.html', name=widgetId)

class FloatWidget(Widget):
    def __init__(self, default=0):
        self.default = default

    def generateHTML(self, widgetId):
        return render_template('float_widget.html', name=widgetId)

report_generators = {}

def get_default_inputs(widgets):
    inputs = {}
    for keyVal in widgets:
        name = keyVal[0]
        widget = keyVal[1]
        inputs[name] = widget.default
    return inputs

def register_report(name, figure_generator, widgets=[]):
    def generate():
        figureHTML = ''
        if len(widgets) > 0:
            inputs = get_default_inputs(widgets)
            figureHTML = figure_generator(inputs)
        else:
            figureHTML = figure_generator() 
        widgetsHTML = []
        for keyVal in widgets:
            name = keyVal[0]
            widget = keyVal[1]
            widgetsHTML.append(widget.generateHTML(name))
        return render_template('figure_report.html',
                figureHTML=figureHTML,
                widgetsHTML=widgetsHTML)
    report_generators[name] = generate

# figure out how to do it like below. Decorators are made 
# for this purpose!
#@reports.add('report_name', [widget_list])
def figure_a(inputs):
    plt.figure()
    plt.plot([3,1,4,1,inputs['floatName']], 'ks-', mec='w', mew=5, ms=20)
    htmlString = mpld3.fig_to_html(plt.gcf()) 
    return htmlString
register_report('foo', figure_a, [('textName', TextWidget("yo")), ('floatName', FloatWidget(20))])

def figure_b():
    plt.figure()
    plt.plot([1, 2, 3, 4], 'ks-', mec='w', mew=5, ms=20)
    htmlString = mpld3.fig_to_html(plt.gcf())
    return htmlString

def figure_c():
    df = pd.DataFrame(np.random.randn(20, 20))
    tableString = df.to_string()
    # return '<pre>' + tableString + '</pre>'
    # TODO: set some basic formatting on the html table
    return df.to_html()

register_report('bar', figure_b)
register_report('pan', figure_c)

for i in range(100):
    name = 'foo{}'.format(i)
    register_report(name, figure_a)

reports = []
for key, value in report_generators.items():
    reports.append({'name': key, 'href': key})

@app.route('/')
@app.route('/<reportname>')
def index(reportname=None):
    if reportname is None:
        return render_template(
                'index.html', reports=reports)
    else:
        # TODO: ensure that generator actually exists
        generator = report_generators[reportname]
        # TODO: pass the generator any args from widgets
        htmlOutput = generator()
        return render_template(
                'report.html',
                reports=reports,
                reportHTML=htmlOutput)


