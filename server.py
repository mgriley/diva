# TODO: import reports
import matplotlib
# use the Agg backend, which is non-interactivate (just for PNGs)
# this way, a separate script isn't started by matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, mpld3
import numpy as np
import pandas as pd
from flask import Flask, render_template
app = Flask(__name__)

report_generators = {}

def register_report(name, figure_generator):
    report_generators[name] = figure_generator

# figure out how to do it like below. Decorators are made 
# for this purpose!
#@reports.add('report_name', [widget_list])
def figure_a():
    plt.figure()
    plt.plot([3,1,4,1,5], 'ks-', mec='w', mew=5, ms=20)
    htmlString = mpld3.fig_to_html(plt.gcf()) 
    return htmlString

def figure_b():
    plt.figure()
    plt.plot([1, 2, 3, 4], 'ks-', mec='w', mew=5, ms=20)
    htmlString = mpld3.fig_to_html(plt.gcf())
    return htmlString

register_report('foo', figure_a)
register_report('bar', figure_b)

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
                reports=reports, reportHtml=htmlOutput)


