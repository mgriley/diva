# import reports
from flask import Flask, render_template
app = Flask(__name__)

report_generators = {}

def register_report(name, figure_generator):
    report_generators[name] = figure_generator

# figure out how to do it like below. Decorators are made 
# for that purpose!
#@reports.add('report_name', [widget_list])
def figure_a():
    return '<div>Figure A</div>'

def figure_b():
    return '<div>Figure B</div>'

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


